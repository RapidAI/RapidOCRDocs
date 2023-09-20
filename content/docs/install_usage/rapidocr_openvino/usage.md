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
- 以config.yaml方式
  1. 找到`rapidocr_onnxruntime`安装目录下的`config.yaml`文件，可以通过`pip show rapidocr_onnxruntime`找到其安装路径。
  2. 将`config.yaml`拷贝出来，放到当前运行目录下
  3. 按需自定义参数修改即可，具体参数解释，参见[config.yaml]()

- (推荐) 以具体参数传入
  ```python {linenos=table}
  class RapidOCR:
      def __init__(self, config_path: Optional[str] = None, **kwargs):
          pass
  ```

### 脚本使用
- 初始化`RapidOCR`类可不提供[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/29d5f5fc01fbff7c49926a3c297fa8a3fb1624af/python/rapidocr_onnxruntime/config.yaml)文件，默认使用安装目录下的`config.yaml`。如有自定义需求：
  - 方案一：可直接通过初始化参数传入。详细参数参考下面命令行部分，和`config.yaml`基本对应。
  - 方案二：复制`config.yaml`，自行更改，然后初始化给出。示例如下：
    ```python {linenos=table}
    engine = RapidOCR(config_path="your.yaml")
    ```

- 输入：`Union[str, np.ndarray, bytes, Path]`
- 输出：
  - 有值：`([[文本框坐标], 文本内容, 置信度], 推理时间)`，示例如下：
    ```text
    [[左上, 右上, 右下, 左下], '小明', '0.99'], [0.02, 0.02, 0.85]
    ```
  - 无值：`(None, None)`
- 示例：
  ```python {linenos=table}
  from pathlib import Path

  import cv2
  from rapidocr_onnxruntime import RapidOCR

  # RapidOCR可传入的参数参考下面的命令行部分
  engine = RapidOCR()

  img_path = 'tests/test_files/ch_en_num.jpg'

  # 输入格式一：str
  result, elapse = engine(img_path)

  # 输入格式二：np.ndarray
  img = cv2.imread('tests/test_files/ch_en_num.jpg')
  result, elapse = engine(img)

  # 输入格式三：bytes
  with open(img_path, 'rb') as f:
      img = f.read()
  result, elapse = engine(img)

  # 输入格式四：Path
  result, elapse = engine(Path(img_path))
  print(result)
  ```
