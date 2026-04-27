from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
POST_DIRECTORIES = (
    ("blog", DOCS_DIR / "blog" / "posts"),
    ("changelog", DOCS_DIR / "changelog"),
)
SECTION_LABELS = {
    "blog": "文章",
    "changelog": "更新日志",
}


def _load_front_matter(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}

    _, _, remainder = content.partition("---\n")
    front_matter, _, _ = remainder.partition("\n---\n")
    if not front_matter:
        return {}

    data = yaml.safe_load(front_matter)
    return data if isinstance(data, dict) else {}


def _normalize_created(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _iter_posts():
    for section, base_dir in POST_DIRECTORIES:
        for path in sorted(base_dir.rglob("*.md")):
            relative = path.relative_to(base_dir)
            if "drafts" in relative.parts:
                continue

            meta = _load_front_matter(path)
            date_meta = meta.get("date")
            if isinstance(date_meta, dict):
                created = _normalize_created(date_meta.get("created"))
            else:
                created = _normalize_created(date_meta)
            slug = meta.get("slug")
            title = meta.get("title")
            if not created or not slug or not title:
                continue

            yield {
                "section": section,
                "created": created,
                "slug": slug,
                "title": title,
            }


def on_config(config, **kwargs):
    posts = list(_iter_posts())
    if not posts:
        config.extra["latest_announcement"] = None
        return config

    latest_by_section = {}
    for section in SECTION_LABELS:
        section_posts = [post for post in posts if post["section"] == section]
        latest_post = max(section_posts, key=lambda item: item["created"], default=None)
        if not latest_post:
            continue

        latest_post = latest_post.copy()
        latest_post["url"] = f"/latest/{section}/{latest_post['slug']}/"
        latest_post["label"] = SECTION_LABELS[section]
        latest_post["created_display"] = latest_post["created"].strftime("%Y-%m-%d")
        latest_post["created"] = latest_post["created"].isoformat()
        latest_by_section[section] = latest_post

    overall_latest = max(posts, key=lambda item: item["created"]).copy()
    overall_latest["label"] = SECTION_LABELS[overall_latest["section"]]
    overall_latest["url"] = f"/latest/{overall_latest['section']}/{overall_latest['slug']}/"
    overall_latest["created_display"] = overall_latest["created"].strftime("%Y-%m-%d")
    overall_latest["created"] = overall_latest["created"].isoformat()

    config.extra["latest_announcement"] = {
        "overall": overall_latest,
        "sections": latest_by_section,
    }
    return config
