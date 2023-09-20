---
weight: 200
date: "2023-09-11"
draft: false
author: "SWHL"
title: "使用说明"
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

### 安装
```bash {linenos=table}
pip install rapidocr-onnxruntime
```

### 初始化
类RapidOCR是主类，其初始化函数如下：
```python {linenos=table}
class RapidOCR:
    def __init__(self, config_path: Optional[str] = None, **kwargs):
        pass
```
支持两种自定义传参数的方案，下面分别详细说明：
- 以`config.yaml`方式
  1. 找到`rapidocr_onnxruntime`安装目录下的`config.yaml`文件，可以通过`pip show rapidocr_onnxruntime`找到其安装路径。
  2. 将`config.yaml`拷贝出来，放到当前运行目录下
  3. 按需自定义参数修改即可，具体参数解释，参见[config.yaml]()
      ```python {linenos=table}
      engine = RapidOCR(config_path="your.yaml")
      ```
- (推荐) 以具体参数传入，参数基本和`config.yaml`中对应，只是个别名称有所区别。
  ```python {linenos=table}
  class RapidOCR:
      def __init__(
          self,
          text_score: float = 0.5,
          print_verbose: bool = False,
          min_height: int = 30,
          width_height_ratio: float = 8,
          det_use_cuda: bool = False,
          det_model_path: Optional[str] = None,
          det_limit_side_len: float = 736,
          det_limit_type: str = "min",
          det_thresh: float = 0.3,
          det_box_thresh: float = 0.5,
          det_unclip_ratio: float = 1.6,
          det_donot_use_dilation: bool = False,
          det_score_mode: str = "fast",
          cls_use_cuda: bool = False,
          cls_model_path: Optional[str] = None,
          cls_image_shape: List[int] = [3, 48, 192],
          cls_label_list: List[str] = ["0", "180"],
          cls_batch_num: int = 6,
          cls_thresh: float = 0.9,
          rec_use_cuda: bool = False,
          rec_model_path: Optional[str] = None,
          rec_img_shape: List[int] = [3, 48, 320],
          rec_batch_num: int = 6,
      ):
          pass

  engine = RapidOCR()

  res, elapse = engine(img, use_det=True, use_cls=True, use_rec=True)
  ```

### 输入和输出
- 输入：`Union[str, np.ndarray, bytes, Path]`
- 输出：
  - 有值：`([[文本框坐标], 文本内容, 置信度], 推理时间)`，示例如下：
    ```text
    [[左上, 右上, 右下, 左下], '小明', '0.99'], [0.02, 0.02, 0.85]
    ```
  - 无值：`(None, None)`

### 不同传入方式使用示例
{{< tabs tabTotal="3">}}
{{% tab tabName="str" %}}

```python {linenos=table}
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
img_path = 'tests/test_files/ch_en_num.jpg'
result, elapse = engine(img_path)
print(result)
print(elapse)
```

{{% /tab %}}
{{% tab tabName="np.ndarray" %}}

```python {linenos=table}
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
img = cv2.imread('tests/test_files/ch_en_num.jpg')
result, elapse = engine(img)
print(result)
print(elapse)
```

{{% /tab %}}
{{% tab tabName="Bytes" %}}

```python {linenos=table}
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_path = 'tests/test_files/ch_en_num.jpg'
with open(img_path, 'rb') as f:
    img = f.read()
result, elapse = engine(img)
print(result)
print(elapse)
```

{{% /tab %}}
{{% tab tabName="Path" %}}

```python {linenos=table}
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_path = Path('tests/test_files/ch_en_num.jpg')
result, elapse = engine(img_path)
print(result)
print(elapse)
```
{{% /tab %}}
{{< /tabs >}}
