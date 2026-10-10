---
title: Using Local Models
description: Configure RapidOCR to use local PaddlePaddle, ONNX, PyTorch or other model files.
comments: true
hide:
  - toc
---

Local models can be configured through a YAML file or the `params` mapping. Detection, orientation classification and recognition use their corresponding `model_path` or `model_dir` fields.

## PaddlePaddle model directories

PaddlePaddle models use `model_dir`. Recognition models may also require `rec_keys_path`:

```python
from rapidocr import EngineType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Rec.model_dir": "models/paddle/PP-OCRv6_rec_tiny",
        "Rec.rec_keys_path": "models/paddle/PP-OCRv6_rec_tiny/ppocrv6_tiny_dict.txt",
        "Rec.engine_type": EngineType.PADDLE,
        "Rec.ocr_version": OCRVersion.PPOCRV6,
    }
)

result = engine("test.jpg")
print(result)
```

## Other model formats

ONNX, PyTorch and other file-based backends use `model_path`:

```python
from rapidocr import EngineType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Det.model_path": "models/torch/PP-OCRv6_det_tiny.pth",
        "Det.engine_type": EngineType.TORCH,
        "Det.ocr_version": OCRVersion.PPOCRV6,
    }
)

result = engine("test.jpg")
print(result)
```

The model architecture, OCR version, dictionary and preprocessing parameters must match. See the [model list](../../model_list.md) and [parameter reference](parameters.md) before combining custom files.
