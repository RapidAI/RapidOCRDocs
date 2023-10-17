---
weight: 3451
lastmod: "2023-10-17"
draft: false
author: "SWHL"
title: "如何更换其他检测和识别模型？"
icon: "code"
toc: true
description: ""
---

#### 引言
`rapidocr`系列库中默认打包了轻量版的中英文检测和识别模型，这种配置可以覆盖到大部分场景。但是也总会有一些其他场景，要用到其他检测和识别模型。

这一点，在设计接口时，已经做了考虑，留出了接口，只是没有专门博客来介绍这个事情。

这个博客就是以如何更换`rapidocr_onnxruntime`的识别模型为英文和数字的识别模型为例做讲解。其他模型同理。



