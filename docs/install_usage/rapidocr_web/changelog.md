---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-web/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-web"></a>
    <a href="https://pepy.tech/projects/rapidocr_web"><img src="https://static.pepy.tech/personalized-badge/rapidocr_web?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

!!! warning

    因 RapidOCR Web 有了自己的仓库，该更新日志不再更新。最新日志请移步：[link](https://github.com/RapidAI/RapidOCRWeb/releases)

#### 2024-07-08 v0.1.10 update

- 修复 issue [#197](https://github.com/RapidAI/RapidOCR/issues/197)

#### ❤2023-05-20 ocrweb update

- 增加桌面版 RapidOCRWeb，详情可参见 [RapidOCRWeb 桌面版使用教程](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr_web/usage/)
- 对仓库文档做了整理

#### 🌹2023-05-14 ocrweb v0.1.5 update

- 增加界面版返回坐标框的返回值 ([issue #85](https://github.com/RapidAI/RapidOCR/issues/85))
- API 模式增加 base64 格式传入
- 详情参见：[link](https://github.com/RapidAI/RapidOCR/blob/main/ocrweb/README.md)

#### 🏸2023-04-16 ocrweb v0.1.1 update

- API 部署改为 FastAPI 库支持
- 将 API 模式与 Web 解耦合，可通过 `pip install rapidocr_web[api]` 来选择性安装
- 详情参见：[link](https://github.com/RapidAI/RapidOCR/blob/main/ocrweb/README.md)
