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

我一直想做一个类似 YOLO 仓库那样的 benchmark 工具——只需一键，就能在相同环境下快速比较不同推理引擎的性能表现。可惜一直没抽出时间来实现。

最近又有小伙伴问起 OCR 推理速度的问题，索性先写一篇简单的评测博客吧！

做性能评测最基本的原则是：**控制变量**。至少要确保运行环境一致，并明确列出所用各依赖库的具体版本，以便他人能够轻松复现结果。

## 运行环境

最初我尝试在百度星河社区新建一个项目来进行评测，但无奈其网络环境实在不太理想，连模型下载都成了问题。

随后我又转战 Google Colab，却遇到了一个更奇怪的报错：
`RuntimeError: PDX has already been initialized. Reinitialization is not supported.`
我在网上查了很久，也尝试切换了不同的 Colab 运行时版本，但始终没能解决。

于是，这次就先在自己的笔记本上跑一遍吧。

- **操作系统**：macOS Tahoe 26.2（Apple M2）
- **Python 版本**：3.10.0
- **其他依赖包**：

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
Model files already exist. Using cached files. To redownload, please delete the directory manually: `/Users/xxxx/.paddlex/official_models/PP-OCRv5_mobile_det`.
/Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/paddle/utils/cpp_extension/extension_utils.py:715: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
Creating model: ('PP-OCRv5_mobile_rec', None)
Model files already exist. Using cached files. To redownload, please delete the directory manually: `/Users/xxxx/.paddlex/official_models/PP-OCRv5_mobile_rec`.
[INFO] 2026-02-06 09:24:17,252 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,313 [RapidOCR] download_file.py:60: File exists and is valid: /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_mobile_det.onnx
[INFO] 2026-02-06 09:24:17,313 [RapidOCR] main.py:53: Using /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_mobile_det.onnx
[INFO] 2026-02-06 09:24:17,363 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,365 [RapidOCR] download_file.py:60: File exists and is valid: /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
[INFO] 2026-02-06 09:24:17,365 [RapidOCR] main.py:53: Using /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
[INFO] 2026-02-06 09:24:17,383 [RapidOCR] base.py:22: Using engine_name: onnxruntime
[INFO] 2026-02-06 09:24:17,395 [RapidOCR] download_file.py:60: File exists and is valid: /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_rec_mobile_infer.onnx
[INFO] 2026-02-06 09:24:17,395 [RapidOCR] main.py:53: Using /Users/xxxx/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv5_rec_mobile_infer.onnx
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

从结果来看，在当前测试条件下，**RapidOCR + ONNX Runtime 的推理速度整体优于 PaddleOCR（CPU 模式）**。

## 写在最后

以上测试还比较粗糙，仅供初步参考！后续我会整理一个更严谨、更系统的 benchmark 方案。
另外强调一下：**本文无意“捧一踩一”**，只是客观记录一次简单的对比实验。欢迎大家交流指正！
