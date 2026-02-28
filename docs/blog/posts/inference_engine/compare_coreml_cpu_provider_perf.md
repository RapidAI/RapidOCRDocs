---
title: 基于 ONNX Runtime 来看 CoreML Provider 和 CPU Provider 在 RapidOCR 表现
date: 2026-02-28
authors: [SWHL]
slug: coreml-vs-cpu-provider-onnxruntime-rapidocr
categories:
  - 推理引擎
comments: true
hide:
  - toc
links:
  - 使用不同推理引擎: install_usage/rapidocr/how_to_use_infer_engine.md
---

记录 ONNX Runtime 在 MacBook Pro M2 上 CoreML Provider 和 CPU Provider 表现，包括速度和精度。

<!-- more -->

## 引言

首先感谢Github [@HighDoping](https://github.com/HighDoping) 小伙伴的PR [#634](https://github.com/RapidAI/RapidOCR/pull/634)。小伙们不仅高质量实现了相关代码，还给出了贴心提示：

> CoreML support should be considered experimental due to compatibility issues with certain models (incompatible with PPOCRv5).
Using the ModelFormat: "NeuralNetwork" yields performance improvements but results in significant accuracy loss.
>
> 由于某些型号的兼容性问题（与 PPOCRv5 不兼容），CoreML 支持应被视为实验性。使用模型格式：“NeuralNetwork”能带来性能提升，但会显著丢失准确性。

下面的测试结果使用的是小伙伴在 PR 中给的默认配置：

```yaml linenums="1"
coreml_ep_cfg:
    ModelFormat: "MLProgram"
    MLComputeUnits: "ALL"
    RequireStaticInputShapes: 0
    EnableOnSubgraphs: 0
    SpecializationStrategy: "FastPrediction"
    ProfileComputePlan: 0
    AllowLowPrecisionAccumulationOnGPU: 0
    ModelCacheDirectory: "/tmp/RapidOCR"
```

完整的测试代码已经放在 [Gist](https://gist.github.com/SWHL/fc0501d281e3735ff154d7491d8e1a9a) 中。

## 测试环境

- OS: macOS Sequoia 15.3 (MacBook Pro M2)
- Python: 3.10.0
- rapidocr: [commit 7c880e](https://github.com/RapidAI/RapidOCR/commit/7c880e8ac970f9299af5f29e83e76a02c610d110) 代码
- ONNX Runtime: 1.22.0

## 测试方法

本次测试使用标准的 benchmark 数据集，分别对检测（Det）和识别（Rec）模型进行评估：

- **检测模型**：使用 `SWHL/text_det_test_dataset` 数据集
- **识别模型**：使用 `SWHL/text_rec_test_dataset` 数据集

对于每个模型，分别测试 ONNX Runtime 的两种 Execution Provider：

- **CPUProvider**：CPU 推理引擎（默认）
- **CoreMLProvider**：Apple 的 CoreML 硬件加速引擎

测试指标包括：

- **精度指标**：Precision、Recall、H-mean（检测）；ExactMatch、CharMatch（识别）
- **速度指标**：平均每张图片的推理时间（毫秒）

## 检测模型（Det）测试结果

| Exp | 模型 | 推理框架 | 推理引擎 | Precision↑ | Recall↑ | H-mean↑ | Elapse↓(ms) |
|-----|------|----------|----------|------------|---------|---------|-------------|
| 1 | PP-OCRv4 Det | ONNX Runtime | CPUProvider | 0.8595 | 0.8434 | 0.8514 | 172.63 |
| 2 | PP-OCRv4 Det | ONNX Runtime | CoreMLProvider | 0.8595 | 0.8434 | 0.8514 | 597.07 |
| 3 | PP-OCRv5 Det Mobile | ONNX Runtime | CPUProvider | 0.7861 | 0.8266 | 0.8058 | 163.04 |
| 4 | PP-OCRv5 Det Mobile | ONNX Runtime | CoreMLProvider | 0.7861 | 0.8266 | 0.8058 | 1100.35 |

从表格可以看出：

- **精度方面**：CoreMLProvider 和 CPUProvider 的精度**完全一致**，说明模型转换和推理过程没有损失精度
- **速度方面**：
    - PP-OCRv4 Det: CPUProvider (172.63ms) vs CoreMLProvider (597.07ms) - **CoreML 慢 3.46 倍**
    - PP-OCRv5 Det Mobile: CPUProvider (163.04ms) vs CoreMLProvider (1100.35ms) - **CoreML 慢 6.75 倍**

## 识别模型（Rec）测试结果

| Exp | 模型 | 推理框架 | 推理引擎 | ExactMatch↑ | CharMatch↑ | Elapse↓(ms) |
|-----|------|----------|----------|-------------|------------|-------------|
| 1 | PP-OCRv4 Rec Mobile | ONNX Runtime | CPUProvider | 0.8290 | 0.9432 | 17.40 |
| 2 | PP-OCRv4 Rec Mobile | ONNX Runtime | CoreMLProvider | 0.8290 | 0.9432 | 55.00 |
| 3 | PP-OCRv5 Rec Mobile | ONNX Runtime | CPUProvider | 0.7355 | 0.9177 | 18.50 |
| 4 | PP-OCRv5 Rec Mobile | ONNX Runtime | CoreMLProvider | 0.7355 | 0.9177 | 259.70 |

从表格可以看出：

- **精度方面**：CoreMLProvider 和 CPUProvider 的精度**完全一致**
- **速度方面**：
    - PP-OCRv4 Rec Mobile: CPUProvider (17.40ms) vs CoreMLProvider (55.00ms) - **CoreML 慢 3.16 倍**
    - PP-OCRv5 Rec Mobile: CPUProvider (18.50ms) vs CoreMLProvider (259.70ms) - **CoreML 慢 14.04 倍**

## 测试结论

通过上述测试可以得出以下结论：

1. **精度保持**：CoreMLProvider 在所有测试模型上都能保持与 CPUProvider 完全相同的精度，没有任何精度损失
2. **速度表现**：**出乎意料的是**，CoreMLProvider 的推理速度明显慢于 CPUProvider
   - 检测模型：CoreML 慢 3.46-6.75 倍
   - 识别模型：CoreML 慢 3.16-14.04 倍
   - PP-OCRv5 系列模型受影响最严重
3. **性能分析**：CoreML 性能较差可能是由于以下原因：
   - 模型格式转换和缓存的开销
   - CoreML 对 PP-OCR 系列模型架构的优化不足
   - 首次推理的预热时间较长
   - Apple Silicon 的 Neural Engine 可能对这类 OCR 模型架构支持不够优化

## 使用建议

基于测试结果，我们给出以下建议：

- **macOS 平台推荐**：目前在 macOS 平台上**推荐使用默认的 CPUProvider**，可以获得更好的推理性能
- **保留 CoreML 支持**：虽然当前性能不佳，但 CoreML 能够保持精度，未来 Apple 可能会优化对这类模型的支持
- **测试范围**：本次测试仅在 MacBook Pro M2 上进行，不同设备和 macOS 版本可能有不同表现

## 配置方法

如果你想尝试 CoreMLProvider，可以通过以下方式配置：

```python
from rapidocr import RapidOCR

# 使用 CoreMLProvider
engine = RapidOCR(params={
    "EngineConfig.onnxruntime.use_coreml": True,
})

# 使用默认 CPUProvider（推荐）
engine = RapidOCR()
```

更多推理引擎的使用方法请参考：[使用不同推理引擎](install_usage/rapidocr/how_to_use_infer_engine.md)

## 备注

欢迎大家在不同的 macOS 设备和环境下进行测试，并反馈结果。如果你有任何问题或建议，欢迎在 [GitHub Issues](https://github.com/RapidAI/RapidOCR/issues) 中讨论。
