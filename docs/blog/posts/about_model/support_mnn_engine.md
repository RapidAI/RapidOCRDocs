---
title: Python版支持MNN推理
date: 20260121
authors: [SWHL]
categories:
  - 模型相关
comments: true
hide:
  - toc
draft: true
---

记录支持MNN推理的过程文档。

<!-- more -->

### 引言

首先感谢[narc1ssus1](https://github.com/narc1ssus1)小伙伴的PR [#613](https://github.com/RapidAI/RapidOCR/pull/613)。有了这个PR，我这也有了着手来推动支持MNN作为推理引擎的动力。

### 支持Det模型

!!! note

    MNN部分主要参考官方文档：https://mnn-docs.readthedocs.io/en/latest/tools/convert.html

#### 安装MNN

```bash linenums="1"
pip install MNN
```

#### 转换ONNX模型

转换命令：

```bash linenums="1"
MNNConvert -f ONNX --modelFile rapidocr/models/ch_PP-OCRv4_det_infer.onnx --MNNModel mnn/ch_PP-OCRv4_det_infer.mnn --bizCode MNN
```

