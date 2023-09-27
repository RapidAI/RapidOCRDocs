---
weight: 40
lastmod: "2022-09-28"
draft: false
author: "SWHL"
title: "支持识别语言"
icon: "support"
description: ""
toc: true
---

### 简介
- 因为本项目依托于PaddleOCR，所以理论上PaddleOCR支持识别的模型，RapidOCR都是支持的。

### 中英文检测和识别（可以直接使用）
- 因为中英文是最为常用的模型，所以在打包时，就默认将中英文识别的模型放到了`rapidocr_onnxruntime`和`rapidocr_openvino`中，直接pip安装即可使用。

### 其他语种检测和识别（需要转换）
- PaddleOCR中已有文本检测模型列表：[link](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md#1-%E6%96%87%E6%9C%AC%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9E%8B)
- PaddleOCR已有文本识别模型列表： [link](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md#2-%E6%96%87%E6%9C%AC%E8%AF%86%E5%88%AB%E6%A8%A1%E5%9E%8B)
- 除了slim量化版的模型，上面链接中的其他模型都可以转换为ONNX格式，通过RapidOCR快速部署。

### [转换教程](./convert_model.md)