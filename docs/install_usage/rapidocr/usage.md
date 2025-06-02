---
comments: true
hide:
  - toc
---

### 引言

该部分涉及如何使用`rapidocr`库来进行图像文字识别工作。

### 最简单的使用

一切都使用默认值。默认使用来自PP-OCRv4的DBNet中文轻量检测，来自PP-OCRv4的SVTR_LCNet中文识别模型。

推荐可以先使用ONNXRuntime CPU版作为推理引擎。

```bash linenums="1"
pip install onnxruntime
```

其他默认值的详细参数设置参见：[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/config.yaml)

```python linenums="1"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

### 初始化RapidOCR实例输入

输入支持传入YAML格式的配置文件，同时支持参数直接传入使用。

=== "方法一：传入配置文件"

    1. 生成 **default_rapidocr.yaml** 的配置文件。终端执行以下代码，即可在当前目录下生成默认的 **default_rapidocr.yaml** 文件。

        ```bash linenums="1"
        $ rapidocr config
        # The config file has saved in ./default_rapidocr.yaml
        ```

    2. 根据自己的需要更改 **default_rapidocr.yaml** 相应的值。例如使用OpenVINO作为作为文本检测的推理引擎，同时使用`ch_mobile`，PP-OCRv4版本的模型，更改如下：

        ```yaml linenums="1" hl_lines="3"
        # 该配置文件命名为1.yaml
        Det:
            # 以下4个值可以查看https://github.com/RapidAI/RapidOCR/blob/123a129c613ca99c3b007f0591a3587cc01a4c32/python/rapidocr/utils/typings.py来查看
            engine_type: 'openvino'
            lang_type: 'ch'
            model_type: 'mobile'
            ocr_version: 'PP-OCRv4'

            task_type: 'det'

            model_path: null
            model_dir: null

            limit_side_len: 736
            limit_type: min
            std: [ 0.5, 0.5, 0.5 ]
            mean: [ 0.5, 0.5, 0.5 ]

            thresh: 0.3
            box_thresh: 0.5
            max_candidates: 1000
            unclip_ratio: 1.6
            use_dilation: true
            score_mode: fast
        ```

    3. 传入到`RapidOCR`中使用。

        ```python linenums="1" hl_lines="4-5"
        from rapidocr import RapidOCR

        # 步骤2中的1.yaml
        config_path = "1.yaml"
        engine = RapidOCR(config_path=config_path)

        img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
        result = engine(img_url)
        print(result)

        result.vis("vis_result.jpg")
        ```

=== "方法二：直接传入相应参数"

    !!! tip

        `rapidocr>=3.0.0`版本之后，将`engine_type`、`lang_type`、`model_type`和`ocr_version`三个参数的设置下放到了文本检测、文本行方向分类和文本识别三个阶段中。这样更加灵活。可以为不同阶段中，指定不同的推理引擎， 不同的模型type。

    由于rapidocr中涉及可调节的参数众多，为了便于维护，引入[omageconf](https://github.com/omry/omegaconf)库来更新参数。这样带来的代价是传入参数没有1.x系列中直观一些。但是现阶段方式也容易理解和使用。

    例如，我想使用OpenVINO作为各个流程的推理引擎，可以通过下面这种方式使用：

    ```python linenums="1" hl_lines="5-7"
    from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.OPENVINO,
            "Cls.engine_type": EngineType.OPENVINO,
            "Rec.engine_type": EngineType.OPENVINO,
        }
    )

    img_url = "<https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true>"
    result = engine(img_url)
    print(result)

    result.vis("vis_result.jpg")
    ```

    其他参数传入方式，基本就是参考`config.yaml`，关键字之间用点分割，直接写就可以了。例如：

    `config.yaml`部分参数示例：

    ```yaml linenums="1"
    Det:
        engine_type: 'openvino'
        lang_type: 'ch'
        model_type: 'mobile'
        ocr_version: 'PP-OCRv4'

    EngineConfig:
       torch:
          use_cuda: true
          gpu_id: 0
    ```

    **对应参数写法**

    ```python linenums="1" hl_lines="5-10"
    from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TORCH,
            "Det.lang_type": LangDet.CH,
            "Det.model_type": ModelType.MOBILE,
            "Det.ocr_version": OCRVersion.PPOCRV5,
            "EngineConfig.torch.use_cuda": True,  # 使用torch GPU版推理
            "EngineConfig.torch.gpu_id": 0,  # 指定GPU id
        }
    )
    ```

### 输出

RapidOCR输出包括4种类型：`Union[TextDetOutput, TextClsOutput, TextRecOutput, RapidOCROutput]`。这4种类型均是Dataclasses类，可以直接访问对应的键值。

- `TextDetOutput`：仅有检测
- `TextClsOutput`: 仅有文本行方向分类
- `TextRecOutput`: 仅有识别
- `RapidOCROutput`: 检测+方向分类+识别

详细搭配如下：

=== "检测 + 分类 + 识别"

    ```python linenums="1" hl_lines="8"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/ch_en_num.jpg"

    # 默认都为True
    result = engine(img_url, use_det=True, use_cls=True, use_rec=True)
    print(result)
    result.vis("vis_det_cls_rec.jpg")
    ```

    ![](../../images/vis_det_cls_rec.jpg)

    返回值为`RapidOCROutput`，可以通过`result.xxxx`直接访问。主要包含以下字段：

    - `RapidOCROutput.img (np.ndarray)`: 传入的原始图像
    - `RapidOCROutput.boxes (np.ndarray)`: 图像中每行坐标框，shape为`(N, 4, 2)`。`N`表示有多少文本行。
    - `RapidOCROutput.txts (Tuple[str])`: 和`boxes`文本框对应识别到的文本内容。长度和`RapidOCROutput.boxes`长度一致。
    - `RapidOCROutput.scores (Tuple[float])`: 每行识别文本结果的置信度。长度和`RapidOCROutput.boxes`长度一致。
    - `RapidOCROutput.word_results (Tuple[Any])`: 该部分结果只有在`return_word_box=True`时，才会有值。
    - `RapidOCROutput.elapse_list (List[float])`: 文本检测，文本行方向分类和文本识别三部分各自推理耗时，单位为秒。
    - `RapidOCROutput.elapse (float)`: 三部分整体耗时，单位为秒。

    ??? example "详细返回值示例"

        ```python linenums="1"
        RapidOCROutput(img=array([[[120,   3,  52],
            [130,   0,  63],
            [155,   9,  91],
            ...,
            [188,  10, 129],
            [189,  11, 130],
            [189,  11, 130]],

            [122,   3,  54],
            [133,   1,  67],
            [157,  11,  93],
            ...,
            [187,  11, 135],
            [187,  11, 135],
            [186,  10, 134]],
            [218,   0, 114],
            [218,   0, 114],
            [218,   0, 114]]], dtype=uint8),
         boxes=array([[[  6.,   2.],
              [322.,   9.],
              [320., 104.],
              [  4.,  97.]],

              [ 70.,  98.],
              [252.,  98.],
              [252., 125.],
              [ 70., 125.]],

              [ 68., 144.],
              [256., 144.],
              [256., 165.],
              [ 68., 165.]],

              [108., 170.],
              [217., 170.],
              [217., 182.],
              [108., 182.]],], dtype=float32),
            txts=('正品促销', '大桶装更划算', '强力去污符合国标', '40°C深度防冻不结冰', '日常价￥', '真击', '10.0  起', '10.0起', '日常价￥', '底价', '5.8', '券后价￥', '起', '惊喜福利不容错过', '极速发货', '冰点标准', '破损就赔', '假一赔十'),
            scores=  (0.99893, 0.9843, 0.97842, 0.93412, 0.81418, 0.66226, 0.99243, 0.99849, 0.81369, 0.99633, 0.9999, 0.83907, 0.99993, 0.99782, 0.99813, 0.99786, 0.92679, 0.99717),
            word_results=(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),
            elapse_list=[0.14605145796667784, 0.017657041549682617, 0.4013413330540061],
            elapse=0.5650498325703666,
            lang_rec='ch_mobile')
        ```

=== "检测 + 识别"

    ???+ tip

        只有文本检测和文本识别的组合可以正常使用的前提是：确保传入图像中文字都是正的。

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/ch_en_num.jpg"
    result = engine(img_url, use_det=True, use_cls=False, use_rec=True)
    print(result)
    result.vis("vis_det_rec.jpg")
    ```

    ![](../../images/vis_det_rec.jpg)

    返回值类型同 **检测 + 分类 + 识别** 部分。

