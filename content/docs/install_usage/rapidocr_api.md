---
weight: 6
date: "2023-09-08"
draft: false
author: "SWHL"
title: "rapidocr_api"
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
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

### 简介
- 该包是将`rapidocr_onnxruntime`库做了API封装，采用`FastAPI` + `uvicorn`实现。
- 定位是一个快速搭建示例的demo，没有考虑多进程处理并发请求，如果有这需求的小伙伴，可以看看[gunicorn](https://gunicorn.org/)等。

### 安装
```bash {linenos=table}
pip install rapidocr_api
```

### 启动服务端
- 用法:
    ```bash {linenos=table}
    $ rapidocr_api -h
    usage: rapidocr_api [-h] [-ip IP] [-p PORT]

    optional arguments:
    -h, --help            show this help message and exit
    -ip IP, --ip IP       IP Address
    -p PORT, --port PORT  IP port
    ```
- 启动:
    ```bash {linenos=table}
    rapidocr_api -ip 0.0.0.0 -p 9003
    ```

### 调用
{{< alert context="info" text="调用本质就是发送一个POST请求，以下给出curl和python的调用示例，其他编程语言同理。" />}}

#### Curl调用
```bash {linenos=table}
curl -F image_file=@1.png http://0.0.0.0:9003/ocr
```

#### Python调用
- 以文件的方式发送POST请求
    ```python {linenos=table}
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as f:
        file_dict = {'image_file': (img_path, f, 'image/png')}
        response = requests.post(url, files=file_dict, timeout=60)

    print(response.json())
    ```
- 以`base64`方式发送POST请求
    ```python {linenos=table}
    import base64
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as fa:
        img_str = base64.b64encode(fa.read())

    payload = {'image_data': img_str}
    response = requests.post(url, data=payload)

    print(response.json())
    ```

### API输出
- 输出结果说明：
    - 如果图像中存在文字，则会输出字典格式，具体介绍如下：
        ```python {linenos=table}
        {
        "0": {
            "rec_txt": "香港深圳抽血，",  # 识别的文本
            "dt_boxes": [  # 依次为左上角 → 右上角 → 右下角 → 左下角
                [265, 18],
                [472, 231],
                [431, 271],
                [223, 59]
            ],
            "score": "0.8175641223788261"  # 置信度
            }
        }
        ```
    - 如果没有检测到文字，则会输出空json(`{}`)。
- 示例结果：
    <details>
    <summary>详情</summary>

    ```json {linenos=table}
    {
        "0": {
            "rec_txt": "8月26日！",
            "dt_boxes": [
                [333.0, 72.0],
                [545.0, 40.0],
                [552.0, 90.0],
                [341.0, 122.0]
            ],
            "score": "0.7342076812471662"
        },
        "1": {
            "rec_txt": "澳洲名校招生信息",
            "dt_boxes": [
                [266.0, 163.0],
                [612.0, 116.0],
                [619.0, 163.0],
                [272.0, 210.0]
            ],
            "score": "0.8261737492349412"
        },
        "2": {
            "rec_txt": "解读！！",
            "dt_boxes": [
                [341.0, 187.0],
                [595.0, 179.0],
                [598.0, 288.0],
                [344.0, 296.0]
            ],
            "score": "0.6152311325073242"
        },
        "3": {
            "rec_txt": "Rules...",
            "dt_boxes": [
                [446.0, 321.0],
                [560.0, 326.0],
                [559.0, 352.0],
                [445.0, 347.0]
            ],
            "score": "0.8704230123096042"
        }
    }
    ```
    </details>

{{< alert context="warning" text="OCR API的输出结果为最原始结果，大家可按需进一步扩展。" />}}
