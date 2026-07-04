---
title: RapidOCR 适配 PP-OCRv6 Det 模型支持 Paddle, PyTorch 和 MNN 记录
date:
  created: 2026-06-27
authors: [SWHL]
categories:
  - 模型相关
comments: true
hide:
  - toc
links:
  - RapidOCR 集成 PP-OCRv5_det 模型(mobile/server)记录: blog/posts/about_model/adapt_PP-OCRv5_det.md
  - RapidOCR 集成 PP-OCRv6 Rec 模型记录: blog/posts/about_model/adapt_PP-OCRv6_rec.md
---

<!-- more -->

### 引言

`rapidocr==3.9.0` 仅支持 ONNXRuntime 和 OpenVINO 两个推理引擎，PaddlePaddle, PyTorch 和 MNN 打算在下个版本（v3.9.1）都支持了。

本篇文章就是用来记录 RapidOCR PP-OCRv6 Det 模型支持 PaddlePaddle, PyTorch, MNN 的过程，一是备忘，二是希望帮助需要的小伙伴们。

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

需要做的：

- 将 Paddle 格式模型托管到魔搭仓库中，包括模型文件和字典文件。
- 更新 `default_models.yaml` 文件中 Paddle 部分模型的路径和 SHA256，这个配置好后，可以直接通过参数指定 `EngineType` 为 Paddle 格式，程序会自动下载对应的模型。

测试代码如下：

```python linenums="1"
from rapidocr import EngineType, RapidOCR

engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.PADDLE,
        "Rec.engine_type": EngineType.PADDLE,
    }
)


img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

以上代码可以正确打印出结果，说明程序跑通了。接下来跑一下在评测集上文字检测的指标，看看和之前跑的是否一致。

```python linenums="1"
import cv2
import numpy as np
from rapidocr import EngineType, OCRVersion, RapidOCR
from tqdm import tqdm

from datasets import load_dataset

engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.engine_type": EngineType.PADDLE,
        "Det.model_type": ModelType.TINY,
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

最终结果汇总到文章末尾了。

### 支持 PyTorch

PP-OCRv6 中，官方支持 safetensors 格式，支持用 transformers 库推理。经过我的调研，发现 safetensors 格式仅仅是权重，里面并没有具体网络结构。

经过社区小伙伴的提醒，我才发现 PP-OCRv6 已经集成到了 transformers 库了。我本以为这个事情就变得简单了。后来发现 transformers 中集成了很多模型的推理，想要单独抠出 PP-OCRv6 的相关最小可执行代码，太难了。

我这里给出 transformers 库中如何使用 PP-OCRv6 det 系列模型，代码来自 [transformers 模型卡片](https://github.com/huggingface/transformers/blob/b70d02fc724d04c916832ca4ead03ff05e8fb1ee/docs/source/en/model_doc/pp_ocrv6_medium_det.md)

```python linenums="1"
from io import BytesIO

import httpx
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from transformers.image_utils import load_image

model_path = "PaddlePaddle/PP-OCRv6_medium_det_safetensors"
model = AutoModelForObjectDetection.from_pretrained(model_path, device_map="auto")
image_processor = AutoImageProcessor.from_pretrained(model_path)

image_url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_001.png"
image = load_image(image_url)
inputs = image_processor(images=image, return_tensors="pt").to(model.device)
outputs = model(**inputs)

results = image_processor.post_process_object_detection(
    outputs,
    target_sizes=inputs["target_sizes"],
    threshold=0.2,
    box_threshold=0.45,
    max_candidates=3000,
    unclip_ratio=1.4,
)

for result in results:
    print(result)
```

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
MNNConvert -f ONNX --modelFile rapidocr/models/PP-OCRv6_det_medium.onnx --MNNModel mnn/PP-OCRv6_det_medium.mnn --bizCode MNN
```

测试转换后的模型指标

```python linenums="1"
import cv2
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

from rapidocr import EngineType, ModelType, OCRVersion, RapidOCR

# 依次跑 Tiny, small 和 Medium 三个模型
model_path = "mnn/PP-OCRv6_det_tiny.mnn"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.model_path": model_path,
        "Det.engine_type": EngineType.MNN,
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

最终结果汇总到文章末尾了。

### 不同推理引擎指标汇总

在这里将 ONNXRuntime, OpenVINO, PaddlePaddle, MNN 和 PyTorch 在 PP-OCRv6 Det 模型上指标和速度都汇总起来了，便于大家选用最合适的。

TensorRT 的指标等有时间再补哈！

各个推理引擎对应不同的模型，最终指标效果如下：

|模型|推理框架|模型格式|Precision↑|Recall↑|H-mean↑|Elapse↓|
|:---|:---|:---|:---:|:---:|:---:|:---:|
|PP-OCRv6_medium_det| RapidOCR| ONNX Runtime |0.8251|0.8598|0.8421|0.9491|
|PP-OCRv6_medium_det| RapidOCR| OpenVINO |0.8256|0.8587|0.8418|**0.4476**|
|PP-OCRv6_medium_det| RapidOCR| PaddlePaddle |0.8254|0.8598|**0.8423**|3.2856|
|PP-OCRv6_medium_det| RapidOCR| MNN |0.8254|0.8598|0.8423|0.6936|
|PP-OCRv6_medium_det| RapidOCR| PyTorch |0.8251|0.8598|0.8421|3.4131|
||||||||
|PP-OCRv6_small_det| RapidOCR| ONNX Runtime |0.854|0.8445|0.8492|0.2277|
|PP-OCRv6_small_det| RapidOCR| OpenVINO |0.8532|0.8457|0.8494|**0.1617**|
|PP-OCRv6_small_det| RapidOCR| PaddlePaddle|0.854|0.8445|0.8492|0.8097|
|PP-OCRv6_small_det| RapidOCR| MNN|0.8541|0.8449|**0.8495**|0.1926|
|PP-OCRv6_small_det| RapidOCR| PyTorch|0.8540|0.8445|0.8492|0.8752|
||||||||
|PP-OCRv6_tiny_det| RapidOCR| ONNX Runtime |0.8241|0.8285|0.8263|0.1451|
|PP-OCRv6_tiny_det| RapidOCR| OpenVINO |0.8299|0.8331|**0.8315**|**0.104**|
|PP-OCRv6_tiny_det| RapidOCR| PaddlePaddle|0.8244|0.8285|0.8264|0.4245|
|PP-OCRv6_tiny_det| RapidOCR| MNN|0.8238|0.8285|0.8261|0.1352|
|PP-OCRv6_tiny_det| RapidOCR| PyTorch|0.8241|0.8285|0.8263|0.4136|

从以上推理速度来看，OpenVINO 竟然是最快的了。这个有点出乎我的意料。

上述推理引擎的支持，将会随 `rapidocr==3.9.1` 发布，敬请期待！
