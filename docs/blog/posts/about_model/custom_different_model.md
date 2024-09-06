---
title: 如何更换其他检测和识别模型？
date:
  created: 2023-10-17
  updated: 2024-09-06
authors: [SWHL]
categories:
  - 模型相关
comments: true
---


> 本文详尽地给出了如何更换其他检测和识别模型的保姆级教程。

<!-- more -->

!!! note

    建议用`rapidocr_onnxruntime>=1.3.x`版本来加载PaddleOCR v3/v4版本训练所得模型。

### 引言

`rapidocr`系列库中默认打包了轻量版的中英文检测和识别模型，这种配置可以覆盖到大部分场景。但是也总会有一些其他场景，要用到其他检测和识别模型。

这一点在设计时已经做了考虑，留出了接口，这个博客就是以如何更换`rapidocr_onnxruntime`的识别模型为**英文和数字的识别模型**为例做讲解，其他模型同理。

**⚠️注意：使用其他模型的前提条件**：使用的模型必须是PaddleOCR中文本检测DBNet系列、文本识别CRNN系列模型，这样才能保证前后处理代码可以复用，其他模型不能直接替换模型路径使用。

以下以使用**英文和数字识别模型**为例讲解。

### 1. 安装`rapidocr_onnxruntime`

```bash linenums="1"
pip install rapidocr_onnxruntime
```

详细教程参考：[link](../../../install_usage/rapidocr/install.md)

### 2. 获得英文和数字的ONNX识别模型

!!! note

    如果想用RapidOCR仓库推理其他模型，必须要用PaddleOCRModelConvert工具转换模型 <br/>转换模型时，字典会自动写入到onnx模型里，`rapidocr_onnxruntime`推理时无须额外指定字典。

**模型地址：**
    ```text
    https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar
    ```

**字典地址:**
    ```text
    https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppocr/utils/en_dict.txt
    ```

**在线转换:** 基于[PaddleOCRModelConvert](https://huggingface.co/spaces/SWHL/PaddleOCRModelConverter)工具得到`en_PP-OCRv4_rec_infer.onnx`模型。

详细教程参见：[link](./convert_model.md)

### 3. 使用模型

!!! note

    检测模型，对应模型路径参数为`det_model_path`<br/>识别模型，对应模型路径参数为`rec_model_path` <br/> 详细说明参见：[link](../../../install_usage/api/RapidOCR.md)

如果得到的识别模型，没有将字典文件写入到ONNX模型中，可以通过初始化RapidOCR类时，通过`rec_keys_path`来指定对应的字典文件。

```python linenums="1"
from rapidocr_onnxruntime import RapidOCR

# det_model_path同理
model = RapidOCR(rec_model_path="en_PP-OCRv4_rec_infer.onnx")

img_path = "1.png"
result, elapse = model(img_path)
print(result)
print(elapse)
```
