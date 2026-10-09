---
title: RapidOCR 模型许可与归属声明
comments: true
hide:
  - navigation
---

本文档记录 RapidOCR 分发的所有 OCR 模型制品的许可协议、版权归属、来源溯源及二次分发要求。本文档不替代、不修改 Apache 2.0 开源许可证。

## 一、独立授权作品分类

RapidOCR 包含两类版权相互独立的作品，归属与授权主体互不混淆：

1. **源代码与工程组件**：版权归 RapidOCR 作者所有，依据 RapidOCR 项目根目录的 `LICENSE` 文件，以 Apache 2.0 许可证开源发布。

2. **OCR 模型权重制品**：上游模型权重的版权归属百度及 PaddleOCR 相关合法权利人。RapidOCR 不拥有该上游模型权重的所有权。

以上两类作品均基于 Apache 2.0 许可证分发，但版权归属与溯源来源相互独立、分开认定。

## 二、本声明适用范围

本声明仅适用于本文第六条所列的模型制品。RapidOCR 提供的其他模型制品可能基于不同上游版本、遵循不同授权条款，二次分发前需单独核查其原始溯源记录。

本声明 **不自动覆盖** 非 PaddleOCR 官方衍生的第三方模型、数据集、字体、示例图片、推理运行库及其他资源，此类资源均遵循其自身对应的授权协议。

## 三、上游归属与授权依据

本文第六条所列模型均源自百度 PaddleOCR 项目、基于其官方开源模型衍生开发。PaddleOCR 整体采用 Apache 2.0 许可证发布，其官方模型卡片明确标注 PP-OCRv6 系列权重及 ONNX 格式制品遵循 Apache-2.0 协议，官方模型列表同步归档了传统文本角度分类模型的合规分发来源。

上游合规溯源参考链接：

