from pathlib import Path


_MARKDOWN_EXPORTS = []


def on_files(files, config):
    _MARKDOWN_EXPORTS.clear()
    for file in files.documentation_pages():
        if not file.src_uri.endswith(".md"):
            continue
        if "/drafts/" in f"/{file.src_uri}":
            continue
        _MARKDOWN_EXPORTS.append(file.src_uri)
    return files


def on_post_build(config):
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])

    for src_uri in _MARKDOWN_EXPORTS:
        src_path = docs_dir / src_uri
        if not src_path.is_file():
            continue

        dest_path = site_dir / src_uri
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(
            _strip_front_matter(src_path.read_text(encoding="utf-8-sig")).lstrip(),
            encoding="utf-8",
        )


def _strip_front_matter(text):
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return text

    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :])
    return text
