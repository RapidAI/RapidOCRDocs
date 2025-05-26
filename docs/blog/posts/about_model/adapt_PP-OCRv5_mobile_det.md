---
title: RapidOCR集成PP-OCRv5_mobile_det模型记录
date: 2025-05-26
authors: [SWHL]
categories:
  - 模型相关
comments: true
hide:
  - toc
---


> 该文章主要记录RapidOCR集成PP-OCRv5_mobile_det模型记录的，涉及模型转换，模型精度测试等步骤。

<!-- more -->

### 引言

### 以下代码运行环境

- OS: macOS Sequoia 15.5
- Python: 3.10.14
- PaddlePaddle: 3.0.0
- paddle2onnx: 2.0.2.rc1
- paddlex: 3.0.0
- rapidocr: 2.1.0

### 1. 模型跑通

该步骤主要先基于PaddleX可以正确使用PP-OCRv5_mobile_det模型得到正确结果。

该部分主要参考文档：[docs](https://paddlepaddle.github.io/PaddleX/latest/module_usage/tutorials/ocr_modules/text_recognition.html#_3)

安装`paddlex`:

```bash linenums="1"
pip install "paddlex[ocr]==3.0.0rc1"
```

测试PP-OCRv5_mobile_det模型能否正常识别：

测试用图：

![alt text](../images/1.jpg)

!!! tip

    运行以下代码时，模型会自动下载到 **/Users/用户名/.paddlex/official_models** 下。

```python linenums="1"

from paddleocr import PaddleOCR
# 初始化 PaddleOCR 实例

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

# 对示例图像执行 OCR 推理
result = ocr.predict(
    input="https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png")

# 可视化结果并保存 json 结果
for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")
```

预期结果如下，表明成功运行：

![alt text](../images/general_ocr_002_ocr_res_img.png)

### 2. 模型转换

该部分主要参考文档： [docs](https://paddlepaddle.github.io/PaddleX/latest/pipeline_deploy/paddle2onnx.html?h=paddle2onnx#22)

PaddleX官方集成了paddle2onnx的转换代码：

```bash linenums="1"
paddlex --paddle2onnx --paddle_model_dir models/PP-OCRv5_mobile_det --onnx_model_dir models/PP-OCRv5_mobile_det
```

输出日志如下，表明转换成功：

```bash linenums="1"
Input dir: models/PP-OCRv5_mobile_det
Output dir: models/PP-OCRv5_mobile_det
Paddle2ONNX conversion starting...
  warnings.warn(warning_message)
[Paddle2ONNX] Start parsing the Paddle model file...
[Paddle2ONNX] Use opset_version = 7 for ONNX export.
[Paddle2ONNX] PaddlePaddle model is exported as ONNX format now.
2025-05-14 08:21:23 [INFO]      Try to perform optimization on the ONNX model with onnxoptimizer.
2025-05-14 08:21:23 [INFO]      ONNX model saved in models/PP-OCRv5_mobile_det/inference.onnx.
Paddle2ONNX conversion succeeded
Done
```

### 3. 模型推理验证

该部分主要是在RapidOCR项目中测试能否直接使用onnx模型。要点主要是确定模型前后处理是否兼容。从PaddleX[官方文档](https://paddlepaddle.github.io/PaddleX/latest/module_usage/tutorials/ocr_modules/text_recognition.html#_2)中可以看到：

> PP-OCRv5_mobile_det是在PP-OCRv4_server_rec的基础上，在更多中文文档数据和PP-OCR训练数据的混合数据训练而成，增加了部分繁体字、日文、特殊字符的识别能力，可支持识别的字符为1.5万+，除文档相关的文字识别能力提升外，也同时提升了通用文字的识别能力

以上说明了该模型与PP-OCRv4_server_rec模型结构相同，前后处理也相同。唯一做的就是添加了更多数据，扩展了字典个数，从6623扩展到15630个。因此，可以直接使用RapidOCR来快速推理验证。代码如下：

```python linenums="1"
from rapidocr import RapidOCR

model_path = "models/PP-OCRv5_mobile_det/inference.onnx"
key_path = "models/ppocrv4_doc_dict.txt"
engine = RapidOCR(params={"Rec.model_path": model_path, "Rec.rec_keys_path": key_path})

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_path)
print(result)

result.vis("vis_result.jpg")
```

![alt text](../images/vis_result.jpg)

### 4. 模型精度测试

该部分主要使用[TextRecMetric](https://github.com/SWHL/TextRecMetric)和测试集[text_rec_test_dataset](https://huggingface.co/datasets/SWHL/text_rec_test_dataset)来评测。

需要注意的是，**PP-OCRv5_mobile_det模型更加侧重生僻字和一些符号识别。** 当前测试集并未着重收集生僻字和一些符号的数据，因此以下指标会有些偏低。如需自己使用，请在自己场景下测试效果。

相关测试步骤请参见[TextRecMetric](https://github.com/SWHL/TextRecMetric)的README，一步一步来就行。我这里测试最终精度如下：

```json
{'ExactMatch': 0.8097, 'CharMatch': 0.9444, 'avg_elapse': 0.0818}
```

该结果已经更新到[开源OCR模型对比](./model_summary.md)中。

### 5. 集成到rapidocr中

该部分主要包括将字典文件写入到ONNX模型中、托管模型到魔搭、更改rapidocr代码适配等。

#### 字典文件写入ONNX模型

该步骤仅存在文本识别模型中，文本检测模型没有这个步骤。

??? info "详细代码"

    ```python linenums="1"
    from pathlib import Path
    from typing import List, Union

    import onnx
    import onnxruntime as ort
    from onnx import ModelProto


    def read_txt(txt_path: Union[Path, str]) -> List[str]:
        with open(txt_path, "r", encoding="utf-8") as f:
            data = [v.rstrip("\n") for v in f]
        return data


    class ONNXMetaOp:
        @classmethod
        def add_meta(
            cls,
            model_path: Union[str, Path],
            key: str,
            value: List[str],
            delimiter: str = "\n",
        ) -> ModelProto:
            model = onnx.load_model(model_path)
            meta = model.metadata_props.add()
            meta.key = key
            meta.value = delimiter.join(value)
            return model

        @classmethod
        def get_meta(
            cls, model_path: Union[str, Path], key: str, split_sym: str = "\n"
        ) -> List[str]:
            sess = ort.InferenceSession(model_path)
            meta_map = sess.get_modelmeta().custom_metadata_map
            key_content = meta_map.get(key)
            key_list = key_content.split(split_sym)
            return key_list

        @classmethod
        def del_meta(cls, model_path: Union[str, Path]) -> ModelProto:
            model = onnx.load_model(model_path)
            del model.metadata_props[:]
            return model

        @classmethod
        def save_model(cls, save_path: Union[str, Path], model: ModelProto):
            onnx.save_model(model, save_path)


    dicts = read_txt(
        "models/ppocrv4_doc_dict.txt"
    )
    model_path = "models/PP-OCRv5_mobile_det.onnx"
    model = ONNXMetaOp.add_meta(model_path, key="character", value=dicts)

    new_model_path = "models/PP-OCRv5_mobile_det_with_dict.onnx"
    ONNXMetaOp.save_model(new_model_path, model)

    t = ONNXMetaOp.get_meta(new_model_path, key="character")
    print(t)
    ```

#### 托管模型到魔搭

该部分主要是涉及模型上传到对应位置，并合理命名。注意上传完成后，需要打Tag，避免后续rapidocr whl包中找不到模型下载路径。

我这里已经上传到了魔搭上，详细链接参见：[link](https://www.modelscope.cn/models/RapidAI/RapidOCR/files?version=v2.1.0)

#### 更改rapidocr代码适配

该部分主要涉及到更改[default_models.yaml](https://github.com/RapidAI/RapidOCR/blob/4d35ed272a1192afbcb95e823d99eb14c86b7893/python/rapidocr/default_models.yaml)和[paddle.py](https://github.com/RapidAI/RapidOCR/blob/4d35ed272a1192afbcb95e823d99eb14c86b7893/python/rapidocr/inference_engine/paddle.py)的代码来适配。

同时，需要添加对应的单元测试，在保证之前单测成功的同时，新的针对性该模型的单测也能通过。

我这里已经做完了，小伙伴们感兴趣可以去看看源码。

#### 发布新版本

因为这次算是功能新增，按照语义化版本号来看，我们版本号需要从v2.0.7 → v2.1.0。

我只需要在github仓库中，打一个v2.1.0的tag，Github Action会自动跑所有单元测试，自动发版到pypi。

### 写在最后

至此，集成工作就基本完成了。
