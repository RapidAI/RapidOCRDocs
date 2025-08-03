---
title: 开源OCR模型对比
date:
  created: 2022-04-16
  updated: 2025-05-26
authors: [SWHL]
categories:
  - 模型相关
comments: true
hide:
  - toc
---

> 本文主要给出了常见开源文本检测和文本识别模型的对比和评测，给大家一个使用参考。

<!-- more -->

#### 引言

目前，开源的项目中有很多OCR模型，但是没有一个统一的基准来衡量哪个是更好一些的。

面对这么多的模型，让我们有些不知所措。为此，最近一段时间以来，我一直想要构建这样一个基准。现在来看，已经初步具有雏形。

为了能更好地评测各个模型效果，收集标注了两个开源评测集：

- [text_det_test_dataset](https://huggingface.co/datasets/SWHL/text_det_test_dataset)
- [text_rec_test_dataset](https://huggingface.co/datasets/SWHL/text_rec_test_dataset)

为了能够方便计算各个模型指标，整理开源了两个计算常用指标的库：

- [TextDetMetric](https://github.com/SWHL/TextDetMetric)
- [TextRecMetric](https://github.com/SWHL/TextRecMetric)

以下结果均是基于以上4个库来的，其指标结果仅仅代表在指定评测集上效果，不代表在其他测试集上结果也是如此，仅供参考。

以下表格中推理时间是基于MacBook Pro M2运行所得，不同机器会有差别，请侧重查看彼此之间的比较。

指标计算都是在相同参数下计算得来，差别仅在于模型文件不同。

对应模型下载地址，参见：[link](./download_onnx.md)。

#### 已知开源OCR项目

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [MMOCR](https://github.com/open-mmlab/mmocr/blob/main/README_zh-CN.md)
- [CnOCR](https://github.com/breezedeus/cnocr)
- [DAVAR-Lab-OCR](https://github.com/hikopensource/DAVAR-Lab-OCR)
- [mindocr](https://github.com/mindspore-lab/mindocr)
- [surya](https://github.com/VikParuchuri/surya)

#### 文本检测模型

评测依赖仓库：

- `rapidocr_onnxruntime==1.3.16`: [link](https://github.com/RapidAI/RapidOCR)
- `rapidocr==2.1.0`: [link](https://github.com/RapidAI/RapidOCR)
- 计算指标库 TextDetMetric: [link](https://github.com/SWHL/TextDetMetric)
- 测试集 text_det_test_dataset: [link](https://huggingface.co/datasets/SWHL/text_det_test_dataset)

详情可以移步[AI Studio](https://aistudio.baidu.com/projectdetail/6679889?sUid=57084&shared=1&ts=1693054678460)运行查看。

|  模型  | 模型大小| Precision | Recall | H-mean   | Speed(s/img) |
| :---------------------------- | :----------------: | :-------: | :----: | :----: | :------ |
|     ch_PP-OCRv5_mobile_det.onnx      |     4.6M      |  0.7861   | 0.8266 | 0.8058 |   -   |
|     ch_PP-OCRv4_det_infer.onnx      |     4.5M      |  0.8301   | 0.8659 | 0.8476 |   0.2256   |
|     ch_PP-OCRv3_det_infer.onnx      |     2.3M      |  0.8021   | 0.8457 | 0.8234 |   0.1660  |
|     ch_PP-OCRv2_det_infer.onnx      |     2.2M      |  0.7579   | 0.8010 | 0.7788 |   0.1570   |
||||||
| ch_PP-OCRv5_server_det.onnx |    84M      |  0.7394   | 0.8442 | 0.7883 |   -   |
| ch_PP-OCRv4_det_server_infer.onnx |    108M      |  0.7922   | 0.8533 | 0.8216 |   3.9093   |
| ch_ppocr_server_v2.0_det_infer.onnx |     47M      |  0.7298   | 0.8128 | 0.7691 |   0.7419   |
||||||
|     [读光-文字检测-轻量化端侧DBNet行检测模型-中英-通用领域](https://www.modelscope.cn/models/iic/cv_proxylessnas_ocr-detection-db-line-level_damo/summary)      |     5.8M      |  0.7666  | 0.8128 | 0.7890 |   0.6636   |
|     [读光-文字检测-DBNet行检测模型-中英-通用领域](https://www.modelscope.cn/models/iic/cv_resnet18_ocr-detection-db-line-level_damo/summary)      |     47.2M      |  0.7749  | 0.8167 | 0.7952 |   0.4121   |
|     [读光-文字检测-行检测模型-中英-通用领域](https://modelscope.cn/models/iic/cv_resnet18_ocr-detection-line-level_damo/summary) 未跑通     |     312M      |  -  | - | - |   -  |

不同推理引擎下，效果比较：

|推理引擎|                       模型                       | 模型大小 | Precision | Recall | H-mean | Speed(s/img) |
|:--| :---- | :------: | :-------: | :----: | :----: | :---- |
|rapidocr_onnxruntime==1.3.16| ch_PP-OCRv4_det_infer.onnx |   4.5M   |  0.8301   | 0.8659 | 0.8476 | 0.2256       |
|rapidocr_openvino==1.3.16| ch_PP-OCRv4_det_infer.onnx |   4.5M   |  0.8339   | 0.8629 | 0.8481 | 0.6447       |
|rapidocr_paddle==1.3.18 | ch_PP-OCRv4_det_infer.onnx|   4.5M   |  0.8301   | 0.8659 | 0.8476 | 0.9924       |

#### 文本识别模型

评测依赖仓库：

- `rapidocr_onnxruntime==1.3.16`: [link](https://github.com/RapidAI/RapidOCR)
- 计算指标库 TextRecMetric: [link](https://github.com/SWHL/TextRecMetric)
- 测试集 text_rec_test_dataset: [link](https://huggingface.co/datasets/SWHL/text_rec_test_dataset)

|                模型                  | 对应PaddleOCR分支|  模型大小  |    Exact Match   |   Char Match     |Speed(s/img)  |
| :----- |:---- | :-----| :-------: | :--- | :--|
|ch_PP-OCRv5_rec_infer.onnx | release/v3.0      |       16M        |      0.7355      |     0.9177  |  0.0713 |
|ch_PP-OCRv4_rec_infer.onnx | release/v2.7      |       10M        |      0.8323      |     0.9355  |  0.6836 |
|ch_PP-OCRv3_rec_infer.onnx | release/v2.6      |       11M        |      0.7097      |     0.8919  |  0.6362 |
|||||||
|ch_PP-OCRv5_rec_server_infer.onnx | release/v3.0      |       81M        |      0.8129      |     0.9431  |  0.1133 |
|ch_PP-OCRv4_rec_server_infer.onnx | release/v2.7      |       86M        |      0.7968      |     0.9381  |  0.6967 |
|ch_doc_PP-OCRv4_rec_server.onnx | release/v2.10      |       94.93M        |      0.8097      |     0.9444  |  0.6836 |
|ch_PP-OCRv2_rec_infer.onnx | release/v2.3     |      8.0M        |       0.6387      |     0.8398      | 0.6138|
|ch_ppocr_mobile_v2.0_rec_infer.onnx  |  release/v2.0    |  4.3M  |       0.5323      |     0.7823     | 0.5575|
|其他OCR |  版本    |  模型大小  |    Exact Match   |   Char Match     |Speed(s/img)  |
|[读光-文字识别-行识别模型-中英-文档印刷体文本领域](https://www.modelscope.cn/models/iic/cv_convnextTiny_ocr-recognition-document_damo/summary)  |  -    |  73M  |       0.5968      |     0.7705     | - |
|[读光-文字识别-行识别模型-中英-通用领域](https://www.modelscope.cn/models/iic/cv_convnextTiny_ocr-recognition-general_damo/summary)  |  -    |  73M  |       0.5839      |     0.7615     | - |
|[读光-文字识别-行识别模型-中英-自然场景文本领域](https://www.modelscope.cn/models/iic/cv_convnextTiny_ocr-recognition-scene_damo/summary)  |  -    |  73M  |       0.5903      |     0.7779     | - |
|[读光-文字识别-轻量化端侧识别模型-中英-通用领域](https://www.modelscope.cn/models/iic/cv_LightweightEdge_ocr-recognitoin-general_damo/summary)  |  -    |  7.4M  |       0.5484      |     0.7515     | - |
|[读光-文字识别-CRNN模型-中英-通用领域](https://www.modelscope.cn/models/iic/cv_crnn_ocr-recognition-general_damo/summary)  |  -    |  46M  |       0.5935      |     0.7671     | - |
|[OFA文字识别-中文-通用场景-base](https://www.modelscope.cn/models/iic/ofa_ocr-recognition_general_base_zh/summary) 未跑通 |  -    |  -  |       -      | -  | - |
|[PHOCRv1](https://github.com/puhuilab/phocr/tree/main)  |  v1.0.3   |  224M  |       0.6452      | 0.7648  | 0.0613 |

不同推理引擎下，效果比较：

|           推理引擎           |            模型            | 模型大小 | Exact Match | Char Match | Speed(s/img) |
| :--- | :------ | :------: | :-------: | :----: | :----: |
| rapidocr_onnxruntime==1.3.16 | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |
|  rapidocr_openvino==1.3.16   | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |
|   rapidocr_paddle==1.3.18    | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |

- 输入Shape:
    - v2: `[3, 32, 320]`
    - v3~v4: `[3, 48, 320]`

- 不同模型，实例化示例如下：

  ```python  linenums="1"
  from rapidocr_onnxruntime import RapidOCR

  # v3 or v4
  engine = RapidOCR(
    rec_model_path="models/ch_PP-OCRv3_rec_infer.onnx",
  )

  # v2
  engine = RapidOCR(
    rec_model_path="models/ch_ppocr_mobile_v2.0_rec_infer.onnx",
    rec_img_shape=[3, 32, 320],
  )
  ```
