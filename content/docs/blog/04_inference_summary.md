---
weight: 3410
title: "推理引擎汇总"
description:
icon: menu_book
lastmod: "2022-09-22"
toc: true
---


{{% alert context="warning" text="**Caution** - This documentation is in progress" /%}}

#### 引言
- 关于模型的推理框架有很多，包括PC/移动端等等。之前在[老潘的个人博客](https://ai.oldpan.me/t/topic/24)里看到过相关介绍
- 我在这里做一个简单汇总。但更侧重于寻找一个在GPU上，可以支持动态输入且在GPU上更快，轻量的推理引擎。

#### 目前已知推理引擎
- CPU端：ONNXruntime、OpenVINO、libtorch、Caffe、PaddleInference
- GPU端：TensorRT、OpenPPL、AITemplate
- 移动端：NCNN，MNN, Paddle-Lite
- 通吃：TVM、OpenPPL

---

#### ONNXRuntime（微软）
- 目前仓库中已经在使用的推理引擎，CPU端最好用的轻量推理引擎。支持动态输入。
- 目前在GPU端，动态输入的情况下，速度比CPU上还要慢一些，暂时尚未解决。
- ONNXRuntime + TensorRT结合 → 尝试但未跑通

#### OpenVINO（英特尔）
- CPU端推理速度更快，支持动态输入。但是占用内存较大，拿空间换了时间。
- 当自己资源不吃紧时，但要求更快地推理速度时，可以考虑用这个。
- GPU端仅支持自家显卡，暂时用不到。

#### MNN（阿里）
- GPU端没有找到容易的使用方式，需要自行编译，门槛太高。理想情况是像`onnxruntime-gpu`这种，可以快速安装使用。
- 说是支持动态输入，但是尚未找到有效验证方法。

#### TensorRT（英伟达）
- GPU端快速推理，占坑
- 据说存在内存泄漏的bug，暂时没有尝试。

#### Paddle Inference（百度）
- 依赖Paddle框架，有些重，但是不失为GPU上推理模型的一个选择。
- 暂时不考虑这个，因为paddlepaddle-gpu版有大约500M左右，太太了。

#### NCNN（腾讯）
- 移动端比较好用的

#### [FastDeploy（百度）](https://github.com/PaddlePaddle/FastDeploy)
- TODO