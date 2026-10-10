---
title: RapidOCR API Installation and Usage
description: Install, start and call the FastAPI-based RapidOCR HTTP service.
comments: true
hide:
  - toc
---

## Overview

Source repository: <https://github.com/RapidAI/RapidOCRAPI>

`rapidocr_api` exposes RapidOCR through FastAPI and Uvicorn. It is intended as a simple HTTP wrapper. For production concurrency and process management, place it behind an appropriate deployment setup and consult the upstream repository.

!!! note

    The API returns low-level OCR results. Applications should validate requests and transform the response for their own domain.

## Version compatibility

| `rapidocr_api` | OCR dependency |
| --- | --- |
| `v0.2.x` | `rapidocr>1.0.0,<3.0.0` |
| `v0.1.x` | Legacy `rapidocr_onnxruntime` package |

Check the package release notes before combining newer RapidOCR versions with this API wrapper.

## Installation

```bash
pip install rapidocr_api
```

## Start the server

```bash
rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
```

The interactive FastAPI documentation is available at:

```text
http://localhost:9005/docs
```

Model paths can be supplied through environment variables. For example on Linux:

```bash
export det_model_path=/path/to/detection.onnx
export rec_model_path=/path/to/recognition.onnx
rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
```

## Call the API

### cURL

```bash
curl -F image_file=@image.png http://localhost:9005/ocr
```

### Python file upload

```python
import requests

url = "http://localhost:9005/ocr"
image_path = "image.png"

with open(image_path, "rb") as image_file:
    files = {"image_file": (image_path, image_file, "image/png")}
    response = requests.post(url, files=files, timeout=60)

response.raise_for_status()
print(response.json())
```

### Base64 input

```python
import base64
from pathlib import Path

import requests

encoded = base64.b64encode(Path("image.png").read_bytes())
response = requests.post(
    "http://localhost:9005/ocr",
    data={"image_data": encoded},
    timeout=60,
)

response.raise_for_status()
print(response.json())
```

## Response format

When text is detected, the response maps result indexes to recognized text, box coordinates and confidence scores:

```json
{
  "0": {
    "rec_txt": "RapidOCR",
    "dt_boxes": [[10, 20], [180, 20], [180, 60], [10, 60]],
    "score": "0.98"
  }
}
```

If no text is detected, the API returns an empty object: `{}`.

For Docker examples, historical package layouts and additional request flags, see the [complete Chinese API reference](https://rapidai.github.io/RapidOCRDocs/install_usage/rapidocr_api/usage/).
