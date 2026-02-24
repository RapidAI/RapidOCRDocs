---
title: RapidOCR支持MNN推理引擎
date: 2026-01-21
authors: [SWHL]
slug: rapidocr-support-mnn-engine
categories:
  - 推理引擎
comments: true
hide:
  - toc
links:
  - 如何使用不同推理引擎？: install_usage/rapidocr/how_to_use_infer_engine.md
---

记录支持MNN推理引擎的过程文档。

<!-- more -->

## 引言

首先感谢Github @[narc1ssus1](https://github.com/narc1ssus1)小伙伴的PR [#613](https://github.com/RapidAI/RapidOCR/pull/613)。有了这个PR，我这也有了抓手来推动支持MNN作为推理引擎。

## 运行环境¶

- 操作系统：macOS Tahoe 26.2
- 硬件：MacBookPro M2

- Python环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.5.0
  mnn==3.2.0
  text_det_metric==0.0.8
  text_rec_metric==0.0.1
  datasets==3.6.0
  ```

## 安装MNN

!!! note

    该部分主要参考官方文档：https://mnn-docs.readthedocs.io/en/latest/tools/convert.html

```bash linenums="1"
pip install MNN
```

## 转换ONNX模型

转换命令：

```bash linenums="1"
MNNConvert -f ONNX --modelFile rapidocr/models/ch_PP-OCRv4_det_infer.onnx --MNNModel mnn/ch_PP-OCRv4_det_infer.mnn --bizCode MNN
```

输出以下内容，表示转换成功：

```bash linenums="1"
The device supports: i8sdot:1, fp16:1, i8mm: 1, sve2: 0, sme2: 0
Start to Convert Other Model Format To MNN Model..., target version: 3.2
[09:38:49] :46: ONNX Model ir version: 10
[09:38:49] :47: ONNX Model opset version: 14
Start to Optimize the MNN Net...
caution: some weight absolute values are not zero and smaller than float min:1.175494e-38, please check your training process. op name:Add.119
inputTensors : [ x, ]
outputTensors: [ fetch_name_0, ]
Converted Success!
```

## 支持Det模型

### 比较转化前后推理精度差异

两者对比的模型为`ch_PP-OCRv4_det_infer`模型，Exp1基于`RapidOCR+ONNXRuntime`格式模型推理, Exp2基于`RapidOCR+MNN`格式模型推理。

两次实验除模型不一样外，其余均相同。其余未列出的实验均只换了模型。

=== "(Exp1) RapidOCR + ONNXRuntime"

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

=== "(Exp2) RapidOCR + MNN"

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

!!! tip

    ```markdwon
    1. 其他版本的模型，我这里就直接给出对比结果了。因为教程都是一样的，仅换了一个模型而已。
    2. 下面指标仅作为转换前后，比较模型精度差异使用哈！
    ```

|Exp|模型|推理框架|推理引擎|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|
|1|ch_PP-OCRv4_det_infer|RapidOCR|ONNXRuntime|0.8595|0.8434|0.8514|0.182|
|2|ch_PP-OCRv4_det_infer|RapidOCR|MNN|0.8595|0.8434|0.8514|0.159|
|||||||||
|3|ch_PP-OCRv5_mobile_det|RapidOCR|ONNXRuntime|0.7861|0.8266|0.8058|0.1835|
|4|ch_PP-OCRv5_mobile_det|RapidOCR|MNN|0.7861|0.8266|0.8058|0.1526|
|||||||||
|5|ch_PP-OCRv4_det_server_infer|RapidOCR|ONNXRuntime|0.7713|0.8579|0.8123|2.8449|
|6|ch_PP-OCRv4_det_server_infer|RapidOCR|MNN|0.7713|0.8579|0.8123|1.889|
|||||||||
|7|en_PP-OCRv3_det_infer|RapidOCR|ONNXRuntime|0.8066|0.8380|0.8220|0.1463|
|8|en_PP-OCRv3_det_infer|RapidOCR|MNN|0.8066|0.8380|0.8220|0.1262|
|||||||||
|9|Multilingual_PP-OCRv3_det_infer|RapidOCR|ONNXRuntime|0.4228|0.6921|0.5249|0.1681|
|10|Multilingual_PP-OCRv3_det_infer|RapidOCR|MNN|0.4228|0.6921|0.5249|0.1282|
|||||||||
|11|ch_PP-OCRv5_server_det|RapidOCR|ONNXRuntime|0.7394|0.8442|0.7883|2.0193|
|12|ch_PP-OCRv5_server_det|RapidOCR|MNN|0.7394|0.8442|0.7883|1.6048|

## 支持Rec模型

### 比较转化前后推理精度差异

两者对比的模型为`ch_PP-OCRv4_rec_infer`模型，Exp1基于`RapidOCR+ONNXRuntime`格式模型推理, Exp2基于`RapidOCR+MNN`格式模型推理。两次实验除模型不一样外，其余均相同。

=== "(Exp1) RapidOCR + ONNXRuntime"

    Step 1: 获得推理结果

    ```python linenums="1"
    import time

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, OCRVersion, RapidOCR

    model_path = "rapidocr/models/ch_PP-OCRv4_rec_infer.onnx"
    dict_path = "rapidocr/models/ppocr_keys_v1.txt"
    engine = RapidOCR(
        params={
            "Rec.model_path": model_path,
            "Rec.rec_keys_path": dict_path,
        }
    )

    dataset = load_dataset("SWHL/text_rec_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        t0 = time.perf_counter()
        result = engine(img, use_rec=True, use_cls=False, use_det=False)
        elapse = time.perf_counter() - t0

        rec_text = result.txts[0]
        if len(rec_text) <= 0:
            rec_text = ""
            elapse = 0

        gt = one_data.get("label", None)
        content.append(f"{rec_text}\t{gt}\t{elapse}")

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

=== "(Exp2) RapidOCR + MNN"

    Step 1: 获得推理结果

    ```python linenums="1"
    import time

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, OCRVersion, RapidOCR

    model_path = "mnn/rec/PP-OCRv4/ch_PP-OCRv4_rec_infer.onnx"
    dict_path = "rapidocr/models/ppocr_keys_v1.txt"
    engine = RapidOCR(
        params={
            "Rec.model_path": model_path,
            "Rec.rec_keys_path": dict_path,
            "Rec.engine_type": EngineType.MNN,
        }
    )

    dataset = load_dataset("SWHL/text_rec_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        t0 = time.perf_counter()
        result = engine(img, use_rec=True, use_cls=False, use_det=False)
        elapse = time.perf_counter() - t0

        rec_text = result.txts[0]
        if len(rec_text) <= 0:
            rec_text = ""
            elapse = 0

        gt = one_data.get("label", None)
        content.append(f"{rec_text}\t{gt}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    ```

    Step 2: 计算指标

    ```python linenums="1"
    from text_rec_metric import TextRecMetric

    metric = TextRecMetric()

    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

### 结果对比

!!! tip

    ```markdwon
    1. 仅测试了中文相关的识别模型，其他语言的模型，因为没有对应评测集，就不测试指标了。
    2. 下面指标仅作为转换前后，比较模型精度差异使用哈！
    ```

|Exp|模型|推理框架|推理引擎|ExactMatch↑|CharMatch↑|Elapse↓|
|:---:|:---|:---|:---|:---:|:---:|:---:|
|1|ch_PP-OCRv4_rec_infer|RapidOCR|ONNXRuntime|0.829|0.9432|0.0176|
|2|ch_PP-OCRv4_rec_infer|RapidOCR|MNN|0.829|0.9432|0.0213|
||||||||
|3|ch_PP-OCRv4_rec_server_infer|RapidOCR|ONNXRuntime|0.8065|0.9375|0.0811|
|4|ch_PP-OCRv4_rec_server_infer|RapidOCR|MNN|0.8065|0.9375|0.0639|
||||||||
|5|ch_doc_PP-OCRv4_rec_server_infer|RapidOCR|ONNXRuntime|0.8097|0.9444|0.0809|
|6|ch_doc_PP-OCRv4_rec_server_infer|RapidOCR|MNN|0.8065|0.9375|0.0763|
||||||||
|7|ch_PP-OCRv5_rec_mobile_infer|RapidOCR|ONNXRuntime|0.7355|0.9177|0.0196|
|8|ch_PP-OCRv5_rec_mobile_infer|RapidOCR|MNN|0.7355|0.9177|0.0373|
||||||||
|9|ch_PP-OCRv5_rec_server_infer|RapidOCR|ONNXRuntime|0.8129|0.9431|0.0582|
|10|ch_PP-OCRv5_rec_server_infer|RapidOCR|MNN|0.8129|0.9431|0.0724|

### 其他单独校验模型

#### PP-OCRv4

- [x] arabic_PP-OCRv4_rec_infer
- [x] chinese_cht_PP-OCRv3_rec_infer
- [x] cyrillic_PP-OCRv3_rec_infer
- [x] devanagari_PP-OCRv4_rec_infer
- [x] en_PP-OCRv4_rec_infer
- [x] japan_PP-OCRv4_rec_infer
- [x] ka_PP-OCRv4_rec_infer
- [x] korean_PP-OCRv4_rec_infer
- [x] latin_PP-OCRv3_rec_infer
- [x] ta_PP-OCRv4_rec_infer
- [x] te_PP-OCRv4_rec_infer

#### PP-OCRv5

- [x] arabic_PP-OCRv5_rec_mobile_infer
- [x] cyrillic_PP-OCRv5_rec_mobile_infer
- [x] devanagari_PP-OCRv5_rec_mobile_infer
- [x] en_PP-OCRv5_rec_mobile_infer
- [x] el_PP-OCRv5_rec_mobile_infer
- [x] eslav_PP-OCRv5_rec_mobile_infer
- [x] korean_PP-OCRv5_rec_mobile_infer
- [x] latin_PP-OCRv5_rec_mobile_infer
- [x] ta_PP-OCRv5_rec_mobile_infer
- [x] te_PP-OCRv5_rec_mobile_infer
- [x] th_PP-OCRv5_rec_mobile_infer

相关MNN模型已经上传到[魔搭模型库](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)中。

## 写在最后

从以上基准比较来看，MNN推理引擎整体推理速度要比ONNXRuntime更快一些。值得一提的是，我这里仅测试了小批量的数据下效果，难免存在疏漏。更多全面测试，仍需要使用到的小伙伴多多反馈。

`rapidocr`已经在`>=v3.6.0`集成以上模型，欢迎使用和反馈。
