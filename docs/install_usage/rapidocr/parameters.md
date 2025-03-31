---
comments: true
hide:
  - toc
---

### `config.yaml`的生成

```bash linenums="1"
rapidocr config
```

### `default_rapidocr.yaml`常用参数介绍

#### Global

```yaml linenums="1"
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
    with_openvino: false
    with_paddle: false
    with_torch: false

    font_path: null
```

**text_score** (*float, optional*): 文本识别结果置信度，值越大，把握越大。取值范围：`[0, 1]`, 默认值是0.5。

#### EngineConfig

```yaml linenums="1"
EngineConfig:
    onnxruntime:
        intra_op_num_threads: -1
        inter_op_num_threads: -1
        use_cuda: false
        use_dml: false

    openvino:
        inference_num_threads: -1

    paddlepaddle:
        cpu_math_library_num_threads: -1
        use_cuda: false
        gpu_id: 0
        gpu_mem: 500

    torch:
        use_cuda: false
        gpu_id: 0
```

#### Det

```yaml linenums="1"
Det:
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

#### Cls

```yaml linenums="1"
Cls:
    model_path: null
    model_dir: null

    cls_image_shape: [3, 48, 192]
    cls_batch_num: 6
    cls_thresh: 0.9
    label_list: ['0', '180']
```

#### Rec

```yaml linenums="1"
Rec:
    model_path: null
    model_dir: null

    rec_keys_path: null
    rec_img_shape: [3, 48, 320]
    rec_batch_num: 6
```

**print_verbose** (*bool, optional*): 是否打印各个部分耗时信息。 默认为`False`。

**min_height** (*int, optional*): 图像最小高度（单位是像素），低于这个值，会跳过文本检测阶段，直接进行后续识别。默认值为30。`min_height`是用来过滤只有一行文本的图像（如下图），这类图像不会进入文本检测模块，直接进入后续过程。

![](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/single_line_text.jpg)

**width_height_ratio** (*float, optional*): 如果输入图像的宽高比大于`width_height_ratio`，则会跳过文本检测，直接进行后续识别，取值为-1时：不用这个参数. 默认值为8。

- **max_side_len** (*int, optional*): 如果输入图像的最大边大于`max_side_len`，则会按宽高比，将最大边缩放到`max_side_len`。默认为2000px。
- **min_side_len** (*int, optional*): 如果输入图像的最小边小于`min_side_len`，则会按宽高比，将最小边缩放到`min_side_len`。默认为30px。
- **return_word_box** (*bool, optional*): 是否返回文字的单字坐标。默认为`False`。在`rapidocr_onnxruntime==1.4.0`中，汉字会返回单字坐标，英语返回单词坐标。在`rapidocr_onnxruntime>=1.4.1`中，汉字返回单字坐标，英语返回单字母坐标。
- **det_use_cuda** (*bool, optional*): 是否使用CUDA加速推理。默认值为`False`。
- **det_use_dml** (*bool, optional*): 是否使用DirectML加速推理(仅限于Window10及以上)。默认值为`False`。详细参见 → [link](../../blog/posts/how_to_use_directml.md) 。
- **det_model_path** (*Optional[str], optional*): 文本检测模型路径，仅限于基于PaddleOCR训练所得DBNet文本检测模型。默认值为`None`。
- **det_limit_side_len** (*float, optional*): 限制图像边的长度的像素值。默认值为736。
- **det_limit_type** (*str, optional*): 限制图像的最小边长度还是最大边为`limit_side_len` <br/> 示例解释：当`limit_type=min`和`limit_side_len=736`时，图像最小边小于736时，<br/>会将图像最小边拉伸到736，另一边则按图像原始比例等比缩放。 取值范围为：`[min, max]`，默认值为`min`。
- **det_thresh** (*float, optional*): 图像中文字部分和背景部分分割阈值。值越大，文字部分会越小。取值范围：`[0, 1]`，默认值为0.3。
- **det_box_thresh** (*float, optional*): 文本检测所得框是否保留的阈值，值越大，召回率越低。取值范围：`[0, 1]`，默认值为0.5。
- **det_unclip_ratio** (*float, optional*): 控制文本检测框的大小，值越大，检测框整体越大。取值范围：`[1.6, 2.0]`，默认值为1.6。
- **det_donot_use_dilation** (*bool, optional*): 不使用膨胀操作。默认值为`False`。
- **det_score_mode** (*str, optional*): 计算文本框得分的方式。取值范围为：`[slow, fast]`，默认值为`fast`。
- **cls_use_cuda** (*bool, optional*): 是否使用CUDA加速推理。默认值为`False`。
- **cls_use_dml** (*bool, optional*): 是否使用DirectML加速推理(仅限于Window10及以上)。默认值为`False`。详细参见 → [link](../../blog/posts/how_to_use_directml.md) 。
- **cls_model_path** (*Optional[str], optional*): 文本行方向分类模型路径，仅限于PaddleOCR训练所得二分类分类模型。默认值为`None`。
- **cls_image_shape** (*List[int], optional*): 输入方向分类模型的图像Shape(CHW)。默认值为`[3, 48, 192]`。
- **cls_label_list** (*List[str], optional*): 方向分类的标签，0°或者180°，**该参数不能动**。默认值为`["0", "180"]`。
- **cls_batch_num** (*int, optional*): 批次推理的batch大小，一般采用默认值即可，太大并没有明显提速，效果还可能会差。默认值为6。
- **cls_thresh** (*float, optional*): 方向分类结果的置信度。取值范围：`[0, 1]`，默认值为0.9。
- **rec_use_cuda** (*bool, optional*): 是否使用CUDA加速推理。默认值为`False`。
- **rec_use_dml** (*bool, optional*): 是否使用DirectML加速推理(仅限于Window10及以上)。默认值为`False`。详细参见 → [link](../../blog/posts/how_to_use_directml.md) 。
- **rec_keys_path** (*bool, optional*): 文本识别模型对应的字典文件，默认为`None`。
- **rec_model_path** (*Optional[str], optional*): 文本识别模型路径，仅限于PaddleOCR训练文本识别模型。默认值为`None`。
- **rec_img_shape** (*List[int], optional*): 输入文本识别模型的图像Shape(CHW)。默认值为`[3, 48, 320]`。
- **rec_batch_num** (*int, optional*): 批次推理的batch大小，一般采用默认值即可，太大并没有明显提速，效果还可能会差。默认值为6。
- **intra_op_num_threads** (*int, optional*): 参见[docs](https://onnxruntime.ai/docs/api/python/api_summary.html#onnxruntime.SessionOptions.inter_op_num_threads)。默认值为-1.
- **inter_op_num_threads** (*int, optional*): 参见[docs](https://onnxruntime.ai/docs/api/python/api_summary.html#onnxruntime.SessionOptions.intra_op_num_threads)。默认值为-1.
