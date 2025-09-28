---
comments: true
hide:
  - toc
---

## 如何使用不同推理引擎？

`rapidocr`支持4种推理引擎（**ONNXRuntime / OpenVINO / PaddlePaddle / PyTorch**），推荐首先使用 **ONNXRuntime CPU** 版。默认为ONNXRuntime。

`rapidocr`是通过指定不同参数来选择使用不同的推理引擎的。当然，使用不同推理引擎的前提是事先安装好对应的推理引擎库，并确保安装正确。

!!! info

    `rapidocr>=3.0.0`版本，可以单独为文本检测、文本行方向分类和文本识别单独指定不同的推理引擎。例如：文本检测使用ONNXRuntime，文本识别使用Paddle（`params={"Rec.engine_type": EngineType.PADDLE}`）。同时，不同版本的OCR也可以通过`Det.ocr_version`灵活指定。

### 使用ONNXRuntime

1. 安装ONNXRuntime。推荐用CPU版的ONNXRuntime，GPU版不推荐在`rapidocr`中使用，相关原因参见：[ONNXRuntime GPU推理](../../blog/posts/inference_engine/onnxruntime/onnxruntime-gpu.md)

    ```bash linenums="1"
    pip install onnxruntime
    ```

2. ONNXRuntime作为默认推理引擎，无需显式指定即可使用。

    ```python linenums="1"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了**Using engine_name: onnxruntime**，则证明使用的推理引擎是ONNXRuntime。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### 使用OpenVINO

1. 安装OpenVINO

    ```bash linenums="1"
    pip install openvino
    ```

2. 指定OpenVINO作为推理引擎

    ```python linenums="1" hl_lines="5-7"
    from rapidocr import RapidOCR, EngineType

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.OPENVINO,
            "Cls.engine_type": EngineType.OPENVINO,
            "Rec.engine_type": EngineType.OPENVINO,
        }
    )

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了**Using engine_name: openvino**，则证明使用的推理引擎是OpenVINO。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### 使用PaddlePaddle

1. 安装PaddlePaddle。

    参见PaddlePaddle官方安装文档 → [快速安装](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

    大家可以根据实际情况，选择安装CPU版、GPU版。

2. 指定PaddlePaddle作为推理引擎

    CPU版

    ```python linenums="1" hl_lines="5-7"
    from rapidocr import EngineType, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.PADDLE,
            "Cls.engine_type": EngineType.PADDLE,
            "Rec.engine_type": EngineType.PADDLE,
        }
    )

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

    GPU版

    ```python linenums="1" hl_lines="3-9"
    from rapidocr import EngineType, RapidOCR

    engine = RapidOCR(
        params={
        "Det.engine_type": EngineType.PADDLE,
        "EngineConfig.paddle.use_cuda": True,  # 使用PaddlePaddle GPU版推理
        "EngineConfig.paddle.gpu_id": 0,  # 指定GPU id
        }
    )

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了**Using engine_name: paddle**，则证明使用的推理引擎是PaddlePaddle。

    ```bash linenums="1" hl_lines="3 6"
    [INFO] 2025-03-22 15:20:45,528 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,529 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdiparams
    [INFO] 2025-03-22 15:20:45,746 base.py:30: Using engine_name: paddle
    [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdiparams
    [INFO] 2025-03-22 15:20:45,903 base.py:30: Using engine_name: paddle
    [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdiparams
    ```

### 使用PyTorch

1. 安装PyTorch。

    参见PyTorch官方安装文档 → [Install PyTorch](https://pytorch.org/#:~:text=and%20easy%20scaling.-,INSTALL%20PYTORCH,-Select%20your%20preferences)

    大家可以根据实际情况，选择安装CPU版、GPU版。

2. 指定PyTorch作为推理引擎

    CPU版

    ```python linenums="1" hl_lines="3"
    from rapidocr import RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TORCH,
            "Cls.engine_type": EngineType.TORCH,
            "Rec.engine_type": EngineType.TORCH,
        }
    )

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

    GPU版

    ```python linenums="1" hl_lines="3-9"
    from rapidocr import EngineType, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TORCH,
            "Cls.engine_type": EngineType.TORCH,
            "Rec.engine_type": EngineType.TORCH,
            "EngineConfig.torch.use_cuda": True,  # 使用torch GPU版推理
            "EngineConfig.torch.gpu_id": 0,  # 指定GPU id
        }
    )

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了**Using engine_name: torch**，则证明使用的推理引擎是PyTorch。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.pth
    [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ptocr_mobile_v2.0_cls_infer.pth
    [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.pth
    ```
