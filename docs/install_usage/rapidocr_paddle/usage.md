---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-paddle/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-paddle?style=flat-square"></a>
    <a href="https://pepy.tech/project/rapidocr_paddle"><img src="https://static.pepy.tech/personalized-badge/rapidocr_paddle?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Paddle"></a>
</p>

#### 简介

`rapidocr_paddle`系列包是基于PaddlePaddle框架作为推理引擎的，支持CPU和GPU上推理。推荐GPU上用这个，CPU端还是以`rapidocr_onnxruntime`和`rapidocr_openvino`为主。毕竟PaddlePaddle的CPU端还是比较重的。

值得说明的是，这个包和PaddleOCR相比，代码基本都是一样的，只不过这个库将里面核心推理代码抽了出来，更加精简而已。

#### 安装

1. 安装PaddlePaddle框架GPU版，并验证可行性，详细参见: [官方教程](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html)。验证是否安装成功代码如下：

    ```python linenums="1"
    import paddle

    print(paddle.utils.run_check())
    # 如果出现PaddlePaddle is installed successfully!，说明您已成功安装。
    ```

2. 安装`rapidocr_paddle`

    ```bash linenums="1"
    pip install rapidocr_paddle
    ```

#### 使用

```python linenums="1"
import cv2

from rapidocr_paddle import RapidOCR

# 注意这里的参数
engine = RapidOCR(det_use_cuda=True, cls_use_cuda=True, rec_use_cuda=True)

image_path = "tests/test_files/ch_en_num.jpg"
result, elapse_list = engine(image_path)

```

其他使用详情，同`rapidocor_onnxruntime`系列，参见: [link](./rapidocr/usage.md)

#### 推理速度比较

相关测评代码，参见[AI Studio](https://aistudio.baidu.com/projectdetail/6924494)，Fork可直接运行查看。不要只推理一张来测试推理速度，需要先推理一张作为预热，后续再看推理速度。

经过初步粗略估计，同一张图像，推理10次，耗时情况见下表：

|         推理库         | 平均耗时(s/img) |   运行环境   |
| :--------------------: | :-------------: | :------: |
| `rapidocr_onnxruntime` |     1.6505      | CPU 2 Cores RAM 16GB         |
| `rapidocr_paddle[GPU]` |     0.0508      | CPU 2 Cores RAM 16GB <br/> GPU Tesla V100 16G |
