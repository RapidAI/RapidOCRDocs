---
comments: true
hide:
  - navigation
  - toc
---

针对PaddleOCR已经发布的常用模型，我们这里已经做了统一转换和汇总，包括PP-OCRv1、PP-OCRv2、PP-OCRv3和PP-OCRv4。

以下涉及到的ONNX模型对应原始模型，均可在[模型列表](https://github.com/PaddlePaddle/PaddleOCR/blob/40c56628fda416e1c8710eb19e4b260536902520/doc/doc_ch/models_list.md)找到。

所有ONNX模型目前托管在了[HuggingFace](https://huggingface.co/SWHL/RapidOCR)上，可移步详细查看。

!!! note

    建议用`rapidocr_onnxruntime>=1.3.x`版本来加载PP-OCR v3/v4版本训练所得模型。 <br/> 不推荐PP-OCR v2/v1模型。

### 使用方式

```python linenums="1"
from rapidocr_onnxruntime import RapidOCR

# det_model_path同理
model = RapidOCR(rec_model_path="en_PP-OCRv4_rec_infer.onnx")

img_path = "1.png"
result, elapse = model(img_path)
print(result)
print(elapse)
```

### PP-OCRv4

|ONNX模型|下载链接|
|:---|:---|
|ch_PP-OCRv4_det_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv4/ch_PP-OCRv4_det_infer.onnx)|
|ch_PP-OCRv4_det_server_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx)|
|-|-|
|ch_PP-OCRv4_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv4/ch_PP-OCRv4_rec_infer.onnx)|
|ch_PP-OCRv4_rec_server_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv4/ch_PP-OCRv4_rec_server_infer.onnx)|

### PP-OCRv3

|ONNX模型|下载链接|
|:---|:---|
|ch_PP-OCRv3_det_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv3/ch_PP-OCRv3_det_infer.onnx)|
|-|-|
|ch_PP-OCRv3_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv3/ch_PP-OCRv3_rec_infer.onnx)|
|ch_PP-OCRv3_rec_train_student.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv3/ch_PP-OCRv3_rec_train_student.onnx)|
|en_PP-OCRv3_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv3/en_PP-OCRv3_rec_infer.onnx)|
|-|-|
|ch_ppocr_mobile_v2.0_cls_train.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv3/ch_ppocr_mobile_v2.0_cls_train.onnx)|

### PP-OCRv2

|ONNX模型|下载链接|
|:---|:---|
|ch_PP-OCRv2_det_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv2/ch_PP-OCRv2_det_infer.onnx)|
|ch_PP-OCRv2_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv2/ch_PP-OCRv2_rec_infer.onnx)|

### PP-OCRv1

|ONNX模型|下载链接|
|:---|:---|
|ch_ppocr_mobile_v2.0_det_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/ch_ppocr_mobile_v2.0_det_infer.onnx)|
|ch_ppocr_server_v2.0_det_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/ch_ppocr_server_v2.0_det_infer.onnx)|
|-|-|
|ch_ppocr_mobile_v2.0_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/ch_ppocr_mobile_v2.0_rec_infer.onnx)|
|ch_ppocr_server_v2.0_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/ch_ppocr_server_v2.0_rec_infer.onnx)|
|en_number_mobile_v2.0_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/en_number_mobile_v2.0_rec_infer.onnx)|
|japan_rec_crnn.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/japan_rec_crnn.onnx)|
|korean_mobile_v2.0_rec_infer.onnx|[link](https://huggingface.co/SWHL/RapidOCR/blob/main/PP-OCRv1/korean_mobile_v2.0_rec_infer.onnx)|
