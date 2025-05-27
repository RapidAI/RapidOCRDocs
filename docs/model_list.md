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

[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/a9bb7c1f44b6e00556ada90ac588f020d7637c4b/python/rapidocr/default_models.yaml)

### 使用默认mobile或server模型

`rapidocr`库基本集成了PaddleOCR发布的所有模型，其中中英文检测识别模型仅集成最新的版本。同时只有中英文检测识别模型分为 **mobile** 和 **server** 两个版本，分别侧重速度和精度。

默认使用的是 **mobile** 的中英文检测识别模型，通过`lang_det`和`lang_rec`来指定。

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

engine = RapidOCR(
    params={"Global.lang_det": "ch_mobile", "Global.lang_rec": "ch_mobile"}
)
```

如果想要使用**server**版默认模型，则直接更改参数为`ch_server`即可。

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

engine = RapidOCR(
    params={"Global.lang_det": "ch_server", "Global.lang_rec": "ch_server"}
)
```

!!! note

    并不是所有的模型都有 **server** 版本，具体哪个有，可以参见：[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/a9bb7c1f44b6e00556ada90ac588f020d7637c4b/python/rapidocr/default_models.yaml)。配置文件中带有server字样的即是有server版本。

### 具体字段对应

文本检测模型：

|语种类型名称|程序使用字段|支持模型类型(`lang_det`)|ONNXRuntime| OpenVINO| PaddlePaddle | PyTorch|
|---:|:---|:---|:---:|:---:|:---:|:---:|
|中英|`ch`|`ch_mobile` `ch_server`|✅|`ch_mobile`✅ `ch_server` ❌([link](https://github.com/RapidAI/RapidOCR/issues/395))|✅|✅|
|英语和拉丁语|`en`|`en_mobile` `en_server`|✅|✅|✅|✅|
|多语种|`multi`|`multi_mobile`|✅|✅|✅|✅|

文本识别模型：

|语种|描述|程序使用字段|支持模型类型(`lang_rec`)|ONNXRuntime| OpenVINO| PaddlePaddle | PyTorch|
|---:|:---|:---|:---|:---:|:---:|:---:|:---:|
|中文文档、部分繁体、日文|-|`ch`|`ch_doc_server`|✅|✅|✅|🚧|
|中文|Chinese & English|`ch`|`ch_mobile` `ch_server`|✅|✅|✅|✅|
|中文繁体|Chinese (Traditional)|`chinese_cht`|`chinese_cht`|✅|✅|✅|✅|
|英文|English|`en`|`en_mobile`|✅|✅|✅|✅|
|阿拉伯文|Arabic|`ar`|`ar_mobile`|✅|✅|✅|✅|
|塞尔维亚文（cyrillic)|Serbian(cyrillic)|`cyrillic`|`cyrillic_mobile`|✅|✅|✅|✅|
|梵文|Devanagari|`devanagari`|`devanagari_mobile`|✅|✅|✅|✅|
|日文|Japan|`japan`|`japan_mobile`|✅|✅|✅|✅|
|卡纳达语|kannaḍa|`ka`|`ka_mobile`|✅|✅|✅|✅|
|韩文|Koran|`korean`|`korean_mobile`|✅|✅|✅|✅|
|拉丁文|Latin|`latin`|`latin_mobile`|✅|✅|✅|✅|
|泰米尔文|Tamil |`ta`|`ta_mobile`|✅|✅|✅|✅|
|泰卢固文|Telugu |`te`|`te_mobile`|✅|✅|✅|✅|

### 使用方式

以上模型可直接通过字段指定，程序会自动下载使用。

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR, VisRes

engine = RapidOCR(
    params={"Global.lang_det": "ch_mobile", "Global.lang_rec": "ch_mobile"}
)
img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```
