---
weight: 300
date: "2023-09-11"
draft: false
author: "SWHL"
title: "命令行工具"
icon: "code"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---

`rapidocr_onnxruntime`包含了命令行工具，安装之后，即可使用。

### 参数说明
```bash {linenos=table}
$ rapidocr_onnxruntime -h
usage: rapidocr_onnxruntime [-h] -img IMG_PATH [-p] [--text_score TEXT_SCORE]
                            [--no_det] [--no_cls] [--no_rec] [--print_verbose]
                            [--min_height MIN_HEIGHT]
                            [--width_height_ratio WIDTH_HEIGHT_RATIO]
                            [--det_use_cuda] [--det_model_path DET_MODEL_PATH]
                            [--det_limit_side_len DET_LIMIT_SIDE_LEN]
                            [--det_limit_type {max,min}]
                            [--det_thresh DET_THRESH]
                            [--det_box_thresh DET_BOX_THRESH]
                            [--det_unclip_ratio DET_UNCLIP_RATIO]
                            [--det_donot_use_dilation]
                            [--det_score_mode {slow,fast}] [--cls_use_cuda]
                            [--cls_model_path CLS_MODEL_PATH]
                            [--cls_image_shape CLS_IMAGE_SHAPE]
                            [--cls_label_list CLS_LABEL_LIST]
                            [--cls_batch_num CLS_BATCH_NUM]
                            [--cls_thresh CLS_THRESH] [--rec_use_cuda]
                            [--rec_model_path REC_MODEL_PATH]
                            [--rec_img_shape REC_IMG_SHAPE]
                            [--rec_batch_num REC_BATCH_NUM] [-vis]
                            [--vis_font_path VIS_FONT_PATH]
                            [--vis_save_path VIS_SAVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -img IMG_PATH, --img_path IMG_PATH
  -p, --print_cost

Global:
  --text_score TEXT_SCORE
  --no_det
  --no_cls
  --no_rec
  --print_verbose
  --min_height MIN_HEIGHT
  --width_height_ratio WIDTH_HEIGHT_RATIO

Det:
  --det_use_cuda
  --det_model_path DET_MODEL_PATH
  --det_limit_side_len DET_LIMIT_SIDE_LEN
  --det_limit_type {max,min}
  --det_thresh DET_THRESH
  --det_box_thresh DET_BOX_THRESH
  --det_unclip_ratio DET_UNCLIP_RATIO
  --det_donot_use_dilation
  --det_score_mode {slow,fast}

Cls:
  --cls_use_cuda
  --cls_model_path CLS_MODEL_PATH
  --cls_image_shape CLS_IMAGE_SHAPE
  --cls_label_list CLS_LABEL_LIST
  --cls_batch_num CLS_BATCH_NUM
  --cls_thresh CLS_THRESH

Rec:
  --rec_use_cuda
  --rec_model_path REC_MODEL_PATH
  --rec_img_shape REC_IMG_SHAPE
  --rec_batch_num REC_BATCH_NUM

Visual Result:
  -vis, --vis_res
  --vis_font_path VIS_FONT_PATH
                        When -vis is True, the font_path must have value.
  --vis_save_path VIS_SAVE_PATH
                        The directory of saving the vis image.
```

### 使用示例
{{< alert text="以下只给出常见用例，具体可自行探索使用" />}}

{{< tabs tabTotal="4">}}
{{% tab tabName="图像预测" %}}

```bash {linenos=table}
rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg
```

{{% /tab %}}
{{% tab tabName="只使用检测" %}}

```bash {linenos=table}
rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -no_cls -no_rec
```

{{% /tab %}}
{{% tab tabName="只使用识别" %}}

```bash {linenos=table}
rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -no_det -no_cls
```

{{% /tab %}}
{{% tab tabName="可视化查看" %}}

```bash {linenos=table}
raprapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -vis --vis_font_path resources/fonts/FZYTK.TTF
```

{{% /tab %}}
{{< /tabs >}}