- PaddleOCR 开源项目：[https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

- PaddleOCR 官方许可证：[https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE](https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE)

- PaddleOCR 3.x 官方模型列表：[https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/model_list.md](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/model_list.md)

- PaddleOCR ONNX 模型转换官方文档：[https://paddlepaddle.github.io/PaddleOCR/latest/en/version3.x/inference_deployment/others/obtaining_onnx_models.html](https://paddlepaddle.github.io/PaddleOCR/latest/en/version3.x/inference_deployment/others/obtaining_onnx_models.html)

- PP-OCRv6 轻量化检测 ONNX 官方模型卡：[https://huggingface.co/PaddlePaddle/PP-OCRv6_small_det_onnx](https://huggingface.co/PaddlePaddle/PP-OCRv6_small_det_onnx)

- PP-OCRv6 轻量化识别 ONNX 官方模型卡：[https://huggingface.co/PaddlePaddle/PP-OCRv6_small_rec_onnx](https://huggingface.co/PaddlePaddle/PP-OCRv6_small_rec_onnx)

- 传统文本角度分类模型官方归档列表：[https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version2.x/ppocr/model_list.en.md](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version2.x/ppocr/model_list.en.md)

传统模型 `ch_ppocr_mobile_v2.0_cls` 发布时间早于 Hugging Face 托管服务上线时间，其合规性与溯源依据以 PaddleOCR 官方模型列表及官方下载服务为准。

## 四、适用许可证条款

本文第六条所列所有模型制品均依据 **Apache 2.0 许可证**（Apache-2.0）开源分发，完整许可证文本可查阅：[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)。

在遵守 Apache 2.0 协议条款的前提下，使用者可自由对模型进行使用、复制、修改、制作衍生作品、公开展示、次级授权及源码 / 二进制形式分发，**无商用限制**。

本授权仅涵盖授权方合法授予的权利，对于本声明覆盖的 PaddleOCR 衍生模型制品，暂无额外专属使用限制。

## 五、模型转换制品说明

RapidOCR 对上游 PaddleOCR 推理模型进行格式转换与重打包，以适配各类推理引擎。该类转换仅为模型存储格式的机械适配，**不转移上游模型权重的所有权**，不覆盖、不免除原始版权归属与署名义务。

RapidOCR 分发的转换后模型制品，完全沿用对应 PaddleOCR 上游模型的 Apache 2.0 授权条款。所有转换脚本、配置文件及 RapidOCR 自主编写的元数据，版权归 RapidOCR 作者所有，随项目源代码一并以 Apache 2.0 协议开源。

RapidOCR 转换后的模型制品，与百度官方托管的 ONNX 模型并非逐字节完全一致。因此，模型真伪与版本溯源需以 **溯源记录与哈希值** 为准，不可仅依据文件名判定。

## 六、内置捆绑模型制品清单

以下模型制品随 RapidOCR 默认 ONNX 运行环境配置分发，适用本声明全部条款：

|RapidOCR 制品名称|上游原始模型|SHA-256 哈希值|RapidOCR 溯源地址|
|---|---|---|---|
|`PP-OCRv6_det_small.onnx`|`PP-OCRv6_small_det`|090f04abcd9d9a7498bc4ebf677e4cb9bdce1fe4197ddb7e529f1ef44e1ff94f|[ModelScope 溯源链接](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/onnx/PP-OCRv6/det/PP-OCRv6_det_small.onnx)|
|`PP-OCRv6_rec_small.onnx`|`PP-OCRv6_small_rec`|6f327246b50388f3c176ae304bd95767ea6dc0c9ae92153ef8cbe210b3c14884|[ModelScope 溯源链接](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/onnx/PP-OCRv6/rec/PP-OCRv6_rec_small.onnx)|
|`ch_ppocr_mobile_v2.0_cls_mobile.onnx`|`ch_ppocr_mobile_v2.0_cls`|e47acedf663230f8863ff1ab0e64dd2d82b838fceb5957146dab185a89d6215c|[ModelScope 溯源链接](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/onnx/PP-OCRv4/cls/ch_ppocr_mobile_v2.0_cls_mobile.onnx)|

项目配置文件 `rapidocr/default_models.yaml` 为所有模型制品溯源地址与 SHA-256 哈希值的 **权威发布记录**。

## 七、二次分发要求

二次分发、修改或重新编译本文档覆盖的模型制品时，必须严格遵守 Apache 2.0 协议第四条规定，具体要求如下：

1. 向所有接收方提供完整的 Apache 2.0 许可证副本；

2. 对模型文件进行任何修改后，需在文件中显著标注修改记录；

3. 完整保留上游作品的版权、专利、商标及归属声明（与分发内容无关的声明除外）；

4. 若上游原版分发包包含 `NOTICE` 声明文件，需以合规形式完整保留其内容。

本声明发布之日，上述模型制品暂无专属的 `NOTICE` 文件。若后续上游版本新增相关声明文件，二次分发时需同步合规保留。

模型转换制品的标准修改标注文案：

> 本模型由 PaddleOCR 官方模型转换适配而来，专为 RapidOCR 推理场景打包优化。上游模型权重版权归百度及 PaddleOCR 相关权利人所有，遵循 Apache 2.0 开源许可证分发。
>
>

## 八、商标与背书说明

Apache 2.0 许可证 **未授予** 使用者百度、飞桨、PaddleOCR, RapidOCR 的商品名、商标、服务标识及产品名称的商用授权。仅可在客观描述模型来源时合理使用。

未经单独书面授权，二次分发行为不得暗示获得上述品牌的背书、赞助或官方关联认证。

## 九、免责声明

除非法律法规强制要求或双方书面约定，所有模型制品均以 **现状交付（AS IS）** 方式提供，不附带任何明示或暗示的担保与使用条件。Apache 2.0 协议中的免责条款与责任限制条款完全适用。

模型的识别精度、适用性、安全性及合规性，均由使用者及下游分发方自行承担全部责任。RapidOCR 非医疗设备，本模型许可与官方声明 **不支持、不担保** 任何医疗、安全关键场景及受监管场景的使用合规性。

## 十、版本维护规范

RapidOCR 版本新增或替换模型制品时，维护人员需严格执行以下规范：

1. 核验上游模型的版权归属与有效授权协议；

2. 完整记录上游溯源地址、固定版本号或修订信息；

3. 记录模型转换工具、工具版本、输出格式及转换参数；

4. 校验并归档模型制品的 SHA-256 哈希值；

5. 完整保留上游版权声明、归属标注及 `NOTICE` 合规内容；

6. 模型系列或授权条款发生变更时，同步更新本声明文档。
