---
title: RapidOCR 集成 PP-LCNet textline 文本行方向分类模型记录
date:
  created: 2026-03-24
authors:
 - SWHL
categories:
  - 模型相关
slug: rapidocr-pp-lcnet-textline-cls
hide:
  - toc
---


该文章主要记录 RapidOCR 集成 PP-LCNet textline 文本行方向分类模型记录，涉及模型转换，模型精度测试等步骤。

<!-- more -->

### 引言

该部分主要是支持 [文本行方向分类模块使用教程](https://www.paddleocr.ai/latest/version3.x/module_usage/textline_orientation_classification.html) 中两个文本行方向分类模型：**PP-LCNet_x0_25_textline_ori** 和 **PP-LCNet_x1_0_textline_ori**。

下面是从上述链接中得到的这两个模型的情况：

| 模型 | 模型下载链接  | Top-1 Acc（%） | GPU 推理耗时（ms） | CPU 推理耗时 (ms) | 模型存储大小（MB） | 介绍                                                         |
|-------|---|----|---|------------------|--------------------|-----|
| PP-LCNet_x0_25_textline_ori   | [推理模型](https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-LCNet_x0_25_textline_ori_infer.tar) / [训练模型](https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-LCNet_x0_25_textline_ori_pretrained.pdparams) | 98.85          | 2.16 / 0.41       | 2.37 / 0.73      | 0.96               | 基于 PP-LCNet_x0_25 的文本行分类模型，含有两个类别，即 0 度，180 度 |
| PP-LCNet_x1_0_textline_ori    | [推理模型](https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-LCNet_x1_0_textline_ori_infer.tar) / [训练模型](https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-LCNet_x1_0_textline_ori_pretrained.pdparams) | 99.42          | - / -             | 2.98 / 2.98      | 6.5                | 基于 PP-LCNet_x1_0 的文本行分类模型，含有两个类别，即 0 度，180 度 |

### 以下代码运行环境

- OS: macOs Tahoe 26.3.1 (a)
- Python: 3.10.0
- PaddlePaddle: 3.1.0
- paddle2onnx: 2.1.0
- paddlex: 3.0.0
- rapidocr: 2.1.0

### 1. 模型跑通

测试图：[link](https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/textline_rot180_demo.jpg)

```python linenums="1"
from paddleocr import TextLineOrientationClassification

# model: PP-LCNet_x1_0_textline_ori  /  PP-LCNet_x0_25_textline_ori
img_path = "datasets/textline_rot180_demo.jpg"
model = TextLineOrientationClassification(model_name="PP-LCNet_x1_0_textline_ori")
output = model.predict(img_path, batch_size=1)
for res in output:
    res.print(json_format=False)
    res.save_to_img("./output/demo.png")
    res.save_to_json("./output/res.json")
```

预期结果如下，表明成功运行：

```bash linenums="1"
Model files already exist. Using cached files. To redownload, please delete the directory manually: `/Users/xxxx/.paddlex/official_models/PP-LCNet_x1_0_textline_ori`.
{'res': {'input_path': 'datasets/textline_rot180_demo.jpg', 'page_index': None, 'class_ids': array([1], dtype=int32), 'scores': array([0.89868], dtype=float32), 'label_names': ['180_degree']}}
```

### 2. 模型转换

转换代码：

```bash linenums="1"
paddle2onnx --model_dir official_models/PP-LCNet_x0_25_textline_ori \
             --model_filename inference.json \
             --params_filename inference.pdiparams \
             --save_file official_models/onnx/PP-LCNet_x0_25_textline_ori.onnx
```

输出日志如下，表明转换成功：

```bash linenums="1"
[Paddle2ONNX] Start parsing the Paddle model file...
[Paddle2ONNX] Use opset_version = 9 for ONNX export.
[Paddle2ONNX] PaddlePaddle model is exported as ONNX format now.
2026-03-24 11:53:36 [INFO]      Try to perform constant folding on the ONNX model with Polygraphy.
[W] 'colored' module is not installed, will not use colors when logging. To enable colors, please install the 'colored' module: python3 -m pip install colored
[I] Folding Constants | Pass 1
[I]     Total Nodes | Original:   307, After Folding:   143 |   164 Nodes Folded
[I] Folding Constants | Pass 2
[I]     Total Nodes | Original:   143, After Folding:   143 |     0 Nodes Folded
2026-03-24 11:53:37 [INFO]      ONNX model saved in official_models/onnx/PP-LCNet_x0_25_textline_ori.onnx.
```

### 3. 模型精度测试

将上一步中转换得到的 ONNX 模型，在 PaddleOCR 源码模型推理时，插入 ONNX Runtime 推理 ONNX 模型的代码，确保相同输入，来比较输出是否在误差范围内。

```python linenums="1" title="/miniconda3/envs/py310/lib/python3.10/site-packages/paddlex/inference/models/image_classification/predictor.py"
# 省略上面代码
import numpy as np
import onnxruntime

model_path = "official_models/onnx/PP-LCNet_x0_25_textline_ori.onnx"
ort_session = onnxruntime.InferenceSession(model_path)
ort_inputs = {"x": x[0]}
ort_outputs = ort_session.run(None, ort_inputs)

if self._use_static_model:
    batch_preds = self.infer(x=x)
else:
    with TemporaryDeviceChanger(self.device):
        batch_preds = self.infer(x=x)

# 这里是比较相同输入时，输出结果数值差异有多大。如果这行代码可以执行通过，就说明模型转换前后差异很小。
np.testing.assert_allclose(batch_preds[0], ort_outputs[0], atol=1e-5, rtol=1e-5)

# 省略下面代码
```

### 4. 集成到 rapidocr 中

该部分主要包括将托管模型到魔搭、更改 rapidocr 代码适配等。

#### 托管模型到魔搭

该部分主要是涉及模型上传到对应位置，并合理命名。注意上传完成后，需要打 Tag，避免后续 rapidocr whl 包中找不到模型下载路径。

我这里已经上传到了魔搭上，详细链接参见：[link](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)

#### 更改 rapidocr 代码适配

该部分主要涉及到更改 [default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/4d35ed272a1192afbcb95e823d99eb14c86b7893/python/rapidocr/default_models.yaml) 和 [paddle.py](https://github.com/RapidAI/RapidOCR/blob/4d35ed272a1192afbcb95e823d99eb14c86b7893/python/rapidocr/inference_engine/paddle.py) 的代码来适配。

同时，需要添加对应的单元测试，在保证之前单测成功的同时，新的针对性该模型的单测也能通过。

我这里已经做完了，小伙伴们感兴趣可以去看看源码。

### 写在最后

