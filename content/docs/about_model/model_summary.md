---
weight: 30
date: "2023-09-29"
draft: false
author: "SWHL"
title: "不同版本模型之间比较"
icon: "model_training"
toc: true
description: ""
katex: true
---

### 各个版本ONNX模型效果对比(仅供参考)
{{< alert text="以下测试结果均在自己构建测试集上评测所得，不代表在其他测试集上结果也是如此。"/>}}

#### 文本检测模型
{{< alert text="以下表格中推理时间是基于MacBook Pro M1运行所得，不同机器会有差别，请侧重查看彼此之间的比较。"/>}}

- 评测采用的是[TextDetMetric库](https://github.com/SWHL/TextDetMetric) + [文本检测测试集](https://www.modelscope.cn/datasets/liekkas/text_det_test_dataset/summary)，详情可以移步[AI Studio](https://aistudio.baidu.com/projectdetail/6679889?sUid=57084&shared=1&ts=1693054678460)运行查看。
- 指标计算都是在以下参数下计算得来，差别仅在于模型文件不同。
  <details>

  ```yaml {linenos=table}
  pre_process:
      DetResizeForTest:
          limit_side_len: 736
          limit_type: min
      NormalizeImage:
          std: [0.229, 0.224, 0.225]
          mean: [0.485, 0.456, 0.406]
          scale: 1./255.
          order: hwc
      ToCHWImage:
      KeepKeys:
          keep_keys: ['image', 'shape']

  post_process:
      thresh: 0.3
      box_thresh: 0.5
      max_candidates: 1000
      unclip_ratio: 1.6
      use_dilation: true
      score_mode: "fast"
  ```
  </details>

|  模型  | 模型大小| Precision | Recall | H-mean   | Speed(s/img) |
| :---------------------------------: | :----------------: | :-------: | :----: | :----: | :------ |
|     ch_PP-OCRv4_det_infer.onnx      |     4.5M      |  0.6958   | 0.8608 | 0.7696 |   0.6176   |
| ch_PP-OCRv4_det_server_infer.onnx |    108M      |  0.7070   | 0.9330 | **0.8044** |   13.9348   |
||||||
|     ch_PP-OCRv3_det_infer.onnx      |     2.3M      |  0.7056   | 0.8402 | 0.7671 |   0.4047  |
||||||
|     ch_PP-OCRv2_det_infer.onnx      |     2.2M      |  0.7850   | 0.8093 | **0.7970** |   0.3441   |
| ch_ppocr_server_v2.0_det_infer.onnx |     47M      |  0.6736   | 0.8402 | 0.7477 |   2.6560   |

#### 文本识别模型
- 测试集: 自己构建`中英文(168个)`
- 输入Shape:
  - v2: `[3, 32, 320]`
  - v3~v4: `[3, 48, 320]`

|                模型                  | 对应PaddleOCR分支|  模型大小  |    Exact Match   |   Char Match    | Score |Speed(s/img)  |
| :---------------------------: |:--:| :--------------:    | :-------: | :--------------: | :-------------: | :--: |
|ch_PP-OCRv4_rec_infer.onnx | release/v2.7      |       10M        |      0.5655      |     0.9261      |   0.7458   | 0.0218 |
| ch_PP-OCRv4_rec_server_infer.onnx | release/v2.7      |  86M  |        0.6310      |     0.9382      | **0.7846**   | 0.1622 |
||||||||
|     ch_PP-OCRv3_rec_infer.onnx | release/v2.6      |       10M         |     0.5893      |     0.9209      |  **0.7551**   |  0.0183 |
||||||||
|     ch_PP-OCRv2_rec_infer.onnx | release/v2.3     |      8.0M        |       0.4881      |     0.9029      | 0.6955   | 0.0193 |
| ch_ppocr_mobile_v2.0_rec_infer.onnx | release/v2.0 |      4.3M        |        0.5595      |     0.8979      | 0.7287   |0.0045  |

#### 指标说明

{{< tabs tabTotal="3">}}
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
{{% tab tabName="Score(两者综合)" %}}

$$
Score = \frac{1}{2}(Exact\ Match + Char\ Match)
$$

{{% /tab %}}
{{< /tabs >}}
