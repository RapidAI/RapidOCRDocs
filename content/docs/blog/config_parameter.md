---
weight: 300
date: "2022-10-05"
draft: false
author: "SWHL"
title: "config.yaml参数解释"
icon: "code"
toc: true
description: ""
---

#### [config.yaml源码](https://github.com/RapidAI/RapidOCR/blob/29d5f5fc01fbff7c49926a3c297fa8a3fb1624af/python/rapidocr_onnxruntime/config.yaml)


#### `Global`部分

|    参数名称      | 取值范围   | 默认值   |                       作用                       |
|:------------: | :----------: | :-----: | :----------------------------------------------|
| `text_score`  |    `[0, 1]`    |   0.5   |       文本识别结果置信度，值越大，把握越大       |
| `use_angle_cls`  |  `bool`      |   `true`   |       是否使用文本行的方向分类       |
| `print_verbose`  |    `bool`    |   `true`   |       是否打印各个部分耗时信息       |
| `min_height`  |    `int`    |   30   |       图像最小高度（单位是像素）<br/>低于这个值，会跳过文本检测阶段，直接进行后续识别       |
|`width_height_ratio`| `int`| 8| 如果输入图像的宽高比大于`width_height_ratio`，则会跳过文本检测，直接进行后续识别<br/>`width_height_ratio=-1`：不用这个参数 |

- `min_height`是用来过滤只有一行文本的图像（如下图），这类图像不会进入文本检测模块，直接进入后续过程。

    ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/single_line_text.jpg)

#### `Det`部分

|    参数名称      | 取值范围   | 默认值   |                       作用                       |
| :------------: | :----------: | :-----: | :----------------------------------------------|
|  `use_cuda`   |    `bool`     | `false` |              是否使用CUDA，加速推理              |
|`limit_side_len`| - | 736 | 限制图像边的长度的像素值 |
|`limit_type`| `[min, max]` | `min` | 限制图像的最小边长度还是最大边为`limit_side_len` <br/> 示例解释：当`limit_type=min`和`limit_side_len=736`时，图像最小边小于736时，<br/>会将图像最小边拉伸到736，另一边则按图像原始比例等比缩放。 |
|  `thresh`      | `[0, 1]` | 0.3 | 图像中文字部分和背景部分分割阈值<br/>值越大，文字部分会越小 |
|  `box_thresh`  |    `[0, 1]`    |   0.5   | 文本检测所得框是否保留的阈值，值越大，召回率越低 |
|`max_candidates`| - | 1000 | 图像中最大可检测到的文本框数目，一般够用|
| `unclip_ratio` |  `[1.6, 2.0]`  |   1.6   |   控制文本检测框的大小，值越大，检测框整体越大   |
|`use_dilation`| `bool` | `true` | 是否使用形态学中的膨胀操作，一般采用默认值即可 |
|`score_mode` | `string`| `fast` | `fast`是求rectangle区域的平均分数，容易造成弯曲文本漏检，`slow`是求polygon区域的平均分数，会更准确，但速度有所降低，可按需选择 |

#### `Cls`部分
|    参数名称      | 取值范围   | 默认值   |                       作用                       |
| :------------: | :----------: | :-----: | :----------------------------------------------|
|`cls_img_shape`| - |`[3, 48, 192]`| 输入方向分类模型的图像Shape（CHW） |
|`cls_batch_num`| - | 6 | 批次推理的batch大小，一般采用默认值即可，太大并没有明显提速，效果还可能会差 |
|`cls_thresh`|`[0, 1]`|0.9| 方向分类结果的置信度|
|`label_list`| - | `[0, 180]` | 方向分类的标签，0°或者180°，**该参数不能动** |

#### `Rec`部分

|    参数名称      | 取值范围   | 默认值   |                       作用                       |
|:------------: | :----------: | :-----: | :----------------------------------------------|
|`rec_img_shape`| - |`[3, 48, 320]`| 输入文本识别模型的图像Shape（CHW） |
|`rec_batch_num`| - | 6 | 批次推理的batch大小，一般采用默认值即可，太大并没有明显提速，效果还可能会差 |
