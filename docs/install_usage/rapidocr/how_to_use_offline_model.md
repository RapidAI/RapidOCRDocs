---
comments: true
hide:
  - toc
---

使用方法同样也是有两种：一是通过配置文件传入；二是通过初始化参数传入。文本检测、方向分类模型和文本识别模型均有对应的 `model_path` 参数。

### PaddlePaddle 格式离线模型指定

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

# 以指定 PP-OCRv6 Rec Tiny 模型为例
model_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_tiny"
dict_path = "modelscope/paddle/PP-OCRv6/rec/PP-OCRv6_rec_tiny/ppocrv6_tiny_dict.txt"
engine = RapidOCR(
    params={
        "Rec.model_dir": model_path,
        "Rec.rec_keys_path": dict_path,
        "Rec.engine_type": EngineType.PADDLE,
        "Rec.ocr_version": OCRVersion.PPOCRV5,
    }
)

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

### PaddlePaddle 格式以外离线模型指定

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

model_path = "torch/PP-OCRv6/det/PP-OCRv6_det_tiny.pth"
engine = RapidOCR(
    params={
        "Det.ocr_version": OCRVersion.PPOCRV6,
        "Det.model_path": model_path,
        "Det.engine_type": EngineType.TORCH,
    }
)

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```
