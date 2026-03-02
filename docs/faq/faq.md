---
title: 常见问题 (FAQ)
comments: true
hide:
  - toc
---

#### Q: 为什么我的模型在 ONNX Runtime GPU 版上比在 CPU 上还要慢？

**A:** 因为 OCR 任务中输入图像 Shape 是动态的。每次 GPU 上都需要重新清空上一次不同 Shape 的缓存结果。如果输入图像 Shape 不变的情况下，ONNX Runtime GPU 版一般都要比 CPU 快的。该问题已经提了相关 issue #13198。

推荐 CPU 端推理用 `rapidocr_onnxruntime` 或者 `rapidocr_openvino`，GPU 端用 `rapidocr_paddle`。关于 `rapidocr_onnxruntime` 和 `rapidocr_paddle` 两者之间推理，可参见：[docs](https://rapidai.github.io/RapidOCRDocs/v1.4.4/install_usage/rapidocr_paddle/usage/#_4)

#### Q: 请问这个能在 32 位 C#中用嘛?

**A:** C#可以 32 位，要用 32 位的 dll，但 nuget 上的 onnxruntime 不支持 win7。

#### Q: Windows 系统下，装完环境之后，运行示例程序之后，报错 OSError: [WinError 126] 找不到指定的模組

**A:** 原因是 Shapely 库没有正确安装，如果是在 Windows，可以在 [Shapely whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) 下载对应的 whl 包，离线安装即可；另外一种解决办法是用 conda 安装也可。

#### Q: Linux 部署 python 的程序时，`import cv2` 时会报 `ImportError: ligGL.so.1: cannot open shared object file: No such file or directory`?

**A:** [解决方法](https://stackoverflow.com/questions/63977422/error-trying-to-import-cv2opencv-python-package/63978454
) 有两个 (来自群友 ddeef)：

  1. 安装 `opencv-python-headless` 取代 `opencv-python`;
  2. 运行 `sudo apt-get install -y libgl1-mesa-dev`

#### Q: 询问下，我编译出来的进程在 win7 下面通过 cmd 调用，发生了崩溃的情况?

**A:** 不支持 win7 (by @如果我有時光機)

#### Q: 能不能搞个 openmmlab 类似的那个提取信息的?

**A:** 这个目前正在调研测试当中，如果 mmocr 中关键信息提取效果还可以，后期会考虑整合进来。

#### Q: RapidOCR 和 PaddleOCR 是什么关系呢？

**A:** RapidOCR 是将 PaddleOCR 的预训练模型转为 onnx 模型，不依赖 paddle 框架，方便各个平台部署。

#### Q: onnxruntime arm32 有人编译过吗？ 我编译成功了，但是使用的时候 libonnxruntime.so:-1: error: file not recognized: File format not recognized  应该是版本不匹配

**A:** 没遇到过。我是直接在当前平台编译的，我们用的是 arm。估计是平台不兼容,建议在本身平台上编译。没遇到过问题。通常出在交叉编译方式下。

#### Q: 请问一下 c++ demo 必须要 vs2017 及以上版本吗?

**A:** 最好用 vs2019

#### Q: 可以达到百度 EasyEdge Free App 的效果吗？

**A:** edge 的模型应该没有开源。百度开源的模型里 server det 的识别效果可以达到，但是模型比较大。

#### Q: 我用 c++ 推理 onnx 貌似是 cpu 推理的，gpu 没有反应?

**A:** 如果想用 GPU 的话，需要安装 onnxruntime-gpu 版，自己在 onnxruntime 的代码中添加 EP (execution provider)。我们的定位是通用，只用 cpu 推理。

#### Q: 您好，我想部署下咱们的 ocr 识别，有提供 linux 版本的 ocr 部署包吗?

**A:** linux 版本的自己编译即可, 可以参考我们的 action 中的脚本；其实编译非常容易，安装个 opencv 后，在 cmakelists.txt 中修改一下 onnxruntime 的路径即可，具体参考这个： <https://github.com/RapidAI/RapidOCR/blob/v0.1.5/.github/workflows/make-linux.yml>

#### Q: onnxruntime 编译好的 C++ 库，哪里可以下载到？

**A:** 从这里：<https://github.com/RapidAI/OnnxruntimeBuilder/releases/tag/1.7.0>

#### Q: 目前简单测试环境是  Win10 + Cygwin + gcc + 纯 C 编程，可以在 C 程序中直接接入简单 OCR 功能吗？

**A:** 直接使用 API 就行，API 就是由 c 导出的

#### Q: 模型下载地址

**A:** [百度网盘](https://pan.baidu.com/s/1PTcgXG2zEgQU6A_A3kGJ3Q?pwd=jhai) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing)

#### Q: onnxruntime 1.7 下出错：onnxruntime::SequentialExecutor::Execute] Non-zero status code returned while running ScatterND node. Name:'ScatterND@1' Status Message: updates

**A:** 由于模型只支持 `onnxruntime=1.5.0` 导致，请更新模型,下载地址见 `Q3`

#### Q: 边缘总有一行文字无法识别，怎么办？

**A:** 在 padding 参数中添加一个值 ，默认是 0,你可以添加 5 或 10, 甚至更大，直到能识别为止。注意不要添加过大，会浪费内存。
