---
title: 如何使用DirectML加速推理OCR？
date:
  created: 2024-07-13
  updated: 2024-07-13
authors: [SWHL]
slug: how-to-use-directml
categories:
  - General
comments: true
---

本篇文章主要介绍一下DirectML，以及它在OCR推理过程中是如何使用的。

<!-- more -->

### DirectML是什么？[^microsoft]

直接机器学习 (DirectML) 是机器学习 (ML) 的低级 API。 API 具有常见的（本机 C++、nano-COM）编程接口和 DirectX 12 样式的工作流。 可将机器学习推断工作负荷集成到游戏、引擎、中间件、后端或其他应用程序中。 所有与 DirectX 12 兼容的硬件都支持 DirectML。

硬件加速的机器学习基元（称为“运算符”）是 DirectML 的构建基块。 在这些构建基块中，可以开发纵向扩展、抗锯齿和样式转移等机器学习技术。 例如，使用噪声抑制和超解析度，可以实现令人印象深刻的光线跟踪效果且可以减少每个像素的光线。

可将机器学习推断工作负荷集成到游戏、引擎、中间件、后端或其他应用程序中。 DirectML 提供用户熟悉的（本机C++、nano-COM）DirectX 12 式编程接口和工作流，且受所有 DirectX 12 兼容硬件的支持。 有关 DirectML 示例应用程序（包括精简 DirectML 应用程序的示例），请参阅 [DirectML 示例应用程序](https://learn.microsoft.com/zh-cn/windows/ai/directml/dml-min-app)。

**DirectML 是在 Windows 10 版本 1903 和 Windows SDK 的相应版本中引入的。**

### RapidOCR下如何使用DirectML加速呢？

目前在`rapidocr_onnxruntime>=1.3.23`中，配置了使用DirectML的开关。在满足一定条件后，可以正常使用DirectML加速推理OCR。

要想使用DirectML加速，需要满足以下条件：

- [x] 设备系统要大于等于Windows 10 版本 1903
- [x] 安装`rapidocr_onnxruntime>=1.3.23`版本
- [x] 安装`onnxruntime-directml`包

### 具体使用教程

首先需要确定自己设备是Windows系统，且版本要大于等于Window 10 1903

#### 安装`rapidocr_onnxruntime>=1.3.23`

```bash linenums="1"
pip install rapidocr_onnxruntime
```

#### 安装`onnxruntime-directml`

```bash linenums="1"
# 首先卸载上一步默认安装的onnxruntime
pip uninstall onnxruntime

# 安装onnxruntime-directml
pip install onnxruntime-directml
```

#### Python使用

```python linenums="1"
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_path = 'tests/test_files/ch_en_num.jpg'

# 默认都为False
result, elapse = engine(img_path, det_use_dml=True, cls_use_dml=True, rec_use_dml=True)
print(result)
print(elapse)
```

### Benchmark

由于自己手头没有Windows机器，暂时没有相关测评，可以参考下面Disscussions中评测。

### 有关DirectML的讨论

- [Discussions #175](https://github.com/RapidAI/RapidOCR/discussions/175)

[^microsoft]: <https://learn.microsoft.com/zh-cn/windows/ai/directml/dml>
