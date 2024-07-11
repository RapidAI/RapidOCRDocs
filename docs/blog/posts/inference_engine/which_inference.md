---
title: OCR推理引擎选择指南
authors: [SWHL]
slug: which-inference
date:
  created: 2022-10-04
  updated: 2024-07-11
categories:
  - 推理引擎
comments: true
---

介绍在CPU端和GPU端，OCR模型的推理引擎选择问题。

<!-- more -->

## CPU端推理引擎选择

### ☆ 推荐：`rapidocr_onnxruntime`

目前可用的推理库有：`rapidocr_onnxruntime`，`rapidocr_openvino`和`rapid_paddle`。这三个库均可在CPU上推理，除推理引擎不同外，其他接口均相同。

其中，因为openvino推理引擎在推理完大图后，所占用的内存不释放问题（issue [#11939](https://github.com/openvinotoolkit/openvino/issues/11939)），不作为优先考虑。

paddlepaddle推理引擎，并未测试与其他两个速度差异。但是相比于其CPU版安装包较大，较为臃肿，不利于分发，因此也不作考虑。个人认为，paddlepaddle优势在于对国产机器的适配。

|安装包名称|大小|
|:---|:---:|
|[paddlepaddle-3.0.0b0-cp312-cp312-win_amd64.whl](https://pypi.org/project/paddlepaddle/3.0.0b0/#files)|90.1MB|
|[openvino-2024.2.0-15519-cp312-cp312-win_amd64.whl](https://pypi.org/project/openvino/#files)|32.4MB|
|[onnxruntime-1.18.1-cp312-cp312-win_amd64.whl](https://pypi.org/project/onnxruntime/#files)| 5.6MB|

汇总如下：

|推理引擎|推理速度更快|占用内存更少|
|:---|:---:|:---:|
|`rapidocr_onnxruntime`||✓|
|`rapidocr_openvino`|✓||

## GPU端推理引擎选择

### ☆ 推荐：`rapidocr_paddle`

### 推荐理由 → [link](../../../install_usage/rapidocr_paddle/usage.md)

### 其他不推荐原因

`rapidocr_openvino`: 出自英特尔，只适配自家GPU，因此，肯定不支持其他家的。如果支持了，烦请留言告知。

`rapidocr_onnxruntime`: onnxruntime-gpu版对动态图支持较差，推理速度很慢。OCR中文本检测部分输入就是动态的。详细参见文档 → [link](./onnxruntime/onnxruntime-gpu.md)

## 如果遇到内存泄露怎么办？

### 内存泄露问题是什么？

内存泄露问题指的是推理引擎在提取较大图像文字时，会申请较多内存。而在提取完成之后，不释放这些临时申请的内存。如果后续再遇到一张更大尺寸的图像，当前内存不够用的话，推理引擎会申请更多内存。同样，这些内存也不会被推理引擎释放。

这样，后续如果再遇到更大尺寸图像，则机器很容易内存溢出。

### 哪些推理引擎有这个问题？

已知的是OpenVino和PaddlePaddle存在这个问题，ONNXRuntime没有。

### 可能的解决方案

总结自群友：**多进程/线程 + 定时重启**
