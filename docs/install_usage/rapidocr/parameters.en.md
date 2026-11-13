---
title: RapidOCR Parameters
description: Configuration file and detection, classification and recognition parameter reference for RapidOCR.
comments: true
hide:
  - toc
---

## Generation of `config.yaml`

```bash linenums="1"
rapidocr config
```

## Introduction to Common Parameters in `default_rapidocr.yaml`

### Global

This section is the global configuration.

```yaml linenums="1"
Global:
    text_score: 0.5

    use_det: true
    use_cls: true
    use_rec: true

    use_preprocess_img: true
    min_side_len: 30
    max_side_len: 2000

    use_vertical_padding: true
    min_height: 30
    width_height_ratio: 8

    return_word_box: false
    return_single_char_box: false

    font_path: null
    log_level: "info" # debug / info / warning / error / critical

    model_root_dir: null
```

`text_score (float)`: Confidence of the text recognition result; the larger the value, the greater the certainty. Value range: `[0, 1]`, default value is 0.5.

`use_det (bool)`: Whether to use text detection. Defaults to `True`.

`use_cls (bool)`: Whether to use text line orientation classification. Defaults to `True`.

`use_rec (bool)`: Whether to use text line recognition. Defaults to `True`.

> ⚠️ Note: If the three parameters `use_det | use_cls | use_rec` are declared both in the configuration file and at call time, the parameters passed at call time will override those in the configuration file.

`use_preprocess_img (bool)`: Whether to use image preprocessing. The preprocessing here mainly relies on the two parameters `min_hegiht` and `width_height_ratio` to control whether padding is applied to the image. If set to `False`, both the `min_hegiht` and `width_height_ratio` parameters become ineffective. Defaults to `True`.

> This parameter was added in `rapidocr>=3.9.2`.

`min_height (int)` : Minimum image height (in pixels). When the value is below this, the image top-and-bottom padding operation is triggered; padding allows the text detection model to detect text lines more accurately. Default value is 30.

![](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/single_line_text.jpg)

`width_height_ratio (float)`: If the aspect ratio of the input image is greater than `width_height_ratio`, the image top-and-bottom padding operation is triggered. When the value is -1: this parameter is not used. Default value is 8.

`use_vertical_padding (bool)`: Whether to apply top-and-bottom padding to the image. This parameter mainly controls whether the two parameters `max_side_len` and `min_side_len` take effect. If set to `False`, both of these parameters become ineffective. Defaults to `True`.

> This parameter was added in `rapidocr>=3.9.2`.

`max_side_len (int)`: If the longest side of the input image is greater than `max_side_len`, the longest side will be scaled to `max_side_len` according to the aspect ratio. Defaults to 2000 px.

`min_side_len (int)`: If the shortest side of the input image is less than `min_side_len`, the shortest side will be scaled to `min_side_len` according to the aspect ratio. Defaults to 30 px.

`return_word_box (bool)`: Whether to return the single-character coordinates of the text. Defaults to `False`.

> In `rapidocr>=2.1.0`, pure Chinese and mixed Chinese-English return single-character coordinates, while pure English returns word coordinates.
>
> In `rapidocr<=2.0.7`, pure Chinese, mixed Chinese-English and pure English all return single-character coordinates.
>
> In `rapidocr_onnxruntime>=1.4.1`, Chinese characters return single-character coordinates, while English returns single-letter coordinates.
>
> In `rapidocr_onnxruntime==1.4.0`, Chinese characters return single-character coordinates, while English returns word coordinates.

`return_single_char_box (bool)`: When the text content contains only English and digits, whether to return single-character coordinates. Defaults to `False`.

> This parameter was added in `rapidocr>=3.1.0`; it only takes effect when `return_word_box=True`.

```python
result = engine(img_url, return_word_box=True, return_single_char_box=True)
```

`font_path (str)`: Path to the font file. If not provided, the program will automatically download the preset font file to the local machine. Defaults to `None`.

`log_level (str)`: Log level setting. Available options are `debug / info / warning / error / critical`; the default is `info`, which prints logs such as model loading. If set to `critical`, no logs will be printed.

> This parameter was added in `rapidocr>=3.4.0`.

