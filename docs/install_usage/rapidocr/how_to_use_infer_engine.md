---
comments: true
# hide:
#   - toc
---

### 引言

在 `rapidocr>=3.0.0` 版本之后，`rapidocr` 可以单独为文本检测、文本行方向分类和文本识别单独指定不同的推理引擎。

例如：文本检测使用 ONNX Runtime，文本识别使用PaddlePaddle（`params={"Rec.engine_type": EngineType.PADDLE}`）。同时，不同版本的OCR也可以通过 `Det.ocr_version` 灵活指定。

`rapidocr` 支持 5 种推理引擎（**ONNX Runtime / OpenVINO / PaddlePaddle / PyTorch / MNN (`rapidocr>=3.6.0`)**），推荐首先使用 **ONNX Runtime CPU** 版。默认为 ONNX Runtime。

`rapidocr` 是通过指定不同参数来选择使用不同的推理引擎的。当然，使用不同推理引擎的前提是事先安装好对应的推理引擎库，并确保安装正确。

### 使用 ONNX Runtime

1. 安装 ONNX Runtime。推荐用 CPU 版的 ONNX Runtime，GPU 版不推荐在 `rapidocr` 中使用，相关原因参见：[ONNX Runtime GPU 推理](../../blog/posts/inference_engine/onnxruntime/onnxruntime-gpu.md)。

    ```bash linenums="1"
    pip install onnxruntime
    ```

2. ONNX Runtime 作为默认推理引擎，无需显式指定即可使用。

    === "CPU"

        ```python linenums="1"
        from rapidocr import RapidOCR

        engine = RapidOCR()

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "NPU"

        !!! tip

            仅在 `rapidocr>=3.1.0` 中支持。ONNX Runtime 官方相关文档：[link](https://onnxruntime.ai/docs/execution-providers/community-maintained/CANN-ExecutionProvider.html)

        1. 安装

            ```bash linenums="1"
            pip install rapidocr onnxruntime-cann
            ```

        2. 使用

            ```python linenums="1"
            from rapidocr import RapidOCR

            engine = RapidOCR(params={"EngineConfig.onnxruntime.use_cann": True})

            img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
            result = engine(img_url)
            print(result)

            result.vis("vis_result.jpg")
            ```

    === "DirectML"

        !!! tip

            DirectML 仅能 Windows 10 Build 18362 及以上使用。
            ONNX Runtime 官方相关文档：[link](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html)

        1. 安装

            ```bash linenums="1"
            pip install rapidocr onnxruntime-directml
            ```

        2. 使用

            ```python linenums="1"
            from rapidocr import RapidOCR

            engine = RapidOCR(params={"EngineConfig.onnxruntime.use_dml": True})

            img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
            result = engine(img_url)
            print(result)

            result.vis("vis_result.jpg")
            ```

    === ":material-flask: CoreML"

        !!! warning

            仅在 `rapidocr>=3.7.0` 中 **实验性** 支持。ONNX Runtime 官方相关文档：[CoreML Execution Provider](https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html)。详细 Benchmark 参见：[基于 ONNX Runtime 来看 CoreML Provider 和 CPU Provider 在 RapidOCR 表现](../../blog/posts/inference_engine/compare_coreml_cpu_provider_perf.md)

        1. 安装

            从 `onnxruntime>=1.16` 开始， ONNX Runtime 本身已支持 macOS Apple Silicon（M1/M2/M3）的 CoreML 后端，无需额外安装 `coreml` 包。

            ```bash linenums="1"
            pip install onnxruntime
            ```

        2. 使用

            ```python linenums="1"
            from rapidocr import RapidOCR

            engine = RapidOCR(params={"EngineConfig.onnxruntime.use_coreml": True})

            img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
            result = engine(img_url)
            print(result)

            result.vis("vis_result.jpg")
            ```

3. 查看输出日志。下面日志中打印出了 **Using engine_name: onnxruntime**，则证明使用的推理引擎是 ONNX Runtime。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### 使用 OpenVINO

1. 安装 OpenVINO。

    ```bash linenums="1"
    pip install openvino
    ```

2. 指定 OpenVINO 作为推理引擎。

    ```python linenums="1" hl_lines="5-7"
    from rapidocr import RapidOCR, EngineType

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.OPENVINO,
            "Cls.engine_type": EngineType.OPENVINO,
            "Rec.engine_type": EngineType.OPENVINO,
        }
    )

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了 **Using engine_name: openvino**，则证明使用的推理引擎是 OpenVINO。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### 使用 MNN

!!! tip

    `rapidocr>=3.6.0`支持。

1. 安装 MNN

    ```bash linenums="1"
    pip install MNN
    ```

2. 指定 MNN 作为推理引擎。

    === "CPU"

        ```python linenums="1" hl_lines="5-7"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
                "Det.engine_type": EngineType.MNN,
                "Cls.engine_type": EngineType.MNN,
                "Rec.engine_type": EngineType.MNN,
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "GPU"

        敬请期待！

3. 查看输出日志。下面日志中打印出了 **Using engine_name: mnn**，则证明使用的推理引擎是 MNN。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.mnn
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.mnn
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.mnn
    ```

### 使用 PaddlePaddle

