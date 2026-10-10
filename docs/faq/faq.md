---
title: 常见问题 (FAQ)
description: RapidOCR 常见问题，覆盖 ONNX Runtime GPU/CPU 性能、Windows/Linux 依赖、PaddleOCR 关系、模型下载等问题。
comments: true
hide:
  - navigation
  - toc
---

#### Q: 为什么我的模型在 ONNX Runtime GPU 版上比在 CPU 上还要慢？

**A:** 因为 OCR 任务中输入图像 Shape 是动态的。每次 GPU 上都需要重新清空上一次不同 Shape 的缓存结果。如果输入图像 Shape 不变的情况下，ONNX Runtime GPU 版一般都要比 CPU 快的。该问题已经提了相关 issue #13198。

当前版本建议统一使用 `rapidocr`，再按需选择 ONNX Runtime, OpenVINO, Paddle, PyTorch 或其他推理引擎。具体安装方式和限制请参见 [使用不同推理引擎](../install_usage/rapidocr/how_to_use_infer_engine.md)。

#### Q: 请问这个能在 32 位 C#中用嘛?

**A:** C#可以 32 位，要用 32 位的 dll，但 nuget 上的 onnxruntime 不支持 win7。

#### Q: Windows 系统下，装完环境之后，运行示例程序之后，报错 OSError: [WinError 126] 找不到指定的模組

**A:** 原因通常是 Shapely 二进制依赖没有正确安装。建议优先升级 `pip` 后重新安装：

```bash
python -m pip install -U pip
python -m pip install -U Shapely
```

如果使用 Conda，也可以运行 `conda install -c conda-forge shapely`。

#### Q: Linux 部署 Python 程序时，`import cv2` 报 `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`，怎么办？

**A:** [解决方法](https://stackoverflow.com/questions/63977422/error-trying-to-import-cv2opencv-python-package/63978454) 有两个 (来自群友 ddeef)：

  1. 安装 `opencv-python-headless` 取代 `opencv-python`;
  2. 运行 `sudo apt-get install -y libgl1-mesa-dev`

#### Q: 询问下，我编译出来的进程在 win7 下面通过 cmd 调用，发生了崩溃的情况?

**A:** 不支持 win7 (by @如果我有時光機)

#### Q: 能不能搞个 openmmlab 类似的那个提取信息的?

**A:** 这个目前正在调研测试当中，如果 mmocr 中关键信息提取效果还可以，后期会考虑整合进来。

#### Q: RapidOCR 和 PaddleOCR 是什么关系呢？

**A:** RapidOCR 是将 PaddleOCR 的预训练模型转为 onnx 模型，不依赖 paddle 框架，方便各个平台部署。

#### Q: onnxruntime arm32 有人编译过吗？我编译成功了，但是使用的时候 libonnxruntime.so:-1: error: file not recognized: File format not recognized  应该是版本不匹配

**A:** 这通常是库文件架构与运行环境不一致导致的。建议依次检查：

1. 运行 `uname -m` 确认设备架构；
2. 运行 `file libonnxruntime.so` 确认动态库架构，二者应一致；
3. 如果使用交叉编译，确认目标平台、ABI 和 C/C++ 运行库版本一致；
4. 使用 `ldd libonnxruntime.so` 检查是否存在缺失的动态库依赖。

建议优先在目标设备上直接编译，或下载与设备架构匹配的构建产物。

#### Q: 请问一下 c++ demo 必须要 vs2017 及以上版本吗?

**A:** 建议使用 Visual Studio 2019 或更高版本，并确保项目、OpenCV 和 ONNX Runtime 使用相同的目标架构（通常为 x64）。如果需要支持更旧的编译器，请以对应 C++ 示例工程的构建配置为准。

#### Q: 可以达到百度 EasyEdge Free App 的效果吗？

**A:** edge 的模型应该没有开源。百度开源的模型里 server det 的识别效果可以达到，但是模型比较大。

#### Q: 我用 c++ 推理 onnx 貌似是 cpu 推理的，gpu 没有反应?

**A:** 如果想用 GPU 的话，需要安装 onnxruntime-gpu 版，自己在 onnxruntime 的代码中添加 EP (execution provider)。我们的定位是通用，只用 cpu 推理。

#### Q: 您好，我想部署下咱们的 ocr 识别，有提供 linux 版本的 ocr 部署包吗?

**A:** 当前仓库没有统一发布的 Linux C++ 二进制包。建议参考 [RapidOcrOnnx](https://github.com/RapidAI/RapidOcrOnnx) 的构建说明，或根据目标平台自行编译 OpenCV 和 ONNX Runtime。

#### Q: onnxruntime 编译好的 C++ 库，哪里可以下载到？

**A:** 从这里：<https://github.com/RapidAI/OnnxruntimeBuilder/releases/tag/1.7.0>

#### Q: 目前简单测试环境是  Win10 + Cygwin + gcc + 纯 C 编程，可以在 C 程序中直接接入简单 OCR 功能吗？

**A:** 直接使用 API 就行，API 就是由 c 导出的

#### Q: 模型下载地址

**A:** [百度网盘](https://pan.baidu.com/s/1PTcgXG2zEgQU6A_A3kGJ3Q?pwd=jhai) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing)

#### Q: onnxruntime 1.7 下出错：onnxruntime::SequentialExecutor::Execute] Non-zero status code returned while running ScatterND node. Name:'ScatterND@1' Status Message: updates

**A:** 这是旧模型与旧版 ONNX Runtime 的兼容性问题。请优先升级 RapidOCR 和模型；如果仍然报错，请提供 RapidOCR, ONNX Runtime, Python 版本以及完整错误日志。

#### Q: 边缘总有一行文字无法识别，怎么办？

**A:** 在 padding 参数中添加一个值，默认是 0,你可以添加 5 或 10, 甚至更大，直到能识别为止。注意不要添加过大，会浪费内存。
