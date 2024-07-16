---
comments: true
---

!!! info

    该部分以`rapidocr_onnxruntime`库下`RapidOCR`为例作讲解，其他推理引擎与这个基本类似，请移步具体源码查看。

### **\_\_init\_\_** [[SOURCE]](https://github.com/RapidAI/RapidOCR/blob/bc12d446e9761c48377490cae2059c32e978ba9f/python/rapidocr_onnxruntime/utils/parse_parameters.py#L23)

```python linenums="1"
def __init__(self, text_score: float = 0.5,
    print_verbose: bool = False,
    min_height: int = 30,
    width_height_ratio: float = 8,
    det_use_cuda: bool = False,
    det_use_dml: bool = False,
    det_model_path: Optional[str] = None,
    det_limit_side_len: float = 736,
    det_limit_type: str = "min",
    det_thresh: float = 0.3,
    det_box_thresh: float = 0.5,
    det_unclip_ratio: float = 1.6,
    det_donot_use_dilation: bool = False,
    det_score_mode: str = "fast",
    cls_use_cuda: bool = False,
    cls_use_dml: bool = False,
    cls_model_path: Optional[str] = None,
    cls_image_shape: List[int] = [3, 48, 192],
    cls_label_list: List[str] = ["0", "180"],
    cls_batch_num: int = 6,
    cls_thresh: float = 0.9,
    rec_use_cuda: bool = False,
    rec_use_dml: bool = False,
    rec_model_path: Optional[str] = None,
    rec_img_shape: List[int] = [3, 48, 320],
    rec_batch_num: int = 6,
    intra_op_num_threads: int = -1,
    inter_op_num_threads: int = -1,
):
    pass
```

#### 参数

- **text_score** (*float, optional*): 文本识别结果置信度，值越大，把握越大。取值范围：`[0, 1]`, 默认值是0.5。
- **print_verbose** (*bool, optional*): 是否打印各个部分耗时信息。 默认为`False`。
- **min_height** (*int, optional*): 图像最小高度（单位是像素），低于这个值，会跳过文本检测阶段，直接进行后续识别。默认值为30。`min_height`是用来过滤只有一行文本的图像（如下图），这类图像不会进入文本检测模块，直接进入后续过程。

    ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/single_line_text.jpg)

