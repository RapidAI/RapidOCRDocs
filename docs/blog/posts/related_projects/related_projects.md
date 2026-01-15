---
title: 垂直项目(偏学术)
date: 2022-10-01
authors: [SWHL]
slug: inference-summary
categories:
  - OCR相关项目
comments: true
---

<!-- more -->

### 引言

- 以下几个方向，每个都是比较独立的方向，但是却和OCR有着千丝万缕的关系，关于它们的资料就像散落在天空中的星星一般，散发着微弱的光芒，这里要做的就是将这些点点光芒聚集起来。
- 这里将会汇总出以下几个OCR周边项目的一些文档和资源，包括学术动态和一些工程化代码。
- 欢迎各位小伙伴提供PR。

### Visual Text Rendering

- [Glyph-ByT5: A Customized Text Encoder for Accurate Visual Text Rendering](https://glyph-byt5.github.io/)

### 阅读序列抽取

数据集：

- [ReadingBank](https://github.com/doc-analysis/ReadingBank)

### 手写体识别

TODO

### 手写体公式识别

TODO

### 公式识别

TODO

### 公式检测

图像中公式检测需求一般出现于文档分析和还原需求中。

单纯公式检测任务包括对行内公式和行间公式的检测。而版面分析任务中，仅有对行间公式的标注，缺乏行内公式标注。如果想要精细化做版面还原，行内公式的检测识别就变得尤为重要。

这一块的工作，breezedeus做得比较好，详情可以参见其博客：[Pix2Text (P2T) 新版公式检测模型](https://www.breezedeus.com/article/p2t-mfd-20230613)。

有关数据集：[IBEM](https://zenodo.org/records/4757865) 和中文 [CnMFD_Dataset](https://github.com/breezedeus/CnMFD_Dataset)

### 发票识别

- [CSIG 2022 Competition on Invoice Recognition and Analysis](https://davar-lab.github.io/competition/CSIG2022-invoice-ch.html##)

### 图像文字擦除

- [CTRNet](https://github.com/lcy0604/CTRNet)：图像文字擦除 | [Demo](https://huggingface.co/spaces/SWHL/CTRNetDemo)

### 文档增强

- [DocDiff](https://arxiv.org/pdf/2305.03892)（[Github](https://github.com/Royalvice/DocDiff)）: 文档增强模型，可以用于文档去模糊、文档去噪、文档二值化、文档去水印和印章等任务。

### 文档图像矫正

- [PaperEdge](https://github.com/cvlab-stonybrook/PaperEdge)：文档图像矫正 | [Demo](https://huggingface.co/spaces/SWHL/PaperEdgeDemo)
- [DocTr++](https://arxiv.org/pdf/2304.08796) | [Demo](https://demo.doctrp.top/) | [Code](https://github.com/fh2019ustc/DocTr-Plus)
- [DocRes](https://github.com/ZZZHANG-jx/DocRes)： 统一文档图像恢复任务的广义模型

### 版面分析

- 相关论文和帖子：
    - [版面分析方法汇总](https://zhuanlan.zhihu.com/p/392058153)
- 相关工程：
    - [PaddleOCR Layout](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/ppstructure/layout/README_ch.md)
    - [海康DAVAR VSR](https://github.com/hikopensource/DAVAR-Lab-OCR/tree/main/demo/text_layout/VSR)
- 数据集汇总：
    - 英文版面分析数据集：
        - [PubLayNet](https://github.com/ibm-aur-nlp/PubLayNet): IBM构建，34万张图像，分为5类：text, title list table figure。
        - [DocBank](https://doc-analysis.github.io/docbank-page/index.html)：微软亚洲研究院构建，50万英文文档图像，分为12类：摘要、作者、标题、公式、图形、页脚、列表、段落、参考、节标题、表格和文章标题。
        - [D4LA](https://modelscope.cn/datasets/iic/D4LA/summary): 阿里通义实验室构建，11092张图像，12个文档种类，27个类别，手工标注。详情可参见论文[Vision Grid Transformer for Document Layout Analysis](https://arxiv.org/pdf/2308.14978)

    - 中文版面分析数据集：
        - [CDLA](https://github.com/buptlihang/CDLA)：中文文档版面分析数据集，面向中文文献类（论文）场景，总共6000张（5000训练，1000测试），分为10类：正文、标题、图片、图片标题、表格、表格标题、页眉、页脚、注释和公式。

### 表格结构识别

- [table-transformer](https://github.com/microsoft/table-transformer)
- 相关论文和帖子：
    - [OCR之表格结构识别综述](https://blog.csdn.net/shiwanghualuo/article/details/123726879)
    - [合合信息：表格识别与内容提炼技术理解及研发趋势](https://blog.csdn.net/INTSIG/article/details/123000010?spm=1001.2014.3001.5502)
    - [论文阅读: （ICDAR2021 海康威视）LGPMA（表格识别算法）及官方源码对应解读](https://blog.csdn.net/shiwanghualuo/article/details/125047732?spm=1001.2014.3001.5501)
- 相关工程：
    - [海康官方LGPMA源码](https://github.com/hikopensource/DAVAR-Lab-OCR/tree/main/demo/table_recognition/lgpma)
    - [LGPMA Inference](https://github.com/SWHL/LGPMA_Infer)
    - [PaddleOCR Table](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/ppstructure/table/README_ch.md)
- 数据集汇总：
    - 英文表格识别数据集：
        - [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet): IBM构建，568k+文档图像数据，包括表格图像和对应的HTML标注。

### 视频OCR

- 相关论文和帖子：
    - [【NeurIPS2021】A Bilingual, OpenWorld Video Text Dataset and End-to-end Video Text Spotter with Transformer](https://arxiv.org/abs/2112.04888) | [博客解读](https://blog.csdn.net/shiwanghualuo/article/details/122712872?spm=1001.2014.3001.5501)
    - [【ACM MM 2019】You only recognize once: Towards fast video text spotting](https://arxiv.org/pdf/1903.03299)
    - [VimTS: A Unified Video and Image Text Spotter for Enhancing the Cross-domain Generalization](https://arxiv.org/pdf/2404.19652)
- 相关工程：
    - [video-subtitle-extractor](https://github.com/YaoFANGUK/video-subtitle-extractor): 一款将视频中的硬字幕提取为外挂字幕文件(srt格式)的软件
    - [RapidVideOCR](https://github.com/SWHL/RapidVideOCR): 提取视频中硬字幕
- 数据集汇总：
    - [BOVText: A Large-Scale, Bilingual Open World Dataset for Video Text Spotting](https://github.com/weijiawu/BOVText-Benchmark): 快手科技、浙江大学和北京邮电大学合作提出，大规模双语开放场景下的视频文本基准数据集，该数据集主要提供了2000+视频，1,750,000帧开放视频场景的视频。同时，还提供了丰富的标注类型（标题、字幕、场景文本等）。该数据集支持四个任务：视频帧检测、视频帧识别、视频文本跟踪和端到端视频文本识别。

### 卡证OCR

- 相关论文和帖子：
- 相关工程：
    - [fake_certificate_generator](https://github.com/deep-practice/fake_certificate_generator): 假的证件合成器，包括身份证、驾驶证、营业执照。
- 数据集汇总：
    - 暂无，一般这类数据较为敏感，通常都合成假数据来使用。

### 印章OCR

- 相关论文和帖子：
    - [来也智能文档处理系统中的印章识别实践](https://laiye.com/tech-blog/2613)
    - [【技术新趋势】合合信息：复杂环境下ocr与印章识别技术理解及研发趋势](https://blog.csdn.net/INTSIG/article/details/125203307)
    - [基于文字分割的印章识别技术](https://pdf.hanspub.org/CSA20210300000_33555311.pdf)
- 相关工程：
    - [JS生成印章](https://github.com/niezhiliang/canvas-draw-seal)
    - [Python绘制透明背景印章](https://www.bilibili.com/opus/641999668409008129)
    - [TrOCR-Seal-Recognition](https://github.com/Gmgge/TrOCR-Seal-Recognition)
- 数据集汇总：
    - [DocDiff](https://github.com/Royalvice/DocDiff)
