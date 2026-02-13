---
title: 支持TensorRT推理引擎
authors: [SWHL]
slug: support-tensorrt-engine
date:
  created: 20260213
categories:
  - 推理引擎
comments: true
---

记录支持TensorRT推理引擎的过程文档。

<!-- more -->

## 引言

首先感谢Github @[LocNgoXuan23](https://github.com/LocNgoXuan23)小伙伴的PR [#623](https://github.com/RapidAI/RapidOCR/pull/623)。有了这个PR，我这也有了抓手来推动支持TensorRT作为推理引擎。

## 运行环境¶

- 操作系统：Docker Ubuntu
- NVIDIA环境：(详细参见：[link](https://gist.github.com/SWHL/0efe902ee469d49fc63d50e297d7fd98) )
    - cuda: 12.2
    - tensorrt: 8.6.1
    - cuda-python: 12.2.0
- Python环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.5.0
  text_det_metric==0.0.8
  text_rec_metric==0.0.1
  datasets==3.6.0
  ```