=== "分类 + 识别"

    ```python linenums="1" hl_lines="6"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=False, use_cls=True, use_rec=True)
    print(result)
    print(elapse)
    ```

    ![](../../images/vis_cls_rec.jpg)

    返回值为`TextClsOutput`类，主要包含以下字段：

    - `TextClsOutput.img_list (List[np.ndarray])`: 多个文本行图像组成的列表。
    - `TextClsOutput.cls_res (List[Tuple(str, float)])`: 每个文本行对应的方向及置信度。
    - `TextClsOutput.elapse (float)`: 识别耗时，单位为秒。

    ???+ example "详细返回值示例"

        ```python linenums="1"
        TextRecOutput(imgs=[array([[[123,  56,   1],
            [124,  55,   0],
            [131,  55,   0],
            ...,
            [137,  56,   5],
            [138,  57,   6],
            [139,  58,   7]],
            ...,
            [128,  54,   6],
            [127,  51,   2],
            [126,  50,   1]]], dtype=uint8)],
        txts=('韩国小馆',),
        scores=(0.99916,),
        word_results=(None,),
        elapse=0.024567584041506052,
        lang_rec='ch_mobile')
        ```

=== "只有检测"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/ch_en_num.jpg"
    result = engine(img_url, use_det=True, use_cls=False, use_rec=False)
    print(result)
    result.vis('vis_only_det.jpg')
    ```

    ![](../../images/vis_only_det.jpg)

    返回值为`TextDetOutput`类，主要包含以下字段：

    - `TextDetOutput.img (np.ndarray)`: 传入的原始图像
    - `TextDetOutput.boxes (np.ndarray)`: 文本行坐标，4个点组成，依次是`[左上，右上，右下，左下]`
    - `TextDetOutput.scores (List[float])`: 每个文本行对应的置信度。
    - `TextDetOutput.elapse (float): 文本检测整体耗时，单位为秒。

    ???+ example "详细返回值示例"

        ```python linenums="1"
        TextDetOutput(img=array([[[120,   3,  52],
            [130,   0,  63],
            [155,   9,  91],
            ...,
            [[122,   3,  54],
            [133,   1,  67],
            [157,  11,  93],
            ...,
            [187,  11, 135],
            [187,  11, 135],
            [186,  10, 134]]], dtype=uint8),
        boxes=array([[[  6.,   2.],
            [322.,   9.],
            [320., 104.],
            [  4.,  97.]],
            ...
            [[ 68., 391.],
            [151., 391.],
            [151., 413.],
            [ 68., 413.]],

            [[202., 391.],
            [287., 391.],
            [287., 413.],
            [202., 413.]]], dtype=float32),
        scores=[0.8829081288294226, 0.8744070886972952, 0.8937022144061125],
        elapse=0.15039170801173896)
        ```

