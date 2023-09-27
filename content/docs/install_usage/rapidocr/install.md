---
weight: 100
lastmod: "2022-08-25T15:39:03+01:00"
draft: false
author: "SWHL"
title: "安装"
icon: "code"
toc: true
description: ""
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-onnxruntime/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-onnxruntime?style=flat-square"></a>
    <a href="https://pepy.tech/project/rapidocr_onnxruntime"><img src="https://static.pepy.tech/personalized-badge/rapidocr_onnxruntime?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Ort"></a>
</p>

{{< alert context="info" text="`rapidocr_onnxruntime`和`rapidocr_openvino`两个包除推理引擎不同之外，其余均相同，后续说明文档均以`rapidocr_onnxruntime`为例<br/>如使用`rapidocr_openvino`，直接更换关键词`rapidocr_onnxruntime`为`rapidocr_openvino`即可。" />}}


{{% alert context="info" %}}
#### pypi上各个版本的对应关系：

|版本|内置模型版本|对应PaddleOCR 分支|
|:---:|:---:|:---:|
|`v1.3.x`|PaddleOCR v4版| [release/2.7](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.7)|
|`v1.2.x`<br/>`v1.1.x`<br/>`v1.0.x`|PaddleOCR v3版| [release/2.6](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6)|

{{% /alert %}}

{{< alert text="请使用Python3.6及以上版本。" />}}

顺利的话，一行命令即可。包大小约为14M左右，包含了三个模型。因为mobile版模型较小，因此将相关模型都已打到Whl包，可直接pip安装使用。

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