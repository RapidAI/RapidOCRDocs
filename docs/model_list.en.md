---
title: RapidOCR Model List
description: Detection, orientation classification and recognition models for PP-OCRv4, PP-OCRv5 and PP-OCRv6 supported by RapidOCR, along with the inference engine and language support matrix.
comments: true
hide:
  - navigation
#   - toc
---


## Introduction

For the commonly used models already released by PaddleOCR, we have carried out a unified conversion and aggregation here, including the PP-OCRv4, PP-OCRv5 and PP-OCRv6 series in PaddlePaddle, ONNX, MNN and PyTorch formats. TensorRT dynamically builds an Engine file matching the current hardware from the ONNX model on first run.

All models are currently hosted on [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/files).

`rapidocr` v3 has integrated all the hosted models, which can be downloaded automatically by specifying the parameters below. Corresponding configuration file: [default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml). Of course, you can also download them yourself from the link above.

Starting from `rapidocr>=3.10.0`, model selection is managed uniformly by the model routes in [default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml). After the user passes in the language, model type and OCR version, RapidOCR automatically resolves the actual model file.

Starting from `rapidocr>=3.10.0`, `lang_type` is no longer limited to the `LangDet`, `LangCls` or `LangRec` enums; it can also be passed directly as a language code string, such as `"japan"`, `"korean"` or `"arabic"`. The string code must match a route for the current task, OCR version and model type; the supported codes and aliases are governed by the model route details in this document and `default_models.yaml`. The original enum syntax remains compatible.

For example, the following recognition configuration uses a language code string directly, without first converting it to the `LangRec` enum:

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

When using RTL languages such as Arabic, please first install the [RTL extra dependencies](install_usage/rapidocr/install.md).

## Default Configuration

After installing `rapidocr` via pip, you can use it directly without specifying any parameters, because the whl package pre-packages the default models and provides the default configuration at the same time.

The default configuration differs between versions of `rapidocr`. The default configurations corresponding to the different versions are given in detail below.

