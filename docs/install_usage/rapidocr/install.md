---
comments: true
---

<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pepy.tech/project/rapidocr"><img src="https://static.pepy.tech/personalized-badge/rapidocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=🔥%20Downloads%20rapidocr"></a>
<a href="https://pypi.org/project/rapidocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr"></a>

#### 简介

`rapidocr`是合并了`rapidocr_onnxruntime`、`rapidocr_openvino`、`rapidocr_paddle`以及支持PyTorch推理的版本。

`rapidocr`默认支采用ONNXRuntime CPU版作为推理引擎，可以通过安装其他推理引擎，通过相应参数来使用GPU推理。该部分请参见后续文档。

!!! note

    `rapidocr_onnxruntime`, `rapidocr_openvino`, `rapidocr_paddle`三个库逐渐不再维护，后续会以`rapidocr`为主。

#### 安装

顺利的话，一行命令即可。包大小约为14M左右，包含了三个模型（文本检测、文本行方向分类和文本识别）。因为其中mobile版模型较小，因此将相关模型都已打到whl包，可直接pip安装使用。

!!! info

    请使用Python3.6及以上版本。<br/> `rapidocr_onnxruntime`系列库目前仅在CPU上支持较好，GPU上推理很慢，这一点可参考[link](https://rapidai.github.io/RapidOCRDocs/docs/inference_engine/onnxruntime/onnxruntime-gpu/)。因此不建议用`onnxruntime-gpu`版推理。<br/>GPU端推理推荐用[`rapidocr_paddle`](../rapidocr_paddle.md)

```bash linenums="1"
pip install rapidocr
```

安装速度慢的话，可以指定国内的安装源，如使用清华源：

```bash linenums="1"
pip install rapidocr-i https://pypi.tuna.tsinghua.edu.cn/simple/
```

依赖的包如下：

!!! info

    如果在安装过程中，出现某个依赖包不能正确安装时，可先单独安装某个依赖包，之后再安装`rapidocr`即可。

```txt linenums="1"
pyclipper>=1.2.0
opencv_python>=4.5.1.48
numpy>=1.19.5,<3.0.0
six>=1.15.0
Shapely>=1.7.1,!=2.0.4  # python3.12 2.0.4 bug
PyYAML
Pillow
onnxruntime>=1.7.0
tqdm
omegaconf
```
