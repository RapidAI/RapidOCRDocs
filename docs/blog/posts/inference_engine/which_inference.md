---
title: 选择哪个推理引擎？
date: 2022-10-04
authors: [SWHL]
slug: which-inference
categories:
  - 推理引擎
comments: true
---


<!-- more -->

!!! warning

    OpenVINO存在内存不释放的问题，参见[issue #11939](https://github.com/openvinotoolkit/openvino/issues/11939)

|推理引擎|推理速度更快|占用内存更少|
|:---|:---:|:---:|
|`rapidocr_onnxruntime`||✓|
|`rapidocr_openvino`|✓||

