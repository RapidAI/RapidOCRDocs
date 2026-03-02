---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/projects/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

!!! warning

    因 RapidOCR API 有了自己的仓库，该更新日志不再更新。最新日志请移步：[link](https://github.com/RapidAI/RapidOCRAPI/releases)

#### 2025-01-01 v0.1.5 update

Merge PR[#309](https://github.com/RapidAI/RapidOCR/pull/309)

- 为 uvicorn 日志添加时间戳
- 给 docker image 增加 vim 方便临时编辑
- 运行 docker 加时区环境变量，让时间戳打印本地时间

#### 2024-12-04 v0.1.4 update

Merge PR[#282](https://github.com/RapidAI/RapidOCR/pull/282) [#281](https://github.com/RapidAI/RapidOCR/pull/281)
主要是支持多种 RapidOCR 推理引擎选择。

#### 2024-11-12 v0.1.2 update

- Merge PR [#263](https://github.com/RapidAI/RapidOCR/pull/253): 修复浮点类型使用错误导致不显示分数

#### 2024-10-28 v0.1.1 update

- 去掉 `def ocr()` 函数前的 `async` 声明，此处为误用。后期会考虑是否添加。

#### 2024-10-28 v0.1.0 update

- Merged PR [#242](https://github.com/RapidAI/RapidOCR/pull/242)

#### 🍿2024-10-15 v0.0.9 update

- 修复 issue [#223](https://github.com/RapidAI/RapidOCR/issues/223)

#### 2024-07-11 v0.0.7 update

- Merge PR [#200](https://github.com/RapidAI/RapidOCR/pull/200)

#### 🥥2024-03-04 v0.0.6 update

- 优化图像读取部分，与 `rapidocr_onnxruntime>=1.3.13` 版本保持一致
- 统一接口返回值类型为字典

#### 🍜2023-05-22 api update

- 将 API 从 ocrweb 中解耦出来，作为单独模块维护，详情参见 [API](https://github.com/RapidAI/RapidOCR/tree/main/api)
- `rapidocr_web>0.1.6` 之后，将不支持 `pip install rapidocr_web[api]` 方式安装，可直接 `pip install rapidocr_api` 安装使用。
