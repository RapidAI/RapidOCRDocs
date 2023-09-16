---
weight: 1
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


### 简介
- `rapidocr_onnxruntime`为基于ONNXRuntime推理引擎的OCR包，默认在CPU上运行。
- 因为模型较小，因此将相关模型都已打到Whl包，可直接pip安装使用。
- `rapidocr_onnxruntime`各个版本的对应关系：
    |版本|内置模型版本|对应PaddleOCR 分支|
    |:---:|:---:|:---:|
    |`v1.3.x`|PaddleOCR v4版| [release/2.7](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.7)|
    |`v1.2.x`<br/>`v1.1.x`<br/>`v1.0.x`|PaddleOCR v3版| [release/2.6](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6)|
- 推荐使用[PaddleOCRModelConveter](https://github.com/RapidAI/PaddleOCRModelConverter)在线转换，现用现转。推理代码都是同一个，只需更换模型即可。已转好**ONNX模型下载地址：**[百度网盘](https://pan.baidu.com/s/1PTcgXG2zEgQU6A_A3kGJ3Q?pwd=jhai) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing)，大家可自行搭配使用。
- 所有常用的参数配置都在[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr_onnxruntime/config.yaml)下，其中每个独立的模块下均有独立的`config.yaml`配置文件，可以单独使用。
- 关于选择哪个版本的包（`rapidocr_onnxruntime` 或者 `rapidocr_openvino`）?
    |推理引擎|推理速度更快|占用内存更少|
    |:---:|:---:|:---:|
    |`rapidocr_onnxruntime`||✓|
    |`rapidocr_openvino`|✓|⚠️ openvino存在内存不释放的问题，参见[wiki](https://github.com/RapidAI/RapidOCR/wiki/openvino%E5%85%A5%E9%97%A8)|


### Installation
```bash
pip install rapidocr-onnxruntime
```

### Usage
1. python脚本使用
    - ⚠️注意：初始化RapidOCR可不提供`config.yaml`，默认使用安装目录下的`config.yaml`。如有自定义需求：
      - 一是可直接通过初始化参数传入。详细参数参考下面命令行部分，和`config.yaml`基本对应。
      - 二是复制`config.yaml`，自行更改，然后初始化给出。e.g. `engine = RapidOCR(config_path="custom.yaml")`

    - 输入：`Union[str, np.ndarray, bytes, Path]`
    - 输出：
      - 有值：`([[文本框坐标], 文本内容, 置信度], 推理时间)`，e.g. `[[左上, 右上, 右下, 左下], '小明', '0.99'], [0.02, 0.02, 0.85]`
      - 为空：`(None, None)`
    - 示例：
      ```python
      import cv2
      from rapidocr_onnxruntime import RapidOCR
      # from rapidocr_openvino import RapidOCR

      # RapidOCR可传入参数参考下面的命令行部分
      rapid_ocr = RapidOCR()

      img_path = 'tests/test_files/ch_en_num.jpg'

      # 输入格式一：str
      result, elapse = rapid_ocr(img_path)

      # 输入格式二：np.ndarray
      img = cv2.imread('tests/test_files/ch_en_num.jpg')
      result, elapse = rapid_ocr(img)

      # 输入格式三：bytes
      with open(img_path, 'rb') as f:
          img = f.read()
      result, elapse = rapid_ocr(img)

      # 输入格式四：Path
      result, elapse = rapid_ocr(Path(img_path))
      print(result)
      ```

3. 命令行使用
    - 参数说明：
      ```bash
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
    ```bash
    $ rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg
    ```
