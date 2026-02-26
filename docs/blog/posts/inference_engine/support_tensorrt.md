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
links:
  - RapidOCR支持MNN推理引擎: blog/posts/inference_engine/support_mnn_engine.md
---

记录支持TensorRT推理引擎的过程文档。

<!-- more -->

## 引言

首先，衷心感谢 GitHub 用户 [@LocNgoXuan23](https://github.com/LocNgoXuan23) 提交的 PR [#623](https://github.com/RapidAI/RapidOCR/pull/623)！
正是有了这项贡献，我们才得以顺利推进 TensorRT 作为 RapidOCR 的推理引擎支持。

该 PR 已经实现了非常完善的 TensorRT 集成，不仅包含完整的推理逻辑，还附带了单元测试和详尽的性能基准（benchmark）数据。我所做的主要是通读代码，理解其实现机制。

起初，我以为 TensorRT 可以像其他推理引擎（如 ONNX Runtime 或 MNN）一样，将 ONNX 模型预先转换为通用的目标格式后直接分发使用。但在深入阅读源码后，我才意识到事情并非如此简单：**TensorRT 的 `.engine` 模型文件是与具体硬件强绑定的**，必须根据当前设备的 GPU 架构（如 compute capability）动态生成。

**因此，在实际使用中，用户首次指定 TensorRT 作为推理引擎时，程序会自动触发 `.engine` 文件的构建流程。这一过程的耗时取决于所用设备的性能——通常在桌面级或服务器级 GPU 上较快，在边缘设备（如 Jetson）上则可能稍长。**

为了便于横向对比，我在下方整理了 [@LocNgoXuan23](https://github.com/LocNgoXuan23) 在 PR 中提供的测试结果，并额外补充了 **硬件设备** 一列，方便大家结合自身环境参考性能表现。

## 运行环境¶

- Docker镜像：[@LocNgoXuan23](https://github.com/LocNgoXuan23) 在 [Discord](https://discord.com/channels/1143707958690189373/1143707958690189376/1468529402118672512) 中给出的镜像：[7.0-gc-triton-devel](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream?version=7.0-gc-triton-devel)
- 设备配置：8 CPU / 256 GB
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
  onnxruntime==1.23.2
  ```

[@LocNgoXuan23](https://github.com/LocNgoXuan23) 运行环境：

- GPU: NVIDIA GeForce RTX 3060 (12GB, Compute Capability 8.6)
- Driver: 570.211.01
- TensorRT: 8.6.1
- Python: 3.10.12
- ONNX Runtime: 1.18.0

### 转换耗时参考

#### 文本检测模型

|ONNX 模型| TensorRT Engine 格式 | 硬件设备 | 耗时(s) |
|:---|:---|:---|:---|
| ch_PP-OCRv4_det_infer.onnx | ch_PP-OCRv4_det_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 521.02 |
| ch_PP-OCRv4_det_infer.onnx | ch_PP-OCRv4_det_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 315.53 |
|||||
| ch_PP-OCRv5_mobile_det.onnx  | ch_PP-OCRv5_det_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 1438.65 |
| ch_PP-OCRv5_mobile_det.onnx  | ch_PP-OCRv5_det_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 407.53 |
|||||
| ch_PP-OCRv4_det_server_infer.onnx  | ch_PP-OCRv4_det_server_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 299.10 |
| ch_PP-OCRv4_det_server_infer.onnx  | ch_PP-OCRv4_det_server_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 109.56 |
|||||
| en_PP-OCRv3_det_infer.onnx | en_PP-OCRv4_det_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 224.54 |
| en_PP-OCRv3_det_infer.onnx | en_PP-OCRv4_det_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 87.11 |
|||||
| Multilingual_PP-OCRv3_det_infer.onnx  | multi_PP-OCRv4_det_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 122.11 |
| Multilingual_PP-OCRv3_det_infer.onnx  | multi_PP-OCRv4_det_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 52.64 |
|||||
| ch_PP-OCRv5_server_det.onnx  | ch_PP-OCRv5_det_server_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | - |
| ch_PP-OCRv5_server_det.onnx  | ch_PP-OCRv5_det_server_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | - |

#### 文本识别模型

|ONNX 模型| TensorRT Engine 格式 | 硬件设备 | 耗时(s) |
|:---|:---|:---|:---|
| ch_PP-OCRv4_rec_infer.onnx | ch_PP-OCRv4_rec_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 603.08 |
| ch_PP-OCRv4_rec_infer.onnx | ch_PP-OCRv4_rec_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 480.52 |
|||||
| ch_PP-OCRv4_rec_server_infer.onnx | ch_PP-OCRv4_rec_server_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 175.15 |
| ch_PP-OCRv4_rec_server_infer.onnx | ch_PP-OCRv4_rec_server_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 77.45 |
|||||
| ch_doc_PP-OCRv4_rec_server_infer.onnx | ch_doc_PP-OCRv4_rec_server_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 107.10 |
| ch_doc_PP-OCRv4_rec_server_infer.onnx | ch_doc_PP-OCRv4_rec_server_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 45.46 |
|||||
| ch_PP-OCRv5_rec_mobile_infer.onnx | ch_PP-OCRv5_rec_mobile_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 1437.16 |
| ch_PP-OCRv5_rec_mobile_infer.onnx | ch_PP-OCRv5_rec_mobile_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 543.68 |
|||||
| ch_PP-OCRv5_rec_server_infer.onnx | ch_PP-OCRv5_rec_server_sm80_fp16.engine | NVIDIA A800-SXM4-80GB | 159.35 |
| ch_PP-OCRv5_rec_server_infer.onnx | ch_PP-OCRv5_rec_server_sm80_fp32.engine | NVIDIA A800-SXM4-80GB | 69.82 |

## 支持Det模型

### 比较转化前后推理精度差异

这里主要采用 [@LocNgoXuan23](https://github.com/LocNgoXuan23) 给出的 [benchmark 脚本](https://github.com/RapidAI/RapidOCR/pull/623#issuecomment-3805793254) 来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNX Runtime"

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

    ```python linenums="1" hl_lines="10"
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

    ```python linenums="1" hl_lines="10"
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
    1. 其他版本的模型，我这里就直接给出对比结果了。因为教程都是一样的，仅换了一个模型而已。
    2. 下面指标仅作为转换前后，比较模型精度差异使用哈！
    3. TensorRT FP32 和 FP16 精度对比。
    ```

| Exp | 模型                          | 推理框架  | 推理引擎       | 硬件                        | Precision↑ | Recall↑ | H-mean↑ | Elapse↓ |
|:---:|:-----------------------------|:----------|:---------------|:----------------------------|:----------:|:-------:|:-------:|:-------:|
| 1   | ch_PP-OCRv4_det_infer        | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8595     | 0.8434  | 0.8514  | 1.0932   |
| 2   | ch_PP-OCRv4_det_infer        | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8677     | 0.8396  | 0.8534  | 0.0402  |
| 3   | ch_PP-OCRv4_det_infer        | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8667     | 0.8396  | 0.8529  | 0.0406  |
|     |                              |           |                |                             |            |         |         |         |
| 4   | ch_PP-OCRv4_det_infer        | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8595     | 0.8434  | 0.8514  | 0.1044  |
| 5   | ch_PP-OCRv4_det_infer        | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8685     | 0.8403  | 0.8542  | 0.0288  |
| 6   | ch_PP-OCRv4_det_infer        | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8677     | 0.8396  | 0.8534  | 0.0266  |
|     |                              |           |                |                             |            |         |         |         |
| 7   | ch_PP-OCRv5_mobile_det       | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.7858     | 0.8266  | 0.8057  | 1.1108  |
| 8   | ch_PP-OCRv5_mobile_det       | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.7938     | 0.8220  | 0.8077  | 0.0402  |
| 9   | ch_PP-OCRv5_mobile_det       | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.7943     | 0.8216  | 0.8077  | 0.0415  |
|     |                              |           |                |                             |            |         |         |         |
| 10  | ch_PP-OCRv5_mobile_det       | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.7858     | 0.8266  | 0.8057  | 0.1296  |
| 11  | ch_PP-OCRv5_mobile_det       | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.7938     | 0.8220  | 0.8077  | 0.0341  |
| 12  | ch_PP-OCRv5_mobile_det       | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.7950     | 0.8220  | 0.8083  | 0.0333  |
|     |                              |           |                |                             |            |         |         |         |
| 13  | ch_PP-OCRv4_det_server_infer | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.7710     | 0.8579  | 0.8121  | 5.4996  |
| 14  | ch_PP-OCRv4_det_server_infer | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.7811     | 0.8545  | 0.8161  | 0.0579  |
| **15** | **ch_PP-OCRv4_det_server_infer** | **RapidOCR** | **TensorRT FP16** | **NVIDIA A800-SXM4-80GB** | **0.3689** | **0.0516** | **0.0905** | **0.0415** |
|     |                              |           |                |                             |            |         |         |         |
| 16  | ch_PP-OCRv4_det_server_infer | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.7710     | 0.8579  | 0.8121  | 7.2283  |
| 17  | ch_PP-OCRv4_det_server_infer | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.7805     | 0.8545  | 0.8158  | 0.1167  |
| **18**  | **ch_PP-OCRv4_det_server_infer** | **RapidOCR**  | **TensorRT FP16**  | **NVIDIA GeForce RTX 3060**     | **0.3757**     | **0.0519**  | **0.0913**  | **0.0184**  |
|     |                              |           |                |                             |            |         |         |         |
| 19  | en_PP-OCRv3_det_infer        | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8066     | 0.8380  | 0.8220  | 0.7376  |
| 20  | en_PP-OCRv3_det_infer        | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8153     | 0.8346  | 0.8248  | 0.04    |
| 21  | en_PP-OCRv3_det_infer        | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8147     | 0.8346  | 0.8245  | 0.0384  |
|     |                              |           |                |                             |            |         |         |         |
| 22  | en_PP-OCRv3_det_infer        | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8066     | 0.8380  | 0.8220  | 0.0839  |
| 23  | en_PP-OCRv3_det_infer        | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8144     | 0.8346  | 0.8244  | 0.0283  |
| 24  | en_PP-OCRv3_det_infer        | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8144     | 0.8346  | 0.8244  | 0.0269  |
|     |                              |           |                |                             |            |         |         |         |
| 25  | Multilingual_PP-OCRv3_det_infer | RapidOCR | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.4228     | 0.6921  | 0.5249  | 0.7334  |
| 26  | Multilingual_PP-OCRv3_det_infer | RapidOCR | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.4223     | 0.6906  | 0.5241  | 0.0452  |
| 27  | Multilingual_PP-OCRv3_det_infer | RapidOCR | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.4221     | 0.6906  | 0.5240  | 0.0447  |
|     |                              |           |                |                             |            |         |         |         |
| 28  | Multilingual_PP-OCRv3_det_infer | RapidOCR | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.4161     | 0.6841  | 0.5175  | 0.1638  |
| 29  | Multilingual_PP-OCRv3_det_infer | RapidOCR | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.4223     | 0.6906  | 0.5241  | 0.0348  |
| 30  | Multilingual_PP-OCRv3_det_infer | RapidOCR | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.4220     | 0.6906  | 0.5239  | 0.0329  |
|     |                              |           |                |                             |            |         |         |         |
| 31  | ch_PP-OCRv5_server_det       | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.7394     | 0.8442  | 0.7883  | 4.7435  |
| 32 | ch_PP-OCRv5_server_det        | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | -          |   -     |  -      |  -  |
| 33  | ch_PP-OCRv5_server_det       | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.4143     | 0.2059  | 0.2751  | 0.0387  |
|     |                              |           |                |                             |            |         |         |         |
| 34  | ch_PP-OCRv5_server_det       | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.7394     | 0.8442  | 0.7883  | 5.7514  |
| 35  | ch_PP-OCRv5_server_det       | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.7503     | 0.8411  | 0.7931  | 0.0976  |
| 36  | ch_PP-OCRv5_server_det       | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.4163     | 0.2070  | 0.2765  | 0.0453  |

在 Exp 15 和 Exp 18 中， 模型转为 TensorRT FP16 `.engine` 格式后，各项指标均有大幅度下降，原因暂未查明，小伙伴们使用时注意。

在 Exp 32 中，我在当前设备上尝试构建对应的 TensorRT `.engine` 模型时未能成功，问题目前尚未解决。具体的错误日志如下：

```bash linenums="1" hl_lines="6"
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

这里主要采用[@LocNgoXuan23](https://github.com/LocNgoXuan23)给出的 [benchmark 脚本](https://github.com/RapidAI/RapidOCR/pull/623#issuecomment-3805793254)来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNX Runtime"

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

    ```python linenums="1" hl_lines="12"
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

    ```python linenums="1" hl_lines="12"
    # Step 1: 获得推理结果
    import time

    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangRec, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "EngineConfig.tensorrt.use_fp16": False,  # 默认为FP32
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

!!! tip

    ```markdwon
    1. 仅测试了中文相关的识别模型，其他语言的模型，因为没有对应评测集，就不测试指标了。
    2. 下面指标仅作为转换前后，比较模型精度差异使用哈！
    3. TensorRT 下的耗时是GPU的，ONNX Runtime 是 CPU 的。
    ```

| Exp | 模型                              | 推理框架  | 推理引擎       | 硬件                        | ExactMatch↑ | CharMatch↑ | Elapse↓ |
|:---:|:---------------------------------|:----------|:---------------|:----------------------------|:-----------:|:----------:|:-------:|
| 1   | ch_PP-OCRv4_rec_infer            | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8290      | 0.9432     | 0.1243  |
| 2   | ch_PP-OCRv4_rec_infer            | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8290      | 0.9432     | 0.0022  |
| 3   | ch_PP-OCRv4_rec_infer            | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8290      | 0.9430     | 0.0023  |
|     |                                  |           |                |                             |             |            |         |
| 4   | ch_PP-OCRv4_rec_infer            | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8290      | 0.9432     | 0.0081  |
| 5   | ch_PP-OCRv4_rec_infer            | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8290      | 0.9432     | 0.0019  |
| 6   | ch_PP-OCRv4_rec_infer            | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8290      | 0.9428     | 0.0015  |
|     |                                  |           |                |                             |             |            |         |
| 7   | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8065      | 0.9375     | 3.3677  |
| 8   | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8065      | 0.9376     | 0.0047  |
| 9   | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8097      | 0.9376     | 0.0025  |
|     |                                  |           |                |                             |             |            |         |
| 10  | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8065      | 0.9375     | 4.9997  |
| 11  | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8065      | 0.9375     | 0.0063  |
| 12  | ch_PP-OCRv4_rec_server_infer     | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8097      | 0.9376     | 0.0028  |
|     |                                  |           |                |                             |             |            |         |
| 13  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8097      | 0.9444     | 3.3989  |
| 14  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8097      | 0.9444     | 0.0051  |
| 15  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8097      | 0.9444     | 0.0028  |
|     |                                  |           |                |                             |             |            |         |
| 16  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8097      | 0.9444     | 5.2886  |
| 17  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8097      | 0.9444     | 0.0062  |
| 18  | ch_doc_PP-OCRv4_rec_server_infer | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8065      | 0.9439     | 0.0032  |
|     |                                  |           |                |                             |             |            |         |
| 19  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.7355      | 0.9177     | 0.1035  |
| 20  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.7355      | 0.9177     | 0.0039  |
| 21  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.7387      | 0.9193     | 0.0024  |
|     |                                  |           |                |                             |             |            |         |
| 22  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.7355      | 0.9177     | 0.0064  |
| 23  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.7355      | 0.9178     | 0.0035  |
| 24  | ch_PP-OCRv5_rec_mobile_infer     | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.7387      | 0.9191     | 0.0026  |
|     |                                  |           |                |                             |             |            |         |
| 25  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80GB       | 0.8129      | 0.9431     | 1.4705  |
| 26  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80GB       | 0.8161      | 0.9439     | 0.0049  |
| 27  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80GB       | 0.8129      | 0.9431     | 0.0039  |
|     |                                  |           |                |                             |             |            |         |
| 28  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060     | 0.8129      | 0.9431     | 1.2137  |
| 29  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     | 0.8129      | 0.9431     | 0.0051  |
| 30  | ch_PP-OCRv5_rec_server_infer     | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     | 0.8129      | 0.9431     | 0.0042  |

## 写在最后

从以上基准比较来看，ONNX 模型在转换为 TensorRT 对应的 `.engine` 模型后， FP32 精度下，检测和识别模型均在误差范围内，推理速度有量级的提升。如果追求极致的推理速度，欢迎试用。

值得一提的是，我这里仅测试了小批量的数据下效果，难免存在疏漏。更多全面测试，仍需要使用到的小伙伴多多反馈。

`rapidocr`将在 `>=v3.7.0` 集成，欢迎届时使用和反馈。
