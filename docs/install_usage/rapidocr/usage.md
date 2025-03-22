---
comments: true
hide:
  - toc
---

#### 引言

该部分涉及如何使用`rapidocr`库来进行图像文字识别工作。

#### 最简单的使用

一切都使用默认值。默认使用来自PP-OCRv4的DBNet中文轻量检测，来自PP-OCRv4的SVTR_LCNet中文识别模型。默认使用ONNXRuntime CPU版作为推理引擎。

其他默认值的详细参数设置参见：[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/config.yaml)

```python linenums="1"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis()
```

#### 初始化RapidOCR实例输入

输入支持传入YAML格式的配置文件，同时支持参数直接传入使用。

=== "方法一：传入配置文件"

    1. 生成**default_rapidocr.yaml**的配置文件。终端执行以下代码，即可在当前目录下生成默认的**default_rapidocr.yaml**文件。

         ```bash linenums="1"
         $ rapidocr config
         # The config file has saved in ./default_rapidocr.yaml
         ```

    2. 根据自己的需要更改**default_rapidocr.yaml**相应的值。例如使用OpenVINO作为推理引擎，更改如下：

         ```yaml linenums="1"
         # 该配置文件命名为1.yaml
         Global:
            lang_det: "ch_mobile" # ch_server
            lang_rec: "ch_mobile"
            text_score: 0.5

            use_det: true
            use_cls: true
            use_rec: true

            min_height: 30
            width_height_ratio: 8
            max_side_len: 2000
            min_side_len: 30

            return_word_box: false

            with_onnx: false
            with_openvino: true   # 更改这里为true
            with_paddle: false
            with_torch: false

            font_path: null
         ```

    3. 传入到`RapidOCR`中使用。

         ```python linenums="1"
         from rapidocr import RapidOCR

         # 步骤2中的1.yaml
         config_path = "1.yaml"
         engine = RapidOCR(config_path=config_path)

         img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
         result = engine(img_url)
         print(result)

         result.vis()
         ```

