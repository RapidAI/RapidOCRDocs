<!-- more -->

### 引言

`rapidocr==3.9.0` 仅支持 ONNXRuntime 和 OpenVINO 两个推理引擎，PaddlePaddle, PyTorch, MNN 和 TensorRT 打算在下个版本（v3.9.1）都支持了。

本篇文章就是用来记录 RapidOCR PP-OCRv6 Rec 模型支持 PaddlePaddle, PyTorch, MNN 的过程，一是备忘，二是希望帮助需要的小伙伴们。

### 以下代码运行环境

- OS: macOS Tahoe 26.5.1
- Python: 3.10.14
- PaddlePaddle: 3.1.0
- paddle2onnx: 2.1.0
- paddlex: 3.7.1
- rapidocr: 3.9.0
- MNN: 3.2.5
- OpenVINO: 2026.2.1
- torch: 2.7.0

### 支持 PaddlePaddle

得益于原始模型就是 PaddlePaddle 格式，因此支持 PaddlePaddle 推理引擎较为容易，加上 [@jaminmei](https://github.com/jaminmei) 提的 PR [#696](https://github.com/RapidAI/RapidOCR/pull/696)。我这里做的工作少了许多，由衷地感谢。

```python linenums="1"
import time

import cv2
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

from rapidocr import EngineType, OCRVersion, RapidOCR

# 依次跑三个规格的模型
model_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_medium"
dict_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_medium/ppocrv6_dict.txt"
engine = RapidOCR(
    params={
        "Rec.model_dir": model_path,
        "Rec.rec_keys_path": dict_path,
        "Rec.engine_type": EngineType.PADDLE,
        "Rec.ocr_version": OCRVersion.PPOCRV5,
    }
)

dataset = load_dataset("SWHL/text_rec_test_dataset")
test_data = dataset["test"]

content = []
for i, one_data in enumerate(tqdm(test_data)):
    img = np.array(one_data.get("image"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    t0 = time.perf_counter()
    result = engine(img, use_rec=True, use_cls=False, use_det=False)
    elapse = time.perf_counter() - t0

    rec_text = result.txts[0]
    if len(rec_text) <= 0:
        rec_text = ""
        elapse = 0

    gt = one_data.get("label", None)
    content.append(f"{rec_text}\t{gt}\t{elapse}")

with open("pred.txt", "w", encoding="utf-8") as f:
    for v in content:
        f.write(f"{v}\n")

from text_rec_metric import TextRecMetric

metric = TextRecMetric()

pred_path = "pred.txt"
metric = metric(pred_path)
print(metric)
```

最终结果汇总到文章末尾了。

### 支持 PyTorch

PP-OCRv6 中，官方支持 safetensors 格式，支持用 transformers 库推理。经过我的调研，发现 safetensors 格式仅仅是权重，里面并没有具体网络结构。

因此想要直接使用 PyTorch 推理，就必须安装 transformers 库来推理。我翻看了 PaddleOCR, PaddleX 和 transformers 源码，试图找到 PP-OCRv6 检测和识别模型的网络结构定义。最终仅在 PaddleX 中找到了 PP-OCRv6_medium_det 的 PaddlePaddle 实现（[source](https://github.com/PaddlePaddle/PaddleX/blob/ffb64904d23708863ff5b8da312a5cbd52a7f462/paddlex/inference/models/text_detection/modeling/pp_ocrv6_medium_det.py)）。**从源码中可以看到，当前版本所谓的支持 PyTorch 推理，也只是包装了一套 PaddlePaddle 实现的网路结构。如果想要不安装 PaddlePaddle，来使用 PyTorch 推理，那是不可能的。** 因此，这条路算是走不通了。

但是 [PaddleOCR2Pytorch](https://github.com/frotms/PaddleOCR2Pytorch) 中已经支持 PP-OCRv6 文本检测和识别模型了。哈哈哈。RapidOCR 之前支持的 PyTorch 推理，其模型都是来自这个仓库。有了这个，剩下工作就是集成和测试一下指标就可以了。感谢大佬的工作。

评测代码：

```python linenums="1"
import cv2
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

model_path = "models/PP-OCRv6_det_tiny.pth"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.model_path": model_path,
        "Det.engine_type": EngineType.TORCH,
    }
)

dataset = load_dataset("SWHL/text_det_test_dataset")
test_data = dataset["test"]

content = []
for i, one_data in enumerate(tqdm(test_data)):
    img = np.array(one_data.get("image"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    ocr_results = engine(img, use_det=True, use_cls=False, use_rec=False)
    dt_boxes = ocr_results.boxes

    dt_boxes = [] if dt_boxes is None else dt_boxes.tolist()
    elapse = ocr_results.elapse

    gt_boxes = [v["points"] for v in one_data["shapes"]]
    content.append(f"{dt_boxes}\t{gt_boxes}\t{elapse}")

with open("pred.txt", "w", encoding="utf-8") as f:
    for v in content:
        f.write(f"{v}\n")

from text_det_metric import TextDetMetric

metric = TextDetMetric()
pred_path = "pred.txt"
metric = metric(pred_path)
print(metric)
```

### 支持 MNN

```bash linenums="1"
# 安装
pip install MNN==3.2.5

# 转换
MNNConvert -f ONNX --modelFile modelscope/onnx/PP-OCRv6/rec/PP-OCRv6_rec_medium.onnx --MNNModel modelscope/mnn/PP-OCRv6/rec/PP-OCRv6_rec_medium.mnn --bizCode MNN

MNNConvert -f ONNX --modelFile modelscope/onnx/PP-OCRv6/rec/PP-OCRv6_rec_small.onnx --MNNModel modelscope/mnn/PP-OCRv6/rec/PP-OCRv6_rec_small.mnn --bizCode MNN

MNNConvert -f ONNX --modelFile modelscope/onnx/PP-OCRv6/rec/PP-OCRv6_rec_tiny.onnx --MNNModel modelscope/mnn/PP-OCRv6/rec/PP-OCRv6_rec_tiny.mnn --bizCode MNN
```

测试转换后的模型指标

```python linenums="1"
import time

import cv2
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

model_path = "modelscope/mnn/PP-OCRv6/rec/PP-OCRv6_rec_tiny.mnn"
dict_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_tiny/ppocrv6_tiny_dict.txt"

# model_path = "modelscope/torch/PP-OCRv6/rec/PP-OCRv6_rec_small.pth"
# dict_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_small/ppocrv6_dict.txt"
# model_path = "modelscope/torch/PP-OCRv6/rec/PP-OCRv6_rec_medium.pth"
# dict_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_small/ppocrv6_dict.txt"

engine = RapidOCR(
    params={
        "Rec.model_path": model_path,
        "Rec.rec_keys_path": dict_path,
        "Rec.ocr_version": OCRVersion.PPOCRV6,
        "Rec.engine_type": EngineType.MNN,
        "Rec.model_type": ModelType.TINY,
    }
)

dataset = load_dataset("SWHL/text_rec_test_dataset")
test_data = dataset["test"]

content = []
for i, one_data in enumerate(tqdm(test_data)):
    img = np.array(one_data.get("image"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    t0 = time.perf_counter()
    result = engine(img, use_rec=True, use_cls=False, use_det=False)
    elapse = time.perf_counter() - t0

    rec_text = result.txts[0]
    if len(rec_text) <= 0:
        rec_text = ""
        elapse = 0

    gt = one_data.get("label", None)
    content.append(f"{rec_text}\t{gt}\t{elapse}")

with open("pred.txt", "w", encoding="utf-8") as f:
    for v in content:
        f.write(f"{v}\n")

from text_rec_metric import TextRecMetric

metric = TextRecMetric()

pred_path = "pred.txt"
metric = metric(pred_path)
print(metric)
```

最终结果汇总到文章末尾了。

### 不同推理引擎指标汇总

在这里将 ONNXRuntime, OpenVINO, PaddlePaddle, MNN 和 PyTorch 在 PP-OCRv6 Det 模型上指标和速度都汇总起来了，便于大家选用最合适的。

TensorRT 的指标等有时间再补哈！

各个推理引擎对应不同的模型，最终指标效果如下：

|模型|推理框架|模型格式|ExactMatch↑|CharMatch↑|Elapse↓|
|:---|:---|:---|:---:|:---:|:---:|
|||||||
|PP-OCRv6_medium_rec|RapidOCR| ONNX Runtime|**0.8613**|0.9491|0.0515|
|PP-OCRv6_medium_rec|RapidOCR| OpenVINO|0.8548|0.9478|0.0316|
|PP-OCRv6_medium_rec|RapidOCR| PaddlePaddle|0.8613|0.9491|0.059|
|PP-OCRv6_medium_rec|RapidOCR| MNN|0.8613|**0.9497**|0.0813|
|PP-OCRv6_medium_rec|RapidOCR| PyTorch|0.8613|0.9491|0.0944|
|||||||
|PP-OCRv6_small_rec|RapidOCR| ONNX Runtime|0.8419|0.9515|0.0159|
|PP-OCRv6_small_rec|RapidOCR| OpenVINO|0.8419|0.9518|0.0123|
|PP-OCRv6_small_rec|RapidOCR| PaddlePaddle|0.8419|0.9515|0.0277|
|PP-OCRv6_small_rec|RapidOCR| MNN|0.8419|**0.9519**|0.0447|
|PP-OCRv6_small_rec|RapidOCR| PyTorch|0.8419|0.9515|0.0429|
|||||||
|PP-OCRv6_tiny_rec|RapidOCR| ONNX Runtime|0.6968|0.8897|0.0041|
|PP-OCRv6_tiny_rec|RapidOCR| OpenVINO|0.6903|0.885|0.0041|
|PP-OCRv6_tiny_rec|RapidOCR| PaddlePaddle|0.6968|0.8897|0.0008|
|PP-OCRv6_tiny_rec|RapidOCR| MNN|0.6935|0.8877|0.0168|
|PP-OCRv6_tiny_rec|RapidOCR| PyTorch|0.0032|0.3461|0.0207|

值得注意的是，PP-OCRv6 Rec Tiny PyTorch 模型在指标上很低，我再三验证发现仍然如此。具体原因，需要我进一步查验。

大家用的时候，注意一下就行。
