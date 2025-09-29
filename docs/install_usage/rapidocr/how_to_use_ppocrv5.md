---
comments: true
hide:
  - toc
---

在`rapidocr>=3.0.0`中，已经支持PP-OCRv5模型的调用了，下面会给出简单示例使用。至于如何具体使用哪些参数，有哪些组合可以使用，请参见[模型列表](../../model_list.md)。

值得说明的是，得益于解耦的设计，现在可以组合不同推理引擎、不同版本模型来灵活搭配使用。大家可以按需搭配哈。

```python linenums="1" hl_lines="3-14"
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

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```
