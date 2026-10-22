<!-- more -->

> 一个零推理框架依赖、能跑在龙芯和苹果芯片上的开源 OCR 引擎，到底强在哪？

如果你用过 RapidOCR，大概率对它的 Python 调用方式很熟悉：

```python
from rapidocr import RapidOCR
engine = RapidOCR()
result = engine("image.png")
```

但你可能听说过另一个名字——`RapidAI/RapidOCRLite`。这里先给大家吃颗定心丸：**RapidOCR 仍然是团队主要维护的项目**，功能迭代、多后端支持都在持续推进，大家可以放心使用、放心依赖。

而 `RapidAI/RapidOCRLite`（5.x 线）更像是团队在 "速度" 方向上的一次 **极致探索**——一个 **纯 C++ 自研的 PP-OCRv6 引擎**，把轻量与性能推到极限。它和 RapidOCR 共享 `rapidocr` 这个导入名、共享几乎一样的 API，但底层完全是另一套思路。这篇文章就把它们的核心区别一次说清。

---

## 一、最大的分叉：引擎到底 "是谁"

这是两者最根本的区别，其他差异几乎都由它派生。

**RapidOCR 3.x（主仓库）** 站在通用推理框架的肩膀上。它支持 ONNX Runtime, OpenVINO, Paddle Inference, PyTorch, TensorRT, MNN 等多后端，本质上是一个 "调度器"——把任意 ONNX 模型丢给框架去跑。模型 zoo 覆盖 PP-OCRv4 和 v5。

**RapidOCRLite 5** 则不一样。它 **不链接 ONNX Runtime、不链接 Paddle Inference、也不依赖 OpenCV**。它自己用 C++ 把官方 PP-OCRv6 的算子（卷积、GEMM、池化、归一化、resize, DB/CTC 后处理……）重新实现了一遍，库内直接解释执行权重文件。

> 一句话：**3.x 是"通用框架 + OCR 模型"，Lite 是"专为 PP-OCRv6 造的 OCR 引擎"。**

这个选择带来的连锁反应是——Lite 只跑 PP-OCRv6，不再充当通用 ONNX 运行时；但换来了 **零外部依赖、更小体积、更快速度**。

💡 **谁做的？** 你没看错——**整个 RapidOCRLite 项目，都是基于 GrokBot 自主完成的**。GrokBot 是一款 AI 智能体，从引擎实现、多平台适配（x86 / 龙芯 / Metal 等）到文档与发布，整个项目都由它独立推进。换句话说，这是一次 "AI 亲自造轮子" 的实打实产物——一个 AI 智能体能够端到端交付这样一个底层 C++ OCR 引擎项目，本身就挺值得玩味。

---

## 二、逐项对比：从 API 到行为的差异

下面这张表把官方迁移文档里的关键差异整理出来，方便你判断迁移成本：

| 维度                | RapidOCR 3.x（main）                                          | RapidOCRLite 5                            |
| ----------------- | ----------------------------------------------------------- | ----------------------------------------- |
| **引擎**            | ONNX Runtime / OpenVINO / Paddle / PyTorch / TensorRT / MNN | 内置 PP-OCRv6 解释器（仅 `EngineType.PPOCR_CPP`） |
| **模型 zoo**        | PP-OCRv4, v5, v6                                                 | PP-OCRv6（det / rec ONNX）                  |
| **外部依赖**          | 需要推理框架                                                      | **零推理框架依赖**                               |
| **支持架构**          | 通用                                                          | 额外原生支持 LoongArch64（龙芯）/ macOS Metal       |
| **GPU 后端**        | 取决于所选框架                                                     | Vulkan（跨平台）/ Metal（macOS 原生）              |
| **`vis()` 输出**    | OpenCV BGR                                                  | Pillow RGB                                |
| **`elapse_list`** | `[det, cls, rec]` 分项耗时                                      | `[None, None, total]` 仅总耗时                |
| **按词 / 按字符框**     | 支持 `return_word_box` 等                                      | 暂不支持，`word_results` 为空                    |
| **GPU 兜底**        | —                                                           | GPU-only 模式无 CPU 神经回退；Hybrid 默认跑 CPU      |

可以看到，大部分 "日常 API"（导入方式、`params` 参数、`txts/scores/boxes/to_json()` 等）都保持一致，变化主要集中在引擎层和行为细节上。

---

## 三、速度对比：Lite 凭什么敢叫 "Lite"

既然自己重写了引擎，速度自然是重点。官方基准（x86 Python，4 vCPU Intel Xeon，对比 RapidOCR 3.9.2）如下：

