from __future__ import annotations

import re
import subprocess
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any

import yaml
from pymdownx.slugs import slugify

PROJECT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_DIR / "docs"
EXCLUDED_PAGES = {
    "tags.md",
}
SECTION_LABELS = {
    "blog": "文章",
    "changelog": "更新日志",
    "docs": "文档",
}
DEFAULT_POST_SLUGIFY = slugify(case="lower")


def _load_page(path: Path) -> tuple[dict[str, Any], str]:
    content = path.read_text(encoding="utf-8-sig")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    for index, line in enumerate(lines[1:], 1):
        if line.strip() != "---":
            continue

        front_matter = "\n".join(lines[1:index])
        body = "\n".join(lines[index + 1 :])
        if not front_matter:
            return {}, body

        data = yaml.safe_load(front_matter)
        return (data if isinstance(data, dict) else {}), body

    return {}, content


def _normalize_created(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        created = value
    elif isinstance(value, date):
        created = datetime.combine(value, time.min)
    elif isinstance(value, str):
        try:
            created = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                created = datetime.combine(date.fromisoformat(value), time.min)
            except ValueError:
                return None
    else:
        return None

    if created.tzinfo:
        return created.astimezone(timezone.utc).replace(tzinfo=None)
    return created


def _created_from_meta(meta: dict[str, Any]) -> datetime | None:
    date_meta = meta.get("date")
    if isinstance(date_meta, dict):
        return _normalize_created(date_meta.get("created"))
    return _normalize_created(date_meta)


def _created_from_git(path: Path) -> datetime | None:
    try:
        relative_path = path.relative_to(PROJECT_DIR)
    except ValueError:
        return None

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--follow",
                "--format=%aI",
                "--",
                relative_path.as_posix(),
            ],
            cwd=PROJECT_DIR,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None

    dates = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not dates:
        return None
    return _normalize_created(dates[-1])


def _created_from_filesystem(path: Path) -> datetime | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None


def _collect_nav_titles(nav_items: Any) -> dict[str, str]:
    titles: dict[str, str] = {}

    def visit(items: Any) -> None:
        if isinstance(items, list):
            for item in items:
                visit(item)
        elif isinstance(items, dict):
            for title, value in items.items():
                if isinstance(value, str):
                    titles[value] = str(title)
                else:
                    visit(value)

    visit(nav_items)
    return titles


def _title_from_markdown(markdown: str) -> str | None:
    for line in markdown.splitlines():
        match = re.match(r"^\s{0,3}#{1,3}\s+(.+?)\s*#*\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def _resolve_title(
    meta: dict[str, Any], markdown: str, src_uri: str, nav_titles: dict[str, str]
) -> str:
    title = meta.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()

    if src_uri in nav_titles:
        return nav_titles[src_uri]

    markdown_title = _title_from_markdown(markdown)
    if markdown_title:
        return markdown_title

    return Path(src_uri).stem.replace("_", " ").replace("-", " ")


def _is_draft(meta: dict[str, Any]) -> bool:
    draft = meta.get("draft")
    if isinstance(draft, bool):
        return draft
    if isinstance(draft, str):
        return draft.lower() in {"1", "true", "yes", "on"}
    return False


def _page_section(src_uri: str) -> str:
    parts = Path(src_uri).parts
    if len(parts) >= 3 and parts[:2] == ("blog", "posts"):
        return "blog"
    if parts and parts[0] == "changelog":
        return "changelog"
    return "docs"


def _blog_slug(meta: dict[str, Any], title: str) -> str:
    slug = meta.get("slug")
    if isinstance(slug, str) and slug.strip():
        return slug.strip("/")
    return DEFAULT_POST_SLUGIFY(title, "-")


def _iter_articles(config):
    nav_titles = _collect_nav_titles(config.get("nav", []))

    for path in sorted(DOCS_DIR.rglob("*.md")):
        src_uri = path.relative_to(DOCS_DIR).as_posix()
        relative_parts = Path(src_uri).parts
        if "drafts" in relative_parts:
            continue
        if path.name == "index.md" or src_uri in EXCLUDED_PAGES:
            continue

        meta, markdown = _load_page(path)
        if _is_draft(meta):
            continue

        created = (
            _created_from_meta(meta)
            or _created_from_git(path)
            or _created_from_filesystem(path)
        )
        if not created:
            continue

        title = _resolve_title(meta, markdown, src_uri, nav_titles)
        section = _page_section(src_uri)

        article = {
            "section": section,
            "created": created,
            "src_uri": src_uri,
            "title": title,
        }
        if section == "blog":
            article["slug"] = _blog_slug(meta, title)
        yield article


def _build_page_url(article: dict[str, Any]) -> str:
    if article["section"] == "blog":
        created = article["created"]
        return f"blog/{created:%Y/%m/%d}/{article['slug']}/"

    src_uri = article["src_uri"]
    if src_uri.endswith(".md"):
        src_uri = src_uri[:-3]
    if src_uri.endswith("/index"):
        src_uri = src_uri[: -len("/index")]
    return f"{src_uri}/"


def _serialize_article(article: dict[str, Any]) -> dict[str, Any]:
    article = article.copy()
    article["url"] = _build_page_url(article)
    article["label"] = SECTION_LABELS.get(article["section"], "文章")
    article["created_display"] = article["created"].strftime("%Y-%m-%d")
    article["created"] = article["created"].date().isoformat()
    return article


def on_config(config, **kwargs):
    articles = list(_iter_articles(config))
    if not articles:
        config.extra["latest_announcement"] = None
        return config

    latest_by_section = {}
    for section in SECTION_LABELS:
        section_articles = [
            article for article in articles if article["section"] == section
        ]
        latest_article = max(
            section_articles, key=lambda item: item["created"], default=None
        )
        if not latest_article:
            continue

        latest_by_section[section] = _serialize_article(latest_article)

    overall_latest = _serialize_article(max(articles, key=lambda item: item["created"]))

    config.extra["latest_announcement"] = {
        "overall": overall_latest,
        "sections": latest_by_section,
    }
    return config
