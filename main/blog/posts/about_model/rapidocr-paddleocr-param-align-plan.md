<!-- more -->

## 引言

在 `rapidocr==1.3.26` 以来，`rapidocr` 库的一些默认参数与 `paddleocr` 默认参数并不相同。在 PaddleOCR 推出了 PP-OCRv5 之后，`rapidocr` 与 `paddleocr` 两者默认模型甚至也不相同。

这就让很多小伙伴有困惑：某些图像上，`rapidocr` 效果好，而另外图像上，`paddleocr` 效果反而更好。

之前版本之所以默认参数不同，是因为两个库出发点不尽相同。`paddleocr` 肯定会集成每次新版本模型，因为新版本模型在百度内部评测肯定要好于上一个版本，他们才会发布新版本的。由于 PaddleOCR 一直没有开源内部评测集，我们看到的好也只能是孤零零的指标而已。我这里就只能在自行构建的评测集上来看新版本模型效果。

`rapidocr` 在一些特殊图像上额外加了一些特殊处理，这也一定程度上导致了两者在某些图像上，效果不同。

在 `rapidocr==3.9.1` 和 `paddleocr==3.7.0` 中，事情迎来了转机。PP-OCRv6 模型在我自建评测集上，效果均好于 PP-OCRv4 和 PP-OCRv5 系列。这就让 `rapidocr` 其默认模型都变为了 PP-OCRv6 small 系列。这就让 `rapidocr` 和 `paddleocr` 两者默认模型一致了，其余不同的地方就在于前后处理了。

接下来，我这会逐一给出不同点，并尽量给出解决方案。

💡 下面的出现的 `rapidocr` 版本是 v3.9.1，`paddleocr` 版本是 v3.7.0。

## 不足之处

- 评测集样本较少，结果可能有偏。
- 结论不够扎实，因为只评测了文本检测这一步，并不能看到将这一步的结果传到后续识别后的指标变化。后续打算出一个端到端的评测集，直接整体评估 OCR pipeline 效果。

## 不同点：文本检测图像归一化值不同

|阶段|库|`std`|`mean`|
|:---|:---|:---|:---|
|文本检测|`rapidocr`|`[ 0.5, 0.5, 0.5 ]`|`[ 0.5, 0.5, 0.5 ]`|
|文本检测|`paddleocr`|`[ 0.229, 0.224, 0.225 ]`|`[ 0.485, 0.456, 0.406 ]`|
|||||
|文本行方向分类|`rapidocr`|`[ 0.5, 0.5, 0.5 ]`|`[ 0.5, 0.5, 0.5 ]`|
|文本行方向分类|`paddleocr`|`[ 0.5, 0.5, 0.5 ]`|`[ 0.5, 0.5, 0.5 ]`|
|||||
|文本识别|`rapidocr`|`[ 0.5, 0.5, 0.5 ]`|`[ 0.5, 0.5, 0.5 ]`|
|文本识别|`paddleocr`|`[ 0.5, 0.5, 0.5 ]`|`[ 0.5, 0.5, 0.5 ]`|

