---
title: RapidOCR Parameters
description: Configuration file and detection, classification and recognition parameter reference for RapidOCR.
comments: true
hide:
  - toc
---

## Generate a configuration file

```bash
rapidocr config
```

This creates `default_rapidocr.yaml` in the current directory. You can pass the file with `RapidOCR(config_path=...)`, or pass individual values through the `params` mapping.

!!! info

    This page summarizes the most frequently used parameters. See the [complete Chinese parameter reference](parameters.md) for every field, default value and version-specific note.

## Common parameter groups

### Global

| Parameter | Description |
| --- | --- |
| `text_score` | Minimum text confidence used for output filtering. |
| `use_det`, `use_cls`, `use_rec` | Enable or disable detection, orientation classification and recognition. |
| `min_side_len`, `max_side_len` | Image resize limits used during preprocessing. |
| `use_vertical_padding` | Add vertical padding for narrow text regions. |
| `return_word_box` | Return word-level boxes when supported. |
| `model_root_dir` | Root directory for downloaded or local models. |

### Det

| Parameter | Description |
| --- | --- |
| `engine_type` | Inference backend, such as `onnxruntime`, `openvino`, `paddle`, `torch`, `mnn` or `tensorrt`. |
| `lang_type` | Detection language route. The available values depend on the OCR version and model route. |
| `model_type` | Model size or variant, such as `tiny`, `small`, `medium`, `mobile` or `server`. |
| `ocr_version` | OCR model family, such as `PP-OCRv4`, `PP-OCRv5` or `PP-OCRv6`. |
| `limit_side_len` | Target side length used by detection preprocessing. |
| `box_thresh` | Detection box threshold. A higher value usually reduces recall. |
| `unclip_ratio` | Expansion ratio applied to detected text boxes. |

### Cls

| Parameter | Description |
| --- | --- |
| `cls_image_shape` | Input shape for orientation classification, default `[3, 48, 192]`. |
| `cls_batch_num` | Classification batch size. The default is usually sufficient. |
| `cls_thresh` | Confidence threshold for orientation correction. |
| `label_list` | Orientation labels, normally `["0", "180"]`. Do not change unless using a compatible custom model. |

### Rec

| Parameter | Description |
| --- | --- |
| `lang_type` | Recognition language route. See the [model list](../../model_list.md). |
| `rec_img_shape` | Recognition input shape, default `[3, 48, 320]`. |
| `rec_batch_num` | Recognition batch size. |
| `rec_keys_path` | Optional dictionary file for a custom recognition model. |

For the complete parameter list, defaults and version-specific notes, see the [Chinese parameter reference](parameters.md).
