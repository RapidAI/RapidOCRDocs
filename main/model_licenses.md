# RapidOCR 模型许可与归属声明

本文档记录 RapidOCR 分发的 OCR 模型制品的许可协议、版权归属、来源溯源及二次分发要求。本文档不替代、也不修改 Apache 许可证 2.0 版。

**所有在 `rapidocr/default_models.yaml` 中注册的模型，均无一例外地依据 Apache 许可证 2.0 版（`Apache-2.0`）授权。**

## 一、独立授权作品分类

RapidOCR 包含两类版权相互独立的作品：

1. **源代码与工程组件**：版权归 RapidOCR 作者所有，依据 RapidOCR 项目 `LICENSE` 文件所述，以 Apache 许可证 2.0 版开源发布。

2. **OCR 模型制品**：上游模型权重的版权归百度及 / 或相应 PaddleOCR 权利人所有。RapidOCR 不主张上游模型权重的所有权。

上述两类作品均以 Apache-2.0 分发，但版权归属与来源溯源相互独立。

## 二、本声明适用范围

本声明适用于 `rapidocr/default_models.yaml` 中注册的每一个模型。该注册表是本声明范围的唯一界定依据：其中记录的所有模型制品，无论模型版本及受支持的推理格式，均以 Apache-2.0 授权。包括但不限于传统的 `ch_ppocr_mobile_v2.0_cls` 模型，PP-OCRv3, PP-OCRv4, PP-OCRv5 与 PP-OCRv6 各代模型，及其检测、识别、分类与文本行方向变体，以及 ONNX, MNN, Paddle 与 PyTorch 表示形式。本声明不限于第六条所列的默认内置制品。

本声明覆盖的模型集合，即 `rapidocr/default_models.yaml` 中注册的模型集合。模型一经在该注册表注册，即纳入覆盖范围。下游分发方应查阅每个条目的溯源记录，以确认其上游来源、格式及密码学哈希值。此类核验用于识别制品身份，并不缩小本声明所述的许可范围。

注册表同时记录非模型资源，包括识别字典（`dict_url`）与字体（`fonts`）。这些资源不属于模型制品，不受本声明中 Apache-2.0 声明的覆盖，仍适用其各自的授权条款。非由 PaddleOCR 官方模型衍生的第三方模型、数据集、示例图片、推理运行时及其他资产，同样不在覆盖范围内。

## 三、上游归属与授权依据

所有在 `rapidocr/default_models.yaml` 中注册的模型，均由 PaddleOCR 项目发布，或衍生自该项目发布的模型，并依据 Apache 许可证 2.0 版授权。PaddleOCR 本身以 Apache-2.0 发布。PaddlePaddle 官方模型卡片将 PP-OCRv6 模型权重及 ONNX 表示形式标注为 `Apache-2.0`。PaddleOCR 官方模型列表列明了更早的各代模型，包括传统文本角度分类模型以及 PP-OCRv3, PP-OCRv4, PP-OCRv5 模型，并给出其官方分发来源。

上游合规溯源参考链接：

- PaddleOCR 项目：<https://github.com/PaddlePaddle/PaddleOCR>

- PaddleOCR 官方许可证：<https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE>

- PaddleOCR 官方模型列表：<https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/model_list.md>

- PaddleOCR ONNX 模型转换官方文档：<https://paddlepaddle.github.io/PaddleOCR/latest/en/version3.x/inference_deployment/others/obtaining_onnx_models.html>

- PP-OCRv6 轻量化检测 ONNX 官方模型卡：<https://huggingface.co/PaddlePaddle/PP-OCRv6_small_det_onnx>

- PP-OCRv6 轻量化识别 ONNX 官方模型卡：<https://huggingface.co/PaddlePaddle/PP-OCRv6_small_rec_onnx>

- 传统文本角度分类模型官方归档列表：<https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version2.x/ppocr/model_list.en.md>

早于 Hugging Face 官方模型托管服务的传统模型，包括 `ch_ppocr_mobile_v2.0_cls` 以及 PP-OCRv3 检测与识别模型，可通过 PaddleOCR 官方模型列表、模型下载服务，以及 `rapidocr/default_models.yaml` 中的溯源记录加以识别。

## 四、适用许可证条款

`rapidocr/default_models.yaml` 中注册的每一个模型，无论模型版本、模型系列或推理格式，均依据 Apache 许可证 2.0 版（`Apache-2.0`）提供。本声明无一例外地适用于注册表中的每一个条目。完整许可证文本见 <https://www.apache.org/licenses/LICENSE-2.0>。

在遵守 Apache-2.0 条款条件的前提下，该许可证允许使用、复制、修改、创作衍生作品、公开展示、次级授权，以及以源码或目标码形式分发。上述许可不限于非商业用途。

该许可证仅在相关授权人有权授予的权利范围内适用。对于 `rapidocr/default_models.yaml` 中注册的任一模型，均未发现额外的模型专属限制。

## 五、模型转换制品说明

RapidOCR 对上游 PaddleOCR 推理模型进行转换或重打包，以适配受支持的推理引擎。此类转换属于模型表示形式的机械变换，不将上游权重的所有权转移给 RapidOCR，也不免除上游版权与归属声明义务。

