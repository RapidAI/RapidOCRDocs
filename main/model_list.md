## 引言

针对 PaddleOCR 已经发布的常用模型，我们这里已经做了统一转换和汇总，包括 PP-OCRv4, PP-OCRv5 和 PP-OCRv6 系列的 PaddlePaddle, ONNX, MNN 和 PyTorch 格式。TensorRT 会在首次运行时基于 ONNX 模型动态构建与当前硬件匹配的 Engine 文件。

所有模型目前托管在 [魔搭社区](https://www.modelscope.cn/models/RapidAI/RapidOCR/files) 上。

`rapidocr` v3 版本已经集成了托管的所有模型，通过下面参数指定可以自动下载。对应的配置文件：[default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml)。当然，小伙伴们也可以自己去上述链接下载。

`rapidocr>=3.10.0` 起，模型选择由 [default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml) 中的模型路由统一管理。用户传入语言、模型类型和 OCR 版本后，RapidOCR 会自动解析实际模型文件。

从 `rapidocr>=3.10.0` 起，`lang_type` 不再只能传 `LangDet`、`LangCls` 或 `LangRec` 枚举，也可以直接传语言编码字符串，例如 `"japan"`、`"korean"`、`"arabic"`。字符串编码必须能在当前任务、OCR 版本和模型类型的路由中匹配；支持的编码和别名以本文的模型路由明细及 `default_models.yaml` 为准。原有枚举写法仍然兼容。

例如，下面的识别配置直接使用语言编码字符串，不需要先转换为 `LangRec` 枚举：

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

使用阿拉伯语等 RTL 语言时，请先安装 [RTL 额外依赖](install_usage/rapidocr/install.md)。

## 默认配置

通过 pip 安装 `rapidocr` 之后，可以直接使用，不用指定任何参数。因为 whl 包中预先打包了默认模型，同时给出了默认配置。

不同版本的 `rapidocr`，默认配置有所不同。下面详细给出不同版本对应的默认配置。

=== "`rapidocr>=3.9.0` 默认配置"

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

    对应的配置文件：[config.yaml](https://github.com/RapidAI/RapidOCR/blob/v3.9.0/python/rapidocr/config.yaml)

=== "`rapidocr<3.9.0` 默认配置"

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

    对应的配置文件：[config.yaml](https://github.com/RapidAI/RapidOCR/blob/v3.8.4/python/rapidocr/config.yaml)

## 配置文件字段对应

以下表格以 `rapidocr>=3.10.0` 的 `default_models.yaml` 为准。`engine_type` 仅列出配置文件中直接登记模型文件的推理引擎；TensorRT 使用对应的 ONNX 模型动态构建 Engine，使用限制参见 [TensorRT 推理引擎说明](install_usage/rapidocr/how_to_use_infer_engine.md)。

PP-OCRv6 的 `tiny`、`small` 和 `medium` 模型均为多语种模型。同一规格下，不同 `lang_type` 会路由到同一个模型文件：

- `small` 和 `medium` 支持：`ch, chinese_cht, en, japan, af, az, bs, ca, cs, cy, da, de, es, et, eu, fi, fr, ga, gl, hr, hu, id, is, it, ku, la, lb, lt, lv, mi, ms, mt, nl, no, oc, pl, pt, qu, rm, ro, rs_latin, sk, sl, sq, sv, sw, tl, tr, uz, vi, french, german`。
- `tiny` 支持上述语种中的除 `japan` 之外的所有语种。
- 兼容别名：`zh`、`zh_cn`、`zh-cn` → `ch`；`zh_tw`、`zh-tw` → `chinese_cht`；`ja`、`jp` → `japan`。

### 模型路由明细

下表中的 `model_key` 是 `default_models.yaml` 中的实际键。`lang_type` 是路由入口；PP-OCRv6 的 `multi` 入口实际接受上面列出的语言，PP-OCRv5 检测和分类的 `multi` 入口接受 `ch`、`multi`。

| 模块 | ocr_version | lang_type | model_type | model_key | engine_type |
| --- | --- | --- | --- | --- | --- |
| det | `PP-OCRv6` | `multi` | `tiny` | `multi_PP-OCRv6_det_tiny` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv6` | `multi` | `small` | `multi_PP-OCRv6_det_small` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv6` | `multi` | `medium` | `multi_PP-OCRv6_det_medium` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv6` | `multi` | `tiny` | `multi_PP-OCRv6_rec_tiny` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv6` | `multi` | `small` | `multi_PP-OCRv6_rec_small` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv6` | `multi` | `medium` | `multi_PP-OCRv6_rec_medium` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv5` | `multi` | `mobile` | `ch_PP-OCRv5_det_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv5` | `multi` | `server` | `ch_PP-OCRv5_det_server` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| cls | `PP-OCRv5` | `multi` | `mobile` | `ch_PP-LCNet_x0_25_textline_ori_cls_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| cls | `PP-OCRv5` | `multi` | `server` | `ch_PP-LCNet_x1_0_textline_ori_cls_server` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `ch` | `mobile` | `ch_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv5` | `korean` | `mobile` | `korean_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `latin` | `mobile` | `latin_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `eslav` | `mobile` | `eslav_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `en` | `mobile` | `en_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `th` | `mobile` | `th_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `el` | `mobile` | `el_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `arabic` | `mobile` | `arabic_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `cyrillic` | `mobile` | `cyrillic_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `devanagari` | `mobile` | `devanagari_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `ta` | `mobile` | `ta_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `te` | `mobile` | `te_PP-OCRv5_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle` |
| rec | `PP-OCRv5` | `ch` | `server` | `ch_PP-OCRv5_rec_server` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv4` | `ch` | `mobile` | `ch_PP-OCRv4_det_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv4` | `en` | `mobile` | `en_PP-OCRv3_det_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv4` | `multi` | `mobile` | `multi_PP-OCRv3_det_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| det | `PP-OCRv4` | `ch` | `server` | `ch_PP-OCRv4_det_server` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| cls | `PP-OCRv4` | `multi` | `mobile` | `ch_ppocr_mobile_v2.0_cls_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `arabic` | `mobile` | `arabic_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `ch` | `mobile` | `ch_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `chinese_cht` | `mobile` | `chinese_cht_PP-OCRv3_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `cyrillic` | `mobile` | `cyrillic_PP-OCRv3_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `devanagari` | `mobile` | `devanagari_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `en` | `mobile` | `en_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `japan` | `mobile` | `japan_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `ka` | `mobile` | `ka_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `korean` | `mobile` | `korean_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `latin` | `mobile` | `latin_PP-OCRv3_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `ta` | `mobile` | `ta_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `te` | `mobile` | `te_PP-OCRv4_rec_mobile` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `ch` | `server` | `ch_PP-OCRv4_rec_server` | `onnxruntime`、`openvino`、`mnn`、`paddle`、`torch` |
| rec | `PP-OCRv4` | `ch_doc` | `server` | `ch_doc_PP-OCRv4_rec_server` | `onnxruntime`、`openvino`、`mnn`、`paddle` |

### 文本检测模型

| ocr_version | 语种类型 | lang_type | model_type | engine_type |
| --- | --- | --- | --- | --- |
| `PP-OCRv6` | 多语种 | 上述 PP-OCRv6 支持语种 | `tiny`<br>`small`<br>`medium` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | 多语种 | `ch`<br>`multi` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | 中英 | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | 英语、拉丁语 | `en` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | 多语种 | `multi` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |

对应使用方法：

!!! note

    `lang_type` 字段对应 Det 模块下的 `LangDet`

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

### 文本行方向分类模型

!!! note

    PP-OCRv5 方向分类模型自 `rapidocr>=3.8.0` 起支持。PP-OCRv4 方向分类模型仍保留在当前配置中。

| ocr_version | lang_type | model_type | engine_type |
| --- | --- | --- | --- |
| `PP-OCRv5` | `ch`<br>`multi` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |
| `PP-OCRv4` | `ch`<br>`multi` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |

### 文本识别模型

!!! note

    `lang_type` 字段对应 Rec 模块下的 `LangRec`。

| ocr_version | 语种类型 | lang_type | model_type | engine_type |
| --- | --- | --- | --- | --- |
| `PP-OCRv6` | 多语种 | 上述 PP-OCRv6 支持语种 | `tiny`<br>`small`<br>`medium` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | 中英日混合[^2] | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv5` | 韩语、拉丁语种混合、斯拉夫语、英语、泰语、希腊语、阿拉伯语、西里尔语、天城文、泰米尔语、泰卢固语 | `korean`<br>`latin`<br>`eslav`<br>`en`<br>`th`<br>`el`<br>`arabic`<br>`cyrillic`<br>`devanagari`<br>`ta`<br>`te` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |
| `PP-OCRv4` | 中文 | `ch` | `mobile`<br>`server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | 阿拉伯语、繁体中文、西里尔语、天城文、英语、日语、格鲁吉亚语、韩语、拉丁语、泰米尔语、泰卢固语 | `arabic`<br>`chinese_cht`<br>`cyrillic`<br>`devanagari`<br>`en`<br>`japan`<br>`ka`<br>`korean`<br>`latin`<br>`ta`<br>`te` | `mobile` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle`<br>`torch` |
| `PP-OCRv4` | 中文文档 | `ch_doc` | `server` | `onnxruntime`<br>`openvino`<br>`mnn`<br>`paddle` |

PP-OCRv5 识别模型兼容 `ko` → `korean`、`ar` → `arabic`；PP-OCRv4 识别模型还兼容 `zh_tw`、`zh-tw` → `chinese_cht` 和 `ja`、`jp` → `japan`。各版本均兼容 `zh`、`zh_cn`、`zh-cn` → `ch`。

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

## 语种对照表

| `lang` | 语言名称 | 别名 |
| --- | --- | --- |
| `latin` | 拉丁语 | - |
| `eslav` | 斯拉夫语 | - |
| `devanagari` | 天城文 | - |
| `cyrillic` | 西里尔语 | - |
| `ch_doc` | 中文文档 | - |
| `gl` | 加利西亚语 | - |
| `lb` | 卢森堡语 | - |
| `abq` | 阿布哈兹语 | - |
| `af` | 南非荷兰语 | - |
| `ang` | 古英语 | - |
| `ar` | 阿拉伯语 | `arabic` |
| `ava` | 阿瓦尔语 | - |
| `az` | 阿塞拜疆语 | - |
| `be` | 白俄罗斯语 | - |
| `bg` | 保加利亚语 | - |
| `bgc` | 哈里亚纳语 | - |
| `bh` | 比哈尔语 | - |
| `bho` | 博杰普尔语 | - |
| `bs` | 波斯尼亚语 | - |
| `ca` | 加泰罗尼亚语 | - |
| `ch` | 简体中文 | - |
| `che` | 车臣语 | - |
| `chinese_cht` | 繁体中文 | - |
| `cs` | 捷克语 | - |
| `cy` | 威尔士语 | - |
| `da` | 丹麦语 | - |
| `dar` | 达尔格瓦语 | - |
| `de` | 德语 | `german` |
| `el` | 希腊语 | - |
| `en` | 英语 | - |
| `es` | 西班牙语 | - |
| `et` | 爱沙尼亚语 | - |
| `fa` | 波斯语 | - |
| `fr` | 法语 | `french` |
| `ga` | 爱尔兰语 | - |
| `gom` | 孔卡尼语 | - |
| `hi` | 印地语 | - |
| `hr` | 克罗地亚语 | - |
| `hu` | 匈牙利语 | - |
| `id` | 印尼语 | - |
| `inh` | 印古什语 | - |
| `is` | 冰岛语 | - |
| `it` | 意大利语 | - |
| `japan` | 日语 | - |
| `ka` | 格鲁吉亚语 | - |
| `kbd` | 卡巴尔达语 | - |
| `korean` | 韩语 | - |
| `ku` | 库尔德语 | - |
| `la` | 拉丁语 | - |
| `lbe` | 拉克语 | - |
| `lez` | 列兹金语 | - |
| `lt` | 立陶宛语 | - |
| `lv` | 拉脱维亚语 | - |
| `mah` | 马加希语 | - |
| `mai` | 迈蒂利语 | - |
| `mi` | 毛利语 | - |
| `mn` | 蒙古语 | - |
| `mr` | 马拉地语 | - |
| `ms` | 马来语 | - |
| `mt` | 马耳他语 | - |
| `ne` | 尼泊尔语 | - |
| `new` | 尼瓦尔语 | - |
| `nl` | 荷兰语 | - |
| `no` | 挪威语 | - |
| `oc` | 奥克语 | - |
| `pi` | 巴利语 | - |
| `pl` | 波兰语 | - |
| `pt` | 葡萄牙语 | - |
| `ro` | 罗马尼亚语 | - |
| `rs_cyrillic` | 塞尔维亚语（西里尔字母） | - |
| `rs_latin` | 塞尔维亚语（拉丁字母） | - |
| `ru` | 俄语 | - |
| `sa` | 梵语 | - |
| `sck` | 萨达里语 | - |
| `sk` | 斯洛伐克语 | - |
| `sl` | 斯洛文尼亚语 | - |
| `sq` | 阿尔巴尼亚语 | - |
| `sv` | 瑞典语 | - |
| `sw` | 斯瓦希里语 | - |
| `tab` | 塔巴萨兰语 | - |
| `ta` | 泰米尔语 | - |
| `te` | 泰卢固语 | - |
| `th` | 泰语 | - |
| `tl` | 他加禄语 | - |
| `tr` | 土耳其语 | - |
| `ug` | 维吾尔语 | - |
| `uk` | 乌克兰语 | - |
| `ur` | 乌尔都语 | - |
| `uz` | 乌兹别克语 | - |
| `vi` | 越南语 | - |
| `qu` | 克丘亚语 | - |
| `rm` | 罗曼什语 | - |
| `eu` | 巴斯克语 | - |
| `fi` | 芬兰语 | - |

[^2]: 简体中文、中文拼音、繁体中文、英文、日文
