---
title: 推理引擎汇总
date: 2022-09-22
authors: [SWHL]
slug: inference-summary
categories:
  - 推理引擎
comments: true
---

<!-- more -->

!!! warning

    This documentation is in progress

### 引言

- 关于模型的推理框架有很多，包括PC/移动端等等。
- 我在这里做一个简单汇总。但更侧重于寻找一个在GPU上，可以支持动态输入且在GPU上更快，轻量的推理引擎。

### 目前已知推理引擎

- CPU端：ONNXruntime、OpenVINO、libtorch、Caffe、PaddleInference
- GPU端：TensorRT、OpenPPL、AITemplate
- 移动端：NCNN，MNN, Paddle-Lite
- 通吃：TVM、OpenPPL

---

### ONNXRuntime（微软）

- 目前仓库中已经在使用的推理引擎，CPU端最好用的轻量推理引擎。支持动态输入。
- 目前在GPU端，动态输入的情况下，速度比CPU上还要慢一些，暂时尚未解决。
- ONNXRuntime + TensorRT结合 → 尝试但未跑通

### OpenVINO（英特尔）

- CPU端推理速度更快，支持动态输入。但是占用内存较大，拿空间换了时间。
- 当自己资源不吃紧时，但要求更快地推理速度时，可以考虑用这个。
- GPU端仅支持自家显卡，暂时用不到。

### MNN（阿里）

- GPU端没有找到容易的使用方式，需要自行编译，门槛太高。理想情况是像`onnxruntime-gpu`这种，可以快速安装使用。
- 说是支持动态输入，但是尚未找到有效验证方法。

### TensorRT（英伟达）

- GPU端快速推理，占坑
- 据说存在内存泄漏的bug，暂时没有尝试。

### NCNN（腾讯）

- 移动端比较好用的
- 存在一个问题：已有模型转换为NCNN格式，会遇到某些算子不支持情况

### Paddle Inference（百度）

- 定位是服务端推理框架
- 依赖Paddle框架，有些重，但是不失为GPU上推理模型的一个选择。
- 目前已经采用，对应`rapidocr_paddle`库，用以弥补GPU推理的短板。

### [Paddle Lite](https://www.paddlepaddle.org.cn/lite/v2.12/guide/introduction.html)

- Paddle Lite 是一组工具，可帮助开发者在移动设备、嵌入式设备和 loT 设备上运行模型，以便实现设备端机器学习。
- 定位是移动端和边缘端推理引擎

### Paddle.js

网页前端推理引擎

### [FastDeploy（百度）](https://github.com/PaddlePaddle/FastDeploy)

FastDeploy是一款全场景、易用灵活、极致高效的AI推理部署工具， 支持云边端部署。提供超过 🔥160+ Text，Vision， Speech和跨模态模型📦开箱即用的部署体验，并实现🔚端到端的推理性能优化。包括 物体检测、字符识别（OCR）、人脸、人像扣图、多目标跟踪系统、NLP、Stable Diffusion文图生成、TTS 等几十种任务场景，满足开发者多场景、多硬件、多平台的产业部署需求。

总结来说就是，将各个场景下的推理引擎做了集成，更加方便易用，大而全。

### [PaddleX](https://paddlepaddle.github.io/PaddleX/latest/)

PaddleX 集成飞桨智能视觉领域图像分类、目标检测、语义分割、实例分割任务能力，将深度学习开发全流程从数据准备、模型训练与优化到多端部署端到端打通，并提供统一任务API接口及图形化开发界面Demo。开发者无需分别安装不同套件，以低代码的形式即可快速完成飞桨全流程开发。

总结来说，PaddleX就是一个整合已有模型的低代码平台。严格意义来说，不算一个推理引擎。
