---
comments: true
---

`rapidocr_onnxruntime`包含了命令行工具，安装之后，即可使用。

### 参数说明

```bash linenums="1"
$ rapidocr_onnxruntime -h
usage: rapidocr_onnxruntime [-h] -img IMG_PATH [-p] [--text_score TEXT_SCORE] [--no_det]
                            [--no_cls] [--no_rec] [--print_verbose] [--min_height MIN_HEIGHT]
                            [--width_height_ratio WIDTH_HEIGHT_RATIO]
                            [--max_side_len MAX_SIDE_LEN] [--min_side_len MIN_SIDE_LEN]
                            [--return_word_box] [--intra_op_num_threads INTRA_OP_NUM_THREADS]
                            [--inter_op_num_threads INTER_OP_NUM_THREADS] [--det_use_cuda]
                            [--det_use_dml] [--det_model_path DET_MODEL_PATH]
                            [--det_limit_side_len DET_LIMIT_SIDE_LEN] [--det_limit_type {max,min}]
                            [--det_thresh DET_THRESH] [--det_box_thresh DET_BOX_THRESH]
                            [--det_unclip_ratio DET_UNCLIP_RATIO] [--det_donot_use_dilation]
                            [--det_score_mode {slow,fast}] [--cls_use_cuda] [--cls_use_dml]
                            [--cls_model_path CLS_MODEL_PATH] [--cls_image_shape CLS_IMAGE_SHAPE]
                            [--cls_label_list CLS_LABEL_LIST] [--cls_batch_num CLS_BATCH_NUM]
                            [--cls_thresh CLS_THRESH] [--rec_use_cuda] [--rec_use_dml]
                            [--rec_model_path REC_MODEL_PATH] [--rec_keys_path REC_KEYS_PATH]
                            [--rec_img_shape REC_IMG_SHAPE] [--rec_batch_num REC_BATCH_NUM] [-vis]
                            [--vis_font_path VIS_FONT_PATH] [--vis_save_path VIS_SAVE_PATH]

options:
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
  --max_side_len MAX_SIDE_LEN
  --min_side_len MIN_SIDE_LEN
  --return_word_box
  --intra_op_num_threads INTRA_OP_NUM_THREADS
  --inter_op_num_threads INTER_OP_NUM_THREADS

Det:
  --det_use_cuda
  --det_use_dml
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
  --cls_use_dml
  --cls_model_path CLS_MODEL_PATH
  --cls_image_shape CLS_IMAGE_SHAPE
  --cls_label_list CLS_LABEL_LIST
  --cls_batch_num CLS_BATCH_NUM
  --cls_thresh CLS_THRESH

Rec:
  --rec_use_cuda
  --rec_use_dml
  --rec_model_path REC_MODEL_PATH
  --rec_keys_path REC_KEYS_PATH
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

!!! example

    以下只给出常见用例，具体可自行探索使用

=== "图像预测"

    ```bash linenums="1"
    rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg
    ```

=== "只使用检测"

    ```bash linenums="1"
    rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -no_cls -no_rec
    ```

=== "只使用识别"

    ```bash linenums="1"
    rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -no_det -no_cls
    ```

=== "可视化查看"

    ```bash linenums="1"
    rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg -vis --vis_font_path resources/fonts/FZYTK.TTF
    ```
