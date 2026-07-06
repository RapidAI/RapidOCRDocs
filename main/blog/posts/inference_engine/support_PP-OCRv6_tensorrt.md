<!-- more -->

## 引言

这篇博客基于 [RapidOCR 支持 TensorRT 推理引擎](https://rapidai.github.io/RapidOCRDocs/latest/blog/2026/02/13/support-tensorrt-engine/)，测试了 PP-OCRv6 模型的效果是否符合预期。

**因此，在实际使用中，用户首次指定 TensorRT 作为推理引擎时，程序会自动触发 `.engine` 文件的构建流程。这一过程的耗时取决于所用设备的性能——通常在桌面级或服务器级 GPU 上较快，在边缘设备（如 Jetson）上则可能稍长。**

## 运行环境¶

- Docker 镜像：[@LocNgoXuan23](https://github.com/LocNgoXuan23) 在 [Discord](https://discord.com/channels/1143707958690189373/1143707958690189376/1468529402118672512) 中给出的镜像：[7.0-gc-triton-devel](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream?version=7.0-gc-triton-devel)
- 设备配置：8 CPU / 256 GB
- NVIDIA 环境：(详细参见：[link](https://gist.github.com/SWHL/0efe902ee469d49fc63d50e297d7fd98) )
    - cuda: 12.2
    - tensorrt: 8.6.1
    - cuda-python: 12.2.0
- Python 环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.9.1
  text_det_metric==0.0.8
  text_rec_metric==0.0.1
  datasets==3.6.0
  onnxruntime==1.23.2
  ```

## 支持 Det 模型

### 比较转化前后推理精度差异

这里主要采用 [@LocNgoXuan23](https://github.com/LocNgoXuan23) 给出的 [benchmark 脚本](https://github.com/RapidAI/RapidOCR/pull/623#issuecomment-3805793254) 来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNX Runtime"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.model_type": ModelType.MEDIUM,
        "Det.ocr_version": OCRVersion.PPOCRV6,
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
        "Det.model_type": ModelType.MEDIUM,
        "Det.ocr_version": OCRVersion.PPOCRV6,
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
        "Det.model_type": ModelType.MEDIUM,
        "Det.ocr_version": OCRVersion.PPOCRV6,
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
| 1   | PP-OCRv6_det_medium        | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80 GB       |   0.8251   |  0.8598 | 0.8421  |  4.7016  |
| 2   | PP-OCRv6_det_medium         | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80 GB       |  0.8336    |  0.8571 |  0.8452 | 0.0645  |
| 3   | PP-OCRv6_det_medium         | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80 GB       |   0.8338  | 0.8568  | 0.8451  | 0.0563  |
|     |                              |           |                |                             |            |         |         |         |
| 4   | PP-OCRv6_det_small        | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060    |   0.854   | 0.8445  | 0.8492  |  1.128 |
| 5   | PP-OCRv6_det_small        | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     |    0.8579   |  0.8396 |  0.8486 | 0.0469  |
| 6   | PP-OCRv6_det_small        | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     |  0.8583    | 0.8396  |   0.8488 |  0.0457 |
|| || || |  | | |
| 7   | PP-OCRv6_det_tiny       | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80 GB       |   0.8241   | 0.8285  | 0.8263  | 0.5663  |
| 8   | PP-OCRv6_det_tiny       | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80 GB        |   0.8291   | 0.8247  |  0.8269 | 0.0504  |
| 9   | PP-OCRv6_det_tiny       | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80 GB        |  0.8301    |  0.8247 | 0.8274  |  0.0526 |

## 支持 Rec 模型

### 比较转化前后推理精度差异

这里主要采用 [@LocNgoXuan23](https://github.com/LocNgoXuan23) 给出的 [benchmark 脚本](https://github.com/RapidAI/RapidOCR/pull/623#issuecomment-3805793254) 来批量测试。下面是测试单个模型的脚本。

=== "(Exp1) RapidOCR + ONNX Runtime"

    ```python linenums="1"
    # Step 1: 获得推理结果
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import EngineType, LangRec, ModelType, OCRVersion, RapidOCR

    engine_config = {
        "Rec.engine_type": EngineType.ONNXRUNTIME,
        "Rec.lang_type": LangRec.CH,
        "Rec.model_type": ModelType.MEDIUM,
        "Rec.ocr_version": OCRVersion.PPOCRV6,
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
        "Rec.model_type": ModelType.MEDIUM,
        "Rec.ocr_version": OCRVersion.PPOCRV6,
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
        "Rec.model_type": ModelType.MEDIUM,
        "Rec.ocr_version": OCRVersion.PPOCRV6,
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
| 1   | PP-OCRv6_rec_medium            | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80 GB      |   0.8613    | 0.9491     |  0.4538 |
| 2   | PP-OCRv6_rec_medium            | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80 GB       |  0.8613     |      0.9497 |  0.0034 |
| 3   | PP-OCRv6_rec_medium            | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80 GB       |    0.8581   |   0.9494    | 0.0034  |
|     |                                  |           |                |                            |             |            |         |
| 4   | PP-OCRv6_rec_small            | RapidOCR  | ONNX Runtime    | NVIDIA GeForce RTX 3060    |  0.8419     |   0.9515   |  0.079 |
| 5   | PP-OCRv6_rec_small            | RapidOCR  | TensorRT FP32  | NVIDIA GeForce RTX 3060     |    0.8419   |  0.9516    | 0.0026  |
| 6   | PP-OCRv6_rec_small            | RapidOCR  | TensorRT FP16  | NVIDIA GeForce RTX 3060     |    0.8419   |   0.9515   |  0.0034 |
|     |             |           |                |                             |             |            |         |
| 7   | PP-OCRv6_rec_tiny     | RapidOCR  | ONNX Runtime    | NVIDIA A800-SXM4-80 GB      |    0.6968   |  0.8897    | 0.0316  |
| 8   | PP-OCRv6_rec_tiny     | RapidOCR  | TensorRT FP32  | NVIDIA A800-SXM4-80 GB       |     0.6968  | 0.8894     |  0.0015 |
| 9   | PP-OCRv6_rec_tiny     | RapidOCR  | TensorRT FP16  | NVIDIA A800-SXM4-80 GB       |    0.6935    |    0.8876  |  0.0021 |

## 写在最后

从以上基准比较来看，ONNX 模型在转换为 TensorRT 对应的 `.engine` 模型后，FP32 精度下，检测和识别模型均在误差范围内，推理速度有量级的提升。如果追求极致的推理速度，欢迎试用。

值得一提的是，我这里仅测试了小批量的数据下效果，难免存在疏漏。更多全面测试，仍需要使用到的小伙伴多多反馈。

`rapidocr` 将在 `>=v3.9.2` 集成，欢迎届时使用和反馈。