经过阅读源码，总结了上述的异同点。`rapidocr` 为啥选择 0.5，是因为 @郑喜 实践发现 0.5 作为归一化值，整体效果更好一些。当时讨论的 Discussions [#246](https://github.com/RapidAI/RapidOCR/discussions/246#top) 中，我这里的确做了定量实验，的确如此。

从理论上来讲，模型训练和推理，前后处理要保持一致，才是最优的。那么在 PP-OCRv6 场景下，这个结论是否仍然如此呢？为此，我重新设计实验来比较不同图像归一化值，在指标上差异如何？

=== "std和mean为0.5 (默认)"

    ```python linenums="1"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.std": [0.5, 0.5, 0.5],
            "Det.mean": [0.5, 0.5, 0.5],
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "std和mean为PaddleOCR值"

    ```python linenums="1"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.std": [0.229, 0.224, 0.225],
            "Det.mean": [0.485, 0.456, 0.406],
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

|模型|推理库|std|mean|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---|:---|:---|:---|:---|:---|:---|:---|
|PP-OCRv6_small_det| RapidOCR| `[0.229, 0.224, 0.225]` |`[0.485, 0.456, 0.406]`|0.8375|0.835|0.8363|0.2313|
|PP-OCRv6_small_det| RapidOCR| `[0.5, 0.5, 0.5]` |`[0.5, 0.5, 0.5]`|0.854|0.8445|0.8492|0.2267|

经过上述实验，std 和 mean 都设为 0.5，指标会更好。至于原因，不得而知。这一点，我这里后续仍然沿用 0.5 的默认值了。有想要严格对齐的小伙伴，可以自行更改这部分。更改方法：

```python linenums="1"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.std": [0.229, 0.224, 0.225],
        "Det.mean": [0.485, 0.456, 0.406],
    },
)
```

## 不同点：`limit_side_len` 不同

以下来自参数介绍 [文档](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/parameters/)：

> `limit_side_len (float)`: 限制图像边的长度的像素值。默认值为 736。
>
> `limit_type (str)`: 限制图像的最小边长度还是最大边为 `limit_side_len`。示例解释：当 `limit_type=min` 和 `limit_side_len=736` 时，图像最小边小于 736 时，会将图像最小边拉伸到 736，另一边则按图像原始比例等比缩放。

在 `limit_type="min"` 前提下，我这里给出 `limit_side_len` 的具体例子说明：

| 场景编号 | 原图尺寸 (高×宽) | 原图短边 | limit_side_len 配置 | 是否缩放 | 送入模型最终尺寸 (高×宽) | 核心效果说明 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 极小截图 | 50 × 120 | 50 | 64 | 是（50＜64） | 64 × 154 | 仅小幅放大，画面依旧极小，文字糊成块，基本识别不出内容 |
| 极小截图 | 50 × 120 | 50 | 736 | 是（50＜736） | 736 × 1766 | 放大 14.72 倍，文字笔画充分展开，可正常识别文字内容 |
| 中等文档图 | 600 × 1200 | 600 | 64 | 否（600＞64） | 600 × 1200 | 原图输入，速度快，细小文字识别效果一般 |
| 中等文档图 | 600 × 1200 | 600 | 736 | 是（600＜736） | 736 × 1472 | 放大 1.23 倍，分辨率提升，票据、证件小字识别准确率更高 |
| 高清大图 | 1200 × 2400 | 1200 | 64 | 否（1200＞64） | 1200 × 2400 | 原图不变，无缩放计算开销 |
| 高清大图 | 1200 × 2400 | 1200 | 736 | 否（1200＞736） | 1200 × 2400 | 和 64 处理结果完全一致，速度、精度无任何差异 |

现在两个库的参数情况：

|阶段|库|`limit_side_len`|`limit_side_mode`|
|:---|:---|:---|:---|
|文本检测|`rapidocr`|736|`min`|
|文本检测|`paddleocr`|64|`min`|

为了比较 `limit_side_len` 参数值的不同带来的差异，我这里做了控制变量的实验，以 `rapidocr` 库为基准，仅比较更改 `limit_side_len` 值，检测指标变化。

=== "`limit_side_len=736` (默认)"

    ```python linenums="1" hl_lines="11"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.limit_side_len": 736,
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "`limit_side_len=64`"

    ```python linenums="1" hl_lines="11"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.limit_side_len": 64,
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

|阶段|库|`limit_side_len`|`limit_side_mode`|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---|:---|:---|:---|:---|:---|:---|:---|
|文本检测|`rapidocr`|736|`min`|0.854|0.8445|0.8492|0.235|
|文本检测|`rapidocr`|64|`min`|0.8278|0.8079|0.8177|0.165|

从上述实验指标来看，`limit_side_len=736` 是更优的选择。但是从推理速度来看，`limit_side_len=64` 明显更快。我这里后续仍然采用 `limit_side_len=736` 这个值。有需求的小伙伴可以自行指定其他值，指定方法：

```python linenums="1"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.limit_side_len": 64,
    },
)
```

## 不同点：`use_dilation` 不同

以下来自参数 [文档](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/parameters/)：

> `use_dilation (bool)`: 是否使用膨胀。默认为 true。该参数用于将检测到的文本区域做形态学的膨胀处理。

现在两个库的参数情况：

|阶段|库|`use_dilation`|
|:---|:---|:---|
|文本检测|`rapidocr`|`True`|
|文本检测|`paddleocr`|`False`|

同理，关于该参数，我也设置了对比实验，来看指标变化。

=== "`use_dilation=True`（默认）"

    ```python linenums="1" hl_lines="11"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.use_dilation": True,
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

=== "`use_dilation=False`"

    ```python linenums="1" hl_lines="11"
    import cv2
    import numpy as np
    from datasets import load_dataset
    from tqdm import tqdm

    from rapidocr import OCRVersion, RapidOCR

    engine = RapidOCR(
        params={
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.use_dilation": False,
        },
    )

    dataset = load_dataset("SWHL/text_det_test_dataset")
    test_data = dataset["test"]

    content = []
    for i, one_data in enumerate(tqdm(test_data)):
        img = np.array(one_data.get("image"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
        dt_boxes = ocr_results.boxes

        dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
        elapse = ocr_results.elapse

        gt_boxes = [v["points"] for v in one_data["shapes"]]
        content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

    with open("pred.txt", "w", encoding="utf-8") as f:
        for v in content:
            f.write(f"{v}\n")

    from text_det_metric import TextDetMetric

    metric = TextDetMetric()
    pred_path = "pred.txt"
    metric = metric(pred_path)
    print(metric)
    ```

|阶段|库|`use_dilation`|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---|:---|:---|:---|:---|:---|:---|
|文本检测|`rapidocr`|`True`|0.854|0.8445|0.8492|0.198|
|文本检测|`rapidocr`|`False`|0.8278|0.8079|0.8177|0.165|

从上述实验指标来看，`use_dilatio=True` 效果更好，但是推理速度慢了一些。我这里后续仍然采用 `use_dilation=True`。有需求的小伙伴可以自行指定。

```python linenums="1"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.use_dilation": False,
    },
)
```

## 不同点：图像进入检测模型前预处理

这个属于 `rapidocr` 特有，具体源码：[source code](https://github.com/RapidAI/RapidOCR/blob/44e2e900eccf2ad0702030dce9e20f5c5941be39/python/rapidocr/main.py#L281-L287)。

这个对应以下两个参数：（来自 [参数介绍文档](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/parameters/#global)）

> `max_side_len (int)`: 如果输入图像的最大边大于 `max_side_len`，则会按宽高比，将最大边缩放到 `max_side_len`。默认为 2000 px。
>
> `min_side_len (int)`: 如果输入图像的最小边小于 `min_side_len`，则会按宽高比，将最小边缩放到 `min_side_len`。默认为 30 px。

设置这个参数的初衷是限制图像过大或者过小。图像过大，则存在占满机器内存情况，过小则存在文字不清晰。

计划在下个版本（v3.9.2）中，给出开关来开启或关闭这个前处理。默认仍是开启。

```yaml linenums="1" hl_lines="1"
use_preprocess_img: true
min_side_len: 30
max_side_len: 2000
```

## 不同点：图像进入文本检测上下补边

这个属于 `rapidocr` 特有，具体源码：[source code](https://github.com/RapidAI/RapidOCR/blob/44e2e900eccf2ad0702030dce9e20f5c5941be39/python/rapidocr/main.py#L292-L294)。

这个对应以下两个参数：（来自 [参数介绍文档](https://rapidai.github.io/RapidOCRDocs/latest/install_usage/rapidocr/parameters/#global)）

> `min_height (int)` : 图像最小高度（单位是像素），低于这个值时，会触发图像上下补边操作，补边会让文本检测模型更加准确检测到文本行。默认值为 30。
>
> ![](https://github.com/RapidAI/RapidOCR/releases/download/v1.1.0/single_line_text.jpg)
>
> `width_height_ratio (float)`: 如果输入图像的宽高比大于 `width_height_ratio`，则会触发图像上下补边操作，取值为-1 时：不用这个参数. 默认值为 8。

设置这个参数的初衷是某些图像宽度大，高度小。通过图像预先上下补边，尽可能还原文本检测模型训练时图像比例，来达到图像检测更加准确的目的。

在下个版本（v3.9.2）中，给出开关来开启或关闭这个前处理。默认仍是开启。

```yaml linenums="1" hl_lines="1"
use_vertical_padding: true
min_height: 30
width_height_ratio: 8
```

## 总结

要想和 PaddleOCR 参数基本等价，需要按照下面的配置来设置：

```python linenums="1"
from rapidocr import OCRVersion, RapidOCR

engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.std": [0.229, 0.224, 0.225],
        "Det.mean": [0.485, 0.456, 0.406],
        "Det.limit_side_len": 64,
        "Det.use_dilation": False,
    },
)
```

从以上效果来看，RapidOCR 当前参数基本是更优一些。当然不排除某些图像，情况不同。所以小伙伴在使用时，效果不好时，可以多调调这些参数。
