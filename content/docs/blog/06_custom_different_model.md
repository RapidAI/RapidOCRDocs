---
weight: 3451
lastmod: "2023-10-17"
draft: false
author: "SWHL"
title: "如何更换其他检测和识别模型？"
icon: "code"
toc: true
description: ""
---

#### 引言
`rapidocr`系列库中默认打包了轻量版的中英文检测和识别模型，这种配置可以覆盖到大部分场景。但是也总会有一些其他场景，要用到其他检测和识别模型。

这一点，在设计接口时，已经做了考虑，留出了接口，只是没有专门博客来介绍这个事情。

这个博客就是以如何更换`rapidocr_onnxruntime`的识别模型为**英文和数字的识别模型**为例做讲解。其他模型同理。

#### 1. 安装`rapidocr_onnxruntime`
请先根据教程，装好`rapidocr_onnxruntime`库，具体可参考：[link](https://rapidai.github.io/RapidOCRDocs/docs/install_usage/rapidocr/install/)

#### 2. 获得英文和数字的ONNX识别模型
模型地址：https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar

字典地址；https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppocr/utils/en_dict.txt

基于[PaddleOCRModelConvert工具在线转换](https://www.modelscope.cn/studios/liekkas/PaddleOCRModelConverter/summary)，得到`en_PP-OCRv4_rec_infer.onnx`模型

#### 3. 使用该模型
```python {linenos=table}
from rapidocr_onnxruntime import RapidOCR

model = RapidOCR(rec_model_path="en_PP-OCRv4_rec_infer.onnx")

img_path = "1.png"
result, elapse = model(img_path)
print(result)
print(elapse)
```
