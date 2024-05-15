---
weight: 3800
lastmod: "2022-10-08"
draft: false
author: "SWHL"
title: "rapidocr_onnxruntime/openvino"
icon: "update"
toc: true
description: ""
---

#### 🛠️2024-05-15 v1.3.19 update:
- 因为DirectML受支持设备限制，因此将DirectML作为一个选项写入配置文件，选择性调用
- 在Windows平台仍然恢复到v1.3.18前，默认安装`onnxruntime`库。如DirectML可用，且显式指定时，需要手动安装。
- 相关讨论：[PR #178]() [Discussion #175](https://github.com/RapidAI/RapidOCR/discussions/175)

#### 🧚🏻‍♀️2024-05-12 v1.3.18 update:
- Merge [PR #176](https://github.com/RapidAI/RapidOCR/pull/176)
- 支持python 3.12

#### 🔥2024-04-19 v1.3.17 update:
- Merge [PR](https://github.com/RapidAI/RapidOCR/pull/171)
- 修复[issue #170](https://github.com/RapidAI/RapidOCR/issues/170)

#### 📘2024-04-07 v1.3.16 update:
修复[issue #161](https://github.com/RapidAI/RapidOCR/issues/161)

#### 🍿2024-03-07 v1.3.15 update:
- 修复 [issue #158](https://github.com/RapidAI/RapidOCR/issues/158)
- 增加三个推理引擎（onnxruntime、openvino，paddlepaddle）初始化RapidOCR类，指定线程数的参数

#### 🎂2024-03-05 v1.3.14 update:
添加可使用的CPU核心数，包括三个推理引擎，onnxruntime/OpenVINO/PaddlePaddle

#### 🔖2024-02-28 v1.3.13 update:
- 优化`LoadImage`类，添加对输入`PIL.Image.Image`的支持
- 修复不同输入类型下，图像通道顺序不同的问题

#### 🍉2024-02-27 v1.3.12 update:
可视化函数适配Pillow v9和v10两个版本，自动根据各个版本情况，来选择相应获得char大小的函数

#### ♥️2024-02-04 v1.3.11 update:
Merge [PR #151](https://github.com/RapidAI/RapidOCR/pull/151) by [LWQ2EDU](https://github.com/LWQ2EDU)
- 添加自动padding策略：当传入图像小于`min_height`或者`>width_height_ratio`时，会触发自动padding图像，后续再进入检测。
- ⚠️注意：padding值多少？[当前值](https://github.com/RapidAI/RapidOCR/blob/65369c41f0f04266461e5e9dd81a31ca8c08540d/python/rapidocr_onnxruntime/main.py#L116)是一个权衡设置，大家可根据具体使用场景，自定设置合适值。

#### 🌈2024-01-30 v1.3.10 update:
- 修复`get_boxes_img_without_det` [bug](https://github.com/RapidAI/RapidOCR/pull/150) by [AuroraWright](https://github.com/AuroraWright)

#### 🥰2023-12-28 v1.3.9 update:
- 优化rapidocr系列库主函数代码逻辑，便于小伙伴们二次开发
- Merge [PR #141](https://github.com/RapidAI/RapidOCR/pull/141) by [theikkila](https://github.com/theikkila)
- Merge [PR #139](https://github.com/RapidAI/RapidOCR/pull/139) by [debanjum](https://github.com/debanjum)

#### 😜2023-10-25 v1.3.8 update:
- 修复[issue #133](https://github.com/RapidAI/RapidOCR/issues/133)

#### 📡2023-09-21 v1.3.7 update:
- 完善`VisRes`类在终端情况下的使用
- 修复`auto_text_det`的条件错误
#### 🧸2023-09-20 v1.3.6 update:
- 添加`VisRes`类，便于快速可视化结果。详情参见[demo.py](https://github.com/RapidAI/RapidOCR/blob/508beba09af5549e08340da336b0cff4a101e622/python/demo.py)用法
#### 😀2023-09-20 v1.3.5 update:
- Fixed issue [#122](https://github.com/RapidAI/RapidOCR/issues/122)
#### ⏰2023-09-18 v1.3.4 update:
- 优化更新参数部分的函数实现
#### 🧸2023-09-06 v1.3.2 update:
- 修复issue [#116](https://github.com/RapidAI/RapidOCR/issues/116)
#### ⭐2023-08-29 v1.3.1 update:
- 修复issue [#115](https://github.com/RapidAI/RapidOCR/issues/115)
#### 🎉2023-08-26 v1.3.0 update:
- 将PaddleOCR v4版对应的文本检测和文本识别轻量模型转换为onnx，并打包到whl中。
- 接口与`v1.2.x`一致，直接使用即可。
#### 😉2023-07-12 v1.2.12 update:
- 在`rapidocr_onnxruntime`初始化时，添加`det_use_cuda`、`cls_use_cuda`、`rec_use_cuda`参数
- 兼容配置文件方式传入`RapidOCR`类中
- `rapidocr_openvino`同理

#### 🎮2023-03-11 v1.2.2 update:
- 修复实例化python中RapidOCR类传入参数错误

#### 🧢2023-03-07 v1.2.1 update:
- `rapidocr`系列包更新到`v1.2.0`
- 优化python下rapidocr系列包的接口传入参数，支持实例化类时，动态给定各个参数，更加灵活。
- 如果不指定，则用`config.yaml`下的默认参数。
- 具体可参见：[传入参数](https://github.com/RapidAI/RapidOCR/blob/0a603b4e8919386f3647eca5cdeba7620b4988e0/python/README.md#%E6%8E%A8%E8%8D%90pip%E5%AE%89%E8%A3%85%E5%BF%AB%E9%80%9F%E4%BD%BF%E7%94%A8)

#### ⛸2023-02-16 update:
- 优化ocrweb部分代码，可直接pip安装，快速使用，详情参见[README](../ocrweb/README.md)。
- 优化python中各个部分的推理代码，更加紧凑，同时易于维护。

#### 🎉2023-01-21 update:
- \[python\] 添加含有文字的图像方向分类模块，具体参见[Rapid Orientation](../python/rapid_structure/docs/README_Orientation.md)

#### ⚽2022-12-19 update:
- \[python\] 添加表格结构还原模块，具体参见[Rapid Table](../python/rapid_structure/docs/README_Table.md)

#### 🤖2022-12-14 update:
- \[python\] 将配置参数和模型移到模块里面，同时将模型打到whl包内，可以直接pip安装使用，更加方便快捷。
- 详情参见：[README](../python/README.md#推荐pip安装快速使用)

#### 🧻2022-11-20 update:
- \[python\] 添加版面分析部分,支持中文、英文和表格三种版面的检测分析。详情参见:[Rapid Structure](../python/rapid_structure/README.md)部分。

#### 🎃2022-11-01 update:
- 添加Hugging Face Demo, 增加可以调节超参数的功能，详情可访问[Hugging Face Demo](https://huggingface.co/spaces/SWHL/RapidOCRDemo)

#### 🚩2022-10-01 udpate:
- 修复python部分下一些较小bugs
- merge来自[AutumnSun1996](https://github.com/AutumnSun1996)的[OCRWeb实现的多语言部署](https://github.com/RapidAI/RapidOCR/pull/46)demo，详情参见：[ocrweb_mutli-README](../ocrweb_multi/README.md)
- 添加onnxruntime-gpu推理速度较慢于CPU的问题说明，详情参见：[onnxruntime-gpu版相关说明](../python/README.md#onnxruntime-gpu版相关说明)

#### 🛴2022-09-01 update:
- 由于openvino发布了2022.2.0.dev20220829版本，该版本解决了`cls`部分模型推理的问题。至此，基于openvino的rapidocr完成了统一，全部由openvino推理引擎完成。
- 详细使用方法参见：[python/README](../python/README.md#源码使用步骤)

#### 🧸2022-08-17 update:
- python/ocrweb部分 v1.1.0发布，详情参见[v1.1.0](https://github.com/RapidAI/RapidOCR/releases/tag/v1.1.0)

#### 🕶2022-08-14 update:
- ocrweb部分增加以API方式部署调用的功能，可以通过发送POST请求，来获得OCR识别结果。
- 详情参见：[API方式调用](../ocrweb/README.md#以api方式运行和调用)

#### ✨2022-07-07 update:
- 修复python版中v3 rec推理bug，并将v3 rec与v2 rec合并为同一套推理代码，更加简洁和方便
- 添加python模块下的单元测试
- 该页面添加[致谢模块](../README.md#致谢)，感谢为这个项目作出贡献的小伙伴。

#### 😁2022-07-05 update:
- 添加对单行文本的处理能力，对于单行文本，可自行设定阈值，不过检测模块，直接识别即可。详情参见[README](./python/README.md#configyamlconfigyaml中常用参数介绍)
- 优化python部分代码逻辑，更优雅简洁。

#### 🏝2022-06-30 update:
- python推理部分，增加参数选择使用GPU推理的配置选项，在正确安装`onnxruntime-gpu`版本前提下，可以一键使用（Fix [issue#30](https://github.com/RapidAI/RapidOCR/issues/30)）
- 具体基于GPU的推理情况，需要等我后续整理一下，再更新出来
- 详情参见：[onnxruntime-gpu版推理配置](./python/README.md#onnxruntime-gpu版推理配置)

#### 📌2022-06-25 update:
- 重新整理python部分推理代码，将常用调节参数全部放到yaml文件中，便于调节，更加容易使用
- 详情参见：[README](./python/README.md)

#### 🍿2022-05-15 udpate:
- 增加PaddleOCR v3 rec模型转换后的ONNX模型，直接去网盘下载替换即可。([百度网盘](https://pan.baidu.com/s/1mkirNltJS481In4g81jP3w?pwd=zy37) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing))
- 增加文本识别模型各个版本效果对比表格，详情点击[各个版本ONNX模型效果对比](#各个版本onnx模型效果对比)。v3的文本识别模型从自己构建测试集上的指标来看不如之前的好。

#### 😀2022-05-12 upadte
- 增加PaddleOCR v3 det模型转换的ONNX模型，直接去网盘下载，替换即可。([百度网盘](https://pan.baidu.com/s/1mkirNltJS481In4g81jP3w?pwd=zy37) | [Google Drive](https://drive.google.com/drive/folders/1x_a9KpCo_1blxH1xFOfgKVkw1HYRVywY?usp=sharing))
- 增加各个版本文本检测模型效果对比表格，详情点击[各个版本ONNX模型效果对比](#各个版本onnx模型效果对比)。v3的文本检测模型从指标来看是好于之前的v2的，推荐使用。

#### 🎧2022-04-04 udpate:
- 增加python下的基于OpenVINO推理引擎的支持
- 给出OpenVINO和ONNXRuntime的性能对比表格
- 详情参见:[python/README](./python/README.md)

#### 2022-02-24 udpate:
- 优化python目录下的推理代码
- 添加调用不同语言模型的推理代码示例
- 详情参见：[python/onnxruntime_infer/README](./python/onnxruntime_infer/README.md)

#### 2021-12-18 udpate:
- 添加[Google Colab Demo](https://colab.research.google.com/github/RapidAI/RapidOCR/blob/main/RapidOCRDemo.ipynb)

#### 2021-11-28 udpate:
- 更新[ocrweb](http://rapidocr.51pda.cn:9003/)部分
  - 添加显示各个阶段处理时间
  - 更新说明文档
  - 更换文本检测模型为`ch_PP-OCRv2_det_infer.onnx`,推理更快，更准

#### 2021-11-13 udpate:
- 添加python版本中文本检测和识别可调节的超参数，主要有`box_thresh|unclip_ratio|text_score`，详情见[参数调节](python/README.md#相关调节参数)
- 将文本识别中字典位置以参数方式给出，便于灵活配置，详情见[keys_path](python/rapidOCR.sh)

#### 2021-10-27 udpate:
- 添加使用onnxruntime-gpu版推理的代码（不过gpu版本的onnxruntime不太好用，按照[官方教程](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html)配置，感觉没有调用起来GPU）
- 具体使用步骤参见: [onnxruntime-gpu推理配置](python/README.md)

#### 2021-09-13 udpate:
- 添加基于`python`的whl文件，便于使用，详情参见`release/python_sdk`

#### 2021-09-11 udpate:
- 添加PP-OCRv2新增模型onnx版本
  - 使用方法推理代码不变，直接替换对应模型即可。
- 经过在自有测试集上评测：
  - PP-OCRv2检测模型效果有大幅度提升，模型大小没变。
  - PP-OCRv2识别模型效果无明显提升，模型大小增加了3.58M。
- 模型上传到[百度网盘 提取码：30jv](https://pan.baidu.com/s/1qkqWK4wRdMjqGGbzR-FyWg)

#### 2021-08-07 udpate:
- [x] PP-Structure 表格结构和cell坐标预测 正在整理中
- 之前做的,未完成的，欢迎提PR
  - [ ] 打Dokcer镜像
  - [x] 尝试onnxruntime-gpu推理

#### 2021-07-17 udpate:
- 完善README文档
- 增加**英文、数字识别**onnx模型，具体参见`python/en_number_ppocr_mobile_v2_rec`，用法同其他
- 整理一下[模型转onnx](#模型转onnx)

#### 2021-07-04 udpate:
- 目前仓库下的python程序已经可以在树莓派4B上，成功运行，详细信息请进群，询问群主
- 更新整体结构图，添加树莓派的支持

#### 2021-06-20 udpate:
- 优化ocrweb中识别结果显示，同时添加识别动图演示
- 更新`datasets`目录，添加一些常用数据库链接(搬运一下^-^)
- 更新[FAQ](./FAQ.md)

#### 2021-06-10 udpate:
- 添加server版文本识别模型，详情见[提取码：30jv](https://pan.baidu.com/s/1qkqWK4wRdMjqGGbzR-FyWg)

#### 2021-06-08 udpate:
- 整理仓库，统一模型下载路径
- 完善相关说明文档

#### 2021-03-24 udpate:
- 新模型已经完全兼容ONNXRuntime 1.7 或更高版本。 特别感谢：@Channingss
- 新版onnxruntime比1.6.0 性能提升40%以上。


<script src="https://giscus.app/client.js"
        data-repo="RapidAI/RapidOCRDocs"
        data-repo-id="R_kgDOKS1JHQ"
        data-category="Q&A"
        data-category-id="DIC_kwDOKS1JHc4Ce5E0"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>