| 场景                   | 3.9.2 (ORT) | RapidOCRLite (AVX-512) | 提速        |
| -------------------- | ----------- | ---------------------- | --------- |
| hello（960×240，单行）    | 193.0 ms    | **105.1 ms**           | **约 46%** |
| page（1700×2200，45 行） | 508.3 ms    | **356.7 ms**           | **约 30%** |

苹果芯片上更夸张。M4 开启原生 Metal 后端（无需 Vulkan/MoltenVK），对比纯 CPU（NEON）：

- 单行 hello：25.3 ms → **11.3 ms**
- 整页 45 行：210 ms → **107.2 ms**

接近 **2 倍** 提升，而且结果逐位对齐——在 SWHL 测试集上，检测 H-mean 同为 **0.8492**，识别 Exact/Char 同为 **0.8419 / 0.9515**。又快又准。

---

## 四、你 "牺牲" 了什么

切换之前，这些 trade-off 要心里有数（来自官方 Known limits）：

1. **只跑 PP-OCRv6**：不支持 PP-OCRv4 / v5 的权重文件，也不当通用 ONNX 运行时；
2. **没有词框 / 字符框**：`word_results` 为空；
3. **GPU 无 CPU 兜底**：GPU-only 模式不会自动回退到 CPU 神经推理；
4. **方向分类器受限**：严格 GPU-only（Vulkan）或 `model_type="lite"` 时不运行；
5. **发布版 wheel 不含 Vulkan shader**：需要 Vulkan 加速得自行源码编译。

另外，Lite 内置的 `model_type="lite"`（捆绑 Indra OCR 权重，约 17.1 MB）采用修改版 OpenRAIL-M 许可证，对年收入 / 融资超 2000 万美元的实体及竞品有使用限制，商用前请注意合规。

---

## 五、怎么选：一句话决策

- **选 RapidOCR 3.x，如果你需要**：多后端灵活切换、PP-OCRv4/v5 模型、按词 / 字符框、把任意 ONNX 模型塞进去跑。
- **选 RapidOCRLite 5，如果你需要**：离线 / 边缘部署、龙芯等国产平台、极小依赖体积、极致速度，以及 macOS Metal 原生加速。

> 简单说：**要"大而全、可切换"选 3.x；要"小快灵、零依赖"选 Lite。**

---

## 六、好消息：迁移几乎无痛

尽管底层换了引擎，但 Python 侧几乎不用改代码。安装（注意是预发布，用 `--pre`，且不要和官方 `rapidocr` 同环境）：

```bash
pip uninstall rapidocr
pip install --pre RapidOCRLite
```

调用方式完全一样：

```python
from rapidocr import RapidOCR

engine = RapidOCR(params={
    "Det.model_type": "tiny",   # 自动下载 tiny 模型
    "Rec.model_type": "tiny",
})
result = engine("hello.png")
print(result.txts, result.scores)
result.vis("vis_result.jpg")
```

`result` 依然提供 `txts / scores / boxes / elapse / to_json() / to_markdown() / vis()`，老用户切换成本极低。

---

## 写在最后

RapidOCRLite 本质是一次 "把 OCR 引擎重做一遍" 的工程尝试——用纯 C++ 自研运行时，换掉了笨重的通用推理框架。它不一定是 RapidOCR 的替代品，而是给了社区一个 **更轻、更快、更干净** 的选项。

需要特别说明的是：**整个项目目前仍处于活跃发展中**。当前还是预发布阶段（PyPI `5.0.0a6`，GitHub Release `5.0.0a13`），引擎能力、平台适配（龙芯、Metal 等）和 API 都还在持续打磨。也正因如此，现在正是 **参与和试用的最好时机**——越早上手，越能影响它的演进方向，也越容易在 Issue 里提需求、报 bug、拿第一手支持。

无论你是做离线部署、边缘设备，还是国产平台适配，都欢迎 star 下来亲自跑一跑，也欢迎把使用反馈带回社区。

- 🔗 RapidOCR 主仓库：<https://github.com/RapidAI/RapidOCR>
- 🔗 RapidOCRLite：<https://github.com/RapidAI/RapidOCRLite>
- 📦 安装：`pip install --pre RapidOCRLite`

**如果这篇帮你理清了选型思路，欢迎转发给正在纠结 OCR 方案的同事。有任何问题或试用心得，评论区见~**

---

*（本文差异对比与性能数据均来自各仓库官方 README / 迁移文档，性能以官方基准为准。）*
