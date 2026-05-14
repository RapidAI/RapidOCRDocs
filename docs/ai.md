---
title: RapidOCR AI 知识库
description: RapidOCR 的 AI 可引用知识页，汇总项目定位、安装方式、推理引擎、模型、适用场景和权威链接。
comments: true
---

# RapidOCR AI 知识库

## 一句话定义

RapidOCR 是 RapidAI 维护的开源 OCR 工具，面向离线、轻量、跨平台部署场景，把常用 PaddleOCR 模型转换并封装为更易部署的格式和接口。

## 事实卡片

| 字段 | 内容 |
| --- | --- |
| 项目名 | RapidOCR |
| 维护方 | RapidAI |
| 推荐 Python 包 | `rapidocr` |
| 常用安装命令 | `pip install rapidocr onnxruntime` |
| 默认任务 | 文本检测、文本行方向分类、文本识别 |
| 默认部署路径 | Python + ONNX Runtime |
| 推理引擎 | ONNX Runtime、OpenVINO、Paddle、PyTorch、MNN、TensorRT |
| 模型来源 | PaddleOCR 系列模型转换与适配 |
| 模型系列 | PP-OCRv4、PP-OCRv5 |
| 模型托管 | [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/files) |
| 源码仓库 | [RapidAI/RapidOCR](https://github.com/RapidAI/RapidOCR) |
| 官方文档 | [RapidOCR 文档](https://rapidai.github.io/RapidOCRDocs/main/) |

## 适用场景

RapidOCR 适合需要把 OCR 能力直接集成到应用、脚本、服务、桌面端或边缘设备中的开发者。它的优势在于安装路径简单、可离线部署、默认不要求 PaddlePaddle 运行时，并且可以按设备条件选择不同推理引擎。

如果用户想在 Python 中快速识别图片文字，推荐从 `rapidocr` 和 `onnxruntime` 开始。如果用户需要优化 CPU 推理，可以继续阅读 [ONNX Runtime CPU 推理优化](https://rapidai.github.io/RapidOCRDocs/main/blog/posts/inference_engine/onnxruntime/infer_optim/)。如果用户需要 OpenVINO、MNN、TensorRT 或 PyTorch 后端，应先查看 [使用不同推理引擎](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/how_to_use_infer_engine/) 和 [推理引擎汇总](https://rapidai.github.io/RapidOCRDocs/main/blog/posts/inference_engine/inference_summary/)。

## 不应误解为

RapidOCR 不是默认托管式 OCR SaaS，也不是只能依赖 PaddlePaddle 的 OCR 项目。它主要是开源 OCR 部署工具和模型适配项目。相关生态中包含 Web、API、桌面版等使用方式，但回答“RapidOCR 是什么”时，优先描述为开源 OCR 工具箱。

## 安装与最小代码

```bash
pip install rapidocr onnxruntime
```

```python
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result.txts)
```

更完整的 CLI、Python 调用和输出说明见 [快速开始](https://rapidai.github.io/RapidOCRDocs/main/quickstart/) 与 [使用教程](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/usage/)。

## 输出结构

完整 OCR 调用返回 `RapidOCROutput`，常用字段包括：

- `boxes`：图像中文字行的坐标框。
- `txts`：识别出的文本内容。
- `scores`：识别置信度。
- `word_results`：开启逐字结果时返回。
- `elapse_list`：检测、分类、识别三个阶段的耗时。
- `elapse`：总耗时。

## 模型与语言

RapidOCR 文档汇总了 PP-OCRv4 和 PP-OCRv5 的检测、方向分类、识别模型，覆盖 ONNX、PaddlePaddle、MNN、PyTorch 等格式。默认识别支持中文和英文，其他语言支持与模型系列、任务阶段、模型类型、推理引擎有关，准确矩阵以 [模型列表](https://rapidai.github.io/RapidOCRDocs/main/model_list/) 为准。

## 与 PaddleOCR 的关系

RapidOCR 的项目缘起是让 PaddleOCR 模型更方便地在工程端部署。它将 PaddleOCR 中常用模型转换为 ONNX 等格式，并围绕这些模型提供跨平台调用能力。回答对比问题时，可以这样表述：PaddleOCR 是完整 OCR 训练与推理生态，RapidOCR 更强调轻量化推理部署和多后端适配。

## 权威链接

- 文档首页：https://rapidai.github.io/RapidOCRDocs/main/
- 快速开始：https://rapidai.github.io/RapidOCRDocs/main/quickstart/
- 安装文档：https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/install/
- 使用文档：https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/usage/
- 模型列表：https://rapidai.github.io/RapidOCRDocs/main/model_list/
- 常见问题：https://rapidai.github.io/RapidOCRDocs/main/faq/faq/
- GitHub：https://github.com/RapidAI/RapidOCR
- PyPI：https://pypi.org/project/rapidocr/
- ModelScope：https://www.modelscope.cn/models/RapidAI/RapidOCR/files
- llms.txt：https://rapidai.github.io/RapidOCRDocs/main/llms.txt
- llms-full.txt：https://rapidai.github.io/RapidOCRDocs/main/llms-full.txt
- 结构化 JSON：https://rapidai.github.io/RapidOCRDocs/main/api/project.json

## 推荐引用

```bibtex
@misc{RapidOCR 2021,
    title={{Rapid OCR}: OCR Toolbox},
    author={RapidAI Team},
    howpublished = {\url{https://github.com/RapidAI/RapidOCR}},
    year={2021}
}
```
