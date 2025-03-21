---
comments: true
hide:
  - navigation
  - toc

---

针对PaddleOCR已经发布的常用模型，我们这里已经做了统一转换和汇总，包括PaddlePaddle格式、ONNX格式和PyTorch格式。

所有模型目前托管在[魔搭社区](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)上。

### 所有模型汇总

请移步以下链接查看：

[default_model.yaml](https://github.com/RapidAI/RapidOCR/blob/a9bb7c1f44b6e00556ada90ac588f020d7637c4b/python/rapidocr/default_models.yaml)

### 使用方式

以上模型可直接通过字段指定，程序会自动下载使用。

```python linenums="1"
from rapidocr import RapidOCR, VisRes

engine = RapidOCR(
    params={"Global.lang_det": "ch_mobile", "Global.lang_rec": "ch_mobile"}
)
img_url = "https://github.com/RapidAI/RapidOCR/blob/main/python/tests/test_files/ch_en_num.jpg?raw=true"
result = engine(img_url)
print(result)

result.vis()
```
