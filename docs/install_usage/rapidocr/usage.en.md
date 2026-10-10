---
title: RapidOCR Usage Guide
description: Python and CLI usage, configuration, image inputs and OCR output fields for RapidOCR.
comments: true
hide:
  - toc
---

## Overview

This guide covers the two main ways to use RapidOCR: the Python API and the `rapidocr` command-line interface. For installation, see the [installation guide](install.md).

Starting with `rapidocr>=3.10.0`, model loading is lazy: detection, classification and recognition models are loaded when first used. The first call may therefore take longer than subsequent calls.

!!! info

    This English page covers the primary workflow. The [Chinese usage reference](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/usage/) contains the complete stage-by-stage examples and return-value details.

## Python usage

```python
from rapidocr import RapidOCR

engine = RapidOCR()
image_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(image_url)

print(result.txts)
print(result.scores)
result.vis("vis_result.jpg")
```

You can pass a YAML configuration file:

```bash
rapidocr config
```

```python
from rapidocr import RapidOCR

engine = RapidOCR(config_path="default_rapidocr.yaml")
result = engine(image_url)
```

You can also override individual settings through `params`:

```python
from rapidocr import EngineType, ModelType, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.OPENVINO,
        "Rec.model_type": ModelType.TINY,
    }
)
```

## Image inputs

RapidOCR accepts a local path, URL, encoded bytes, NumPy array, Pillow image and supported memory buffers. See the [image input reference](image_input.md) for examples and buffer layout requirements.

## Output

The return value is one of `TextDetOutput`, `TextClsOutput`, `TextRecOutput` or `RapidOCROutput`, depending on the enabled stages.

For the normal detection + classification + recognition pipeline, the most useful fields are:

| Field | Description |
| --- | --- |
| `boxes` | Four-point coordinates for each detected text line. |
| `txts` | Recognized text, in the same order as `boxes`. |
| `scores` | Confidence score for each recognized line. |
| `word_results` | Word-level results when `return_word_box=True`. |
| `elapse_list` | Detection, classification and recognition times in seconds. |
| `elapse` | Total inference time in seconds. |

```python
print(result.boxes.shape)
print(result.txts)
print(result.scores)
print(result.elapse)
```

Set `use_det`, `use_cls` or `use_rec` to `False` when you need only selected stages. The corresponding return type and fields are documented in the [Chinese usage reference](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/usage/).

## CLI usage

Check the installation:

```bash
rapidocr check
```

Run OCR on an image and save a visualization:

```bash
rapidocr -img "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg" --vis_res
```

Download models for a configuration:

```bash
rapidocr download_models
```

For all available CLI options, run `rapidocr --help`.
