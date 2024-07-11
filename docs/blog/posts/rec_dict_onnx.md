---
title: 关于识别模型中字典的读写
date: 2023-10-08
authors: [SWHL]
slug: read-dict-onnx
categories:
  - General
comments: true
---


<!-- more -->

### 引言

在文本识别时，识别的每一种语言，都有一个对应的字典，用来还原识别的文本内容。例如英文识别模型的字典就是26个英文字母的大小写以及常用符号，中文识别模型的字典一般包括常用汉字、字母和符号等。

受启发于[issue #42](https://github.com/RapidAI/RapidOCR/issues/42)，目前基于ONNXRuntime的推理引擎`rapidocr_onnxruntime`库已经将字典写入到onnx模型中，无需额外指定字典TXT文件。

以下将对这一部分做详细讲解，感兴趣小伙伴，可自行取用。

### 将字典内容写入到ONNX中

!!! note

    在PaddleOCRModelConvert工具中已经将上述操作写到了包中，使用该工具可自动将字典写入到ONNX中。源码位于：[link](https://github.com/RapidAI/PaddleOCRModelConvert/blob/64a66ebe8c6147f0bacc5e0dd22a0809cad332e6/paddleocr_convert/main.py#L51)

```python linenums="1"
import onnx

model = onnx.load_model('/path/to/model.onnx')

# 添加dictionary对应的值
meta = model.metadata_props.add()
meta.key = 'dictionary'
meta.value = open('/path/to/ppocr_keys_v1.txt', 'r', -1, 'u8').read()

# 添加shape对应的值
meta = model.metadata_props.add()
meta.key = 'shape'
meta.value = '[3,48,320]'

onnx.save_model(model, '/path/to/model.onnx')
```

### 获取字典内容

!!! note

    该部分已经在rapidocr_onnxruntime上实现，详情参见：[link](https://github.com/RapidAI/RapidOCR/blob/37e49c6ae25135a339b208f9ac64382ee7d4d688/python/rapidocr_onnxruntime/ch_ppocr_v3_rec/text_recognize.py#L31-L32)

```python linenums="1"
import json
import onnxruntime as ort

sess = ort.InferenceSession('/path/to/model.onnx')
metamap = sess.get_modelmeta().custom_metadata_map

# 读取dictionary键对应的值
chars = metamap['dictionary'].splitlines()

# 读取shape键对应的值
input_shape = json.loads(metamap['shape'])
```
