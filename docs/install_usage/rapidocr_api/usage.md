---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

!!! note

    OCR API的输出结果为最原始结果，大家可按需进一步扩展。

### 简介

- 该包是将[rapidocr_onnxruntime](./rapidocr/install.md)库做了API封装，采用[FastAPI](https://fastapi.tiangolo.com/) + [uvicorn](https://www.uvicorn.org/)实现。
- 定位是一个快速调用`rapidocr_onnxruntime`的API接口，没有考虑多进程处理并发请求，如果有这需求的小伙伴，可以看看[gunicorn](https://gunicorn.org/)等。

### 安装

```bash linenums="1"
pip install rapidocr_api
```

### 启动服务端

在`rapidocr_api>=0.1.0`中，可通过环境变量传递模型参数：det_model_path, cls_model_path, rec_model_path；接口中可传入参数，控制是否使用检测、方向分类和识别这三部分的模型；具体调用可参见下面文档。

=== "Windows下启动"

    ```bash linenums="1"
    set det_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_det_server_infer.onnx
    set det_model_path=

    set rec_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api
    ```

=== "Linux下启动"

    ```bash linenums="1"
    # 默认参数启动
    rapidocr_api

    # 指定参数：端口与进程数量；
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2

    # 指定模型
    expert det_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx
    expert rec_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
    ```

=== "Docker下启动"

    [Dockerfile源码](https://github.com/RapidAI/RapidOCR/blob/3aa4463ad20bc9dc8d8b08766d0f46d7699efc57/api/Dockerfile)

    ```bash linenums="1"
    # 构建镜像
    cd api
    sudo docker build -t="rapidocr_api:0.1.1" .

    # 启动镜像
    docker run -p 9003:9003 --name rapidocr_api1 --restart always -d rapidocr_api:0.1.1
    ```

### 调用

!!! info

    调用本质就是发送一个POST请求，以下给出Curl和Python的调用示例，其他编程语言同理。

#### Curl调用

```bash linenums="1"
curl -F image_file=@1.png http://0.0.0.0:9003/ocr
```

#### Python调用

=== "以文件方式发送POST请求"

    ```python linenums="1"
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as f:
        file_dict = {'image_file': (img_path, f, 'image/png')}
        response = requests.post(url, files=file_dict, timeout=60)

    print(response.json())
    ```

=== "以base64方式发送POST请求"

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

=== "控制是否使用检测、方向分类和识别这三部分的模型"

    ```python linenums="1"
    import requests

    url = 'http://localhost:9003/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'

    with open(img_path, 'rb') as f:
        data = {"use_det": False, "use_cls": True, "use_rec": True}
        response = requests.post(url, files=file_dict, data=data, timeout=60)
    print(response.json())
    ```

### API输出

- 输出结果说明：
    - 如果图像中存在文字，则会输出字典格式，具体介绍如下：

        ```python linenums="1"
        {
        "0": {
            "rec_txt": "香港深圳抽血，",  # 识别的文本
            "dt_boxes": [  # 依次为左上角 → 右上角 → 右下角 → 左下角
                [265, 18],
                [472, 231],
                [431, 271],
                [223, 59]
            ],
            "score": "0.8176"  # 置信度
            }
        }
        ```

    - 如果没有检测到文字，则会输出空字典(`{}`)。
- 示例结果：

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
