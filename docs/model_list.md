---
comments: true
hide:
  - navigation
#   - toc
---


## 引言

针对 PaddleOCR 已经发布的常用模型，我们这里已经做了统一转换和汇总，包括 PP-OCRv4 和 PP-OCRv5 系列的 PaddlePaddle 格式、ONNX 格式、MNN 格式和 PyTorch 格式。

所有模型目前托管在[魔搭社区](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)上。

`rapidocr` v3 版本已经集成了托管的所有模型，通过下面参数指定可以自动下载。对应的配置文件：[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml)。当然，小伙伴们也可以自己去上述链接下载。

## 默认配置

直接通过 pip 安装 `rapidocr` 使用时，可以直接使用，不用指定任何参数。下面写法：

```python linenums="1"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

等价于下面：

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
        "Rec.ocr_version": OCRVersion.PPOCRV5,
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

## 配置文件字段对应

### 文本检测模型

#### PP-OCRv5

|语种类型|engine_type| lang_type|model_type|ocr_version|
|:---|:---|:---|:---|:---|
|多语种[^7]|`onnxruntime` <br/> `openvino` <br/> `paddle`<br>`torch`(`rapidocr>=3.3.0`)<br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)|`ch`|`mobile`<br/> `server (tensorrt可能转换不过)`|`PP-OCRv5`|

#### PP-OCRv4

|语种类型|engine_type| lang_type|model_type|ocr_version|
|:---|:---|:---|:---|:---|
|中英|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`<br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)|`ch`|`mobile`<br/> `server`|`PP-OCRv4`|
|英语、拉丁语|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`<br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)|`en`|`mobile`<br/> `server`|`PP-OCRv4`<br/>|
|多语种|`onnxruntime` <br/> `openvino` <br/> `paddle` <br/> `torch`<br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)|`multi`|`mobile`<br>❎`server` |`PP-OCRv4`<br/>|

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

### 文本识别模型

!!! note

    `lang_type`字段对应Det模块下的`LangRec`

#### PP-OCRv5

| 语种类型       | engine_type               | lang_type         | model_type      | ocr_version       |
|----------------|---------------------------|-------------------|-----------------|-------------------|
| 俄罗斯文[^3] | `rapidocr>=3.5.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch` <br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)| `cyrillic`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 阿拉伯文[^4] | `rapidocr>=3.5.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `arabic`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 梵文等[^5] | `rapidocr>=3.5.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `devanagari`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 泰米尔文、英文 | `rapidocr>=3.5.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch` <br>`mnn`(`rapidocr>=3.6.0`)<br>`tensorrt`(`rapidocr>=3.7.0`)| `ta`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 泰卢固文、英文 | `rapidocr>=3.5.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `te`            | `mobile`<br>❎`server` | `PP-OCRv5` |
||||||
| 英文 | `rapidocr>=3.4.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `en`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 泰文、英文 | `rapidocr>=3.4.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `th`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 希腊文、英文 | `rapidocr>=3.4.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `el`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 拉丁语种混合[^1] | `rapidocr>=3.3.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `latin`            | `mobile`<br>❎`server` | `PP-OCRv5` |
| 俄罗斯文[^6] | `rapidocr>=3.3.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`)| `eslav`            | `mobile`<br>`server` | `PP-OCRv5` |
| 中英日混合[^2] | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`(`rapidocr>=3.3.0`)<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `ch`            | `mobile`<br>`server` | `PP-OCRv5` |
| 韩文   | `rapidocr>=3.3.0支持`<br/><br/>`onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `korean`        | `mobile`<br>❎`server`     | `PP-OCRv5` |

#### PP-OCRv4

| 语种类型       | engine_type               | lang_type         | model_type      | ocr_version       |
|----------------|---------------------------|-------------------|-----------------|-------------------|
| 韩文      | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `korean`        | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 中文文档    | `onnxruntime`<br>`openvino`<br>`paddle`<br>❎`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `ch_doc`            | ❎`mobile`<br>`server` | `PP-OCRv4` |
| 中文        | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `ch`            | `mobile`<br>`server` | `PP-OCRv4` |
| 中文繁体    | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `chinese_cht`   | `mobile`<br>`server`   | `PP-OCRv4` |
| 英文        | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `en`            | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 阿拉伯文    | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch` <br>`mnn`(`rapidocr>=3.6.0`)| `ar`            | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 塞尔维亚文  | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `cyrillic`      | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 梵文        | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `devanagari`    | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 日文        | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `japan`         | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 卡纳达语    | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `ka`            | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 拉丁文      | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `latin`         | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 泰米尔文    | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `ta`            | `mobile`<br>❎`server`     | `PP-OCRv4` |
| 泰卢固文    | `onnxruntime`<br>`openvino`<br>`paddle`<br>`torch`<br>`mnn`(`rapidocr>=3.6.0`) <br>`tensorrt`(`rapidocr>=3.7.0`)| `te`            | `mobile`<br>❎`server`     | `PP-OCRv4` |

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

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

[^1]: 英文、法文、德文、南非荷兰文、意大利文、西班牙文、波斯尼亚文、葡萄牙文、捷克文、威尔士文、丹麦文、爱沙尼亚文、爱尔兰文、克罗地亚文、乌兹别克文、匈牙利文、塞尔维亚文（latin）、印度尼西亚文、欧西坦文、冰岛文、立陶宛文、毛利文、马来文、荷兰文、挪威文、波兰文、斯洛伐克文、斯洛文尼亚文、阿尔巴尼亚文、瑞典文、西瓦希里文、塔加洛文、土耳其文、拉丁文
[^2]: 简体中文、中文拼音、繁体中文、英文、日文
[^3]: 俄罗斯文、白俄罗斯文、乌克兰文、塞尔维亚文（cyrillic）、保加利亚文、蒙古文、阿布哈兹文、阿迪赫文、卡巴尔达文、阿瓦尔文、达尔格瓦文、印古什文、车臣文、拉克文、列兹金文、塔巴萨兰文、哈萨克文、吉尔吉斯文、塔吉克文、马其顿文、鞑靼文、楚瓦什文、巴什基尔文、马里文、莫尔多瓦文、乌德穆尔特文、科米文、奥塞梯文、布里亚特文、卡尔梅克文、图瓦文、萨哈文、卡拉卡尔帕克文、英文
[^4]: 阿拉伯文、波斯文、维吾尔文、乌尔都文、普什图文、库尔德文、信德文、俾路支文、英文
[^5]: 印地文，马拉地文，尼泊尔文，比哈尔文，迈蒂利文，古英文，博杰普尔文，马加希文，萨达里文，尼瓦尔文，孔卡尼文，梵文，哈里亚纳文、英文
[^6]: 俄罗斯文、白俄罗斯文、乌克兰文
[^7]: 简体中文、中文拼音、繁体中文、英文、日文
