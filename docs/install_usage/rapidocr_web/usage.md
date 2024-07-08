---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-web/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-web"></a>
    <a href="https://pepy.tech/project/rapidocr_web"><img src="https://static.pepy.tech/personalized-badge/rapidocr_web?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>


### 简介
- 该库是`rapidocr_onnxruntime`的web版本，依赖最新版本的[`rapidocr_onnxruntime`](../rapidocr/rapidocr_onnxruntime.md)库。
- 如果想要离线部署，可以先手动下载[`rapidocr_onnxruntime`](https://pypi.org/project/rapidocr-onnxruntime/#files) whl包，再手动安装[`rapidocr_web`](https://pypi.org/project/rapidocr-web/#files) whl包来使用。
- 网页上显示的推理时间具体解释如下：

    <div align="center">
        <img src="https://raw.githubusercontent.com/RapidAI/RapidOCR/ae529c2ba79e6cbf04c54caf2d24feb75e947ca4/assets/ocrweb_time.jpg" width="80%" height="80%">
    </div>

### 安装
```bash linenums="1"
pip install rapidocr_web
```

### 使用
#### 用法:
```bash linenums="1"
$ rapidocr_web -h
usage: rapidocr_web [-h] [-ip IP] [-p PORT]

optional arguments:
-h, --help            show this help message and exit
-ip IP, --ip IP       IP Address
-p PORT, --port PORT  IP port
```
#### 运行:
```bash linenums="1"
rapidocr_web -ip 0.0.0.0 -p 9003
```

#### 浏览器打开 http://localhost:9003/，enjoy it!

!!! info

    浏览器打开的网址是`http`的，不是`https`。

<div align="center">
            <img src="https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/rapidocr_web_demo.gif" width="100%" height="100%">
</div>

