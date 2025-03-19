---
comments: true
hide:
  - toc
---

#### 引言

该部分涉及如何使用`rapidocr`库来进行图像文字识别工作。

#### 最简单的使用

一切都使用默认值。默认使用来自PP-OCRv4的DBNet中文轻量检测，来自PP-OCRv4的SVTR_LCNet中文识别模型。默认使用onnxruntime CPU版作为推理模型。

其他默认值的详细参数设置参见：[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/config.yaml)

```python linenums="1"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis()
```

#### 初始化RapidOCR实例输入

输入支持传入YAML格式的配置文件，同时支持参数直接传入使用。

=== "传入`config.yaml`使用"

    自定义`config.yaml`配置，

    ```bash linenums="1"
    rapidocr -img "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true" --vis_res
    ```

=== "直接传入参数"

    ```python linenums="1"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis()
    ```

#### 输出

#### 选择不同推理引擎

#### 选择CPU / GPU

#### 使用默认mobiel或server模型

#### 可视化结果

#### 选择自定义的模型推理
