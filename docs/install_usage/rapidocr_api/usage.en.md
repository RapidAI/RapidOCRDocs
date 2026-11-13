---
comments: true
hide:
  - toc
---

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RapidAI/RapidOCRAPI/releases/download/v0.2.0/rapidocr_api_logo_v2_dark.png" width="60%" height="60%" class="no-radius">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/RapidAI/RapidOCRAPI/releases/download/v0.2.0/rapidocr_api_logov2_white.png" width="60%" height="60%" class="no-radius">
    <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://github.com/RapidAI/RapidOCRAPI/releases/download/v0.2.0/rapidocr_api_logov2_white.png" class="no-radius">
  </picture>

 <br/>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
  <a href="https://github.com/RapidAI/RapidOCRAPI/graphs/contributors"><img src="https://img.shields.io/github/contributors/RapidAI/RapidOCRAPI?color=9ea"></a>
  <a href="https://github.com/RapidAI/RapidOCRAPI/stargazers"><img src="https://img.shields.io/github/stars/RapidAI/RapidOCRAPI?color=ccf" ></a>
  <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20rapidocr_api"></a>
  <a href="https://pypi.org/project/rapidocr_api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr_api"></a>
  <a href="https://choosealicense.com/licenses/apache-2.0/"><img src="https://img.shields.io/badge/License-Apache%202-dfd.svg"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

## 📖 Introduction

!!! note

    The output of the OCR API is the most raw result; you can extend it further as needed.

Source repository: <https://github.com/RapidAI/RapidOCRAPI>

This package wraps the [rapidocr](../rapidocr/install.md) library into an API, implemented using [FastAPI](https://fastapi.tiangolo.com/) + [uvicorn](https://uvicorn.dev/).

It is positioned as an API interface for quickly calling `rapidocr`, and does not take multi-process handling of concurrent requests into account. If you have such needs, you can take a look at [gunicorn](https://gunicorn.org/) and similar tools.

## 📌 Version Dependencies

|`rapidocr_api`|`rapidocr`|
|:---|:---|
|`v0.2.x`|`rapidocr>1.0.0,<3.0.0`|
|`v0.1.x`|`rapidocr_onnxruntime`|

## Installation

```bash linenums="1"
pip install rapidocr_api
```

## Start the Server

In `rapidocr_api>=0.1.0`, model parameters can be passed through environment variables: det_model_path, cls_model_path, rec_model_path; parameters can also be passed in the interface to control whether to use the three parts of models: detection, orientation classification and recognition; for specific calls, see the documentation below.

=== "Usage on Windows"

    ```bash linenums="1"
    set det_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_det_server_infer.onnx
    set rec_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api
    ```

=== "Usage on Linux"

    ```bash linenums="1"
    # Start with default parameters
    rapidocr_api

    # Specify parameters: port and number of processes;
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2

    # Specify models
    export det_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx
    export rec_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
    ```

=== "Docker Usage"

    [Dockerfile source](https://github.com/RapidAI/RapidOCR/blob/3aa4463ad20bc9dc8d8b08766d0f46d7699efc57/api/Dockerfile)

    Build the image:

    ```bash linenums="1"
    git clone https://github.com/RapidAI/RapidOCR.git
    cd api

    # Build method 1: use the host's network
    docker build -t="rapidocr_api:0.1.4" --network host .

    # Build method 2: use the proxy on the host
    docker build -t rapidocr_api:0.1.4 --network host --build-arg HTTP_PROXY=http://127.0.0.1:8888 --build-arg HTTPS_PROXY=http://127.0.0.1:8888 .
    ```

    Debug run:

    ```bash linenums="1"
    docker run --rm -p 9003:9003 --name rapidocr_api -e TZ=Asia/Shanghai rapidocr_api:0.1.4
    ```

    Run:

    ```bash linenums="1"
    docker run -d -p 9003:9003 --name rapidocr_api -e TZ=Asia/Shanghai rapidocr_api:0.1.4
    ```

    API web interface:

    ```bash linenums="1"
    http://<ip>:9003/docs
    ```

    ---

    How to temporarily modify and verify in Docker

    ```bash linenums="1"
    docker run -p 9003:9003 --name rapidocr_api -e TZ=Asia/Shanghai rapidocr_api:0.1.4
    ```

    Enter the container to modify the Python source files; it is best to add apt-get install vim to the Dockerfile for installation

    ```bash linenums="1"
    docker exec -it rapidocr_api /bin/bash
    cd /usr/local/lib/python3.10/site-packages/rapidocr_api
    ...
    # Modify the parameter file
    vi /usr/local/lib/python3.10/site-packages/rapidocr_onnxruntime/config.yaml
    # Type exit to quit after making the changes
    ```

    Restart the container

    ```bash linenums="1"
    docker restart rapidocr_api
    ```

    View logs:

    ```bash linenums="1"
    docker logs -f rapidocr_api
    ```

## Call the API

!!! info

    Calling is essentially sending a POST request; Curl and Python call examples are given below, and other programming languages work the same way.

### Curl call

```bash linenums="1"
curl -F image_file=@1.png http://0.0.0.0:9003/ocr
```

### Python call

=== "Send a POST request using a file"

    ```python linenums="1"
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as f:
        file_dict = {'image_file': (img_path, f, 'image/png')}
        response = requests.post(url, files=file_dict, timeout=60)

    print(response.json())
    ```

=== "Send a POST request using base64"

    ```python linenums="1"
    import base64
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as fa:
        img_str = base64.b64encode(fa.read())

    payload = {'image_data': img_str}
    response = requests.post(url, data=payload, timeout=60)

    print(response.json())
    ```

=== "Control the use of detection, orientation classification and recognition models"

    ```python linenums="1"
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as f:
        data = {"use_det": False, "use_cls": True, "use_rec": True}
        response = requests.post(url, files=file_dict, data=data, timeout=60)
    print(response.json())
    ```

## Output Result Description

If there is text in the image, a dictionary format will be output, described in detail as follows:

```json linenums="1"
{
 "0": {
  "rec_txt": "香港深圳抽血，", # Recognized text
  "dt_boxes": [  # In order: top-left → top-right → bottom-right → bottom-left
   [265, 18],
   [472, 231],
   [431, 271],
   [223, 59]
  ],
  "score": "0.8176"   # Confidence
 }
}
```

If no text is detected, an empty dictionary (`{}`) will be output.

## Example Results

```json linenums="1"
{
    "0": {
        "rec_txt": "8月26日！",
        "dt_boxes": [
            [333.0, 72.0],
            [545.0, 40.0],
            [552.0, 90.0],
            [341.0, 122.0]
        ],
        "score": "0.7342"
    },
    "1": {
        "rec_txt": "澳洲名校招生信息",
        "dt_boxes": [
            [266.0, 163.0],
            [612.0, 116.0],
            [619.0, 163.0],
            [272.0, 210.0]
        ],
        "score": "0.8262"
    },
    "2": {
        "rec_txt": "解读！！",
        "dt_boxes": [
            [341.0, 187.0],
            [595.0, 179.0],
            [598.0, 288.0],
            [344.0, 296.0]
        ],
        "score": "0.6152"
    },
    "3": {
        "rec_txt": "Rules...",
        "dt_boxes": [
            [446.0, 321.0],
            [560.0, 326.0],
            [559.0, 352.0],
            [445.0, 347.0]
        ],
        "score": "0.8704"
    }
}
```
