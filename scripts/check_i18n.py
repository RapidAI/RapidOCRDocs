#!/usr/bin/env python3
"""Check Markdown translation pairs and report stale translations.

The repository uses ``foo.md`` as the default-language source and
``foo.<locale>.md`` as its translation. A translation is considered stale when
the latest source commit is not an ancestor of the latest translation commit.
This keeps the check independent of commit timestamps and works with merge
commits as well. Uncommitted source changes are also reported as stale during
local runs.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".github" / "i18n-check.yml"


@dataclass(frozen=True)
class LocaleRules:
    locale: str
    suffix: str
    required: frozenset[str]
    exclude: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    level: str
    locale: str
    source: str
    message: str
    translation: str | None = None


def _load_config(path: Path) -> tuple[str, tuple[LocaleRules, ...]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise SystemExit(f"Unable to read i18n config {path}: {exc}") from exc

    default_locale = str(data.get("default_locale", "zh"))
    locales = data.get("locales", {})
    if not isinstance(locales, dict) or not locales:
        raise SystemExit(f"{path} must define at least one locale")

    rules: list[LocaleRules] = []
    for locale, raw in locales.items():
        if not isinstance(raw, dict):
            raise SystemExit(f"Locale {locale!r} must be a mapping")
        suffix = str(raw.get("suffix", f".{locale}.md"))
        if not suffix.startswith(".") or not suffix.endswith(".md"):
            raise SystemExit(f"Locale {locale!r} has invalid suffix {suffix!r}")
        required = frozenset(_normalise_path(item) for item in raw.get("required", []))
        exclude = tuple(_normalise_path(item) for item in raw.get("exclude", []))
        rules.append(LocaleRules(str(locale), suffix, required, exclude))
    return default_locale, tuple(rules)


def _normalise_path(value: Any) -> str:
    return str(value).replace("\\", "/").lstrip("./")


def _is_excluded(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _source_files(
    docs_dir: Path, rules: LocaleRules, all_suffixes: tuple[str, ...]
) -> list[Path]:
    return sorted(
        path
        for path in docs_dir.rglob("*.md")
        if not any(path.name.endswith(suffix) for suffix in all_suffixes)
        and not _is_excluded(path.relative_to(docs_dir).as_posix(), rules.exclude)
    )


def _translation_path(source: Path, suffix: str) -> Path:
    return source.with_name(f"{source.stem}{suffix}")


def _git(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _last_commit(path: Path) -> str | None:
    return _git("rev-list", "-1", "HEAD", "--", path.relative_to(ROOT).as_posix())


def _working_tree_changed(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    return bool(_git("status", "--porcelain", "--", relative))


def _is_stale(source: Path, translation: Path) -> bool:
    # This also makes the script useful before a commit is created locally.
    if _working_tree_changed(source):
        return True

    source_commit = _last_commit(source)
    translation_commit = _last_commit(translation)
    if not source_commit or not translation_commit:
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, translation_commit],
        cwd=ROOT,
        check=False,
    )
    return result.returncode != 0


def _annotation(finding: Finding) -> None:
    if not _github_actions():
        return
    path = f"docs/{finding.translation or finding.source}"
    command = "error" if finding.level == "error" else "warning"
    print(f"::{command} file={path}::{finding.message}")


def _github_actions() -> bool:
    return bool(os.environ.get("GITHUB_ACTIONS"))


def _check_locale(
    docs_dir: Path, rules: LocaleRules, all_suffixes: tuple[str, ...]
) -> list[Finding]:
    findings: list[Finding] = []
    sources = _source_files(docs_dir, rules, all_suffixes)
    source_names = {path.relative_to(docs_dir).as_posix() for path in sources}

    for source in sources:
        source_name = source.relative_to(docs_dir).as_posix()
        translation = _translation_path(source, rules.suffix)
        translation_name = translation.relative_to(docs_dir).as_posix()
        if not translation.exists():
            level = "error" if source_name in rules.required else "warning"
            findings.append(
                Finding(
                    level,
                    rules.locale,
                    source_name,
                    f"Missing {rules.locale} translation: {translation_name}",
                    translation_name,
                )
            )
        elif _is_stale(source, translation):
            level = "error" if source_name in rules.required else "warning"
            findings.append(
                Finding(
                    level,
                    rules.locale,
                    source_name,
                    f"{rules.locale} translation is stale; update {translation_name}",
                    translation_name,
                )
            )

    translated_files = sorted(docs_dir.rglob(f"*{rules.suffix}"))
    for translation in translated_files:
        translation_name = translation.relative_to(docs_dir).as_posix()
        if _is_excluded(translation_name, rules.exclude):
            continue
        source = translation.with_name(translation.name[: -len(rules.suffix)] + ".md")
        source_name = source.relative_to(docs_dir).as_posix()
        if source_name not in source_names and not source.exists():
            findings.append(
                Finding(
                    "error",
                    rules.locale,
                    source_name,
                    f"Orphan {rules.locale} translation has no source: {translation_name}",
                    translation_name,
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail for every missing or stale translation, not only required pages.",
    )
    args = parser.parse_args()

    _, locales = _load_config(args.config.resolve())
    docs_dir = ROOT / "docs"
    all_suffixes = tuple(rules.suffix for rules in locales)
    findings = [
        finding
        for rules in locales
        for finding in _check_locale(docs_dir, rules, all_suffixes)
    ]

    for finding in findings:
        _annotation(finding)
        print(f"{finding.level.upper()}: [{finding.locale}] {finding.message}")

    errors = [finding for finding in findings if finding.level == "error"]
    if args.strict:
        errors.extend(finding for finding in findings if finding.level == "warning")

    print(
        f"i18n check: {len(findings)} finding(s), "
        f"{len(errors)} blocking issue(s){' (strict)' if args.strict else ''}."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
