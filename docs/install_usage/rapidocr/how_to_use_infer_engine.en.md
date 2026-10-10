---
title: Using Different Inference Engines
description: Install and configure ONNX Runtime, OpenVINO, PaddlePaddle, PyTorch, MNN and TensorRT backends in RapidOCR.
comments: true
hide:
  - toc
---

## Overview

Since `rapidocr>=3.0.0`, detection, orientation classification and recognition can use different inference engines. The default backend is ONNX Runtime CPU.

Supported engines include ONNX Runtime, OpenVINO, PaddlePaddle, PyTorch, MNN and TensorRT. Check the [model list](../../model_list.md) before selecting a backend because support depends on the model route.

!!! info

    This page covers the common installation and configuration path. Provider-specific options, benchmark data and troubleshooting details are maintained in the [complete Chinese reference](how_to_use_infer_engine.md).

## ONNX Runtime

Install the CPU backend:

```bash
pip install onnxruntime
```

ONNX Runtime is the default backend, so no extra parameter is required. GPU execution is not generally recommended for OCR detection because dynamic image shapes can reduce performance.

## OpenVINO

```bash
pip install openvino
```

```python
from rapidocr import EngineType, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.OPENVINO,
        "Cls.engine_type": EngineType.OPENVINO,
        "Rec.engine_type": EngineType.OPENVINO,
    }
)
```

## PaddlePaddle

Install the PaddlePaddle package appropriate for your operating system and hardware, then select `EngineType.PADDLE` for the desired stages.

```python
from rapidocr import EngineType, RapidOCR

engine = RapidOCR(params={"Rec.engine_type": EngineType.PADDLE})
```

## PyTorch and Apple MPS

Install PyTorch from the [official selector](https://pytorch.org/get-started/locally/). MPS support requires `rapidocr>=3.7.0` and compatible Apple hardware:

```python
from rapidocr import EngineType, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.TORCH,
        "Cls.engine_type": EngineType.TORCH,
        "Rec.engine_type": EngineType.TORCH,
        "EngineConfig.torch.use_mps": True,
    }
)
```

Verify `torch.backends.mps.is_available()` before running a production workload.

## MNN and TensorRT

MNN is supported from `rapidocr>=3.6.0`. TensorRT is supported from `rapidocr>=3.7.0`; the engine file is built from the selected ONNX model on first use and requires a compatible NVIDIA environment.

For installation details, provider-specific options and troubleshooting, see the [Chinese inference-engine reference](how_to_use_infer_engine.md).