`model_root_dir (str)`: Specifies the location of pre-downloaded models. Defaults to `None`, in which case models are saved under `models` in the `rapidocr` installation directory.

> This parameter was added in `rapidocr>=3.8.0`.

### EngineConfig

!!! note

    The configuration shown below is for the latest version. If you encounter issues such as certain fields not being found, please switch to the documentation for the corresponding version.

This section contains the configuration for the relevant inference engines; configure it as needed. Some keywords may be added to or removed from this section in the future; if you have any requests, feel free to point them out in the comment section below the document.

```yaml linenums="1"
EngineConfig:
    onnxruntime:
        intra_op_num_threads: -1
        inter_op_num_threads: -1
        enable_cpu_mem_arena: false

        cpu_ep_cfg:
            arena_extend_strategy: "kSameAsRequested"

        use_cuda: false
        cuda_ep_cfg:
            device_id: 0
            arena_extend_strategy: "kNextPowerOfTwo"
            cudnn_conv_algo_search: "EXHAUSTIVE"
            do_copy_in_default_stream: true

        use_dml: false
        dml_ep_cfg: null

        use_cann: false
        cann_ep_cfg:
            device_id: 0
            arena_extend_strategy: "kNextPowerOfTwo"
            npu_mem_limit:  21474836480 # 20 * 1024 * 1024 * 1024
            op_select_impl_mode: "high_performance"
            optypelist_for_implmode: "Gelu"
            enable_cann_graph: true

        # rapidocr >= 3.7.0
        use_coreml: false
        coreml_ep_cfg:
            ModelFormat: "MLProgram"
            MLComputeUnits: "ALL"
            RequireStaticInputShapes: 0
            EnableOnSubgraphs: 0
            SpecializationStrategy: "FastPrediction"
            ProfileComputePlan: 0
            AllowLowPrecisionAccumulationOnGPU: 0
            ModelCacheDirectory: "/tmp/RapidOCR"

    openvino:
        inference_num_threads: -1
        performance_hint: null
        performance_num_requests: -1
        enable_cpu_pinning: null
        num_streams: -1
        enable_hyper_threading: null
        scheduling_core_type: null

    paddle:
        cpu_math_library_num_threads: -1

        use_npu: false
        npu_ep_cfg:
            device_id: 0
            envs:
                FLAGS_npu_jit_compile: 0
                FLAGS_use_stride_kernel: 0
                FLAGS_allocator_strategy: "auto_growth"
                CUSTOM_DEVICE_BLACK_LIST: "pad3d,pad3d_grad,set_value,set_value_with_tensor"
                FLAGS_npu_scale_aclnn: "True"
                FLAGS_npu_split_aclnn: "True"

        use_cuda: false
        cuda_ep_cfg:
            device_id: 0
            gpu_mem: 500

    torch:
        use_cuda: false
        cuda_ep_cfg:
            device_id: 0

        use_npu: false
        npu_ep_cfg:
            device_id: 0

    # rapidocr >= 3.7.0
    tensorrt:
        device_id: 0
        use_fp16: true
        use_int8: false
        workspace_size: 1073741824  # 1GB = 1 << 30

        cache_dir: null
        force_rebuild: false

        det_profile:
            min_shape: [1, 3, 32, 32]
            opt_shape: [1, 3, 736, 736]
            max_shape: [1, 3, 2048, 2048]

        rec_profile:
            min_shape: [1, 3, 48, 32]
            opt_shape: [6, 3, 48, 320]
            max_shape: [6, 3, 48, 2048]

        cls_profile:
            min_shape: [1, 3, 48, 32]
            opt_shape: [6, 3, 48, 192]
            max_shape: [6, 3, 48, 192]

    mnn: {}  # rapidocr>=3.6.0
```

For detailed usage of this section, please refer to: [How to use different inference engines?](./how_to_use_infer_engine.md)

APIs of each inference engine:

