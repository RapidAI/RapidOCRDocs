---
title: 调优尝试教程
date: 2022-10-03
authors: [SWHL]
slug: optim-tutorial
categories:
  - General
comments: true
---


<!-- more -->

!!! note

    以下尝试情况，均已经在[在线demo](https://www.modelscope.cn/studios/RapidAI/RapidOCRv3.0.0)中实现，看完之后，可移步那里去尝试。

### 引言

- 由于小伙伴们使用OCR的场景多种多样，单一的参数配置往往不能满足要求，这就涉及到基于现有模型，通过调节参数来达到正确识别的目的。
- 基本的原则是尽量不去动模型内部，降低使用成本。
- 本篇文章就来说说在识别效果不好时，如何去调优。
- 因此博客为一家之言，难免会挂一漏万，希望小伙伴多多指出，共同维护这份教程。

### 常见错例种类

本地使用过程中，识别结果：

- 个别字丢失
- 个别字识别错误

### 个别字丢失调优篇

1. 查看图像是否`shape`太小，导致文本检测丢失。
    - 对于长度较长，高度较小的图像，可尝试对该图像高度做上下补充，来减小文字在原始图像中比例，利于文本检测。类似下图这种，左侧一条为原始图像，右侧为上下补边的图像。
    ![Snipaste_2023-04-09_14-01-45](https://user-images.githubusercontent.com/28639377/230757239-3aad8686-4fbd-4f1a-abff-f7e1cb90f3aa.png)
    - padding代码参考：

    ```python linenums="1"
    from typing import Tuple

    import cv2
    import numpy as np


    def padding_img(img: np.ndarray,
                    padding_value: Tuple[int, int, int, int],
                    padding_color: Tuple = (0, 0, 0)) -> np.ndarray:
        padded_img = cv2.copyMakeBorder(img,
                                        padding_value[0],
                                        padding_value[1],
                                        padding_value[2],
                                        padding_value[3],
                                        cv2.BORDER_CONSTANT,
                                        value=padding_color)
        return padded_img

    img = cv2.imread('xxx.jpg')

    # padding_value: (top, bottom, left, right)
    # 对该图像上下各补充10像素的白边
    padded_img = padding_img(img, (10, 10, 0, 0), (255, 255, 255))
    ```

   - 将padding之后的图像再次送入RapidOCR中尝试，查看是否仍然出现上述问题。

2. 将该图像上传到[在线demo](https://www.modelscope.cn/studios/RapidAI/RapidOCRv3.0.0)中，查看能否复现问题？
   - 如不能复现，着重比对环境是否与在线demo中相关包使用版本不一致情况？
   - 在线demo所用的各个包版本情况：

     ```text
     Python: 3.8
     onnxruntime: 1.14.1
     rapidocr_onnxruntime: 1.2.5
     ```

3. 如能复现，尝试调节在线demo中的三个参数，注意控制变量调节参数
   1. 首先调节`box_thresh`参数，该参数用来控制文本检测部分检测所得框是文本的概率。个别字丢失，一般是单独的字丢失，很大可能是文本检测模型没有检测到该独立的文字。尝试调低`box_thresh`值，查看是否可以检出丢失的文字。（没有找到合适的例子）
   2. 固定`box_thresh`，调节`text_score`参数。该参数是控制识别文本结果正确的概率。尝试调低`text_score`值，查看是否可以识别出丢失的文字。
   3. 固定`box_thresh`和`text_score`两个参数，调节`unclip_ratio`参数。该参数用来控制文本检测所得文本框的大小。尝试调大`unclip_ratio`值，查看是否可以识别出丢失的文字。
4. 如果调节三个参数也不能解决问题，只能尝试`server`版的文本检测和文本识别模型了。
   1. 首先更换`server`版的文本检测模型，查看是否解决问题
   2. 在第1步基础上，更换`server`版的文本识别模型，查看是否解决问题
5. 尝试更换不同版本模型，来查看效果。具体可在[在线demo](https://www.modelscope.cn/studios/RapidAI/RapidOCRv3.0.0)中尝试

### 个别字识别错误调优篇

个别字错误的情况，例如：**成**识别为**戍**，这种一般是文本识别模型的问题。

#### 情况一：轻量中英文模型识别对个别汉字识别错误

1. 尝试padding图像，再重新识别
2. 更换不同版本的识别模型，包括`v2`、`v3`和`server`版尝试

#### 情况二：轻量中英文模型对个别英文或数字识别错误

1. 更换不同版本的识别模型，包括`v2`、`v3`和`server`版尝试
2. 如果是只识别英文单词和数字，可以更换英文和数字专有模型（`en_PP-OCRv3_rec_infer.onnx`和`en_number_mobile_v2.0_rec_infer.onnx`）
