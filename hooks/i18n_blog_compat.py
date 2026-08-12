"""将博客文件对 i18n 插件隐藏，使二者可以共存。

Material 的 blog 插件与 mkdocs-static-i18n 不兼容：两者同时启用时博客页面会渲染为空
（ultrabug/mkdocs-static-i18n#283）。因此博客只保留默认语言（中文），并在 i18n 插件
运行期间把博客文件从文件列表中摘出，运行结束后再放回。

Hides the blog files from the i18n plugin so that both can be used together.

The Material blog plugin is not compatible with mkdocs-static-i18n: when both are
enabled the blog renders empty (ultrabug/mkdocs-static-i18n#283). Blog posts are
therefore kept in the default language only, and detached from the file list while
the i18n plugin runs.

Adapted from a hook by Kamil Krzyśków (HRY), MIT licensed, originally written for
the Gothic Modding Community.
"""

from mkdocs import plugins
from mkdocs.structure.files import File, Files

BLOG_FILES: list[File] = []
"""Blog files removed from the build, kept between the two events below."""


def _blog_prefixes(config) -> tuple[str, ...]:
    """Return the `blog_dir` of every enabled blog plugin, as path prefixes.

    Detection is based on the config attribute rather than the plugin name, which
    differs between `blog` and `material/blog` depending on how it is declared.
    """
    prefixes = []
    for plugin in config.plugins.values():
        blog_dir = getattr(getattr(plugin, "config", None), "blog_dir", None)
        if blog_dir:
            prefixes.append(blog_dir.rstrip("/") + "/")
    return tuple(prefixes)


@plugins.event_priority(-95)
def _detach_blog_files(files: Files, config, *_, **__) -> Files:
    """Runs after the blog plugin (-50) and before the i18n plugin (-100)."""
    global BLOG_FILES
    BLOG_FILES = []

    prefixes = _blog_prefixes(config)
    if not prefixes:
        return files

    kept = []
    for file in files:
        if file.src_uri.startswith(prefixes):
            BLOG_FILES.append(file)
        else:
            kept.append(file)
    return Files(kept)


@plugins.event_priority(-105)
def _reattach_blog_files(files: Files, *_, **__) -> Files:
    """Runs after the i18n plugin has processed the remaining files."""
    for file in BLOG_FILES:
        files.append(file)
    return files


on_files = plugins.CombinedEvent(_detach_blog_files, _reattach_blog_files)
