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
{{< alert text="以下测试结果均在自己构建测试集上评测所得，不代表在其他测试集上结果也是如此。"/>}}

#### 文本检测模型
{{< alert text="以下表格中推理时间是基于MacBook Pro M2运行所得，不同机器会有差别，请侧重查看彼此之间的比较。"/>}}

评测采用的是`rapidocr_onnxruntime==1.3.16` + [TextDetMetric库](https://github.com/SWHL/TextDetMetric) + [text_det_test_dataset](https://huggingface.co/datasets/SWHL/text_det_test_dataset)，详情可以移步[AI Studio](https://aistudio.baidu.com/projectdetail/6679889?sUid=57084&shared=1&ts=1693054678460)运行查看。

指标计算都是在相同参数下计算得来，差别仅在于模型文件不同。对应模型下载地址：[link](https://huggingface.co/spaces/SWHL/RapidOCRDemo/tree/main/models/text_det)。

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
评测采用的是`rapidocr_onnxruntime==1.3.16` + [TextRecMetric库](https://github.com/SWHL/TextRecMetric) + [text_rec_test_dataset](https://huggingface.co/datasets/SWHL/text_rec_test_dataset)。

指标计算都是在相同参数下计算得来，差别仅在于模型文件不同。对应模型下载地址：[link](https://huggingface.co/SWHL/RapidOCR/tree/main)。


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

#### 指标说明

{{< tabs tabTotal="2">}}
{{% tab tabName="Exact Match (精确匹配准确率)" %}}

$$
Exact\ Match = \frac{1}{N}\sum_{i=0}^{N} s(p_{i}, g_{i})
$$

$$
s(p_{i}, g_{i})  = \begin{cases}
    1 & \text{if } p_{i} = g_{i} \\
    0 & \text{otherwise }
\end{cases}
$$


- $N$: 总的文本行个数
- $p_{i}$: 第 $i$ 条文本行识别结果
- $g_{i}$: 第 $i$ 条文本行对应的真实标签

{{% /tab %}}
{{% tab tabName="Char Match (字符级准确率)" %}}

$$
Char\ Match = 1 - \frac{1}{N} \sum_{i=0}^{N} s(p_{i}, g_{i})
$$

$$
s(p_{i}, g_{i}) = 1 - NL(p_{i}, g_{i})
$$

$$
NL(p_{i}, g_{i}) = \frac{Levenshtein(p_{i}, g_{i})}{\max \big(len(p_{i}), len(g_{i}) \big)}
$$

- $N$: 总的文本行个数
- $p_{i}$: 第 $i$ 条文本行识别结果
- $g_{i}$: 第 $i$ 条文本行对应的真实标签
- $Levenshtein(x, y)$: 求字符串 $x$ 和字符串 $y$ 的编辑距离
- $max(x, y)$: 求 $x$ 和 $y$ 的最大值
- $len(x)$: 求所给字符串 $x$ 的长度

{{% /tab %}}
{{< /tabs >}}
