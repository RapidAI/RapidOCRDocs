---
title: Frequently Asked Questions (FAQ)
description: Frequently asked questions about RapidOCR inference engines, dependencies, platforms and model compatibility.
comments: true
hide:
  - toc
---

#### Why can ONNX Runtime GPU be slower than CPU for OCR?

OCR detection uses dynamic image shapes. Different shapes can reduce GPU reuse and add memory-management overhead. For many workloads, ONNX Runtime CPU is therefore faster. See the [inference engine guide](../install_usage/rapidocr/how_to_use_infer_engine.md) for current recommendations.

#### Does RapidOCR support 32-bit C#?

The application and native DLL must use the same architecture. A 32-bit C# application requires a 32-bit DLL and compatible native dependencies. Windows 7 is not supported by recent ONNX Runtime packages.

#### Windows reports `OSError: [WinError 126]` after installation. What should I do?

This is often caused by a missing or incompatible Shapely binary dependency. Upgrade pip and reinstall Shapely:

```bash
python -m pip install -U pip
python -m pip install -U Shapely
```

With Conda, you can use `conda install -c conda-forge shapely`.

#### Linux reports `libGL.so.1` when importing OpenCV.

For headless servers, install `opencv-python-headless` instead of `opencv-python`. If GUI support is required, install the system OpenGL dependency, for example:

```bash
sudo apt-get install -y libgl1-mesa-dev
```

#### What is the relationship between RapidOCR and PaddleOCR?

RapidOCR converts and packages PaddleOCR models for lightweight, cross-platform inference. It does not require the Paddle framework when using the corresponding RapidOCR inference engine.

#### How can I diagnose an ARM library format error?

If `libonnxruntime.so` reports `File format not recognized`, verify that the library and device use the same architecture:

```bash
uname -m
file libonnxruntime.so
ldd libonnxruntime.so
```

For cross-compilation, also verify the target ABI and C/C++ runtime. Building directly on the target device is usually the simplest option.

#### How can I improve recognition near an image edge?

Increase the padding-related parameter gradually, for example to `5` or `10`. Very large padding values increase memory usage and may slow inference.

#### How do I resolve an old `ScatterND` compatibility error?

This usually indicates an old model paired with an incompatible ONNX Runtime version. Upgrade RapidOCR and the model first. If the error remains, include the RapidOCR, ONNX Runtime and Python versions together with the complete traceback when reporting the issue.
