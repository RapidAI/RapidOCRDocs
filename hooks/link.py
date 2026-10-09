import fnmatch
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _url_exists(url, cache):
    """Return whether a URL responds successfully, caching checks per build."""
    if url in cache:
        return cache[url]

    try:
        request = Request(url, method="HEAD")
        with urlopen(request, timeout=5) as response:
            exists = 200 <= response.status < 400
    except HTTPError:
        # If GitHub cannot confirm the target (including rate limiting), leave
        # the source text unchanged rather than guessing.
        exists = False
    except (URLError, TimeoutError, OSError):
        exists = False

    cache[url] = exists
    return exists


def on_page_markdown(markdown, page, config, files):
    """
    将 'issue #数字'、'PR #数字'、'commit 哈希' 以及孤立的 '#数字'（默认视为 PR）替换为 GitHub 链接
    （忽略代码块和行内代码，只在指定页面生效，支持通配符）
    """

    repo_url = config.get("repo_url", "").rstrip("/")
    if not repo_url:
        return markdown

    # 页面白名单，支持通配符
    extra = config.get("extra", {}) or {}
    allowed_pages = extra.get("link_pages", config.get("link_pages", []))
    page_src = page.file.src_path  # 相对于 docs/ 的路径
    # 链接自动转换仅适用于 changelog，避免影响其他文档中的普通编号。
    if not page_src.startswith("changelog/"):
        return markdown
    if allowed_pages:
        matched = any(fnmatch.fnmatch(page_src, pattern) for pattern in allowed_pages)
        if not matched:
            return markdown

    # 保存代码块和行内代码
    placeholders = {}
    link_exists_cache = {}

    def store_placeholder(match):
        key = f"__PLACEHOLDER_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    # 提取代码块（```...``` 或 ~~~...~~~）
    markdown = re.sub(r"```.*?```", store_placeholder, markdown, flags=re.DOTALL)
    markdown = re.sub(r"~~~.*?~~~", store_placeholder, markdown, flags=re.DOTALL)
    # 提取行内代码（`...`）
    markdown = re.sub(r"`[^`]*`", store_placeholder, markdown)
    # 提取已有的 Markdown 链接，避免链接文本中的 issue/PR 编号被再次处理
    markdown = re.sub(r"\[[^\]]*\]\([^)]*\)", store_placeholder, markdown)

    # --- issue 替换 ---
    def issue_replacer(match):
        num = match.group(1)
        url = f"{repo_url}/issues/{num}"
        return (
            f"issue [#{num}]({url})"
            if _url_exists(url, link_exists_cache)
            else match.group(0)
        )

    markdown = re.sub(r"(?i)issue\s*[:#]?\s*#?(\d+)", issue_replacer, markdown)

    # --- PR 替换 ---
    def pr_replacer(match):
        num = match.group(1)
        url = f"{repo_url}/pull/{num}"
        return (
            f"PR [#{num}]({url})"
            if _url_exists(url, link_exists_cache)
            else match.group(0)
        )

    markdown = re.sub(r"(?i)PR\s*[:#]?\s*#?(\d+)", pr_replacer, markdown)

    # --- 孤立的 #数字：默认视为 PR ---
    # 要求 # 前不能是字母、数字、下划线（即非 \w），后跟数字，且不在行内代码中（已保护）
    # 使用 (?<!\w) 确保前面不是单词字符，避免匹配 foo#123
    def hash_pr_replacer(match):
        num = match.group(1)
        url = f"{repo_url}/pull/{num}"
        return (
            f"[#{num}]({url})"
            if _url_exists(url, link_exists_cache)
            else match.group(0)
        )

    # `[` 也作为边界排除，避免处理已有链接（以及前面刚生成的链接）中的编号
    markdown = re.sub(r"(?<![\w\[])#(\d+)\b", hash_pr_replacer, markdown)

    # --- commit 替换 ---
    def commit_replacer(match):
        sha = match.group(1)
        short_sha = sha[:7]
        url = f"{repo_url}/commit/{sha}"
        return (
            f"commit [{short_sha}]({url})"
            if _url_exists(url, link_exists_cache)
            else match.group(0)
        )

    markdown = re.sub(r"(?i)commit\s+([0-9a-f]{6,40})", commit_replacer, markdown)

    # 还原代码块和行内代码
    for key, value in placeholders.items():
        markdown = markdown.replace(key, value)

    return markdown
