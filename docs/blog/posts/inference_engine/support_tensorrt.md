---
title: RapidOCR支持TensorRT推理引擎
authors: [SWHL]
slug: support-tensorrt-engine
date: 2026-02-13
categories:
  - 推理引擎
comments: true
hide:
  - toc
---

记录支持TensorRT推理引擎的过程文档。

<!-- more -->

## 引言

首先感谢Github @[LocNgoXuan23](https://github.com/LocNgoXuan23)小伙伴的PR [#623](https://github.com/RapidAI/RapidOCR/pull/623)。有了这个PR，我这也有了抓手来推动支持TensorRT作为推理引擎。

大部分代码都已经在小伙伴提的 PR 中实现，很完善的实现，包括单元测试和 benchmark。我做的只是过一遍代码，看看怎么做的。

本来我以为 TensorRT 也可以像其他推理引擎一样，将 ONNX 模型预先转为指定格式，然后直接分发。但是随着我看源码的过程中，逐渐发现不是这么简单。 TensorRT 的 engine 格式模型都是根据当前设备来动态生成的。因此，用户在使用前，需要先生成符合当前机器的 engine 格式模型文件，之后再直接使用。

当前代码在指定使用 TensorRT 作为推理引擎后，程序会自动启动构建 engine 格式的模型文件。构建耗时依当前设备而有所不同。

## 运行环境¶

- Docker镜像：@[LocNgoXuan23](https://github.com/LocNgoXuan23)在[Discord](https://discord.com/channels/1143707958690189373/1143707958690189376/1468529402118672512)中给出的镜像：[7.0-gc-triton-devel](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream?version=7.0-gc-triton-devel)
- NVIDIA环境：(详细参见：[link](https://gist.github.com/SWHL/0efe902ee469d49fc63d50e297d7fd98) )
    - cuda: 12.2
    - tensorrt: 8.6.1
    - cuda-python: 12.2.0
- Python环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.5.0
  text_det_metric==0.0.8
  text_rec_metric==0.0.1
  datasets==3.6.0
  ```

## 支持Det模型

### 比较转化前后推理精度差异

这里主要采用@[LocNgoXuan23](https://github.com/LocNgoXuan23)给出的 benchmark 脚本来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNXRuntime"

    ```python linenums="1"
    # Step 1: 获得推理结果
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

    # Step 2: 计算指标
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "(Exp2) RapidOCR + TensorRT + FP16"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "EngineConfig.tensorrt.use_fp16": True,
        "Det.engine_type": EngineType.TENSORRT,
        "Det.lang_type": LangDet.CH,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV4,
        "Det.model_path": "rapidocr/models/ch_PP-OCRv4_det_infer.onnx",
    }
    engine = RapidOCR(params=engine_config)

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

    # Step 2: 计算指标
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "(Exp3) RapidOCR + TensorRT + FP32"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "EngineConfig.tensorrt.use_fp16": False,
        "Det.engine_type": EngineType.TENSORRT,
        "Det.lang_type": LangDet.CH,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV4,
        "Det.model_path": "rapidocr/models/ch_PP-OCRv4_det_infer.onnx",
    }
    engine = RapidOCR(params=engine_config)

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

    # Step 2: 计算指标
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

### 结果对比

!!! tip

    ```markdwon
    1. 仅测试了中文相关的识别模型，其他语言的模型，因为没有对应评测集，就不测试指标了。
    2. 下面指标仅作为转换前后，比较模型精度差异使用哈！
    3. TensorRT 下的耗时是GPU的，ONNXRuntime 是 CPU 的。
    ```

|Exp|模型|推理框架|推理引擎|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|
|1|ch_PP-OCRv4_det_infer|RapidOCR|ONNXRuntime|0.8595|0.8434|0.8514|0.182|
|2|ch_PP-OCRv4_det_infer|RapidOCR|TensorRT FP16|0.8667|0.8396|0.8529|0.0406|
|3|ch_PP-OCRv4_det_infer|RapidOCR|TensorRT FP32|0.8677|0.8396|0.8534|0.0402|
|||||||||
|4|ch_PP-OCRv5_mobile_det|RapidOCR|ONNXRuntime|0.7861|0.8266|0.8058|0.1835|
|5|ch_PP-OCRv5_mobile_det|RapidOCR|TensorRT FP16|0.7943|0.8216|0.8077|0.0415|
|6|ch_PP-OCRv5_mobile_det|RapidOCR|TensorRT FP32|0.7938|0.8220|0.8077|0.0402|
|||||||||
|7|ch_PP-OCRv4_det_server_infer|RapidOCR|ONNXRuntime|0.7713|0.8579|0.8123|2.8449|
|8|ch_PP-OCRv4_det_server_infer|RapidOCR|TensorRT FP16|0.3689|0.0516|0.0905|0.0415|
|9|ch_PP-OCRv4_det_server_infer|RapidOCR|TensorRT FP32|0.7811|0.8545|0.8161|0.0579|
|||||||||
|10|en_PP-OCRv3_det_infer|RapidOCR|ONNXRuntime|0.8066|0.8380|0.8220|0.1463|
|11|en_PP-OCRv3_det_infer|RapidOCR|TensorRT FP16|0.8147|0.8346|0.8245|0.0384|
|12|en_PP-OCRv3_det_infer|RapidOCR|TensorRT FP32|0.8153|0.8346|0.8248|0.04|
|||||||||
|13|Multilingual_PP-OCRv3_det_infer|RapidOCR|ONNXRuntime|0.4228|0.6921|0.5249|0.1681|
|14|Multilingual_PP-OCRv3_det_infer|RapidOCR|TensorRT FP16|0.4221|0.6906|0.5240|0.0447|
|15|Multilingual_PP-OCRv3_det_infer|RapidOCR|TensorRT FP32|0.4223|0.6906|0.5241|0.0452|
|||||||||
|16|ch_PP-OCRv5_server_det|RapidOCR|ONNXRuntime|0.7394|0.8442|0.7883|2.0193|
|17|ch_PP-OCRv5_server_det|RapidOCR|TensorRT FP16|0.4143|0.2059|0.2751|0.0387|
|18[^1]|ch_PP-OCRv5_server_det|RapidOCR|TensorRT FP32|0.7503|0.8411|0.7931|0.1238|

在 Exp 18 中，在我当前设备上，构建对应的 engine 模型没有成功，暂时还未解决，具体报错日志如下：

```bash linenums="1"
[INFO] 2026-02-25 08:10:57,064 [RapidOCR] base.py:22: Using engine_name: tensorrt
[INFO] 2026-02-25 08:10:57,415 [RapidOCR] main.py:519: Building TensorRT engine from rapidocr/models/ch_PP-OCRv5_server_det.onnx
[INFO] 2026-02-25 08:11:03,888 [RapidOCR] engine_builder.py:55: Using FP32 precision
[INFO] 2026-02-25 08:11:03,889 [RapidOCR] engine_builder.py:119: Set optimization profile for x: min=[1, 3, 32, 32], opt=[1, 3, 736, 736], max=[1, 3, 2048, 2048]
[INFO] 2026-02-25 08:11:03,889 [RapidOCR] engine_builder.py:67: Building TensorRT engine (this may take a few minutes)...
[02/25/2026-08:13:28] [TRT] [E] 1: No Myelin Error exists
[02/25/2026-08:13:28] [TRT] [E] 1: [runnerBuilderBase.cpp::buildAndSerializeMyelinGraph::326] Error Code 1: Myelin (No Myelin Error exists)
Traceback (most recent call last):
  File "/xxxxx/RapidOCR/python/test_det.py", line 25, in <module>
    engine = RapidOCR(params=engine_config)
  File "/xxxxx/RapidOCR/python/rapidocr/main.py", line 45, in __init__
    self._initialize(cfg)
  File "/xxxxx/RapidOCR/python/rapidocr/main.py", line 66, in _initialize
    self.text_det = TextDetector(cfg.Det)
  File "/xxxxx/RapidOCR/python/rapidocr/ch_ppocr_det/main.py", line 47, in __init__
    self.session = get_engine(cfg.engine_type)(cfg)
  File "/xxxxx/RapidOCR/python/rapidocr/inference_engine/tensorrt/main.py", line 88, in __init__
    self.engine = self._load_or_build_engine(cfg, engine_path)
  File "/xxxxx/RapidOCR/python/rapidocr/inference_engine/tensorrt/main.py", line 528, in _load_or_build_engine
    return builder.build()
  File "/xxxxx/RapidOCR/python/rapidocr/inference_engine/tensorrt/engine_builder.py", line 71, in build
    raise RuntimeError("Failed to build TensorRT engine")
RuntimeError: Failed to build TensorRT engine
```

## 支持Rec模型

### 比较转化前后推理精度差异

这里主要采用@[LocNgoXuan23](https://github.com/LocNgoXuan23)给出的 benchmark 脚本来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNXRuntime"

    ```python linenums="1"
    # Step 1: 获得推理结果
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

    # Step 2: 计算指标
    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "(Exp2) RapidOCR + TensorRT + FP16"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import time

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangRec, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "EngineConfig.tensorrt.use_fp16": True,
        "Rec.engine_type": EngineType.TENSORRT,
        "Rec.lang_type": LangRec.CH,
        "Rec.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV4,
        "Rec.model_path": "rapidocr/models/ch_PP-OCRv4_rec_infer.onnx",
    }
    engine = RapidOCR(params=engine_config)

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

    # Step 2: 计算指标
    from text_rec_metric import TextRecMetric

    metric = TextRecMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "(Exp3) RapidOCR + TensorRT + FP32"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import time

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangRec, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "EngineConfig.tensorrt.use_fp16": False,
        "Rec.engine_type": EngineType.TENSORRT,
        "Rec.lang_type": LangRec.CH,
        "Rec.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV4,
        "Rec.model_path": "rapidocr/models/ch_PP-OCRv4_rec_infer.onnx",
    }
    engine = RapidOCR(params=engine_config)

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

    # Step 2: 计算指标
    from text_rec_metric import TextRecMetric

    metric = TextRecMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

### 结果对比

| Exp | 模型 | 推理框架 | 推理引擎 | ExactMatch↑ | CharMatch↑ | Elapse↓ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ch_PP-OCRv4_rec_infer | RapidOCR | ONNXRuntime | 0.8290 | 0.9432 | 0.0176 |
| 2 | ch_PP-OCRv4_rec_infer | RapidOCR | TensorRT FP16 | 0.8290 | 0.9430 | 0.0023 |
| 3 | ch_PP-OCRv4_rec_infer | RapidOCR | TensorRT FP32 | 0.8290 | 0.9432 | 0.0022 |
| | | | | | | |
| 4 | ch_PP-OCRv4_rec_server_infer | RapidOCR | ONNXRuntime | 0.8065 | 0.9375 | 0.0811 |
| 5 | ch_PP-OCRv4_rec_server_infer | RapidOCR | TensorRT FP16 | 0.8097 | 0.9376 | 0.0025 |
| 6 | ch_PP-OCRv4_rec_server_infer | RapidOCR | TensorRT FP32 | 0.8065 | 0.9376 | 0.0047 |
| | | | | | | |
| 7 | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR | ONNXRuntime | 0.8097 | 0.9444 | 0.0809 |
| 8 | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR | TensorRT FP16 | 0.8097 | 0.9444 | 0.0028 |
| 9 | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR | TensorRT FP32 | 0.8097 | 0.9444 | 0.0051 |
| | | | | | | |
| 10 | ch_PP-OCRv5_rec_mobile_infer | RapidOCR | ONNXRuntime | 0.7355 | 0.9177 | 0.0196 |
| 11 | ch_PP-OCRv5_rec_mobile_infer | RapidOCR | TensorRT FP16 | 0.7387 | 0.9193 | 0.0024 |
| 12 | ch_PP-OCRv5_rec_mobile_infer | RapidOCR | TensorRT FP32 | 0.7355 | 0.9177 | 0.0039 |
| | | | | | | |
| 13 | ch_PP-OCRv5_rec_server_infer | RapidOCR | ONNXRuntime | 0.8129 | 0.9431 | 0.0582 |
| 14 | ch_PP-OCRv5_rec_server_infer | RapidOCR | TensorRT FP16 | 0.8129 | 0.9431 | 0.0039 |
| 15 | ch_PP-OCRv5_rec_server_infer | RapidOCR | TensorRT FP32 | 0.8161 | 0.9439 | 0.0049 |

[^1]: 该结果来自[link](https://github.com/RapidAI/RapidOCR/pull/623#issuecomment-3805793254)。