=== "方法二：直接传入相应参数"

    由于rapidocr中涉及可调节的参数众多，为了便于维护，引入[omageconf](https://github.com/omry/omegaconf)库来更新参数。这样带来的代价是传入参数没有1.x系列中直观一些。但是现阶段方式也容易理解和使用。

    例如，我想使用OpenVINO作为推理引擎，可以通过下面这种方式使用：

    ```python linenums="1"
    from rapidocr import RapidOCR

    engine = RapidOCR(params={"Global.with_openvino": True})

    img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
    result = engine(img_url)
    print(result)

    result.vis()
    ```

    其他参数传入方式，基本就是参考`config.yaml`，关键字之间用点分割，直接写就可以了。例如：

    `config.yaml`部分参数示例：

    ```yaml linenums="1"
    Global:
       with_torch: true

    EngineConfig:
       torch:
          use_cuda: true
          gpu_id: 0
    ```

    **对应参数写法**

    ```python linenums="1"
    engine = RapidOCR(
       params={
          "Global.with_torch": True,
          "EngineConfig.torch.use_cuda": True,  # 使用torch GPU版推理
          "EngineConfig.torch.gpu_id": 0,  # 指定GPU id
       }
    )
    ```

#### 输出

RapidOCR输出包括4种类型：`Union[TextDetOutput, TextClsOutput, TextRecOutput, RapidOCROutput]`。这4种类型均是Dataclasses类，可以直接访问对应的键值。

#### 选择不同推理引擎

`rapidocr`支持4种推理引擎（**ONNXRuntime / OpenVINO / PaddlePaddle / PyTorch**），默认使用**ONNXRuntime CPU**版。

`rapidocr`是通过指定不同参数来选择使用不同的推理引擎的。当然，使用不同推理引擎的前提是事先安装好对应的推理引擎库，并确保安装正确。

=== "使用ONNXRuntime"

    CPU版在安装`rapidocr`时，已经自动安装好了，无需配置，可直接使用。

    GPU版不推荐在`rapidocr`中使用，相关原因参见：[ONNXRuntime GPU推理](../../blog/posts/inference_engine/onnxruntime/onnxruntime-gpu.md)

=== "使用OpenVINO"

    1. 安装OpenVINO

         ```bash linenums="1"
         pip install openvino
         ```

    2. 指定OpenVINO作为推理引擎

         ```python linenums="1"
         from rapidocr import RapidOCR

         engine = RapidOCR(params={"Global.with_openvino": True})

         img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/ test_files/ch_en_num.jpg?raw=true"
         result = engine(img_url)
         print(result)

         result.vis()
         ```

    3. 查看输出日志。下面日志中打印出了**Using engine_name: openvino**，则证明使用的推理引擎是OpenVINO。

         ```bash linenums="1"
         [INFO] 2025-03-21 09:28:03,457 base.py:30: Using engine_name: openvino
         [INFO] 2025-03-21 09:28:03,553 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
         [INFO] 2025-03-21 09:28:03,767 base.py:30: Using engine_name: openvino
         [INFO] 2025-03-21 09:28:03,768 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
         [INFO] 2025-03-21 09:28:03,861 base.py:30: Using engine_name: openvino
         [INFO] 2025-03-21 09:28:03,862 utils.py:35: File already exists in /Users/joshuawang/projects/_self/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx
         ```

=== "使用PaddlePaddle"

    1. 安装PaddlePaddle。

         参见PaddlePaddle官方安装文档 → [快速安装](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

         大家可以根据实际情况，选择安装CPU版、GPU版。

    2. 指定PaddlePaddle作为推理引擎

         ```python linenums="1"
         from rapidocr import RapidOCR

         # CPU版直接使用
         engine = RapidOCR(params={"Global.with_paddle": True})

         # GPU版，指定GPU id
         engine = RapidOCR(
            params={
               "Global.with_paddle": True,
               "EngineConfig.paddlepaddle.use_cuda": True,  # 使用torch GPU版推理
               "EngineConfig.paddlepaddle.gpu_id": 0,  # 指定GPU id
            }
         )

         img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/ test_files/ch_en_num.jpg?raw=true"
         result = engine(img_url)
         print(result)

         result.vis()
         ```

    3. 查看输出日志。下面日志中打印出了**Using engine_name: paddlepaddle**，则证明使用的推理引擎是PaddlePaddle。

         ```bash linenums="1"
         [INFO] 2025-03-22 15:20:45,528 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,529 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdiparams
         [INFO] 2025-03-22 15:20:45,746 base.py:30: Using engine_name: paddlepaddle
         [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdiparams
         [INFO] 2025-03-22 15:20:45,903 base.py:30: Using engine_name: paddlepaddle
         [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdiparams
         ```

=== "使用PyTorch"

    1. 安装PyTorch。

         参见PyTorch官方安装文档 → [Install PyTorch](https://pytorch.org/#:~:text=and%20easy%20scaling.-,INSTALL%20PYTORCH,-Select%20your%20preferences)

         大家可以根据实际情况，选择安装CPU版、GPU版。

    2. 指定PyTorch作为推理引擎

         ```python linenums="1"
         from rapidocr import RapidOCR

         # CPU版直接使用
         engine = RapidOCR(params={"Global.with_torch": True})

         # GPU版，指定GPU id
         engine = RapidOCR(
            params={
               "Global.with_torch": True,
               "EngineConfig.torch.use_cuda": True,  # 使用torch GPU版推理
               "EngineConfig.torch.gpu_id": 0,  # 指定GPU id
            }
         )

         img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/ test_files/ch_en_num.jpg?raw=true"
         result = engine(img_url)
         print(result)

         result.vis()
         ```

    3. 查看输出日志。下面日志中打印出了**Using engine_name: paddlepaddle**，则证明使用的推理引擎是PaddlePaddle。

         ```bash linenums="1"
         [INFO] 2025-03-22 15:20:45,528 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,529 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer/inference.pdiparams
         [INFO] 2025-03-22 15:20:45,746 base.py:30: Using engine_name: paddlepaddle
         [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,746 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ppocr_mobile_v2_cls_infer/inference.pdiparams
         [INFO] 2025-03-22 15:20:45,903 base.py:30: Using engine_name: paddlepaddle
         [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdmodel
         [INFO] 2025-03-22 15:20:45,904 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer/inference.pdiparams
         ```

#### 使用默认mobiel或server模型


#### 选择自定义的模型推理