1. 安装 PaddlePaddle。

    参见 PaddlePaddle 官方安装文档 → [快速安装](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

    大家可以根据实际情况，选择安装需要的版本。

2. 指定 PaddlePaddle 作为推理引擎。

    === "CPU"

        ```python linenums="1" hl_lines="5-7"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
                "Det.engine_type": EngineType.PADDLE,
                "Cls.engine_type": EngineType.PADDLE,
                "Rec.engine_type": EngineType.PADDLE,
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "GPU"

        ```python linenums="1" hl_lines="3-9"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
            "Det.engine_type": EngineType.PADDLE,
            "EngineConfig.paddle.use_cuda": True,  # 使用PaddlePaddle GPU版推理
            "EngineConfig.paddle.cuda_ep_cfg.device_id": 0,  # 指定GPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "NPU"

        !!! tip

            仅在`rapidocr>=3.3.0`中支持。对应版本的PaddlePaddle安装文档：[link](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

        ```python linenums="1" hl_lines="3-9"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
            "Det.engine_type": EngineType.PADDLE,
            "EngineConfig.paddle.use_npu": True,  # 使用PaddlePaddle NPU版推理
            "EngineConfig.paddle.npu_ep_cfg.device_id": 0,  # 指定NPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

3. 查看输出日志。下面日志中打印出了 **Using engine_name: paddle**，则证明使用的推理引擎是 PaddlePaddle。

    ```bash linenums="1" hl_lines="3 6"
    [INFO] 2025-03-22 15:20:45,528 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,529 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdiparams
    [INFO] 2025-03-22 15:20:45,746 base.py:30: Using engine_name: paddle
    [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdiparams
    [INFO] 2025-03-22 15:20:45,903 base.py:30: Using engine_name: paddle
    [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdmodel
    [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdiparams
    ```

### 使用 PyTorch

1. 安装 PyTorch。

    参见 PyTorch 官方安装文档 → [Install PyTorch](https://pytorch.org/#:~:text=and%20easy%20scaling.-,INSTALL%20PYTORCH,-Select%20your%20preferences)。

    大家可以根据实际情况，选择安装需要的版本。

2. 指定 PyTorch 作为推理引擎。

    === "CPU"

        ```python linenums="1" hl_lines="3"
        from rapidocr import RapidOCR

        engine = RapidOCR(
            params={
                "Det.engine_type": EngineType.TORCH,
                "Cls.engine_type": EngineType.TORCH,
                "Rec.engine_type": EngineType.TORCH,
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "GPU"

        ```python linenums="1" hl_lines="3-9"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
                "Det.engine_type": EngineType.TORCH,
                "Cls.engine_type": EngineType.TORCH,
                "Rec.engine_type": EngineType.TORCH,
                "EngineConfig.torch.use_cuda": True,  # 使用 torch GPU 版推理
                "EngineConfig.torch.cuda_ep_cfg.device_id": 0,  # 指定GPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "NPU"

        !!! tip

            仅在 `rapidocr>=3.4.2` 中支持。`torch_npu` 官方相关文档：[link](https://github.com/Ascend/pytorch)

        1. 安装 `torch_npu`，参见：[docs](https://github.com/Ascend/pytorch#installation)。

        2. 使用

            ```python linenums="1" hl_lines="3-11"
            from rapidocr import EngineType, RapidOCR

            engine = RapidOCR(
                params={
                    "Det.engine_type": EngineType.TORCH,
                    "Cls.engine_type": EngineType.TORCH,
                    "Rec.engine_type": EngineType.TORCH,
                    "EngineConfig.torch.use_npu": True,  # 使用torch NPU版推理
                    "EngineConfig.torch.npu_ep_cfg.device_id": 0,  # 指定NPU id
                }
            )

            img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
            result = engine(img_url)
            print(result)

            result.vis('vis_result.jpg')
            ```

3. 查看输出日志。下面日志中打印出了 **Using engine_name: torch**，则证明使用的推理引擎是 PyTorch。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.pth
    [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_ptocr_mobile_v2.0_cls_infer.pth
    [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.pth
    ```

### 使用 TensorRT

1. 安装 TensorRT 运行环境。

    我在这里仅给出参考配置环境：

    - Docker镜像：[@LocNgoXuan23](https://github.com/LocNgoXuan23) 在 [Discord](https://discord.com/channels/1143707958690189373/1143707958690189376/1468529402118672512) 中给出的镜像：[7.0-gc-triton-devel](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream?version=7.0-gc-triton-devel)
    - 设备配置：8 CPU / 256 GB
    - NVIDIA环境：(详细参见：[link](https://gist.github.com/SWHL/0efe902ee469d49fc63d50e297d7fd98) )
        - cuda: 12.2
        - tensorrt: 8.6.1
        - cuda-python: 12.2.0

    大家可以根据实际情况，选择安装需要的版本。

2. 指定 TensorRT 作为推理引擎。

    运行下面代码，程序会自动现在对应的 ONNX 模型，并转换为 `.engine` 格式。该转换仅在首次运行时执行。因此，首次运行速度会较慢，后面再次运行就快了。

    详细模型的支持情况，请参见博客：[RapidOCR 支持 TensorRT 推理引擎](https://rapidai.github.io/RapidOCRDocs/latest/blog/2026/02/13/support-tensorrt-engine/)

    ```python linenums="1" hl_lines="3-9"
    from rapidocr import EngineType, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TENSORRT,
            "Cls.engine_type": EngineType.TENSORRT,
            "Rec.engine_type": EngineType.TENSORRT,
            "EngineConfig.tensorrt.use_fp16": False,
            "EngineConfig.tensorrt.device_id": 0,  # 指定GPU id
        }
    )

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. 查看输出日志。下面日志中打印出了 **Using engine_name: tensorrt**，则证明使用的推理引擎是 PyTorch。

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_mobile_sm80_fp32.engine
    [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_ptocr_mobile_v2.0_cls_sm80_fp32.engine
    [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_mobile_sm80_fp32.engine
    ```