`rapidocr/default_models.yaml` 中注册的所有模型，包括为每一种受支持推理引擎与格式转换、重打包后的表示形式，均沿用对应上游 PaddleOCR 模型所适用的同一 Apache-2.0 条款。转换与打包脚本、配置，以及由 RapidOCR 编写的元数据，版权单独归 RapidOCR 作者所有，并作为 RapidOCR 源代码的一部分以 Apache-2.0 授权。

RapidOCR 转换后的制品，与 PaddlePaddle 托管的 ONNX 或其他表示形式可能并非逐字节一致。因此，制品身份须依据其溯源记录与密码学哈希值确定，而不能仅凭文件名判定。

## 六、default_models.yaml 中注册的模型

`rapidocr/default_models.yaml` 中的每一个 `model_dir` 条目均受第四条 Apache-2.0 声明覆盖。注册表中记录的版本包括：

- 传统模型：`ch_ppocr_mobile_v2.0_cls`（文本角度分类）以及 PP-OCRv3 检测与识别模型。
- PP-OCRv4, PP-OCRv5 与 PP-OCRv6 的检测、识别、分类及文本行方向模型，涵盖 mobile, server, tiny, small, medium 等规格及其语言变体。
- 上述模型对应的 ONNX, MNN, Paddle（`.pdmodel`）与 PyTorch（`.pth`）表示形式。

下表列出随 RapidOCR 默认 ONNX Runtime 配置分发的代表性制品，仅作示例，不构成对本声明范围的限制。

| RapidOCR 制品 | 上游模型 | SHA-256 | RapidOCR 来源 |
| --- | --- | --- | --- |
| `PP-OCRv6_det_small.onnx` | `PP-OCRv6_small_det` | `090f04abcd9d9a7498bc4ebf677e4cb9bdce1fe4197ddb7e529f1ef44e1ff94f` | [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.10.0/onnx/PP-OCRv6/det/PP-OCRv6_det_small.onnx) |
| `PP-OCRv6_rec_small.onnx` | `PP-OCRv6_small_rec` | `6f327246b50388f3c176ae304bd95767ea6dc0c9ae92153ef8cbe210b3c14884` | [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.10.0/onnx/PP-OCRv6/rec/PP-OCRv6_rec_small.onnx) |
| `ch_ppocr_mobile_v2.0_cls_mobile.onnx` | `ch_ppocr_mobile_v2.0_cls` | `e47acedf663230f8863ff1ab0e64dd2d82b838fceb5957146dab185a89d6215c` | [ModelScope](https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.10.0/onnx/PP-OCRv4/cls/ch_ppocr_mobile_v2.0_cls_mobile.onnx) |

注册表中的 `dict_url` 与 `fonts` 条目属于资源而非模型，不在本声明覆盖范围内。`rapidocr/default_models.yaml` 是每个已注册模型制品的来源 URL 与 SHA-256 值的权威发布记录。

## 七、二次分发要求

再分发受覆盖的模型制品，或其经修改、转换后的形式时，应遵守 Apache-2.0 第 4 条。特别地，必须：

1. 向接收方提供 Apache 许可证 2.0 版的副本。

2. 使修改过的文件带有显著声明，说明文件已被修改。

3. 保留上游作品中适用的版权、专利、商标及归属声明，但与再分发作品无关的声明除外。

4. 若上游分发包包含 `NOTICE` 文件，须以许可的形式收录该声明中的相关内容。

截至本声明发布时，RapidOCR 尚未发现 `rapidocr/default_models.yaml` 中任一模型存在额外的模型专属 `NOTICE` 文件。若未来上游版本提供此类文件，必须保留其中适用的内容。

对于转换后的文件，合适的修改声明示例为：

> 本制品由 PaddleOCR 官方模型转换至所标示的推理格式，并为配合 RapidOCR 使用而重新打包。上游模型权重版权归百度及 / 或相应 PaddleOCR 权利人所有，并依据 Apache 许可证 2.0 版授权。

## 八、商标与背书说明

Apache-2.0 不授予使用百度、PaddlePaddle, PaddleOCR 或 RapidOCR 的商品名、商标、服务标识及产品名称的许可，但为合理且惯常地描述模型制品来源所必需的使用除外。未经单独许可，再分发行为不得暗示获得背书、赞助或关联关系。

## 九、免责声明

除适用法律强制要求或双方书面约定外，模型制品均按 **「现状」（AS IS）** 提供，不附带任何形式的担保或条件。Apache-2.0 中的担保免责与责任限制条款适用。

模型的识别精度、适用性、安全性及法规合规性，由使用者与下游分发方自行负责。RapidOCR 并非医疗设备；无论模型许可还是本声明，均不构成对医疗、安全关键或受监管用途的认证或保证。

## 十、版本维护规范

RapidOCR 版本新增或变更模型制品、模型版本时，维护人员应：

1. 在将上游模型加入 `rapidocr/default_models.yaml` 前，核验其以 Apache-2.0 授权。

2. 在可得的情况下，记录上游来源及不可变版本号或修订号。

3. 在可得的情况下，记录转换工具、工具版本、模型格式及转换选项。

4. 记录并核验制品的 SHA-256 值。

5. 保留所有适用的上游版权、归属及 `NOTICE` 材料。

6. 当模型版本或适用条款变更时，保持 `rapidocr/default_models.yaml` 与第六条的版本覆盖清单同步。
