---
title: RapidOCR与PaddleOCR速度对比
date: 2026-02-06
authors: [SWHL]
slug: rapidocr-vs-paddleocr
categories:
  - General
comments: true
---

同环境下，比较RapidOCR与PaddleOCR速度。

<!-- more -->

## 引言

一直想做一个benchmark，类似于YOLO仓库下那种，一键可以快速比较不同推理引擎在同一环境下的表现。还没来得及。

这不这几天又有小伙伴问到推理速度问题，我想着想写一篇简单评测的博客吧！

评测的最基本要求是：保持变量单一。最起码要用相同环境，明确的所用的各个库的版本，方便他人复现。

## 运行环境

本来我尝试在百度星河社区，新建一个项目来评测的。无奈于星河社区中网速是在不给力，下载模型都是问题。

后来我尝试在Google Colab上评测，遇到了一个更加奇怪的问题：`RuntimeError: PDX has already been initialized. Reinitialization is not supported.`。网上搜索好久，尝试更改Colab版本，也没能成功。

因此，先在自己笔记本上跑一下了。

- 操作系统：macOS Tahoe 26.2 (Apple M2)
- Python: 3.10.0
- 其他依赖包：

    ```bash linenums="1"
    rapidocr==3.6.0
    onnxruntime==1.22.0
    paddleocr==3.4.0
    paddlepaddle==3.1.0
    paddlex==3.4.1
    numpy==2.2.6
    opencv-python==4.11.0.86
    ```

## 运行代码

测试图：

![alt text](./images/8.png)

```python linenums="1"
# test_ocr.py
import time

from paddleocr import PaddleOCR
from rapidocr import EngineType, LangDet, LangRec, ModelType, OCRVersion, RapidOCR

paddle_ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="PP-OCRv5_mobile_rec",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    device="cpu",
)

ort_engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.CH,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV5,
        "Rec.engine_type": EngineType.ONNXRUNTIME,
        "Rec.lang_type": LangRec.CH,
        "Rec.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV5,
    }
)

img_path = "8.png"

for _ in range(10):
    s = time.perf_counter()

    result = ort_engine(img_path, use_det=True, use_rec=True, use_cls=True)

    s1 = time.perf_counter()

    result = paddle_ocr.predict(img_path)
    s2 = time.perf_counter()

    print(f"rapidocr + onnxruntime: {s1 - s} seconds")
    print(f"paddleocr: {s2 - s1} seconds")
    print("-" * 30)
```

我这里的输出日志：

```bash linenums="1"
$ python test_ocr.py

Checking connectivity to the model hosters, this may take a while. To bypass this check, set `PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK` to `True`.
Creating model: ('PP-OCRv5_mobile_det', None)
Model files already exist. Using cached files. To redownload, please delete the directory manually: `/Users/joshuawang/.paddlex/official_models/PP-OCRv5_mobile_det`.
/Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/paddle/utils/cpp_extension/extension_utils.py:715: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
Creating model: ('PP-OCRv5_mobile_rec', None)
Model files already exist. Using cached files. To redownload, please delete the directory manually: `/Users/joshuawang/.paddlex/official_models/PP-OCRv5_mobile_rec`.
[INFO] 2026-02-06 09:24:17,252 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,313 [RapidOCR] download_file.py:60: File exists and is valid: /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_mobile_det.onnx
[INFO] 2026-02-06 09:24:17,313 [RapidOCR] main.py:53: Using /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_mobile_det.onnx
[INFO] 2026-02-06 09:24:17,363 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,365 [RapidOCR] download_file.py:60: File exists and is valid: /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
[INFO] 2026-02-06 09:24:17,365 [RapidOCR] main.py:53: Using /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
[INFO] 2026-02-06 09:24:17,383 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,395 [RapidOCR] download_file.py:60: File exists and is valid: /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_rec_mobile_infer.onnx
[INFO] 2026-02-06 09:24:17,395 [RapidOCR] main.py:53: Using /Users/joshuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_rec_mobile_infer.onnx
rapidocr + onnxruntime: 1.2242828749585897 seconds
paddleocr: 1.929985583992675 seconds
------------------------------
rapidocr + onnxruntime: 1.2603289580438286 seconds
paddleocr: 1.7652709999820217 seconds
------------------------------
rapidocr + onnxruntime: 1.005459832958877 seconds
paddleocr: 1.7479169589933008 seconds
------------------------------
rapidocr + onnxruntime: 1.1810064999153838 seconds
paddleocr: 1.7950388330500573 seconds
------------------------------
rapidocr + onnxruntime: 1.1056153749814257 seconds
paddleocr: 1.787790665985085 seconds
------------------------------
rapidocr + onnxruntime: 1.1712775829946622 seconds
paddleocr: 1.7998320840997621 seconds
------------------------------
rapidocr + onnxruntime: 1.0146936250384897 seconds
paddleocr: 1.7702880839351565 seconds
------------------------------
rapidocr + onnxruntime: 0.9471907910192385 seconds
paddleocr: 1.7666469590039924 seconds
------------------------------
rapidocr + onnxruntime: 0.93433570896741 seconds
paddleocr: 1.7583980000345036 seconds
------------------------------
rapidocr + onnxruntime: 0.9334082090063021 seconds
paddleocr: 1.762385250069201 seconds
------------------------------
```

## 写在最后

以上还是太粗糙，仅供参考哈！后续我这会搞个更加严谨一些的。没有捧谁踩谁意思哈！
