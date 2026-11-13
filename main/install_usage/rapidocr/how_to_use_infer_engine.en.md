### Introduction

Starting from `rapidocr>=3.0.0`, `rapidocr` can individually specify different inference engines for text detection, text line orientation classification, and text recognition.

For example: text detection uses ONNX Runtime, and text recognition uses PaddlePaddle (`params={"Rec.engine_type": EngineType.PADDLE}`). At the same time, different versions of OCR can also be flexibly specified via `Det.ocr_version`.

`rapidocr` supports 6 inference engines (**ONNX Runtime / OpenVINO / PaddlePaddle / PyTorch / MNN (`rapidocr>=3.6.0`) / TensorRT (`rapidocr>=3.7.0`)**). It is recommended to use the **ONNX Runtime CPU** version first. The default is ONNX Runtime.

`rapidocr` selects which inference engine to use by specifying different parameters. Of course, the prerequisite for using different inference engines is that the corresponding inference engine library has been installed beforehand and installed correctly.

Before using different inference engines, please first confirm whether your current `rapidocr` version supports that inference engine. For details, see: [Model List](../../model_list.md)

### Using ONNX Runtime

1. Install ONNX Runtime. It is recommended to use the CPU version of ONNX Runtime; the GPU version is not recommended for use in `rapidocr`. For the relevant reasons, see: [ONNX Runtime GPU Inference](../../blog/posts/inference_engine/onnxruntime/onnxruntime-gpu.md).

    ```bash linenums="1"
    pip install onnxruntime
    ```

