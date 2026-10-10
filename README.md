## RapidOCR 官方文档站点

[![Check Links](https://github.com/RapidAI/RapidOCRDocs/actions/workflows/links-check.yml/badge.svg)](https://github.com/RapidAI/RapidOCRDocs/actions/workflows/links-check.yml)

<https://rapidai.github.io/RapidOCRDocs/>

### 多语言文档约定

- 中文 `.md` 文件是源文档，英文翻译与源文件放在同一目录并使用 `.en.md` 后缀。
- 首页、快速开始、安装、使用、参数、推理引擎、模型列表、在线 Demo 和 FAQ 是必须维护的核心英文页面。
- 博客、更新日志和其他非核心页面可以回退到中文，不需要复制目录结构。
- 双语页面之间使用相对 `.md` 链接，由 `mkdocs-static-i18n` 选择当前语言；不要写死 `/zh/`、`/en/` 或版本路径。
- 修改中文核心页面时，应同步更新对应英文页面，并运行：

  ```bash
  conda run -n py310 python scripts/check_i18n.py
  conda run -n py310 python -m mkdocs build
  ```

### 鸣谢仓库

- [giscus-theme-with-font](https://github.com/L33Z22L11/giscus-theme-with-font)
- Mkdocs 教程
- [Xiaokang2022.github.io](https://github.com/Xiaokang2022/Xiaokang2022.github.io/tree/main)
