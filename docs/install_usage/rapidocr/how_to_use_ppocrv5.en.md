---
title: Using PP-OCRv5 Models
description: Select PP-OCRv5 detection and recognition models in RapidOCR.
comments: true
hide:
  - toc
---

PP-OCRv5 models are supported in `rapidocr>=3.0.0`. Detection, classification and recognition are configured independently, so different versions and inference engines can be combined when their routes are compatible.

```python
from rapidocr import EngineType, LangDet, LangRec, ModelType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.CH,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV5,
        "Rec.engine_type": EngineType.ONNXRUNTIME,
        "Rec.lang_type": LangRec.CH,
        "Rec.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV5,
    }
)

image_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(image_url)
print(result)
result.vis("vis_result.jpg")
```

See the [model list](../../model_list.md) for valid language, model size and backend combinations.
