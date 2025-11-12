---
title: 转换PaddleOCR模型为ONNX
date: 2022-09-27
authors: [SWHL]
categories:
  - 模型相关
comments: true
---


> 该文章主要给出了几种转换PaddleOCR模型的方案，便于大家快速转换使用。

<!-- more -->

!!! info

    不支持<strong>slim量化版</strong>的模型转换

### 简介

- PaddleOCR项目模型转换，主要借助[`paddle2onnx`](https://github.com/PaddlePaddle/Paddle2ONNX)库实现。针对PaddleOCR中涉及到的相关模型，直接转换并不太方便。因此，推出了[PaddleOCRModelConverter](https://github.com/RapidAI/PaddleOCRModelConvert)转换工具。

### 在线转换

- [魔搭](https://www.modelscope.cn/studios/liekkas/PaddleOCRModelConverter/summary)
- [Hugging Face](https://huggingface.co/spaces/SWHL/PaddleOCRModelConverter)

<div align="left">
    <iframe src="https://swhl-paddleocrmodelconverter.hf.space" frameborder="0" width="1550" height="850"></iframe>
</div>

### [离线转换](https://github.com/RapidAI/PaddleOCRModelConvert)
