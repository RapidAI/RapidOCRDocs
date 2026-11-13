## Introduction

This section covers how to use the `rapidocr` library to perform text recognition on images. It mainly explains two ways of using the `rapidocr` library: Python scripts and the CLI terminal.

In `rapidocr>=3.10.0`, `RapidOCR()` does not construct all models immediately during initialization; the corresponding models are loaded only when detection, classification, or recognition is called for the first time. The first call may take slightly longer, and subsequent calls return to normal.

## Python Script Usage

Everything uses the default values.

In `rapidocr>=3.9.0`, the defaults are `Det PP-OCRv6 small` + `Cls PP-OCRv4 mobile` + `Rec PP-OCRv6 small`.

In `rapidocr<3.9.0`, the defaults are `Det PP-OCRv4 mobile` + `Cls PP-OCRv4 mobile` + `Rec PP-OCRv4 mobile`.

It is recommended to first use the ONNX Runtime CPU version as the inference engine.

```bash linenums="1"
pip install onnxruntime
```

For detailed parameter settings of other default values, see: [`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/config.yaml)

```python linenums="1"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

Using models of different sizes; all other unspecified parameters use their default values.

```python linenums="1"
from rapidocr import ModelType, RapidOCR

engine = RapidOCR(
    params={
        "Det.model_type": ModelType.TINY, # ModelType.MEDIUM
        "Rec.model_type": ModelType.TINY, # ModelType.MEDIUM
    }
)

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

### Initializing RapidOCR Instance Input

The input supports passing in a YAML-format configuration file, and also supports passing parameters directly.

=== "Method 1: Pass in a Configuration File"

    1. Generate the **default_rapidocr.yaml** configuration file. Run the following code in the terminal to generate the default **default_rapidocr.yaml** file in the current directory.

        ```bash linenums="1"
        $ rapidocr config
        # The config file has saved in ./default_rapidocr.yaml
        ```

    2. Modify the corresponding values in **default_rapidocr.yaml** according to your needs. For example, to use OpenVINO as the inference engine for text detection, along with the `ch_mobile`, PP-OCRv4 version model, change it as follows:

        ```yaml linenums="1" hl_lines="3"
        # This configuration file is named 1.yaml
        Det:
            # The following 4 values can be found at https://github.com/RapidAI/RapidOCR/blob/123a129c613ca99c3b007f0591a3587cc01a4c32/python/rapidocr/utils/typings.py
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

    3. Pass it into `RapidOCR` for use.

        ```python linenums="1" hl_lines="4-5"
        from rapidocr import RapidOCR

        # 1.yaml from Step 2
        config_path = "1.yaml"
        engine = RapidOCR(config_path=config_path)

        img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
        result = engine(img_url)
        print(result)

        result.vis("vis_result.jpg")
        ```

=== "Method 2: Pass in Parameters Directly"

    !!! tip

        After `rapidocr>=3.0.0`, the settings of the three parameters `engine_type`, `lang_type`, `model_type` and `ocr_version` were moved down to the three stages of text detection, text line orientation classification, and text recognition. This is more flexible. You can specify different inference engines and different model types for different stages.

    Since rapidocr involves many adjustable parameters, for ease of maintenance the [omageconf](https://github.com/omry/omegaconf) library is introduced to update parameters. The trade-off is that passing parameters is not as intuitive as in the 1.x series. However, the current approach is still easy to understand and use.

    For example, if I want to use OpenVINO as the inference engine for each stage, I can use it in the following way:

    ```python linenums="1" hl_lines="5-7"
    from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

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

    result.vis("vis_result.jpg")
    ```

    For other ways of passing parameters, basically just refer to `config.yaml`; separate the keys with dots and write them directly. For example:

    ```yaml linenums="1" title="config.yaml Partial Parameter Example"
    Det:
        engine_type: 'openvino'
        lang_type: 'ch'
        model_type: 'mobile'
        ocr_version: 'PP-OCRv4'

    EngineConfig:
        torch:
            use_cuda: false
            cuda_ep_cfg:
                device_id: 0
    ```

    ```python linenums="1" hl_lines="5-10"  title="Corresponding Parameter Syntax"
    from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.engine_type": EngineType.TORCH,
            "Det.lang_type": LangDet.CH,
            "Det.model_type": ModelType.MOBILE,
            "Det.ocr_version": OCRVersion.PPOCRV5,
            "EngineConfig.torch.use_cuda": True,  # Use the torch GPU version for inference
            "EngineConfig.torch.cuda_ep_cfg.device_id": 0,  # Specify the GPU id
        }
    )
    ```

### Image Input

`RapidOCR` supports multiple image input methods such as file paths, URLs, `bytes`, NumPy, Pillow, and memory addresses. For details, see: [Image Input](./image_input.md).

### Output

RapidOCR output includes 4 types: `Union[TextDetOutput, TextClsOutput, TextRecOutput, RapidOCROutput]`. All 4 types are Dataclasses classes, and you can directly access the corresponding key values.

- `TextDetOutput`: Detection only
- `TextClsOutput`: Text line direction classification only
- `TextRecOutput`: Recognition only
- `RapidOCROutput`: Detection + direction classification + recognition

The detailed combinations are as follows:

=== "Detection + Classification + Recognition"

    ```python linenums="1" hl_lines="8"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"

    # All are True by default
    result = engine(img_url, use_det=True, use_cls=True, use_rec=True)
    print(result)
    result.vis("vis_det_cls_rec.jpg")
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-24-08-5100098f.jpg)

    The return value is `RapidOCROutput`, which can be accessed directly via `result.xxxx`. It mainly contains the following fields:

    - `RapidOCROutput.img (np.ndarray)`: The original input image
    - `RapidOCROutput.boxes (np.ndarray)`: The coordinate box of each line in the image, with shape `(N, 4, 2)`. `N` indicates how many text lines there are.
    - `RapidOCROutput.txts (Tuple[str])`: The recognized text content corresponding to the `boxes` text boxes. Its length is consistent with the length of `RapidOCROutput.boxes`.
    - `RapidOCROutput.scores (Tuple[float])`: The confidence of the recognized text result for each line. Its length is consistent with the length of `RapidOCROutput.boxes`.
    - `RapidOCROutput.word_results (Tuple[Any])`: This part of the result only has a value when `return_word_box=True`.
    - `RapidOCROutput.elapse_list (List[float])`: The respective inference time of the three parts: text detection, text line direction classification, and text recognition, in seconds.
    - `RapidOCROutput.elapse (float)`: The overall time of the three parts, in seconds.

    ??? example "Detailed Return Value Example"

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

=== "Detection + Recognition"

    ???+ tip

        The prerequisite for the combination of text detection and text recognition only to work properly is: make sure that the text in the input image is all upright.

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url, use_det=True, use_cls=False, use_rec=True)
    print(result)
    result.vis("vis_det_rec.jpg")
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-24-35-01ae4972.jpg)

    The return value type is the same as in the **Detection + Classification + Recognition** section.

=== "Classification + Recognition"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result = engine(img_path, use_det=False, use_cls=True, use_rec=True)
    print(result)
    print(result.elapse)
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-19-07-ba404f86.jpg)

    The return value is the `TextClsOutput` class, which mainly contains the following fields:

    - `TextClsOutput.img_list (List[np.ndarray])`: A list composed of multiple text line images.
    - `TextClsOutput.cls_res (List[Tuple(str, float)])`: The direction and confidence corresponding to each text line.
    - `TextClsOutput.elapse (float)`: The recognition time, in seconds.

    ???+ example "Detailed Return Value Example"

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

=== "Detection Only"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url, use_det=True, use_cls=False, use_rec=False)
    print(result)
    result.vis('vis_only_det.jpg')
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-25-14-6d325105.jpg)

    The return value is of the `TextDetOutput` class and mainly contains the following fields:

    - `TextDetOutput.img (np.ndarray)`: The original input image
    - `TextDetOutput.boxes (np.ndarray)`: Text line coordinates, consisting of 4 points, in the order `[top-left, top-right, bottom-right, bottom-left]`
    - `TextDetOutput.scores (List[float])`: The confidence score corresponding to each text line.
    - `TextDetOutput.elapse (float)`: The overall text detection time, in seconds.

    ???+ example "Detailed return value example"

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

=== "Classification Only"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://raw.githubusercontent.com/RapidAI/RapidOCR/refs/heads/main/python/tests/test_files/text_rec.jpg"
    result = engine(img_url, use_det=False, use_cls=True, use_rec=False)
    print(result)
    result.vis("vis_only_cls.jpg")
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-24-56-274ec91f.jpg)

    The return value is of the `TextClsOutput` class and mainly contains the following fields:

    - `TextClsOutput.img_list (List[np.ndarray])`: A list composed of multiple text line images.
    - `TextClsOutput.cls_res (List[Tuple(str, float)])`: The orientation and confidence corresponding to each text line.
    - `TextClsOutput.elapse (float)`: The recognition time, in seconds.

    ???+ example "Detailed return value example"

        ```python linenums="1"
        TextClsOutput(img_list=[array([[[123,  56,   1],
                [124,  55,   0],
                [131,  55,   0],], dtype=uint8)],
        cls_res=[('0', 0.9998784)],
        elapse=0.004718780517578125)
        ```

=== "Recognition Only"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://raw.githubusercontent.com/RapidAI/RapidOCR/refs/heads/main/python/tests/test_files/text_rec.jpg"
    result = engine(img_url, use_det=False, use_cls=False, use_rec=True)
    print(result)
    result.vis("vis_only_rec.jpg")
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-25-26-a1276ed8.jpg)

    The return value is of the `TextRecOutput` class and mainly contains the following fields:

    - `TextRecOutput.imgs (List[np.ndarray])`: A list composed of multiple text line images.
    - `TextRecOutput.txts (List[Tuple(str, float)])`: The recognition result corresponding to each text line.
    - `TextRecOutput.scores (float)`: The recognition result for each text line.
    - `TextRecOutput.word_results (Tuple[None])`: Has a value only when `return_word_box=True` is specified.

    ???+ example "Detailed return value example"

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

=== "Return Single-Character Coordinates"

    ```python linenums="1" hl_lines="6"
    from rapidocr import RapidOCR

    engine = RapidOCR()

    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url, return_word_box=True)
    print(result)
    result.vis("vis_return_words.jpg")
    ```

    ![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-25-46-fdd5005f.jpg)

    The return value is of the `RapidOCROutput` class and mainly contains the following fields:

    - `RapidOCROutput.img (np.ndarray)`: The original input image
    - `RapidOCROutput.boxes (np.ndarray)`: The coordinate box of each line in the image, with shape `(N, 4, 2)`. `N` indicates the number of text lines.
    - `RapidOCROutput.txts (Tuple[str])`: The recognized text content corresponding to the `boxes` text boxes. Its length is the same as that of `RapidOCROutput.boxes`.
    - `RapidOCROutput.scores (Tuple[float])`: The confidence of the recognized text result for each line. Its length is the same as that of `RapidOCROutput.boxes`.
    - `RapidOCROutput.word_results (Tuple[Tuple[str, float, List[List[int]]]])`: Composed of `(recognized content, confidence, [[top-left], [top-right], [bottom-right], [bottom-left]])`.
    - `RapidOCROutput.elapse_list (List[float])`: The respective inference time of the three parts (text detection, text line orientation classification, and text recognition), in seconds.
    - `RapidOCROutput.elapse (float)`: The overall time of the three parts, in seconds.

    ??? example "Detailed return value example"

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

## CLI Terminal Usage

Terminal usage is simple, with straightforward commands.

### `rapidocr check`

Automatically checks whether the `rapidocr` library is installed successfully. The main principle: it uses the ONNX Runtime inference engine to process one image, and checks whether the result meets expectations to determine whether the installation was successful.

```bash linenums="1"
rapidocr check
```

Example output:

```bash linenums="1"
[INFO] 2026-06-23 12:51:43,979 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-06-23 12:51:44,045 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_det_small.onnx
[INFO] 2026-06-23 12:51:44,046 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_det_small.onnx
[INFO] 2026-06-23 12:51:44,127 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-06-23 12:51:44,129 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-06-23 12:51:44,129 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_mobile.onnx
[INFO] 2026-06-23 12:51:44,190 [RapidOCR] base.py:23: Using engine_name: onnxruntime
[INFO] 2026-06-23 12:51:44,260 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_rec_small.onnx
[INFO] 2026-06-23 12:51:44,260 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_rec_small.onnx
Success! rapidocr is installed correctly!
```

### `rapidocr config`

Automatically generates the default configuration file used by `rapidocr`, making it easy to modify and customize.

```bash linenums="1"
rapidocr config
```

Example output:

```bash linenums="1"
The config file has saved in ./default_rapidocr.yaml
```

### `rapidocr download_models`

> The default config file was added in `rapidocr>=3.8.2`.
>
> This parameter was added in `rapidocr>=3.7.0`.

Pre-downloads the specified models for convenient offline deployment. Because `rapidocr` has many optional parameters, a specified configuration file is used to quickly download the specified models.

If the `--config` parameter is not passed, running this command by default downloads the following models into the `models` directory under the `rapidocr` installation directory

```text linenums="1"
PP-OCRv6_det_small.onnx
ch_ppocr_mobile_v2.0_cls_mobile.onnx
PP-OCRv6_rec_small.onnx
```

```bash linenums="1"
# Download the models from the default config file directly
rapidocr download_models

# Download the models under the specified config file
rapidocr download_models --config config.yaml
```

Example output:

```bash linenums="1"
[INFO] 2026-03-24 10:37:01,625 [RapidOCR] download_file.py:68: Initiating download: https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.7.0/onnx/PP-OCRv4/cls/ch_ppocr_mobile_v2.0_cls_infer.onnx
[INFO] 2026-03-24 10:37:03,640 [RapidOCR] download_file.py:82: Download size: 0.56MB
[INFO] 2026-03-24 10:37:04,364 [RapidOCR] download_file.py:95: Successfully saved to: /Users/xxxx/RapidOCR/python/test_models/ch_ppocr_mobile_v2.0_cls_infer.onnx
```

### View Supported Languages

`rapidocr>=3.10.0` provides `--list-langs`, which lets you query the languages supported by the current model routing by task, OCR version, and model type:

```bash
# Query the languages supported by the PP-OCRv6 medium recognition model
rapidocr --list-langs --task rec --ocr_version PP-OCRv6 --model_type medium
```

You can also call the same interface in Python:

```python
from rapidocr import RapidOCR

langs = RapidOCR.list_supported_langs("rec", "PP-OCRv6", "medium")
print(langs)
```
