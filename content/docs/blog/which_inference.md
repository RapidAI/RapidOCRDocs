---
weight: 300
date: "2023-09-20"
draft: false
author: "SWHL"
title: "选择哪个推理引擎？"
icon: "code"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---

|推理引擎|推理速度更快|占用内存更少|
|:---|:---:|:---:|
|`rapidocr_onnxruntime`||✓|
|`rapidocr_openvino`|✓||

{{< alert context="warning" text="openvino存在内存不释放的问题，参见[issue #11939](https://github.com/openvinotoolkit/openvino/issues/11939)" />}}