2. ONNX Runtime is the default inference engine and can be used without explicit specification.

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

            Only supported in `rapidocr>=3.1.0`. ONNX Runtime official documentation: [link](https://onnxruntime.ai/docs/execution-providers/community-maintained/CANN-ExecutionProvider.html)

        1. Installation

            ```bash linenums="1"
            pip install rapidocr onnxruntime-cann
            ```

        2. Usage

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

            DirectML can only be used on Windows 10 Build 18362 and above.
            ONNX Runtime official documentation: [link](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html)

        1. Installation

            ```bash linenums="1"
            pip install rapidocr onnxruntime-directml
            ```

        2. Usage

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

            Only **experimentally** supported in `rapidocr>=3.7.0`. ONNX Runtime official documentation: [CoreML Execution Provider](https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html). For a detailed Benchmark, see: [A Look at CoreML Provider vs. CPU Provider Performance in RapidOCR Based on ONNX Runtime](../../blog/posts/inference_engine/compare_coreml_cpu_provider_perf.md)

        1. Installation

            Starting from `onnxruntime>=1.16`, ONNX Runtime itself already supports the CoreML backend on macOS Apple Silicon (M1 / M2 / M3), so there is no need to install the `coreml` package separately.

            ```bash linenums="1"
            pip install onnxruntime
            ```

        2. Usage

            ```python linenums="1"
            from rapidocr import RapidOCR

            engine = RapidOCR(params={"EngineConfig.onnxruntime.use_coreml": True})

            img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
            result = engine(img_url)
            print(result)

            result.vis("vis_result.jpg")
            ```

3. Check the output log. If **Using engine_name: onnxruntime** is printed in the following log, it proves that the inference engine in use is ONNX Runtime.

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### Using OpenVINO

1. Install OpenVINO.

    ```bash linenums="1"
    pip install openvino
    ```

2. Specify OpenVINO as the inference engine.

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

3. Check the output log. If **Using engine_name: openvino** is printed in the following log, it proves that the inference engine in use is OpenVINO.

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: openvino
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
    ```

### Using MNN

!!! tip

    Supported in `rapidocr>=3.6.0`.

1. Install MNN

    ```bash linenums="1"
    pip install MNN
    ```

2. Specify MNN as the inference engine.

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

        Coming soon!

3. Check the output log. If **Using engine_name: mnn** is printed in the following log, it proves that the inference engine in use is MNN.

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.mnn
    [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.mnn
    [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: mnn
    [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.mnn
    ```

### Using PaddlePaddle

1. Install PaddlePaddle.

    See the official PaddlePaddle installation documentation → [Quick Install](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

    You can choose the version you need to install according to your actual situation.

2. Specify PaddlePaddle as the inference engine.

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
            "EngineConfig.paddle.use_cuda": True,  # Use the PaddlePaddle GPU version for inference
            "EngineConfig.paddle.cuda_ep_cfg.device_id": 0,  # Specify the GPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "NPU"

        !!! tip

            Only supported in `rapidocr>=3.3.0`. PaddlePaddle installation documentation for the corresponding version: [link](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

        ```python linenums="1" hl_lines="3-9"
        from rapidocr import EngineType, RapidOCR

        engine = RapidOCR(
            params={
            "Det.engine_type": EngineType.PADDLE,
            "EngineConfig.paddle.use_npu": True,  # Use the PaddlePaddle NPU version for inference
            "EngineConfig.paddle.npu_ep_cfg.device_id": 0,  # Specify the NPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

3. Check the output log. If **Using engine_name: paddle** is printed in the following log, it proves that the inference engine in use is PaddlePaddle.

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

### Using PyTorch

1. Install PyTorch.

    Refer to the official PyTorch installation documentation → [Install PyTorch](https://pytorch.org/#:~:text=and%20easy%20scaling.-,INSTALL%20PYTORCH,-Select%20your%20preferences).

    You can choose the version you need to install according to your actual situation.

2. Specify PyTorch as the inference engine.

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
                "EngineConfig.torch.use_cuda": True,  # Use the torch GPU version for inference
                "EngineConfig.torch.cuda_ep_cfg.device_id": 0,  # Specify the GPU id
            }
        )

        img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
        result = engine(img_url)
        print(result)

        result.vis('vis_result.jpg')
        ```

    === "NPU"

        !!! tip

            Only supported in `rapidocr>=3.4.2`. Official `torch_npu` documentation: [link](https://github.com/Ascend/pytorch)

        1. Install `torch_npu`; refer to: [docs](https://github.com/Ascend/pytorch#installation).

        2. Usage

            ```python linenums="1" hl_lines="3-11"
            from rapidocr import EngineType, RapidOCR

            engine = RapidOCR(
                params={
                    "Det.engine_type": EngineType.TORCH,
                    "Cls.engine_type": EngineType.TORCH,
                    "Rec.engine_type": EngineType.TORCH,
                    "EngineConfig.torch.use_npu": True,  # Use the torch NPU version for inference
                    "EngineConfig.torch.npu_ep_cfg.device_id": 0,  # Specify the NPU id
                }
            )

            img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
            result = engine(img_url)
            print(result)

            result.vis('vis_result.jpg')
            ```

    === "MPS"

        !!! tip

            Only supported in `rapidocr>=3.7.0`. For detailed benchmark data, see: [RapidOCR supports PyTorch MPS as a compute backend](../../blog/posts/inference_engine/support_torch_mps_backend.md)

        1. Install `torch`; refer to: [docs](https://pytorch.org/get-started/locally/?_gl=1*jbgtzm*_up*MQ..*_ga*NTU3NzM0NTIwLjE3NzI2MTY2NTU.*_ga_469Y0W5V62*czE3NzI2MTY2NTQkbzEkZzEkdDE3NzI2MTY2NjEkajUzJGwwJGgw). After installation, you can run the script below to determine whether the machine can use the Apple GPU:

            ```python linenums="1"
            import torch

            print(f"PyTorch version: {torch.__version__}")
            print(f"MPS available: {torch.backends.mps.is_available()}")

            if torch.backends.mps.is_available():
                device = torch.device("mps")
                print(f"✅ Successfully using the Apple GPU (MPS): {device}")
            else:
                print("❌ Please check your PyTorch installation; you may need to reinstall a build that supports MPS.")
            ```

            Output similar to the following indicates that the machine can use the Apple GPU:

            ```bash linenums="1"
            PyTorch version: 2.6.0
            MPS available: True
            ✅ Successfully using the Apple GPU (MPS): mps
            ```

        2. Usage

            ```python linenums="1" hl_lines="3-11"
            from rapidocr import EngineType, RapidOCR

            engine = RapidOCR(
                params={
                    "Det.engine_type": EngineType.TORCH,
                    "Cls.engine_type": EngineType.TORCH,
                    "Rec.engine_type": EngineType.TORCH,
                    "EngineConfig.torch.use_mps": True,  # Use the torch MPS version for inference
                }
            )

            img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
            result = engine(img_url)
            print(result)

            result.vis('vis_result.jpg')
            ```

3. Check the output log. If the following log prints **Using engine_name: torch**, it proves that the inference engine in use is PyTorch.

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in .../site-packages/rapidocr/models/ch_PP-OCRv4_det_infer.pth
    [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in .../site-packages/rapidocr/models/ch_ptocr_mobile_v2.0_cls_infer.pth
    [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: torch
    [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in .../site-packages/rapidocr/models/ch_PP-OCRv4_rec_infer.pth
    ```

### Using TensorRT

!!! tip

    Supported in `rapidocr>=3.7.0`. Related blog: [RapidOCR supports the TensorRT inference engine](../../blog/posts/inference_engine/support_tensorrt.md).

1. Install the TensorRT runtime environment.

    I only provide a reference configuration environment here:

    - Docker image: the image provided by [@LocNgoXuan23](https://github.com/LocNgoXuan23) in [Discord](https://discord.com/channels/1143707958690189373/1143707958690189376/1468529402118672512): [7.0-gc-triton-devel](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/deepstream?version=7.0-gc-triton-devel)
    - Device configuration: 8 CPU / 256 GB
    - NVIDIA environment: (for details, see: [link](https://gist.github.com/SWHL/0efe902ee469d49fc63d50e297d7fd98) )
        - cuda: 12.2
        - tensorrt: 8.6.1
        - cuda-python: 12.2.0

    You can choose the version you need to install according to your actual situation.

2. Specify TensorRT as the inference engine.

    Run the following code; the program will automatically download the corresponding ONNX models and convert them to `.engine` format. This conversion is only performed on the first run; therefore, the first run is slow, and subsequent runs will be significantly faster.

    For detailed model support, see the blog: [RapidOCR supports the TensorRT inference engine](https://rapidai.github.io/RapidOCRDocs/latest/blog/2026/02/13/support-tensorrt-engine/)

    ```python linenums="1" hl_lines="3-9"
    from rapidocr import EngineType, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TENSORRT,
            "Cls.engine_type": EngineType.TENSORRT,
            "Rec.engine_type": EngineType.TENSORRT,
            "EngineConfig.tensorrt.use_fp16": False,
            "EngineConfig.tensorrt.device_id": 0,  # Specify the GPU id
        }
    )

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)
    print(result)

    result.vis('vis_result.jpg')
    ```

3. Check the output log. If the following log prints **Using engine_name: tensorrt**, it proves that the inference engine in use is PyTorch.

    ```bash linenums="1" hl_lines="1 3 5"
    [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_mobile_sm80_fp32.engine
    [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_ptocr_mobile_v2.0_cls_sm80_fp32.engine
    [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: tensorrt
    [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in /Users/SWHL/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_mobile_sm80_fp32.engine
    ```
