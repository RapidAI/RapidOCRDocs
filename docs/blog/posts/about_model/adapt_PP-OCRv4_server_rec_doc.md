---
title: rapidocr集成PP-OCRv4_server_rec_doc模型记录
date: 2022-09-27
authors: [SWHL]
categories:
  - 模型相关
comments: true
---


> 该文章主要记录rapidocr如何集成PP-OCRv4_server_rec_doc模型的，涉及模型转换，模型精度测试等步骤。

<!-- more -->

#### 0. 模型跑通

该步骤主要先基于PaddleX可以正确使用PP-OCRv4_server_rec_doc模型得到正确结果。

该部分主要参考文档：[docs](https://paddlepaddle.github.io/PaddleX/latest/module_usage/tutorials/ocr_modules/text_recognition.html#_3)

安装`paddlex`:

```bash linenums="1"
pip install "paddlex[ocr]==3.0.0rc1"
```

测试PP-OCRv4_server_rec_doc模型能否正常识别：

测试用图：

![alt text](../images/1.jpg)

!!! tip

    运行以下代码时，模型会自动下载到**/Users/用户名/.paddlex/official_models**下。

```python linenums="1"
from paddlex import create_model

model = create_model(model_name="PP-OCRv4_server_rec_doc")
output = model.predict(input="images/1.jpg", batch_size=1)
for res in output:
    res.print()
    res.save_to_img(save_path="./output/")
    res.save_to_json(save_path="./output/res.json")

# 输出以下内容，表明成功：
# {'res': {'input_path': 'images/1.jpg', 'page_index': None, 'rec_text': '绿洲仕格维花园公寓', 'rec_score': 0.9839767813682556}}
```

#### 1. 模型转换

该部分主要参考文档： [docs](https://paddlepaddle.github.io/PaddleX/latest/pipeline_deploy/paddle2onnx.html?h=paddle2onnx#22)

PaddleX官方集成了paddle2onnx的转换代码：

```bash linenums="1"
paddlex --paddle2onnx --paddle_model_dir models/PP-OCRv4_server_rec_doc --onnx_model_dir models/PP-OCRv4_server_rec_doc
```

输出日志如下，表明成功：

```bash linenums="1"
Input dir: models/PP-OCRv4_server_rec_doc
Output dir: models/PP-OCRv4_server_rec_doc
Paddle2ONNX conversion starting...
  warnings.warn(warning_message)
[Paddle2ONNX] Start parsing the Paddle model file...
[Paddle2ONNX] Use opset_version = 7 for ONNX export.
[Paddle2ONNX] PaddlePaddle model is exported as ONNX format now.
2025-05-14 08:21:23 [INFO]      Try to perform optimization on the ONNX model with onnxoptimizer.
2025-05-14 08:21:23 [INFO]      ONNX model saved in models/PP-OCRv4_server_rec_doc/inference.onnx.
Paddle2ONNX conversion succeeded
Done
```

#### 2. 模型推理验证

#### 3. 模型精度测试

`{'ExactMatch': 0.8097, 'CharMatch': 0.9444, 'avg_elapse': 0.0818}`

#### 4. 集成到rapidocr中
