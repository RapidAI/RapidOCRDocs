---
comments: true
---

### **\_\_init\_\_** [[SOURCE]](https://github.com/RapidAI/RapidOCR/blob/ac5547345bf6609818dcb0cd9c5af93db3d17a6f/python/rapidocr_onnxruntime/utils/vis_res.py#L20)

```python linenums="1"
def __init__(self, text_score: float = 0.5):
    pass
```

#### 参数

- text_score (*float, optional*): 文本识别结果置信度，值越大，把握越大。取值范围：`[0, 1]`, 默认值是0.5。

### **\_\_call\_\_** [[SOURCE]](https://github.com/RapidAI/RapidOCR/blob/ac5547345bf6609818dcb0cd9c5af93db3d17a6f/python/rapidocr_onnxruntime/utils/vis_res.py#L24)

```python linenums="1"
def __call__(
    self,
    img_content: Union[str, np.ndarray, bytes, Path, Image.Image],
    dt_boxes: np.ndarray,
    txts: Optional[Union[List[str], Tuple[str]]] = None,
    scores: Optional[Tuple[float]] = None,
    font_path: Optional[str] = None,
) -> np.ndarray:
    pass
```

#### 参数

- **img_content** (*Union[str, np.ndarray, bytes, Path, Image.Image]*): 输入图像。
- **dt_boxes** (*np.ndarray*): 文本检测所得文本框。
- **txts** (*Optional[Union[List[str], Tuple[str]]], optional*): 文本框对应的文本内容。默认为`None`。
- **scores** (*Optional[Tuple[float]], optional*): 文本内容对应的置信度，默认为`None`。
- **font_path** (*Optional[str], optional*): 字体文件路径，默认为`None`。

#### 使用示例

可视化识别结果时，需要提供字体文件。下载链接：[link](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/FZYTK.TTF)。

=== "可视化单字坐标"

    ⚠️注意：在`rapidocr_onnxruntime>=1.4.0`中支持。

    ```python linenums="1"
    import cv2

    from rapidocr_onnxruntime import RapidOCR, VisRes

    engine = RapidOCR()
    vis = VisRes()

    image_path = "tests/test_files/ch_en_num.jpg"
    img = cv2.imread(image_path)

    result, elapse_list = engine(img, return_word_box=True)

    (boxes, txts, scores, words_boxes, words, words_scores) = list(zip(*result))
    font_path = "resources/fonts/FZYTK.TTF"

    words_boxes = sum(words_boxes, [])
    words_all = sum(words, [])
    words_scores = sum(words_scores, [])
    vis_img = vis(img, words_boxes, words_all, words_scores, font_path)
    cv2.imwrite("vis_single.png", vis_img)
    ```

    ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.3.25/vis_rec_word_box.png)

=== "只可视化检测"

    ```python linenums="1"
    import cv2

    from rapidocr_onnxruntime import RapidOCR, VisRes

    engine = RapidOCR()
    vis = VisRes()

    image_path = "tests/test_files/ch_en_num.jpg"
    img = cv2.imread(image_path)

    result, elapse_list = engine(img)
    res = vis(img, result)
    cv2.imwrite("only_vis_det.png", res)
    ```

    ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.3.25/only_vis_det.png)

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

    ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.3.25/vis.png)
