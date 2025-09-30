import fnmatch
import re


def on_page_markdown(markdown, page, config, files):
    """
    将 'issue #数字'、'PR #数字'、'commit 哈希' 替换为 GitHub 链接
    （忽略代码块和行内代码，只在指定页面生效，支持通配符匹配）
    """

    repo_url = config.get("repo_url", "").rstrip("/")
    if not repo_url:
        return markdown

    # 从 mkdocs.yml 读取页面白名单（支持通配符）
    allowed_pages = config.get("link_pages", [])
    page_src = page.file.src_path  # e.g. "docs/releases/v1.0.md"

    if allowed_pages:
        matched = any(fnmatch.fnmatch(page_src, pattern) for pattern in allowed_pages)
        if not matched:
            return markdown

    # 保存代码块和行内代码
    placeholders = {}

    def store_placeholder(match):
        key = f"__PLACEHOLDER_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    # 提取代码块（```...``` 或 ~~~...~~~）
    markdown = re.sub(r"```.*?```", store_placeholder, markdown, flags=re.DOTALL)
    markdown = re.sub(r"~~~.*?~~~", store_placeholder, markdown, flags=re.DOTALL)
    # 提取行内代码（`...`）
    markdown = re.sub(r"`.*?`", store_placeholder, markdown)

    # issue 替换
    def issue_replacer(match):
        num = match.group(1)
        return f"issue [#{num}]({repo_url}/issues/{num})"

    markdown = re.sub(
        r"\bissue\s+#(\d+)", issue_replacer, markdown, flags=re.IGNORECASE
    )

    # PR 替换
    def pr_replacer(match):
        num = match.group(1)
        return f"PR [#{num}]({repo_url}/pull/{num})"

    markdown = re.sub(r"\bPR\s+#(\d+)", pr_replacer, markdown, flags=re.IGNORECASE)

    # commit 替换（显示前 7 位）
    def commit_replacer(match):
        sha = match.group(1)
        short_sha = sha[:7]
        return f"commit [{short_sha}]({repo_url}/commit/{sha})"

    markdown = re.sub(
        r"\bcommit\s+([0-9a-f]{6,40})", commit_replacer, markdown, flags=re.IGNORECASE
    )

    # 还原代码块和行内代码
    for key, value in placeholders.items():
        markdown = markdown.replace(key, value)

    return markdown
