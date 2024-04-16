---
weight: 2400
lastmod: "2022-09-29"
draft: false
author: "SWHL"
title: "Benchmark: 不同版本模型之间比较"
icon: "model_training"
toc: true
description: ""
katex: true
---

### 各个版本ONNX模型效果对比(仅供参考)
以下测试结果均在所指定的开源评测集上评测所得，不代表在其他测试集上结果也是如此，仅供参考。

以下表格中推理时间是基于MacBook Pro M2运行所得，不同机器会有差别，请侧重查看彼此之间的比较。

指标计算都是在相同参数下计算得来，差别仅在于模型文件不同。

对应模型下载地址，参见：[link](./download_onnx.md)。


#### 文本检测模型
评测依赖仓库：
- `rapidocr_onnxruntime==1.3.16`: [link](https://github.com/RapidAI/RapidOCR)
- 计算指标库 TextDetMetric: [link](https://github.com/SWHL/TextDetMetric)
- 测试集 text_det_test_dataset: [link](https://huggingface.co/datasets/SWHL/text_det_test_dataset)

详情可以移步[AI Studio](https://aistudio.baidu.com/projectdetail/6679889?sUid=57084&shared=1&ts=1693054678460)运行查看。

|  模型  | 模型大小| Precision | Recall | H-mean   | Speed(s/img) |
| :---------------------------------: | :----------------: | :-------: | :----: | :----: | :------ |
|     ch_PP-OCRv4_det_infer.onnx      |     4.5M      |  0.8301   | 0.8659 | 0.8476 |   0.2256   |
|     ch_PP-OCRv3_det_infer.onnx      |     2.3M      |  0.8021   | 0.8457 | 0.8234 |   0.1660  |
|     ch_PP-OCRv2_det_infer.onnx      |     2.2M      |  0.7579   | 0.8010 | 0.7788 |   0.1570   |
||||||
| ch_PP-OCRv4_det_server_infer.onnx |    108M      |  0.7922   | 0.8533 | 0.8216 |   3.9093   |
| ch_ppocr_server_v2.0_det_infer.onnx |     47M      |  0.7298   | 0.8128 | 0.7691 |   0.7419   |
||||||
|     [damo/cv_proxylessnas_ocr-detection-db-line-level_damo](https://www.modelscope.cn/models/iic/cv_proxylessnas_ocr-detection-db-line-level_damo/summary)      |     5.8M      |  0.7666  | 0.8128 | 0.7890 |   0.6636   |
|     [damo/cv_resnet18_ocr-detection-db-line-level_damo](https://www.modelscope.cn/models/iic/cv_resnet18_ocr-detection-db-line-level_damo/summary)      |     47.2M      |  0.7749  | 0.8167 | 0.7952 |   0.4121   |
|     [damo/cv_resnet18_ocr-detection-line-level_damo](https://modelscope.cn/models/iic/cv_resnet18_ocr-detection-line-level_damo/summary) 未跑通     |     312M      |  -  | - | - |   -  |


不同推理引擎下，效果比较：
|推理引擎|                       模型                       | 模型大小 | Precision | Recall | H-mean | Speed(s/img) |
|:---:| :----------------------------------------------: | :------: | :-------: | :----: | :----: | :----------- |
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
|ch_PP-OCRv4_rec_infer.onnx | release/v2.7      |       10M        |      0.8323      |     0.9355  |  0.6836 |
|ch_PP-OCRv3_rec_infer.onnx | release/v2.6      |       11M        |      0.7097      |     0.8919  |  0.6362 |
|ch_PP-OCRv4_rec_server_infer.onnx | release/v2.7      |       86M        |      0.7968      |     0.9381  |  0.6967 |
|ch_PP-OCRv2_rec_infer.onnx | release/v2.3     |      8.0M        |       0.6387      |     0.8398      | 0.6138|
|ch_ppocr_mobile_v2.0_rec_infer.onnx  |  release/v2.0    |  4.3M  |       0.5323      |     0.7823     | 0.5575|

不同推理引擎下，效果比较：
|           推理引擎           |            模型            | 模型大小 | Exact Match | Char Match | Speed(s/img) |
| :--------------------------: | :------------------------: | :------: | :-------: | :----: | :----: |
| rapidocr_onnxruntime==1.3.16 | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |
|  rapidocr_openvino==1.3.16   | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |
|   rapidocr_paddle==1.3.18    | ch_PP-OCRv4_rec_infer.onnx |   10M   |  0.8323   | 0.9355 | 0.6836 |

- 输入Shape:
  - v2: `[3, 32, 320]`
  - v3~v4: `[3, 48, 320]`
- 不同模型，实例化如下：
  ```python  {linenos=table}
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
