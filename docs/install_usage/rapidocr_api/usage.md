---
comments: true
hide:
  - toc
---

<p>
    <a href="https://github.com/RapidAI/RapidOCRAPI"><img src="https://img.shields.io/badge/源码-Github-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

!!! note

    OCR API的输出结果为最原始结果，大家可按需进一步扩展。

    `rapidocr_api>=0.2.0`版本是适配了`rapidocr>=2.0.0`版本的。

### 简介

- 该包是将[rapidocr_onnxruntime](./rapidocr/install.md)库做了API封装，采用[FastAPI](https://fastapi.tiangolo.com/) + [uvicorn](https://www.uvicorn.org/)实现。
- 定位是一个快速调用`rapidocr_onnxruntime`的API接口，没有考虑多进程处理并发请求，如果有这需求的小伙伴，可以看看[gunicorn](https://gunicorn.org/)等。

### 安装

```bash linenums="1"
pip install rapidocr_api
```

### 启动服务端

在`rapidocr_api>=0.1.0`中，可通过环境变量传递模型参数：det_model_path, cls_model_path, rec_model_path；接口中可传入参数，控制是否使用检测、方向分类和识别这三部分的模型；具体调用可参见下面文档。

=== "Windows下使用"

    ```bash linenums="1"
    set det_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_det_server_infer.onnx
    set rec_model_path=I:\models\图像相关\OCR\RapidOCR\PP-OCRv4\ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api
    ```

=== "Linux下使用"

    ```bash linenums="1"
    # 默认参数启动
    rapidocr_api

    # 指定参数：端口与进程数量；
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2

    # 指定模型
    export det_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx
    export rec_model_path=/mnt/sda1/models/PP-OCRv4/ch_PP-OCRv4_rec_server_infer.onnx
    rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
    ```

=== "Docker方式使用"

    ##### 快速体验
    
    ###### 直接拉取构建好的
    
    ```bash
    docker run -itd --restart=always --name rapidocr_api -p 9005:9005 qingchen0607/rapid-ocr-api:v20250619 
    ```
    !!! note
    
        镜像大小700MB左右，建议使用网络代理以减少拉取、构建镜像的时间。
        
        此镜像是为了快速体验rapid-ocr，若您有其他额外的配置或者需求需要自行构建。
    
    ###### 本地自行构建镜像运行
    
    ```bash linenums="1"
    git clone https://github.com/RapidAI/RapidOCR.git
    cd docker
    
    # 脚本赋权
    #chmod +x docker_build&run.sh docker_stop&clean.sh
    
    # build image and run 构建镜像并运行容器
    ./docker_build&run.sh
    
    # stop and rm image 停止、删除容器和镜像
    ./docker_stop&clean.sh
    ```
    
    ##### Dockerfile
    
    ```dockerfile
    FROM python:3.10.11-slim-buster
    ENV DEBIAN_FRONTEND=noninteractive
    WORKDIR /app
    RUN pip install --no-cache-dir onnxruntime rapidocr_api -i https://mirrors.aliyun.com/pypi/simple
    RUN pip uninstall -y opencv-python && \
        pip install --no-cache-dir opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple
    EXPOSE 9005
    CMD ["bash", "-c", "rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2"]
    ```
    
    ##### 构建镜像
    
    ```bash
    # build方式1：使用宿主机的网络
    docker build -t rapidocr_api --network host .
    
    # build方式2：使用宿主机上的代理
    docker build -t rapidocr_api --network host --build-arg HTTP_PROXY=http://127.0.0.1:8888 --build-arg HTTPS_PROXY=http://127.0.0.1:8888 .
    ```
    
    ##### 测试
    
    ```bash linenums="1"
    # 运行停止后会自动清理容器
    docker run --rm -p 9005:9005 --name rapidocr_api -e TZ=Asia/Shanghai rapidocr_api
    ```
    
    ##### 运行
    
    ```bash linenums="1"
    docker run -itd --restart=always --name rapidocr_api -p 9005:9005  -e TZ=Asia/Shanghai rapidocr_api
    ```
    
    ##### API Docs
    
    ```bash linenums="1"
    http://<ip>:9005/docs
    ```
    
    ---
    
    ##### Docker 临时修改并验证的方法
    
    进入container修改python源文件，Dockerfile最好加上`apt-get update && apt-get install vim -y`安装
    
    ```bash linenums="1"
    docker exec -it rapidocr_api /bin/bash
    cd /usr/local/lib/python3.10/site-packages/rapidocr_api
    ...
    # 修改参数文件
    vim /usr/local/lib/python3.10/site-packages/rapidocr_onnxruntime/config.yaml
    # 改好后exit退出
    ```
    
    重启container
    
    ```bash linenums="1"
    docker restart rapidocr_api
    ```
    
    查看日志：
    
    ```bash linenums="1"
    docker logs -f rapidocr_api
    ```

### 调用

!!! info

    调用本质就是发送一个POST请求，以下给出Curl和Python的调用示例，其他编程语言同理。

#### Curl调用

```bash linenums="1"
curl -F image_file=@1.png http://0.0.0.0:9005/ocr
```

#### Python调用

=== "以文件方式发送POST请求"

    ```python linenums="1"
    import requests
    
    url = 'http://localhost:9005/ocr'
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
    
    url = 'http://localhost:9005/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'
    
    with open(img_path, 'rb') as fa:
        img_str = base64.b64encode(fa.read())
    
    payload = {'image_data': img_str}
    response = requests.post(url, data=payload, timeout=60)
    
    print(response.json())
    ```

=== "控制使用检测、方向分类和识别模型"

    ```python linenums="1"
    import requests
    
    url = 'http://localhost:9005/ocr'
    img_path = 'tests/test_files/ch_en_num.jpg'
    
    with open(img_path, 'rb') as f:
        data = {"use_det": False, "use_cls": True, "use_rec": True}
        response = requests.post(url, files=file_dict, data=data, timeout=60)
    print(response.json())
    ```

### 输出结果说明

如果图像中存在文字，则会输出字典格式，具体介绍如下：

```json linenums="1"
{
 "0": {
  "rec_txt": "香港深圳抽血，", # 识别的文本
  "dt_boxes": [  # 依次为左上角 → 右上角 → 右下角 → 左下角
   [265, 18],
   [472, 231],
   [431, 271],
   [223, 59]
  ],
  "score": "0.8176"   # 置信度
 }
}
```

如果没有检测到文字，则会输出空字典(`{}`)。

### 示例结果

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
