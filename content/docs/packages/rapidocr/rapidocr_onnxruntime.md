---
weight: 10
date: "2023-09-11"
draft: false
author: "SWHL"
title: "rapidocr_onnxruntime"
icon: "code"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-onnxruntime/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-onnxruntime?style=flat-square"></a>
    <a href="https://pepy.tech/project/rapidocr_onnxruntime"><img src="https://static.pepy.tech/personalized-badge/rapidocr_onnxruntime?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Ort"></a>
</p>


### Installation
```bash {linenos=table}
pip install rapidocr-onnxruntime
```

### 脚本使用
- 初始化`RapidOCR`类可不提供[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/29d5f5fc01fbff7c49926a3c297fa8a3fb1624af/python/rapidocr_onnxruntime/config.yaml)文件，默认使用安装目录下的`config.yaml`。如有自定义需求：
  - 方案一：可直接通过初始化参数传入。详细参数参考下面命令行部分，和`config.yaml`基本对应。
  - 方案二：复制`config.yaml`，自行更改，然后初始化给出。示例如下：
    ```python {linenos=table}
    engine = RapidOCR(config_path="your.yaml")
    ```

- 输入：`Union[str, np.ndarray, bytes, Path]`
- 输出：
  - 有值：`([[文本框坐标], 文本内容, 置信度], 推理时间)`，示例如下：
    ```text
    [[左上, 右上, 右下, 左下], '小明', '0.99'], [0.02, 0.02, 0.85]
    ```
  - 无值：`(None, None)`
- 示例：
  ```python {linenos=table}
  from pathlib import Path

  import cv2
  from rapidocr_onnxruntime import RapidOCR

  # RapidOCR可传入的参数参考下面的命令行部分
  engine = RapidOCR()

  img_path = 'tests/test_files/ch_en_num.jpg'

  # 输入格式一：str
  result, elapse = engine(img_path)

  # 输入格式二：np.ndarray
  img = cv2.imread('tests/test_files/ch_en_num.jpg')
  result, elapse = engine(img)

  # 输入格式三：bytes
  with open(img_path, 'rb') as f:
      img = f.read()
  result, elapse = engine(img)

  # 输入格式四：Path
  result, elapse = engine(Path(img_path))
  print(result)
  ```

### 命令行使用
- 参数说明：
  ```bash {linenos=table}
  $ rapidocr_onnxruntime -h
  usage: rapidocr_onnxruntime [-h] -img IMG_PATH [-p] [--text_score TEXT_SCORE]
                              [--use_angle_cls USE_ANGLE_CLS]
                              [--use_text_det USE_TEXT_DET]
                              [--print_verbose PRINT_VERBOSE]
                              [--min_height MIN_HEIGHT]
                              [--width_height_ratio WIDTH_HEIGHT_RATIO]
                              [--det_use_cuda DET_USE_CUDA]
                              [--det_model_path DET_MODEL_PATH]
                              [--det_limit_side_len DET_LIMIT_SIDE_LEN]
                              [--det_limit_type {max,min}]
                              [--det_thresh DET_THRESH]
                              [--det_box_thresh DET_BOX_THRESH]
                              [--det_unclip_ratio DET_UNCLIP_RATIO]
                              [--det_use_dilation DET_USE_DILATION]
                              [--det_score_mode {slow,fast}]
                              [--cls_use_cuda CLS_USE_CUDA]
                              [--cls_model_path CLS_MODEL_PATH]
                              [--cls_image_shape CLS_IMAGE_SHAPE]
                              [--cls_label_list CLS_LABEL_LIST]
                              [--cls_batch_num CLS_BATCH_NUM]
                              [--cls_thresh CLS_THRESH]
                              [--rec_use_cuda REC_USE_CUDA]
                              [--rec_model_path REC_MODEL_PATH]
                              [--rec_img_shape REC_IMAGE_SHAPE]
                              [--rec_batch_num REC_BATCH_NUM]

  optional arguments:
  -h, --help            show this help message and exit
  -img IMG_PATH, --img_path IMG_PATH MUST
  -p, --print_cost

  Global:
  --text_score TEXT_SCORE
  --use_angle_cls USE_ANGLE_CLS
  --use_text_det USE_TEXT_DET
  --print_verbose PRINT_VERBOSE
  --min_height MIN_HEIGHT
  --width_height_ratio WIDTH_HEIGHT_RATIO

  Det:
  --det_use_cuda DET_USE_CUDA
  --det_model_path DET_MODEL_PATH
  --det_limit_side_len DET_LIMIT_SIDE_LEN
  --det_limit_type {max,min}
  --det_thresh DET_THRESH
  --det_box_thresh DET_BOX_THRESH
  --det_unclip_ratio DET_UNCLIP_RATIO
  --det_use_dilation DET_USE_DILATION
  --det_score_mode {slow,fast}

  Cls:
  --cls_use_cuda CLS_USE_CUDA
  --cls_model_path CLS_MODEL_PATH
  --cls_image_shape CLS_IMAGE_SHAPE
  --cls_label_list CLS_LABEL_LIST
  --cls_batch_num CLS_BATCH_NUM
  --cls_thresh CLS_THRESH

  Rec:
  --rec_use_cuda REC_USE_CUDA
  --rec_model_path REC_MODEL_PATH
  --rec_img_shape REC_IMAGE_SHAPE
  --rec_batch_num REC_BATCH_NUM
  ```
- 示例：
  ```bash {linenos=table}
  $ rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg
  ```