=== "只有分类"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://raw.githubusercontent.com/RapidAI/RapidOCR/refs/heads/main/python/tests/test_files/text_rec.jpg"
    result = engine(img_url, use_det=False, use_cls=True, use_rec=False)
    print(result)
    result.vis("vis_only_cls.jpg")
    ```

    ![](../../images/vis_only_cls.jpg)

    返回值为`TextClsOutput`类，主要包含以下字段：

    - `TextClsOutput.img_list (List[np.ndarray])`: 多个文本行图像组成的列表。
    - `TextClsOutput.cls_res (List[Tuple(str, float)])`: 每个文本行对应的方向及置信度。
    - `TextClsOutput.elapse (float)`: 识别耗时，单位为秒。

    ???+ example "详细返回值示例"

        ```python linenums="1"
        TextClsOutput(img_list=[array([[[123,  56,   1],
                [124,  55,   0],
                [131,  55,   0],], dtype=uint8)],
        cls_res=[('0', 0.9998784)],
        elapse=0.004718780517578125)
        ```

=== "只有识别"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://raw.githubusercontent.com/RapidAI/RapidOCR/refs/heads/main/python/tests/test_files/text_rec.jpg"
    result = engine(img_url, use_det=False, use_cls=False, use_rec=True)
    print(result)
    result.vis("vis_only_rec.jpg")
    ```

    ![](../../images/vis_only_rec.jpg)

    返回值为`TextRecOutput`类，主要包含以下字段：

    - `TextRecOutput.imgs (List[np.ndarray])`: 多个文本行图像组成的列表。
    - `TextRecOutput.txts (List[Tuple(str, float)])`: 每个文本行对应的识别结果。
    - `TextRecOutput.scores (float)`: 每个文本行识别结果。
    - `TextRecOutput.word_results (Tuple[None])`: 仅在指定`return_word_box=True`时，有值。

    ???+ example "详细返回值示例"

        ```python linenums="1"
        TextRecOutput(imgs=[array([[[123,  56,   1],
                [124,  55,   0],
                [131,  55,   0],
                ...,
                [128,  54,   6],
                [127,  51,   2],
                [126,  50,   1]]], dtype=uint8)],
        txts=('韩国小馆',),
        scores=(0.99916,),
        word_results=(None,),
        elapse=0.024397416971623898,
        lang_rec='ch_mobile')
        ```

=== "返回单字坐标"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/ch_en_num.jpg"
    result = engine(img_url, return_word_box=True)
    print(result)
    result.vis("vis_return_words.jpg")
    ```

    ![](../../images/vis_sinlge_words.jpg)

    返回值`RapidOCROutput`类，主要包含以下字段:

    - `RapidOCROutput.img (np.ndarray)`: 传入的原始图像
    - `RapidOCROutput.boxes (np.ndarray)`: 图像中每行坐标框，shape为`(N, 4, 2)`。`N`表示有多少文本行。
    - `RapidOCROutput.txts (Tuple[str])`: 和`boxes`文本框对应识别到的文本内容。长度和`RapidOCROutput.boxes`长度一致。
    - `RapidOCROutput.scores (Tuple[float])`: 每行识别文本结果的置信度。长度和`RapidOCROutput.boxes`长度一致。
    - `RapidOCROutput.word_results (Tuple[Tuple[str, float, List[List[int]]]])`: 由`(识别内容，置信度，[[左上], [右上], [右下], [左下]])`构成。
    - `RapidOCROutput.elapse_list (List[float])`: 文本检测，文本行方向分类和文本识别三部分各自推理耗时，单位为秒。
    - `RapidOCROutput.elapse (float)`: 三部分整体耗时，单位为秒。

    ??? example "详细返回值示例"

        ```python linenums="1"
        RapidOCROutput(img=array([[[120,   3,  52],
            [130,   0,  63],
            [155,   9,  91],
            ...,
            [188,  10, 129],
            [189,  11, 130],
            [189,  11, 130]],

        [[218,   2, 113],
            [218,   0, 114],
            [220,   0, 114],
            ...,
            [218,   0, 114],
            [218,   0, 114],
            [218,   0, 114]]], dtype=uint8),
            boxes=array([[[  6.,   2.],
            [322.,   9.],
            [320., 104.],
            [  4.,  97.]],

        [[257., 234.],
            [304., 236.],
            [303., 254.],
            [257., 253.]],

        [[259., 227.],
            [286., 226.],
            [287., 236.],
            [259., 237.]],

        [[ 68., 391.],
            [151., 391.],
            [151., 413.],
            [ 68., 413.]],

        [[202., 391.],
            [287., 391.],
            [287., 413.],
            [202., 413.]]], dtype=float32),
            txts=('正品促销', '大桶装更划算', '强力去污符合国标', '40°C深度防冻不结冰', '日常价￥', '真击', '10.0起', '10.0起', '日常价￥', '底价', '5.8', '券后价￥', '起', '惊喜福利不容错过', '极速发货', '冰点标准', '破损就赔', '假一赔十'),
            scores=(0.99893, 0.9843, 0.97842, 0.93412, 0.81418, 0.66226, 0.99243, 0.99849, 0.81369, 0.99633, 0.9999, 0.83907, 0.99993, 0.99782, 0.99813, 0.99786, 0.92679, 0.99717),
            word_results=(
                ('正', 0.99974, [[6, 2], [85, 3], [83, 98], [4, 97]]),
                ('品', 0.99977, [[85, 3], [164, 5], [162, 100], [83, 98]]),
                ('促', 0.99804, [[164, 5], [243, 7], [241, 102], [162, 100]]),
                ('销', 0.99817, [[243, 7], [322, 9], [320, 104], [241, 102]]),
                ('大', 0.94109, [[70, 98], [99, 98], [99, 125], [70, 125]]),
                ('桶', 0.99258, [[99, 98], [128, 98], [128, 125], [99, 125]]),
                ('装', 0.97745, [[129, 98], [160, 98], [160, 125], [129, 125]]),
                ('更', 0.99893, [[166, 98], [194, 98], [194, 125], [166, 125]]),
                ('划', 0.99578, [[194, 98], [223, 98], [223, 125], [194, 125]]),
                ('算', 1.0, [[225, 98], [252, 98], [252, 125], [225, 125]]),
                ('强', 0.99905, [[68, 144], [90, 144], [90, 165], [68, 165]]),
                ('力', 0.99299, [[90, 144], [112, 144], [112, 165], [90, 165]]),
                ('去', 0.99093, [[112, 144], [134, 144], [134, 165], [112, 165]]),
                ('污', 0.87521, [[135, 144], [159, 144], [159, 165], [135, 165]]),
                ('符', 0.97693, [[163, 144], [187, 144], [187, 165], [163, 165]]),
                ('合', 0.99713, [[188, 144], [210, 144], [210, 165], [188, 165]]),
                ('国', 0.9977, [[210, 144], [233, 144], [233, 165], [210, 165]]),
                ('标', 0.99739, [[234, 144], [256, 144], [256, 165], [234, 165]]),
                ('4', 0.99911, [[110, 170], [116, 170], [116, 182], [110, 182]]),
                ('0', 0.99867, [[116, 170], [122, 170], [122, 182], [116, 182]]),
                ('°', 0.5525, [[122, 170], [128, 170], [128, 182], [122, 182]]),
                ('C', 0.75113, [[128, 170], [134, 170], [134, 182], [128, 182]]),
                ('深', 0.99939, [[136, 170], [146, 170], [146, 182], [136, 182]]),
                ('度', 0.99875, [[146, 170], [156, 170], [156, 182], [146, 182]]),
                ('防', 0.99903, [[158, 170], [168, 170], [168, 182], [158, 182]]),
                ('冻', 0.99977, [[170, 170], [180, 170], [180, 182], [170, 182]]),
                ('不', 0.99916, [[182, 170], [192, 170], [192, 182], [182, 182]]),
                ('结', 0.99879, [[196, 170], [206, 170], [206, 182], [196, 182]]),
                ('冰', 0.97904, [[206, 170], [216, 170], [216, 182], [206, 182]]),
                ('日', 0.90645, [[35, 227], [41, 227], [41, 236], [35, 236]]),
                ('常', 0.89889, [[41, 227], [47, 227], [47, 236], [41, 236]]),
                ('价', 0.95318, [[49, 227], [54, 227], [54, 236], [49, 236]]),
                ('￥', 0.4982, [[54, 227], [61, 227], [61, 236], [54, 236]]),
                ('真', 0.86379, [[139, 223], [162, 223], [162, 251], [139, 251]]),
                ('击', 0.46073, [[162, 223], [186, 223], [186, 251], [162, 251]]),
                ('1', 0.99983, [[35, 233], [43, 233], [41, 252], [33, 252]]),
                ('0', 0.99964, [[45, 233], [53, 234], [51, 253], [43, 252]]),
                ('.', 0.99809, [[54, 234], [61, 234], [59, 253], [52, 253]]),
                ('0', 0.99884, [[61, 234], [69, 235], [67, 254], [59, 253]]),
                ('起', 0.96575, [[69, 235], [79, 235], [77, 254], [67, 254]]),
                ('1', 0.99957, [[257, 234], [265, 234], [265, 253], [257, 253]]),
                ('0', 0.99959, [[267, 234], [275, 234], [275, 253], [267, 253]]),
                ('.', 0.99764, [[276, 234], [283, 235], [283, 253], [276, 253]]),
                ('0', 0.99934, [[283, 235], [291, 235], [290, 253], [283, 253]]),
                ('起', 0.99631, [[291, 235], [301, 235], [300, 253], [290, 253]]),
                ('日', 0.96985, [[259, 227], [265, 226], [266, 236], [259, 237]]),
                ('常', 0.94479, [[265, 226], [272, 226], [273, 236], [266, 236]]),
                ('价', 0.98408, [[272, 226], [278, 226], [279, 236], [273, 236]]),
                ('￥', 0.35603, [[278, 226], [286, 226], [287, 236], [279, 236]]),
                ('底', 0.99336, [[140, 243], [163, 244], [162, 271], [139, 271]]),
                ('价', 0.9993, [[163, 244], [186, 245], [186, 272], [162, 271]]),
                ('5', 0.99993, [[138, 289], [157, 289], [156, 339], [137, 339]]),
                ('.', 0.99983, [[157, 289], [175, 289], [174, 340], [156, 339]]),
                ('8', 0.99994, [[180, 289], [200, 289], [199, 340], [179, 340]]),
                ('券', 0.87593, [[98, 320], [105, 320], [105, 330], [98, 330]]),
                ('后', 0.96402, [[105, 320], [112, 320], [112, 330], [105, 330]]),
                ('价', 0.99926, [[113, 320], [119, 320], [119, 330], [113, 330]]),
                ('￥', 0.51708, [[119, 320], [127, 320], [127, 330], [119, 330]]),
                ('起', 0.99993, [[205, 316], [221, 316], [221, 335], [205, 335]]),
                ('惊', 0.99903, [[114, 342], [124, 342], [124, 355], [114, 355]]),
                ('喜', 0.99708, [[124, 342], [136, 342], [136, 355], [124, 355]]),
                ('福', 0.99696, [[137, 342], [148, 342], [148, 355], [137, 355]]),
                ('利', 0.99857, [[148, 342], [160, 342], [160, 355], [148, 355]]),
                ('不', 0.99935, [[163, 342], [174, 342], [174, 355], [163, 355]]),
                ('容', 0.99512, [[174, 342], [186, 342], [186, 355], [174, 355]]),
                ('错', 0.99765, [[187, 342], [198, 342], [198, 355], [187, 355]]),
                ('过', 0.99883, [[198, 342], [210, 342], [210, 355], [198, 355]]),
                ('极', 0.99958, [[70, 362], [89, 362], [89, 384], [70, 384]]),
                ('速', 0.9989, [[89, 362], [108, 362], [108, 384], [89, 384]]),
                ('发', 0.99474, [[108, 362], [127, 362], [127, 384], [108, 384]]),
                ('货', 0.99929, [[129, 362], [149, 362], [149, 384], [129, 384]]),
                ('冰', 0.99978, [[202, 362], [221, 362], [221, 384], [202, 384]]),
                ('点', 0.99703, [[222, 362], [243, 362], [243, 384], [222, 384]]),
                ('标', 0.99747, [[245, 362], [264, 362], [264, 384], [245, 384]]),
                ('准', 0.99718, [[264, 362], [284, 362], [284, 384], [264, 384]]),
                ('破', 0.9966, [[68, 391], [87, 391], [87, 413], [68, 413]]),
                ('损', 0.99565, [[88, 391], [108, 391], [108, 413], [88, 413]]),
                ('就', 0.89562, [[108, 391], [127, 391], [127, 413], [108, 413]]),
                ('赔', 0.81929, [[132, 391], [151, 391], [151, 413], [132, 413]]),
                ('假', 0.99998, [[204, 391], [223, 391], [223, 413], [204, 413]]),
                ('一', 0.99852, [[223, 391], [244, 391], [244, 413], [223, 413]]),
                ('赔', 0.99349, [[245, 391], [264, 391], [264, 413], [245, 413]]),
                ('十', 0.99671, [[264, 391], [284, 391], [284, 413], [264, 413]])),
                elapse_list=[0.17388120794203132, 0.018943071365356445, 0.3944867078680545],
                elapse=0.5873109871754423, lang_rec='ch_mobile')
        ```

### 选择不同推理引擎

`rapidocr`支持4种推理引擎（**ONNXRuntime / OpenVINO / PaddlePaddle / PyTorch**），推荐首先使用 **ONNXRuntime CPU** 版。默认为ONNXRuntie。

`rapidocr`是通过指定不同参数来选择使用不同的推理引擎的。当然，使用不同推理引擎的前提是事先安装好对应的推理引擎库，并确保安装正确。

!!! info

    `rapidocr>=3.0.0`版本，可以单独为文本检测、文本行方向分类和文本识别单独指定不同的推理引擎。例如：文本检测使用ONNXRuntime，文本识别使用Paddle（`params={"Rec.engine_type": EngineType.PADDLE}`）。同时，不同版本的OCR也可以通过`Det.ocr_version`灵活指定。

=== "使用ONNXRuntime"

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

=== "使用OpenVINO"

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

=== "使用PaddlePaddle"

    1. 安装PaddlePaddle。

         参见PaddlePaddle官方安装文档 → [快速安装](https://www.paddlepaddle.org.cn/install/quick?docurl=undefined)

         大家可以根据实际情况，选择安装CPU版、GPU版。

    2. 指定PaddlePaddle作为推理引擎

        - CPU版

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

        - GPU版

            ```python linenums="1" hl_lines="3-9"
            from rapidocr import EngineType, RapidOCR

            engine = RapidOCR(
                params={
                "Det.engine_type": EngineType.PADDLE,
                "EngineConfig.paddlepaddle.use_cuda": True,  # 使用PaddlePaddle GPU版推理
                "EngineConfig.paddlepaddle.gpu_id": 0,  # 指定GPU id
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

=== "使用PyTorch"

    1. 安装PyTorch。

         参见PyTorch官方安装文档 → [Install PyTorch](https://pytorch.org/#:~:text=and%20easy%20scaling.-,INSTALL%20PYTORCH,-Select%20your%20preferences)

         大家可以根据实际情况，选择安装CPU版、GPU版。

    2. 指定PyTorch作为推理引擎

        - CPU版

            ```python linenums="1" hl_lines="3"
            from rapidocr import RapidOCR

            engine = RapidOCR(params={"Global.with_torch": True})

            img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
            result = engine(img_url)
            print(result)

            result.vis('vis_result.jpg')
            ```

        - GPU版

            ```python linenums="1" hl_lines="3-9"
            from rapidocr import EngineType, RapidOCR

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

    3. 查看输出日志。下面日志中打印出了**Using engine_name: torch**，则证明使用的推理引擎是PyTorch。

         ```bash linenums="1" hl_lines="1 3 5"
         [INFO] 2025-03-22 15:39:13,241 base.py:30: Using engine_name: torch
         [INFO] 2025-03-22 15:39:13,956 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_det_infer.pth
         [INFO] 2025-03-22 15:39:14,136 base.py:30: Using engine_name: torch
         [INFO] 2025-03-22 15:39:14,136 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_ptocr_mobile_v2.0_cls_infer.pth
         [INFO] 2025-03-22 15:39:14,168 base.py:30: Using engine_name: torch
         [INFO] 2025-03-22 15:39:14,168 utils.py:35: File already exists in /Users/jiahuawang/projects/RapidOCR/python/rapidocr/models/ch_PP-OCRv4_rec_infer.pth
         ```

### 使用本地已下载模型

使用方法同样也是有两种：一是通过配置文件传入；二是通过初始化参数传入。下面以通过初始化参数传入为例：

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

engine = RapidOCR(
    params={"Det.model_path": "rapidocr/models/ch_PP-OCRv4_det_infer.onnx"}
)

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

上面第4行通过`Det.model_path`指定了本地已经下载好的文本检测模型。文本方向分类和文本识别模型也可同样指定。(`Cls.model_path`和`Rec.model_path`)

### 推荐阅读

- [如何使用不同语言模型？](../../model_list.md)
