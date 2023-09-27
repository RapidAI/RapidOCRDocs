---
weight: 403
title: "GPU版推理"
description:
icon: menu_book
date: "2022-09-24"
draft: false
toc: true
---

### onnxruntime-gpu版相关说明
- 目前已知在onnxruntime-gpu上测试过的小伙伴，反映都是GPU推理速度比在CPU上慢很多。关于该问题，已经提了相关issue，具体可参见[onnxruntime issue#13198](https://github.com/microsoft/onnxruntime/issues/13198)

### 有关`onnxruntime-gpu`推理慢的相关帖子
- [Pre-allocating dynamic shaped tensor memory for ONNX runtime inference?](https://stackoverflow.com/questions/75553839/pre-allocating-dynamic-shaped-tensor-memory-for-onnx-runtime-inference)

### 快速查看比较版本
- 国外小伙伴可以基于[Google Colab](https://colab.research.google.com/gist/SWHL/673c39bf07f4cc4ddcb0e196c3e378e6/testortinfer.ipynb)，国内的小伙伴可以基于百度的[AI Studio](https://aistudio.baidu.com/aistudio/projectdetail/4634684?contributionType=1&sUid=57084&shared=1&ts=1664700017761)来查看效果

### 结论
onnxruntime-gpu版在动态输入情况下，推理速度要比CPU慢很多。而OCR任务就是动态输入，因此不推荐使用onnxruntime-gpu版推理。

目前一直在找寻GPU端，可以快速推理ONNX模型的推理引擎。

### 相关对比表格
|设备|onnxruntime-gpu|CPU总耗时(s)|CPU平均耗时(s/img)|GPU总耗时(s)|GPU平均耗时(s/img)||
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|设备1[^1]|1.11.0|296.8841|1.18282|646.14667|2.57429|
|设备2[^2]|1.12.1|149.35427|0.50504|250.81760|0.99927|

[^1]: 宏碁(Acer) 暗影骑士·威N50-N93游戏台式机 | Windows | 十代i5-10400F 16G 512G SSD | NVIDIA GeForce GTX 1660Super 6G

[^2]: Linux | AMD R9 5950X | NVIDIA GeForce RTX 3090