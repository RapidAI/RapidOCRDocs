---
weight: 700
title: "[GPU端] rapidocr_paddle"
description: ""
icon: menu_book
date: "2023-10-21"
draft: false
---

#### 简介
`rapidocr_paddle`系列包是基于PaddlePaddle框架作为推理引擎的，支持CPU和GPU上推理。

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

{{< alert context="light" text="相关测评代码，参见[AI Studio](https://aistudio.baidu.com/projectdetail/6924494)，Fork可直接运行查看。" />}}

经过初步粗略估计，同一张图像，推理10次，耗时情况见下表：

|推理库|平均耗时(s/img)|备注|
|:---:|:---:|:---:|
|`rapidocr_onnxruntime`|1.6505||
|`rapidocr_paddle[GPU]`|0.0508|V100 16G|
