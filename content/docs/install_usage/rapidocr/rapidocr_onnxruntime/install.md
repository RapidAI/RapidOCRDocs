---
weight: 100
date: "2023-09-11"
draft: false
author: "SWHL"
title: "安装"
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
    <a href="https://pypi.org/project/rapidocr-onnxruntime/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-onnxruntime?style=flat-square"></a>
    <a href="https://pepy.tech/project/rapidocr_onnxruntime"><img src="https://static.pepy.tech/personalized-badge/rapidocr_onnxruntime?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Ort"></a>
</p>

{{< alert text="请使用Python3.6及以上版本。" />}}

顺利的话，一行命令即可。包大小约为14M左右，包含了三个模型。
```bash {linenos=table}
pip install rapidocr-onnxruntime
```

安装速度慢的话，可以指定国内的安装源，如使用清华源：
```bash {linenos=table}
pip install rapidocr_onnxruntime -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

依赖的包如下：

{{< alert context="info" text="如果在安装过程中，出现某个依赖包不能正确安装时，可先单独安装某个依赖包，之后再安装`rapidocr_onnxruntime`即可。" />}}

```txt {linenos=table}
pyclipper>=1.2.1
onnxruntime>=1.7.0
opencv_python>=4.5.1.48
numpy>=1.19.3
six>=1.15.0
Shapely>=1.7.1
PyYAML
Pillow
```