- ONNX Runtime Python API: see [Python API](https://onnxruntime.ai/docs/api/python/api_summary.html)
- OpenVINO Python API: see [OpenVINO Python API](https://docs.openvino.ai/2025/api/ie_python_api/api.html)
- PaddlePaddle API: see [API Documentation](https://www.paddlepaddle.org.cn/documentation/docs/zh/api/index_cn.html)
- PyTorch API: see [PyTorch documentation](https://docs.pytorch.org/docs/stable/index.html)
- MNN API: see [MNN](https://mnn-docs.readthedocs.io/en/latest/index.html)
- TensorRT API: see [TensorRT Python API](https://docs.nvidia.com/deeplearning/tensorrt/latest/_static/python-api/index.html)

The first 4 parameters of the following three sections are basically similar; the correspondence is shown in the table below. For details, please refer to the [Model List](../../model_list.md) document:

| YAML Parameter  | Corresponding Enum Class | Available Enum Values (Examples)                 |Import | Notes                                |
|-----------------|------------------|------------------|-------------------|-------------------------------------|
| `engine_type`   | `EngineType`     | `ONNXRUNTIME` (onnxruntime)<br/>`OPENVINO` (openvino)<br/>`PADDLE` (paddle)<br/>`TORCH` (torch)<br/>`MNN` (mnn)(`rapidocr>=3.6.0`)<br/>`TENSORRT`(tensorrt)(`rapidocr>=3.7.0`) | `from rapidocr import EngineType`| Inference engine type         |
| `lang_type`     |  `LangDet`<br/> `LangCls`<br/> `LangRec` | `rapidocr<3.10.0`: use the corresponding enum values.<br/>`rapidocr>=3.10.0`: in addition to enums, you can also directly pass the language code strings from `default_models.yaml`, e.g. `"ch"`, `"japan"`, `"korean"`.|`from rapidocr import LangDet`<br/> `from rapidocr import LangCls` <br/>`from rapidocr import LangRec`| Resolves the model route based on the OCR processing stage, OCR version and model type; supported codes are subject to the [Model List](../../model_list.md).|
| `model_type`    | `ModelType`      | `MOBILE` (mobile)<br/>`SERVER` (server)<br/>`TINY`(tiny) <br/> `SMALL`(small)<br/>`MEDIUM`(medium) |`from rapidocr import ModelType`| Model size and performance level      |
| `ocr_version`   | `OCRVersion`     | `PPOCRV4` (PP-OCRv4)<br/>`PPOCRV5` (PP-OCRv5)<br/>`PPOCRV6`(PP-OCRv6) |`from rapidocr import OCRVersion`| Model version    |

### Det

```yaml linenums="1"
Det:
    engine_type: "onnxruntime"
    lang_type: "ch"
    model_type: "small"
    ocr_version: "PP-OCRv6"

    task_type: "det"

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

`engine_type (str)`: Selects the inference engine. Supports four values: `onnxruntime`, `openvino`, `paddle` and `torch`. Defaults to `onnxruntime`.

`lang_type (str)`: Language types supported for detection. The specific available codes are determined by the OCR version and model type; see the [Model List](../../model_list.md) for details. Defaults to `ch`.

> `rapidocr>=3.10.0` supports directly passing language code strings, and is also compatible with the `LangDet` enum.

`model_type (str)`: Model size selection. `PP-OCRv4` and `PP-OCRv5` support `mobile` (lightweight) and `server` (server-grade). `PP-OCRv6` supports `tiny`, `small` and `medium`; the default is `small` of `PP-OCRv6`.

> `PP-OCRv6` is supported in `rapidocr>=3.9.0`.

`ocr_version (str)`: Selection of the OCR version; supports `PP-OCRv4`, `PP-OCRv5` and `PP-OCRv6`. Defaults to `PP-OCRv6`.

> `PP-OCRv6` is supported in `rapidocr>=3.9.0`.

`model_path (str)`: Path to the text detection model, limited to DBNet text detection models trained with PaddleOCR. Default value is `None`.

`model_dir (str)`: Path or directory where the model is stored. For PaddlePaddle, this parameter corresponds to the directory where the model resides. For other inference engines, please use the `model_path` parameter.

`limit_side_len (float)`: The pixel value that limits the length of the image side. Default value is 736.

`limit_type (str)`: Whether to limit the shortest side or the longest side of the image to `limit_side_len`. Example explanation: when `limit_type=min` and `limit_side_len=736`, if the shortest side of the image is less than 736, the shortest side will be stretched to 736, and the other side will be scaled proportionally according to the original aspect ratio. Value range: `[min, max]`, default value is `min`.

> In `rapidocr>=3.10.0`, the issue where `limit_type` set to `max` did not respect the `limit_side_len` constraint was fixed.

`thresh (float)`: The segmentation threshold between the text part and the background part in the image. The larger the value, the smaller the text part. Value range: `[0, 1]`, default value is 0.3.

`box_thresh (float)`: The threshold for whether a box obtained by text detection is retained; the larger the value, the lower the recall. Value range: `[0, 1]`, default value is 0.5.

`max_candidates (int)`: Maximum number of candidate boxes. Default is 1000.

`unclip_ratio (float)`: Controls the size of the text detection box; the larger the value, the larger the overall detection box. Value range: `[1.6, 2.0]`, default value is 1.6.

`use_dilation (bool)`: Whether to use dilation. Defaults to `true`. This parameter is used to apply morphological dilation to the detected text regions.

`score_mode (str)`: The method for computing the text box score. Value range: `[slow, fast]`, default value is `fast`.

### Cls

```yaml linenums="1"
Cls:
    engine_type: "onnxruntime"
    lang_type: "ch"
    model_type: "mobile"
    ocr_version: "PP-OCRv4"

    task_type: "cls"

    model_path: null
    model_dir: null

    cls_image_shape: [3, 48, 192]
    cls_batch_num: 6
    cls_thresh: 0.9
    label_list: ["0", "180"]
```

`engine_type (str)`: Same as described in the Det section.

`lang_type (str)`: Language types supported for classification. Currently the classification model uses the `ch`/`multi` route; defaults to `ch`.

> In `rapidocr>=3.10.0`, language code strings can be passed directly, and the `LangCls` enum is also supported.

`model_type (str)`: Same as described in the Det section.

`ocr_version (str)`: Same as described in the Det section.

`model_path (str)`: Path to the text line orientation classification model, limited to binary classification models trained with PaddleOCR. Default value is `None`.

`model_dir (str)`: Placeholder parameter, currently has no effect.

`cls_image_shape (List[int])`: The image Shape (CHW) input to the orientation classification model. Default value is `[3, 48, 192]`.

`cls_batch_num (int)`: The batch size for batch inference. Generally the default value is sufficient; making it too large does not noticeably speed things up and may even degrade the results. Default value is 6.

`cls_thresh (float)`: Confidence of the orientation classification result. Value range: `[0, 1]`, default value is 0.9.

`label_list (List[str])`: Labels for orientation classification, 0° or 180°, **this parameter must not be changed**. Default value is `["0", "180"]`.

### Rec

```yaml linenums="1"
Rec:
    engine_type: "onnxruntime"
    lang_type: "ch"
    model_type: "small"
    ocr_version: "PP-OCRv6"

    task_type: "rec"

    model_path: null
    model_dir: null

    rec_keys_path: null
    rec_img_shape: [3, 48, 320]
    rec_batch_num: 6
```

`engine_type (str)`: Same as described in the Det section.

`lang_type (str)`: Language types supported for recognition. For the specific supported languages, see the [Model List](../../model_list.md).

> In `rapidocr>=3.10.0`, language code strings can be passed directly, and the `LangRec` enum is also supported.

`model_type (str)`: Same as described in the Det section.

`ocr_version (str)`: Same as described in the Det section.

`model_path (str)`: Path to the text recognition model, limited to text recognition models trained with PaddleOCR. Default value is `None`.

`model_dir (str)`: Path or directory where the model is stored. For PaddlePaddle, this parameter corresponds to the directory where the model resides. For other inference engines, please use the `model_path` parameter.

`rec_keys_path (str)`: The dictionary file corresponding to the text recognition model. Defaults to `None`.

`rec_img_shape (List[int])`: The image Shape (CHW) input to the text recognition model. Default value is `[3, 48, 320]`.

`rec_batch_num (int)`: The batch size for batch inference. Generally the default value is sufficient; making it too large does not noticeably speed things up and may even degrade the results. Default value is 6.