=== "`rapidocr>=3.9.0` Default Configuration"

    ```python linenums="1"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis("vis_result.jpg")
    ```

    Equivalent to the following:

    ```python linenums="1" hl_lines="5-16"
    from rapidocr import EngineType, LangDet, LangRec, ModelType, OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.ONNXRUNTIME,
            "Det.lang_type": LangDet.CH,
            "Det.model_type": ModelType.SMALL,
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Rec.engine_type": EngineType.ONNXRUNTIME,
            "Rec.lang_type": LangRec.CH,
            "Rec.model_type": ModelType.SMALL,
            "Rec.ocr_version": OCRVersion.PPOCRV6,
            "Cls.engine_type": EngineType.ONNXRUNTIME,
            "Cls.lang_type": LangDet.CH,
            "Cls.model_type": ModelType.MOBILE,
            "Cls.ocr_version": OCRVersion.PPOCRV4,
        }
    )

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis("vis_result.jpg")
    ```

    Corresponding configuration file: [config.yaml](https://github.com/RapidAI/RapidOCR/blob/v3.9.0/python/rapidocr/config.yaml)

=== "`rapidocr<3.9.0` Default Configuration"

    ```python linenums="1"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis("vis_result.jpg")
    ```

    Equivalent to the following:

    ```python linenums="1" hl_lines="5-16"
    from rapidocr import EngineType, LangDet, LangRec, ModelType, OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.ONNXRUNTIME,
            "Det.lang_type": LangDet.CH,
            "Det.model_type": ModelType.MOBILE,
            "Det.ocr_version": OCRVersion.PPOCRV4,
            "Rec.engine_type": EngineType.ONNXRUNTIME,
            "Rec.lang_type": LangRec.CH,
            "Rec.model_type": ModelType.MOBILE,
            "Rec.ocr_version": OCRVersion.PPOCRV4,
            "Cls.engine_type": EngineType.ONNXRUNTIME,
            "Cls.lang_type": LangDet.CH,
            "Cls.model_type": ModelType.MOBILE,
            "Cls.ocr_version": OCRVersion.PPOCRV4,
        }
    )

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis("vis_result.jpg")
    ```

    Corresponding configuration file: [config.yaml](https://github.com/RapidAI/RapidOCR/blob/v3.8.4/python/rapidocr/config.yaml)

## Configuration File Field Mapping

The following tables are based on `default_models.yaml` of `rapidocr>=3.10.0`. `engine_type` lists only the inference engines that directly register model files in the configuration file; TensorRT dynamically builds the Engine using the corresponding ONNX model. For usage limitations, see the [TensorRT inference engine description](install_usage/rapidocr/how_to_use_infer_engine.md).

The `tiny`, `small` and `medium` models of PP-OCRv6 are all multilingual models. Under the same specification, different `lang_type` values route to the same model file:

- `small` and `medium` support: `ch, chinese_cht, en, japan, af, az, bs, ca, cs, cy, da, de, es, et, eu, fi, fr, ga, gl, hr, hu, id, is, it, ku, la, lb, lt, lv, mi, ms, mt, nl, no, oc, pl, pt, qu, rm, ro, rs_latin, sk, sl, sq, sv, sw, tl, tr, uz, vi, french, german`.
- `tiny` supports all of the above languages except `japan`.
- Compatible aliases: `zh`, `zh_cn`, `zh-cn` → `ch`; `zh_tw`, `zh-tw` → `chinese_cht`; `ja`, `jp` → `japan`.

### Model Route Details

The `model_key` in the table below is the actual key in `default_models.yaml`. `lang_type` is the route entry; the `multi` entry of PP-OCRv6 actually accepts the languages listed above, while the `multi` entry of PP-OCRv5 detection and classification accepts `ch`, `multi`.

| Module | ocr_version | lang_type | model_type | model_key | engine_type |
| --- | --- | --- | --- | --- | --- |
| det | `PP-OCRv6` | `multi` | `tiny` | `multi_PP-OCRv6_det_tiny` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv6` | `multi` | `small` | `multi_PP-OCRv6_det_small` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv6` | `multi` | `medium` | `multi_PP-OCRv6_det_medium` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv6` | `multi` | `tiny` | `multi_PP-OCRv6_rec_tiny` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv6` | `multi` | `small` | `multi_PP-OCRv6_rec_small` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv6` | `multi` | `medium` | `multi_PP-OCRv6_rec_medium` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv5` | `multi` | `mobile` | `ch_PP-OCRv5_det_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv5` | `multi` | `server` | `ch_PP-OCRv5_det_server` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| cls | `PP-OCRv5` | `multi` | `mobile` | `ch_PP-LCNet_x0_25_textline_ori_cls_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| cls | `PP-OCRv5` | `multi` | `server` | `ch_PP-LCNet_x1_0_textline_ori_cls_server` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `ch` | `mobile` | `ch_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv5` | `korean` | `mobile` | `korean_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `latin` | `mobile` | `latin_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `eslav` | `mobile` | `eslav_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `en` | `mobile` | `en_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `th` | `mobile` | `th_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `el` | `mobile` | `el_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `arabic` | `mobile` | `arabic_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `cyrillic` | `mobile` | `cyrillic_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `devanagari` | `mobile` | `devanagari_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `ta` | `mobile` | `ta_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `te` | `mobile` | `te_PP-OCRv5_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle` |
| rec | `PP-OCRv5` | `ch` | `server` | `ch_PP-OCRv5_rec_server` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv4` | `ch` | `mobile` | `ch_PP-OCRv4_det_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv4` | `en` | `mobile` | `en_PP-OCRv3_det_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv4` | `multi` | `mobile` | `multi_PP-OCRv3_det_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| det | `PP-OCRv4` | `ch` | `server` | `ch_PP-OCRv4_det_server` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| cls | `PP-OCRv4` | `multi` | `mobile` | `ch_ppocr_mobile_v2.0_cls_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `arabic` | `mobile` | `arabic_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `ch` | `mobile` | `ch_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `chinese_cht` | `mobile` | `chinese_cht_PP-OCRv3_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `cyrillic` | `mobile` | `cyrillic_PP-OCRv3_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `devanagari` | `mobile` | `devanagari_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `en` | `mobile` | `en_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `japan` | `mobile` | `japan_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `ka` | `mobile` | `ka_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `korean` | `mobile` | `korean_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `latin` | `mobile` | `latin_PP-OCRv3_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `ta` | `mobile` | `ta_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `te` | `mobile` | `te_PP-OCRv4_rec_mobile` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `ch` | `server` | `ch_PP-OCRv4_rec_server` | `onnxruntime`, `openvino`, `mnn`, `paddle`, `torch` |
| rec | `PP-OCRv4` | `ch_doc` | `server` | `ch_doc_PP-OCRv4_rec_server` | `onnxruntime`, `openvino`, `mnn`, `paddle` |

### Text Detection Models

| ocr_version | Language type | lang_type | model_type | engine_type |
| --- | --- | --- | --- | --- |
| `PP-OCRv6` | Multilingual | the PP-OCRv6 supported languages listed above | `tiny`<br>`small`<br>`medium` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | Multilingual | `ch`<br>`multi` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | Chinese and English | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | English, Latin | `en` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | Multilingual | `multi` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |

Corresponding usage:

!!! note

    The `lang_type` field corresponds to `LangDet` under the Det module.

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

### Text Line Orientation Classification Models

!!! note

    PP-OCRv5 orientation classification models are supported starting from `rapidocr>=3.8.0`. PP-OCRv4 orientation classification models are still retained in the current configuration.

| ocr_version | lang_type | model_type | engine_type |
| --- | --- | --- | --- |
| `PP-OCRv5` | `ch`<br>`multi` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |
| `PP-OCRv4` | `ch`<br>`multi` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |

### Text Recognition Models

!!! note

    The `lang_type` field corresponds to `LangRec` under the Rec module.

| ocr_version | Language type | lang_type | model_type | engine_type |
| --- | --- | --- | --- | --- |
| `PP-OCRv6` | Multilingual | the PP-OCRv6 supported languages listed above | `tiny`<br>`small`<br>`medium` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | Mixed Chinese, English and Japanese[^2] | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | Korean, mixed Latin languages, Slavic, English, Thai, Greek, Arabic, Cyrillic, Devanagari, Tamil, Telugu | `korean`<br>`latin`<br>`eslav`<br>`en`<br>`th`<br>`el`<br>`arabic`<br>`cyrillic`<br>`devanagari`<br>`ta`<br>`te` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |
| `PP-OCRv4` | Chinese | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | Arabic, Traditional Chinese, Cyrillic, Devanagari, English, Japanese, Georgian, Korean, Latin, Tamil, Telugu | `arabic`<br>`chinese_cht`<br>`cyrillic`<br>`devanagari`<br>`en`<br>`japan`<br>`ka`<br>`korean`<br>`latin`<br>`ta`<br>`te` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | Chinese document | `ch_doc` | `server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |

PP-OCRv5 recognition models are compatible with `ko` → `korean`, `ar` → `arabic`; PP-OCRv4 recognition models are additionally compatible with `zh_tw`, `zh-tw` → `chinese_cht` and `ja`, `jp` → `japan`. All versions are compatible with `zh`, `zh_cn`, `zh-cn` → `ch`.

### Usage

The above models can be specified directly through the fields, and the program will download and use them automatically.

```python linenums="1" hl_lines="5-7"
from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Rec.ocr_version": OCRVersion.PPOCRV5,
        "Rec.engine_type": EngineType.PADDLE,
        "Rec.model_type": ModelType.MOBILE,
    }
)

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

## Language Reference Table

| `lang` | Language name | Alias |
| --- | --- | --- |
| `latin` | Latin | - |
| `eslav` | Slavic | - |
| `devanagari` | Devanagari | - |
| `cyrillic` | Cyrillic | - |
| `ch_doc` | Chinese document | - |
| `gl` | Galician | - |
| `lb` | Luxembourgish | - |
| `abq` | Abkhaz | - |
| `af` | Afrikaans | - |
| `ang` | Old English | - |
| `ar` | Arabic | `arabic` |
| `ava` | Avar | - |
| `az` | Azerbaijani | - |
| `be` | Belarusian | - |
| `bg` | Bulgarian | - |
| `bgc` | Haryanvi | - |
| `bh` | Bihari | - |
| `bho` | Bhojpuri | - |
| `bs` | Bosnian | - |
| `ca` | Catalan | - |
| `ch` | Simplified Chinese | - |
| `che` | Chechen | - |
| `chinese_cht` | Traditional Chinese | - |
| `cs` | Czech | - |
| `cy` | Welsh | - |
| `da` | Danish | - |
| `dar` | Dargwa | - |
| `de` | German | `german` |
| `el` | Greek | - |
| `en` | English | - |
| `es` | Spanish | - |
| `et` | Estonian | - |
| `fa` | Persian | - |
| `fr` | French | `french` |
| `ga` | Irish | - |
| `gom` | Konkani | - |
| `hi` | Hindi | - |
| `hr` | Croatian | - |
| `hu` | Hungarian | - |
| `id` | Indonesian | - |
| `inh` | Ingush | - |
| `is` | Icelandic | - |
| `it` | Italian | - |
| `japan` | Japanese | - |
| `ka` | Georgian | - |
| `kbd` | Kabardian | - |
| `korean` | Korean | - |
| `ku` | Kurdish | - |
| `la` | Latin | - |
| `lbe` | Lak | - |
| `lez` | Lezgi | - |
| `lt` | Lithuanian | - |
| `lv` | Latvian | - |
| `mah` | Magahi | - |
| `mai` | Maithili | - |
| `mi` | Maori | - |
| `mn` | Mongolian | - |
| `mr` | Marathi | - |
| `ms` | Malay | - |
| `mt` | Maltese | - |
| `ne` | Nepali | - |
| `new` | Newari | - |
| `nl` | Dutch | - |
| `no` | Norwegian | - |
| `oc` | Occitan | - |
| `pi` | Pali | - |
| `pl` | Polish | - |
| `pt` | Portuguese | - |
| `ro` | Romanian | - |
| `rs_cyrillic` | Serbian (Cyrillic alphabet) | - |
| `rs_latin` | Serbian (Latin alphabet) | - |
| `ru` | Russian | - |
| `sa` | Sanskrit | - |
| `sck` | Sadri | - |
| `sk` | Slovak | - |
| `sl` | Slovenian | - |
| `sq` | Albanian | - |
| `sv` | Swedish | - |
| `sw` | Swahili | - |
| `tab` | Tabassaran | - |
| `ta` | Tamil | - |
| `te` | Telugu | - |
| `th` | Thai | - |
| `tl` | Tagalog | - |
| `tr` | Turkish | - |
| `ug` | Uyghur | - |
| `uk` | Ukrainian | - |
| `ur` | Urdu | - |
| `uz` | Uzbek | - |
| `vi` | Vietnamese | - |
| `qu` | Quechua | - |
| `rm` | Romansh | - |
| `eu` | Basque | - |
| `fi` | Finnish | - |

[^2]: Simplified Chinese, Chinese Pinyin, Traditional Chinese, English, Japanese
