---
weight: 1
date: "2023-09-11"
draft: false
author: "SWHL"
title: "概述"
icon: "circle"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---


<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pepy.tech/project/rapidocr_onnxruntime"><img src="https://static.pepy.tech/personalized-badge/rapidocr_onnxruntime?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Ort"></a>
    <a href="https://pepy.tech/project/rapidocr_openvino"><img src="https://static.pepy.tech/personalized-badge/rapidocr_openvino?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Vino"></a>
</p>

### 简介
- `rapidocr`按照推理引擎的不同，共分为两个包：`rapidocr_onnxruntime`和`rapidocr_openvino`两个。除推理引擎不同之外，其余代码均相同，默认都是在CPU上运行。
- 因为mobile版模型较小，因此将相关模型都已打到Whl包，可直接pip安装使用。

### pypi版本对应关系
- 按语义版本号来讲，两个包其主版本号和次版本号同步更新，修订号可能会有区别。也就是说`x.y.z`中`x`和`y`是一样的，`z`可能不同。
- 各个版本的对应关系：
    |版本|内置模型版本|对应PaddleOCR 分支|
    |:---:|:---:|:---:|
    |`v1.3.x`|PaddleOCR v4版| [release/2.7](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.7)|
    |`v1.2.x`<br/>`v1.1.x`<br/>`v1.0.x`|PaddleOCR v3版| [release/2.6](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6)|

### 选择哪个？

|推理引擎|推理速度更快|占用内存更少|
|:---:|:---:|:---:|
|`rapidocr_onnxruntime`||✓|
|`rapidocr_openvino`|✓|⚠️ openvino存在内存不释放的问题，参见[issue #11939](https://github.com/openvinotoolkit/openvino/issues/11939)|