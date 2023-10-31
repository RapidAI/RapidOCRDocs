---
weight: 700
title: "[GPU端] rapidocr_paddle"
description: ""
icon: menu_book
date: "2023-10-21"
draft: false
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-paddle/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-paddle?style=flat-square"></a>
    <a href="https://pepy.tech/project/rapidocr_paddle"><img src="https://static.pepy.tech/personalized-badge/rapidocr_paddle?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20Paddle"></a>
</p>

#### 简介
`rapidocr_paddle`系列包是基于PaddlePaddle框架作为推理引擎的，支持CPU和GPU上推理。值得说明的是，这个包和PaddleOCR相比，代码基本都是一样的，只不过这个库将里面核心推理代码抽了出来，更加精简而已。

推荐GPU上用这个，CPU端还是以`rapidocr_onnxruntime`和`rapidocr_openvino`为主。毕竟PaddlePaddle的CPU端还是比较重的。

封装这个包的原因是为了弥补GPU端推理的空缺。因为面对成千上万的图像需要提取文字时，CPU端上推理速度还是较慢，不能满足需求。

#### 安装
1. 根据自己需求，先安装PaddlePaddle框架（CPU/GPU），并验证，参见: [官方教程](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html)，注意验证是否安装成功：
    ```python {linenos=table}
    import paddle

    print(paddle.utils.run_check())
    # 如果出现PaddlePaddle is installed successfully!，说明您已成功安装。
    ```
2. 安装`rapidocr_paddle`
    ```bash {linenos=table}
    pip install rapidocr_paddle
    ```

#### 使用

{{< tabs tabTotal="2">}}
{{% tab tabName="CPU端推理" %}}

前提是安装了CPU版的PaddlePaddle

```python {linenos=table}
import cv2

from rapidocr_paddle import RapidOCR

engine = RapidOCR()
image_path = "tests/test_files/ch_en_num.jpg"
result, elapse_list = engine(image_path)

print(result)
print(elapse_list)
```

{{% /tab %}}
{{% tab tabName="GPU端推理" %}}

前提是安装了GPU版的PaddlePaddle，注意在实例化`RapidOCR`类时，需要通过参数显式指定使用GPU。

```python {linenos=table}
import cv2

from rapidocr_paddle import RapidOCR

# 注意这里的参数
engine = RapidOCR(det_use_cuda=True, cls_use_cuda=True, rec_use_cuda=True)

image_path = "tests/test_files/ch_en_num.jpg"
result, elapse_list = engine(image_path)

```

{{% /tab %}}
{{< /tabs >}}


其他使用详情，同`rapidocor_onnxruntime`系列，参见: [link](./rapidocr/usage.md)

#### 推理速度比较

{{< alert context="light" text="相关测评代码，参见[AI Studio](https://aistudio.baidu.com/projectdetail/6924494)，Fork可直接运行查看。不要只推理一张来推理速度，推理第一张时，需要预热。" />}}

经过初步粗略估计，同一张图像，推理10次，耗时情况见下表：

|         推理库         | 平均耗时(s/img) |   备注   |
| :--------------------: | :-------------: | :------: |
| `rapidocr_onnxruntime` |     1.6505      |          |
| `rapidocr_paddle[GPU]` |     0.0508      | V100 16G |
