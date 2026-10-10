---
title: RapidOCR Model List
description: Supported PP-OCRv4, PP-OCRv5 and PP-OCRv6 models, inference engines and language routes.
comments: true
hide:
  - navigation
---

## Overview

RapidOCR provides converted PaddleOCR models in ONNX, OpenVINO, MNN, PaddlePaddle and PyTorch formats. TensorRT engines are built dynamically from the corresponding ONNX model on first use.

Models are hosted on [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/files). In `rapidocr>=3.10.0`, model selection is routed by [`default_models.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml).

You can select a language, OCR version and model size through `RapidOCR` parameters. For example:

!!! info

    This page summarizes the main model routes. The [complete Chinese model reference](https://rapidai.github.io/RapidOCRDocs/latest/model_list/) contains the full route matrix, aliases, language table and version-specific defaults.

```python
from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Rec.engine_type": EngineType.ONNXRUNTIME,
        "Rec.lang_type": "japan",
        "Rec.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV4,
    }
)
```

## Main model routes

| Task | Version | Sizes / languages | Common engines |
| --- | --- | --- | --- |
| Detection | PP-OCRv6 | `tiny`, `small`, `medium`, multilingual | ONNX Runtime, OpenVINO, MNN, Paddle, PyTorch |
| Recognition | PP-OCRv6 | `tiny`, `small`, `medium`, multilingual | ONNX Runtime, OpenVINO, MNN, Paddle, PyTorch |
| Detection | PP-OCRv5 | `mobile`, `server` | ONNX Runtime, OpenVINO, MNN, Paddle, PyTorch |
| Orientation | PP-OCRv5 | `mobile`, `server` | ONNX Runtime, OpenVINO, MNN, Paddle |
| Recognition | PP-OCRv5 | Chinese, Korean, Latin, English and other routes | ONNX Runtime, OpenVINO, MNN, Paddle |
| Detection / recognition | PP-OCRv4 | Chinese, English and multilingual routes | ONNX Runtime, OpenVINO, MNN, Paddle, PyTorch |

PP-OCRv6 `small` and `medium` support the broadest multilingual routes. `tiny` supports the same routes except Japanese. Language aliases such as `zh` → `ch` and `ja` → `japan` are also supported where the selected route provides them.

## Choosing a model

- Use `tiny` when package size and edge-device speed are the priority.
- Use `small` as the general-purpose default.
- Use `medium` when recognition quality is more important than resource usage.
- Check the selected language route before choosing a multilingual model.
- Install the [RTL extra dependency](install_usage/rapidocr/install.md) for right-to-left languages such as Arabic.

For the complete route matrix and language table, see the [Chinese model reference](https://rapidai.github.io/RapidOCRDocs/latest/model_list/) and [`default_models.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml).