- **width_height_ratio** (*float, optional*): 如果输入图像的宽高比大于`width_height_ratio`，则会跳过文本检测，直接进行后续识别，取值为-1时：不用这个参数. 默认值为8。
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
- **rec_model_path** (*Optional[str], optional*): 文本识别模型路径，仅限于PaddleOCR训练文本识别模型。默认值为`None`。
- **rec_img_shape** (*List[int], optional*): 输入文本识别模型的图像Shape(CHW)。默认值为`[3, 48, 320]`。
- **rec_batch_num** (*int, optional*): 批次推理的batch大小，一般采用默认值即可，太大并没有明显提速，效果还可能会差。默认值为6。
- **intra_op_num_threads** (*int, optional*): 参见[docs](https://onnxruntime.ai/docs/api/python/api_summary.html#onnxruntime.SessionOptions.inter_op_num_threads)。默认值为-1.
- **inter_op_num_threads** (*int, optional*): 参见[docs](https://onnxruntime.ai/docs/api/python/api_summary.html#onnxruntime.SessionOptions.intra_op_num_threads)。默认值为-1.

#### 使用示例

```python linenums="1"
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR(text_score=0.6, det_use_cuda=False)

img_path = Path('tests/test_files/ch_en_num.jpg')
result, elapse = engine(img_path)
print(result)
print(elapse)
```

### **\_\_call\_\_** [[SOURCE]](https://github.com/RapidAI/RapidOCR/blob/bc12d446e9761c48377490cae2059c32e978ba9f/python/rapidocr_onnxruntime/main.py#L58)

```python linenums="1"
def __call__(
    self,
    img_content: Union[str, np.ndarray, bytes, Path],
    use_det: Optional[bool] = None,
    use_cls: Optional[bool] = None,
    use_rec: Optional[bool] = None,
    **kwargs,
) -> Tuple[Optional[List[List[Union[Any, str]]]], Optional[List[float]]]:
    pass
```

#### 参数

- **img_content** (*Union[str, np.ndarray, bytes, Path]*): 图像内容。
- **use_det** (*Optional[bool], optional*): 是否使用文本检测模型，当为`None`时，默认使用。默认值为`None`。
- **use_cls** (*Optional[bool], optional*): 是否使用文本行方向分类模型，当为`None`时，默认使用。默认值为`None`。
- **use_rec** (*Optional[bool], optional*): 是否使用文本识别模型，当为`None`时，默认使用。默认值为`None`。

#### 输入

确保输入模型前的图像通道顺序为BGR。当前`LoadImage`类内部已经对此做了处理，参考下面写法即可正常使用。支持4种输入类型：`Union[str, np.ndarray, bytes, Path, PIL.Image.Image]`

=== "str"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path)
    print(result)
    print(elapse)
    ```

=== "np.ndarray"

    ```python linenums="1"
    import cv2
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    img = cv2.imread('tests/test_files/ch_en_num.jpg')
    result, elapse = engine(img)
    print(result)
    print(elapse)
    ```

=== "PIL.Image.Image"

    ```python linenums="1"
    from PIL import Image
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    img = Image.open('tests/test_files/ch_en_num.jpg')
    result, elapse = engine(img)
    print(result)
    print(elapse)
    ```

=== "Bytes"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    with open(img_path, 'rb') as f:
        img = f.read()
    result, elapse = engine(img)
    print(result)
    print(elapse)
    ```

=== "Path"

    ```python linenums="1"
    from pathlib import Path

    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = Path('tests/test_files/ch_en_num.jpg')
    result, elapse = engine(img_path)
    print(result)
    print(elapse)
    ```

#### 输出

RapidOCR在调用时，有三个参数`use_det | use_cls | use_rec`，可以控制是否使用检测、方向分类和识别这三部分，不同的参数决定了不同的输出。

如果图像中未检测到有效文字信息，则返回`Tuple[None, None]`。详细搭配如下：

=== "只有检测"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=True, use_cls=False, use_rec=False)
    print(result)
    print(elapse)
    ```

    返回值`result`: `List[List[float]]` (每个框的坐标`[左上, 右上, 右下, 左下]`)
    ```python
    [
        [[5.0, 2.0], [322.0, 9.0], [319.0, 103.0], [3.0, 96.0]],
        [[70.0, 98.0], [252.0, 97.0], [252.0, 125.0], [70.0, 126.0]],
        ...
    ]
    ```

=== "只有分类"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=False, use_cls=True, use_rec=False)
    print(result)
    print(elapse)
    ```
    返回值`result`: `List[List[str, float]]` (`[方向0或180, 置信度]`)
    ```python
    [
        ['0', 0.9998784],
        ...
    ]
    ```

=== "只有识别"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=False, use_cls=False, use_rec=True)
    print(result)
    print(elapse)
    ```

    返回值`result`: `List[List[str, float]]` (`[识别的文本, 置信度]`)
    ```python linenums="1"
    [
        ['韩国小馆', 0.7992169380187988],
        ...
    ]
    ```

=== "检测 + 识别"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=True, use_cls=False, use_rec=True)
    print(result)
    print(elapse)
    ```
    返回值`result`: `List[List[float], str, float]` (`[[左上, 右上, 右下, 左下], 文本内容, 置信度]`)
    ```python linenums="1"
    [
        [[[9.0, 2.0], [321.0, 11.0], [318.0, 102.0], [6.0, 93.0]], '正品促销', '0.7986101984977723'],
        [[[70.0, 98.0], [251.0, 98.0], [251.0, 125.0], [70.0, 125.0]], '大桶装更划算', '0.7368737288883754'],
        ...
    ]
    ```

=== "分类 + 识别"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path, use_det=False, use_cls=True, use_rec=True)
    print(result)
    print(elapse)
    ```

    返回值`result`: `List[List[str, float]]` (`[识别的文本, 置信度]`)
    ```python linenums="1"
    [
        ['韩国小馆', 0.7992169380187988],
        ...
    ]
    ```

=== "检测 + 分类 + 识别"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'

    # 默认都为True
    result, elapse = engine(img_path, use_det=True, use_cls=True, use_rec=True)
    print(result)
    print(elapse)
    ```

    返回值`result`: `List[List[float], str, float]` (`[[左上, 右上, 右下, 左下], 文本内容, 置信度]`)
    ```python linenums="1"
    [
        [[[9.0, 2.0], [321.0, 11.0], [318.0, 102.0], [6.0, 93.0]], '正品促销', '0.7986101984977723'],
        [[[70.0, 98.0], [251.0, 98.0], [251.0, 125.0], [70.0, 125.0]], '大桶装更划算', '0.7368737288883754'],
        ...
    ]
    ```
