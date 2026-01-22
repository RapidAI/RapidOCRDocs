---
title: Python版支持MNN推理
date: 2026-01-21
authors: [SWHL]
categories:
  - 模型相关
comments: true
hide:
  - toc
---

记录支持MNN推理的过程文档。

<!-- more -->

## 引言

首先感谢[narc1ssus1](https://github.com/narc1ssus1)小伙伴的PR [#613](https://github.com/RapidAI/RapidOCR/pull/613)。有了这个PR，我这也有了着手来推动支持MNN作为推理引擎的动力。

## 运行环境¶

- 操作系统：macOS Tahoe 26.2
- 硬件：MacBookPro M2

- Python环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.5.0
  mnn==3.2.0
  text_det_metric==0.0.8
  datasets==3.6.0
  ```

## 支持Det模型

!!! note

    MNN部分主要参考官方文档：https://mnn-docs.readthedocs.io/en/latest/tools/convert.html

### 安装MNN

```bash linenums="1"
pip install MNN
```

### 转换ONNX模型

转换命令：

```bash linenums="1"
MNNConvert -f ONNX --modelFile rapidocr/models/ch_PP-OCRv4_det_infer.onnx --MNNModel mnn/ch_PP-OCRv4_det_infer.mnn --bizCode MNN
```

### 比较转化前后推理精度差异

#### 运行环境

- 操作系统：macOS Tahoe 26.2
- 硬件：MacBookPro M2
- Python环境：

  ```bash linenums="1"
  rapidocr==3.5.0
  mnn==3.2.0
  text_det_metric==0.0.8
  datasets==3.6.0
  ```

#### 运行推理代码

两者对比的模型为`ch_PP-OCRv4_det_infer`模型，Exp1基于`RapidOCR+ONNXRuntime`格式模型推理, Exp2基于`RapidOCR+MNN`格式模型推理。

两次实验除模型不一样外，其余均相同。

=== "(Exp1) RapidOCR+ONNXRuntime格式模型"

    Step 1: 获得推理结果

    ```python linenums="1"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import RapidOCR

    engine = RapidOCR()

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")
    ```

    Step 2: 计算指标

    ```python linenums="1"
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "(Exp2) RapidOCR+MNN格式模型"

    Step 1: 获得推理结果

    ```python linenums="1"
    from pathlib import Path

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, RapidOCR

    model_path = "mnn/ch_PP-OCRv4_det_infer.mnn"
    engine = RapidOCR(
        params={"Det.engine_type": EngineType.MNN, "Det.model_path": model_path}
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    ```

    Step 2: 计算指标

    ```python linenums="1"
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

### 结果对比

|Exp|模型|推理框架|模型格式|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|
|1|PP-OCRv4_mobile_det|RapidOCR |ONNXRuntime|0.8595|0.8434|0.8514|0.182|
|2|PP-OCRv4_mobile_det|RapidOCR| MNN|0.8595|0.8434|0.8514|0.159|
