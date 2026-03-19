---
title: RapidOCR 支持 PyTorch MPS 作为计算后端
authors:
  - SWHL
slug: support-pytorch-mps
date: 2026-03-04
categories:
  - 推理引擎
comments: true
hide:
  - toc
links:
  - RapidOCR 支持 MNN 推理引擎: blog/posts/inference_engine/support_mnn_engine.md
---

记录 RapidOCR 支持 PyTorch MPS 作为计算后端的过程。

<!-- more -->

## 引言

衷心感谢 Github [@HighDoping](https://github.com/HighDoping) 提交的 PR [#639](https://github.com/RapidAI/RapidOCR/pull/639)！

相关的测试代码已经放到 [Gist](https://gist.github.com/SWHL/fd6e647337346aa3e268887a4bf179e6)，有需要的小伙伴自取。

## 运行环境¶

- 操作系统：macOS Tahoe 26.2
- 硬件：MacBookPro M2

- Python 环境（3.10.0）：

  ```bash linenums="1"
  rapidocr==3.5.0
  text_det_metric==0.0.8
  text_rec_metric==0.0.1
  datasets==3.6.0
  torch==2.6.0
  ```

## Det 模型对比

| Exp | 模型 | 推理框架 | 推理引擎 | Precision↑ | Recall↑ | H-mean↑ | Elapse↓(ms) |
|-----|------|----------|----------|------------|---------|---------|-------------|
| 1 | ch_PP-OCRv4_det_infer | PyTorch | CPU | 0.8121 | 0.8419 | 0.8267 | 609.64 |
| 2 | ch_PP-OCRv4_det_infer | PyTorch | MPS | 0.8121 | 0.8419 | 0.8267 | 896.91 |
| 3 | ch_PP-OCRv5_mobile_det | PyTorch | CPU | 0.7861 | 0.8266 | 0.8058 | 611.07 |
| 4 | ch_PP-OCRv5_mobile_det | PyTorch | MPS | 0.7861 | 0.8266 | 0.8058 | 273.44 |

## Rec 模型对比

| Exp | 模型 | 推理框架 | 推理引擎 | ExactMatch↑ | CharMatch↑ | Elapse↓(ms) |
|-----|------|----------|----------|-------------|------------|-------------|
| 1 | ch_PP-OCRv4_rec_infer | PyTorch | CPU | 0.8290 | 0.9432 | 101.03 |
| 2 | ch_PP-OCRv4_rec_infer | PyTorch | MPS | 0.8290 | 0.9432 | 163.01 |
| 3 | ch_PP-OCRv5_rec_mobile_infer | PyTorch | CPU | 0.7355 | 0.9177 | 134.61 |
| 4 | ch_PP-OCRv5_rec_mobile_infer | PyTorch | MPS | 0.7355 | 0.9177 | 47.41 |

## 写在最后

从以上结果来看，采用 PyTorch MPS 作为计算后端，模型精度维持在误差允许范围内。尽管如此，推理速度的提升并非总是显著，其表现可能与模型内部的具体实现结构有关。有兴趣的读者，可深入探究其背后的原因。

`rapidocr` 将在 `>=v3.7.0` 集成 PyTorch MPS，欢迎届时使用和反馈。
