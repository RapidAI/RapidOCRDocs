---
weight: 50
lastmod: "2022-09-27"
draft: false
author: "SWHL"
title: "转换Paddle模型为ONNX"
icon: "support"
description: ""
toc: true
---

{{< alert context="warning" text="不支持<strong>slim量化版</strong>的模型转换" />}}

### 简介
- Paddle格式模型的转换，主要借助[`paddle2onnx`](https://github.com/PaddlePaddle/Paddle2ONNX)库实现。针对PaddleOCR中涉及到的相关模型，直接转换并不太方便。因此，推出了[PaddleOCRModelConverter](https://github.com/RapidAI/PaddleOCRModelConverter)转换工具。
- 主要有两种使用方式：
    - 方法一：在线转换，借助魔搭和Hugging Face两个平台，搭建在线转换demo；
    - 方法二：离线转换，pip安装该工具，即可本地转换使用。


### 在线快速转换
- [魔搭](https://www.modelscope.cn/studios/liekkas/PaddleOCRModelConverter/summary)
- [Hugging Face](https://huggingface.co/spaces/SWHL/PaddleOCRModelConverter)

### [离线转换](https://github.com/RapidAI/PaddleOCRModelConverter)
