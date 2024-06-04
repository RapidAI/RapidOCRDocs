---
comments: true
---

### 初始化
[RapidOCR](https://github.com/RapidAI/RapidOCR/blob/a981e21743f03d9bbfbe596974123fecfe8a7d62/python/rapidocr_onnxruntime/main.py#L19)类是主类，其初始化函数如下：
```python linenums="1"
class RapidOCR:
    def __init__(self, config_path: Optional[str] = None, **kwargs):
        pass
```

支持两种自定义传参数的方案，下面分别详细说明：
#### 以`config.yaml`方式
1. 找到`rapidocr_onnxruntime`安装目录下的`config.yaml`文件，可以通过`pip show rapidocr_onnxruntime`找到其安装路径。
2. 将`config.yaml`拷贝出来，放到当前运行目录下
3. 按需自定义参数修改即可，具体参数解释，参见[config.yaml](./config_yaml.md)
    ```python linenums="1"
    engine = RapidOCR(config_path="your.yaml")
    ```

#### (推荐) 以具体参数传入
参数基本和[config.yaml](./config_yaml.md)中对应，只是个别名称有所区别。

!!! note

    以下参数均有默认值，可以不传入任何参数，直接初始化使用即可。<br/>`intra_op_num_threads`和`inter_op_num_threads`仅是`rapidocr_onnxruntime`版本下的，其他推理引擎，请参见各自源码"

```python linenums="1"
class RapidOCR:
    def __init__(
        self,
        text_score: float = 0.5,
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
        rec_use_dml bool = False,
        rec_model_path: Optional[str] = None,
        rec_img_shape: List[int] = [3, 48, 320],
        rec_batch_num: int = 6,
        intra_op_num_threads: int = -1,
        inter_op_num_threads: int = -1,
    ):
        pass

engine = RapidOCR()

res, elapse = engine(img, use_det=True, use_cls=True, use_rec=True)
```

### 输入
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

### 输出
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


### 可视化查看
为了便于查看检测和识别结果，该库中封装了[`VisRes`](https://github.com/RapidAI/RapidOCR/blob/a981e21743f03d9bbfbe596974123fecfe8a7d62/python/rapidocr_onnxruntime/utils.py#L351)类，可借助该类快速可视化查看结果。可视化识别结果时，需要提供字体文件。下载链接：[link](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/FZYTK.TTF)


=== "只可视化检测"

    ```python linenums="1"
    import cv2

    from rapidocr_onnxruntime import RapidOCR, VisRes

    engine = RapidOCR()
    vis = VisRes()

    image_path = "tests/test_files/ch_en_num.jpg"
    img = cv2.imread(image_path)

    result, elapse_list = engine(img)
    boxes, txts, scores = list(zip(*result))
    res = vis(img, boxes)
    cv2.imwrite("only_vis_det.png", res)
    ```

=== "可视化检测和识别"

    ```python linenums="1"
    import cv2

    from rapidocr_onnxruntime import RapidOCR, VisRes

    engine = RapidOCR()
    vis = VisRes()

    image_path = "tests/test_files/ch_en_num.jpg"
    img = cv2.imread(image_path)

    result, elapse_list = engine(img)
    boxes, txts, scores = list(zip(*result))

    font_path="resources/fonts/FZYTK.TTF"
    res = vis(img, boxes, txts, scores, font_path)
    cv2.imwrite("vis_det_rec.png", res)
    ```
