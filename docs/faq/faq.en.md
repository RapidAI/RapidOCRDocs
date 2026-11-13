---
title: Frequently Asked Questions (FAQ)
description: Frequently asked questions about RapidOCR, covering ONNX Runtime GPU/CPU performance, Windows/Linux dependencies, the relationship with PaddleOCR, model downloads, and more.
comments: true
hide:
  - navigation
  - toc
---

#### Q: Why is my model slower on the ONNX Runtime GPU build than on CPU?

**A:** Because the input image shape in OCR tasks is dynamic. On the GPU, the cached results from the previous different shape must be cleared each time. If the input image shape stays the same, the ONNX Runtime GPU build is generally faster than the CPU build. A related issue has been filed: issue #13198.

For the current version, it is recommended to use `rapidocr` consistently and then select ONNX Runtime, OpenVINO, Paddle, PyTorch or another inference engine as needed. For installation methods and limitations, see [Using Different Inference Engines](../install_usage/rapidocr/how_to_use_infer_engine.md).

#### Q: Can this be used in 32-bit C#?

**A:** C# can be 32-bit and requires a 32-bit DLL, but the onnxruntime package on NuGet does not support Windows 7.

#### Q: On Windows, after installing the environment and running the sample program, I get `OSError: [WinError 126] The specified module could not be found`.

**A:** The cause is usually that the Shapely binary dependency was not installed correctly. It is recommended to upgrade `pip` first and then reinstall:

```bash
python -m pip install -U pip
python -m pip install -U Shapely
```

If you are using Conda, you can also run `conda install -c conda-forge shapely`.

#### Q: When deploying a Python program on Linux, `import cv2` raises `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`. What should I do?

**A:** There are two [solutions](https://stackoverflow.com/questions/63977422/error-trying-to-import-cv2opencv-python-package/63978454) (from community member ddeef):

  1. Install `opencv-python-headless` instead of `opencv-python`;
  2. Run `sudo apt-get install -y libgl1-mesa-dev`

#### Q: My compiled process crashes when invoked through cmd on Windows 7. What is going on?

**A:** Windows 7 is not supported (by @如果我有時光機)

#### Q: Can you provide something similar to OpenMMLab for information extraction?

**A:** This is currently under investigation and testing. If the key information extraction in MMOCR performs well enough, we will consider integrating it later.

#### Q: What is the relationship between RapidOCR and PaddleOCR?

**A:** RapidOCR converts PaddleOCR pretrained models into ONNX models. It does not depend on the Paddle framework, which makes deployment on various platforms easier.

#### Q: Has anyone compiled onnxruntime for arm32? I compiled it successfully, but when using it I get `libonnxruntime.so:-1: error: file not recognized: File format not recognized`. Is this a version mismatch?

**A:** This is usually caused by a mismatch between the library architecture and the runtime environment. Check the following in order:

1. Run `uname -m` to confirm the device architecture;
2. Run `file libonnxruntime.so` to confirm the shared library architecture; the two should match;
3. If you are cross-compiling, confirm that the target platform, ABI and C/C++ runtime versions are consistent;
4. Run `ldd libonnxruntime.so` to check for missing shared library dependencies.

It is recommended to compile directly on the target device, or to download a build that matches the device architecture.

#### Q: Does the C++ demo require Visual Studio 2017 or later?

**A:** Visual Studio 2019 or later is recommended, and the project, OpenCV and ONNX Runtime should all use the same target architecture (usually x64). If you need to support older compilers, follow the build configuration of the corresponding C++ sample project.

#### Q: Can it achieve the same results as Baidu EasyEdge Free App?

**A:** The edge models are probably not open source. Among Baidu's open-source models, the `server det` model can achieve comparable recognition results, but the model is relatively large.

#### Q: When I run ONNX inference in C++, it seems to use only the CPU; the GPU does not respond. Why?

**A:** To use the GPU, you need to install the `onnxruntime-gpu` build and add the EP (execution provider) in the onnxruntime code yourself. Our positioning is general-purpose, so we only use CPU inference.

#### Q: I would like to deploy OCR recognition. Do you provide a Linux OCR deployment package?

**A:** This repository does not publish a unified Linux C++ binary package. It is recommended to refer to the build instructions of [RapidOcrOnnx](https://github.com/RapidAI/RapidOcrOnnx), or compile OpenCV and ONNX Runtime yourself for the target platform.

#### Q: Where can I download the compiled onnxruntime C++ libraries?

**A:** Here: <https://github.com/RapidAI/OnnxruntimeBuilder/releases/tag/1.7.0>

#### Q: My current simple test environment is Windows 10 + Cygwin + gcc + pure C programming. Can I integrate simple OCR functionality directly into a C program?

**A:** Just use the API directly; the API is exported by C.

#### Q: Model download addresses

**A:** [Baidu Netdisk](https://pan.baidu.com/s/1PTcgXG2zEgQU6A_A3kGJ3Q?pwd=jhai) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing)

#### Q: Error under onnxruntime 1.7: `onnxruntime::SequentialExecutor::Execute] Non-zero status code returned while running ScatterND node. Name:'ScatterND@1' Status Message: updates`

**A:** This is a compatibility issue between an old model and an old version of ONNX Runtime. Please upgrade RapidOCR and the model first. If the error persists, provide the RapidOCR, ONNX Runtime and Python versions along with the complete error log.

#### Q: A line of text near the image edge is never recognized. What should I do?

**A:** Add a value to the padding parameter; the default is 0, and you can add 5 or 10, or even more, until it can be recognized. Be careful not to add too much, as it wastes memory.
