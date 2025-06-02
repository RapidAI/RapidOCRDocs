---
comments: true
hide:
  - navigation
  - toc

---

针对PaddleOCR已经发布的常用模型，我们这里已经做了统一转换和汇总，包括PaddlePaddle格式、ONNX格式和PyTorch格式。

所有模型目前托管在[魔搭社区](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)上。

### 所有模型汇总

请移步以下链接查看：

[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml)

!!! note

    并不是所有的模型都有 **server** 版本，具体哪个有，可以参见：[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/a9bb7c1f44b6e00556ada90ac588f020d7637c4b/python/rapidocr/default_models.yaml)。配置文件中带有server字样的即是有server版本。

### 具体配置文件中字段对应

文本检测模型：

|语种类型|engine_type| lang_type|model_type|ocr_version|
|:---|:---|:---|:---|:---|
|简体中文、中文拼音、繁体中文、英文、日文|`onnxruntime` <br/> `openvino` <br/> `paddle`|`ch`|`mobile`<br/> `server`|`PP-OCRv5`|
|中英|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`|`ch`|`mobile`<br/> `server`|`PP-OCRv4`|
|英语和拉丁语|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`|`en`|`mobile`<br/> `server`|`PP-OCRv4`<br/>|
|多语种|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`|`multi`|`mobile`|`PP-OCRv4`<br/>|

对应使用方法：

!!! note

    `lang_type`字段对应Det模块下的`LangDet`

```python linenums="1" hl_lines="5-8"
from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.TORCH,
        "Det.lang_type": LangDet.CH,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV5
    }
)
```

文本识别模型：

!!! note

    `lang_type`字段对应Det模块下的`LangRec`

| 语种类型       | engine_type               | lang_type         | model_type      | ocr_version       |
|----------------|---------------------------|-------------------|-----------------|-------------------|
| 简体中文、中文拼音、繁体中文、英文、日文 | `onnxruntime`<br>`openvino`<br>`paddle` | `ch`            | `mobile`<br>`server` | `PP-OCRv5` |
| 中文文档       | `onnxruntime`<br>`openvino`<br>`paddle` | `ch`            | `server` | `PP-OCRv4` |
| 中文           | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `ch`            | `mobile`<br>`server` | `PP-OCRv4` |
| 中文繁体       | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `chinese_cht`   | `mobile`<br>`server`   | `PP-OCRv4` |
| 英文           | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `en`            | `en_mobile`     | `PP-OCRv4` |
| 阿拉伯文       | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `ar`            | `ar_mobile`     | `PP-OCRv4` |
| 塞尔维亚文     | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `cyrillic`      | `cyrillic_mobile` | `PP-OCRv4` |
| 梵文           | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `devanagari`    | `devanagari_mobile` | `PP-OCRv4` |
| 日文           | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `japan`         | `japan_mobile`  | `PP-OCRv4` |
| 卡纳达语       | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `ka`            | `ka_mobile`     | `PP-OCRv4` |
| 韩文           | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `korean`        | `korean_mobile` | `PP-OCRv4` |
| 拉丁文         | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `latin`         | `latin_mobile`  | `PP-OCRv4` |
| 泰米尔文       | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `ta`            | `ta_mobile`     | `PP-OCRv4` |
| 泰卢固文       | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` | `te`            | `te_mobile`     | `PP-OCRv4` |

### 使用方式

以上模型可直接通过字段指定，程序会自动下载使用。

```python linenums="1" hl_lines="5-7"
from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Rec.ocr_version": OCRVersion.PPOCRV5,
        "Rec.engine_type": EngineType.PADDLE,
        "Rec.model_type": ModelType.MOBILE,
    }
)

img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```
