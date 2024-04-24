---
weight: 4000
lastmod: "2022-10-10"
draft: false
author: "SWHL"
title: "rapidocr_api"
icon: "update"
toc: true
description: ""
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

#### 🥥2024-03-04 v0.0.6 update:
- 优化图像读取部分，与`rapidocr_onnxruntime>=1.3.13`版本保持一致
- 统一接口返回值类型为字典

#### 🍜2023-05-22 api update:
- 将API从ocrweb中解耦出来，作为单独模块维护，详情参见[API](https://github.com/RapidAI/RapidOCR/tree/main/api)
- `rapidocr_web>0.1.6`之后，将不支持`pip install rapidocr_web[api]`方式安装，可直接`pip install rapidocr_api`安装使用。


<script src="https://giscus.app/client.js"
        data-repo="RapidAI/RapidOCRDocs"
        data-repo-id="R_kgDOKS1JHQ"
        data-category="Q&A"
        data-category-id="DIC_kwDOKS1JHc4Ce5E0"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>