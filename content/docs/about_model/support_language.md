---
weight: 4
date: "2023-09-11"
draft: false
author: "SWHL"
title: "支持识别语言及自助转换模型"
icon: "support"
description: ""
publishdate: "2023-09-08"
tags:
categories:
toc: true
---


## 支持识别的语言
- 因为本项目依托于PaddleOCR，所以理论上PaddleOCR支持识别的模型，RapidOCR都是支持的。


### 中英文检测和识别（可以直接使用）
- 因为中英文是最为常用的模型，所以在打包时，就默认将中英文识别的模型放到了`rapidocr_onnxruntime`和`rapidocr_openvino`中，直接pip安装即可使用。

### 其他语种检测和识别（需要转换）
- PaddleOCR中已有文本检测模型列表：[link](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md#1-%E6%96%87%E6%9C%AC%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9E%8B)
- PaddleOCR已有文本识别模型列表： [link](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md#2-%E6%96%87%E6%9C%AC%E8%AF%86%E5%88%AB%E6%A8%A1%E5%9E%8B)
- 除了slim和蒸馏过的模型，上面链接中的其他模型都可以转换为ONNX格式，通过RapidOCR快速部署。

### 自助转换使用教程
- ⚠️ 主要借助[`paddleocr_convert`](https://github.com/RapidAI/PaddleOCRModelConverter)库来实现。

#### [在线快速转换](https://swhl-paddleocrmodelconverter.hf.space/)
- 通过Hugging Face上的应用，快速转换模型。整体界面是下面这个样子
<div align="center">
    <img width="747" alt="image" src="https://github.com/RapidAI/RapidOCR/assets/28639377/fc9758e6-52c1-4f37-bf50-20c5384da2e1">
</div>

#### 离线安装库转换
1. 安装`paddleocr_convert`
   ```bash {linenos=table}
   pip install paddleocr_convert
   ```
2. 命令行使用
   - 用法:
        ```bash {linenos=table}
        $ paddleocr_convert -h
        usage: paddleocr_convert [-h] [-p MODEL_PATH] [-o SAVE_DIR]
                                [-txt_path TXT_PATH]

        optional arguments:
        -h, --help            show this help message and exit
        -p MODEL_PATH, --model_path MODEL_PATH
                                The inference model url or local path of paddleocr.
                                e.g. https://paddleocr.bj.bcebos.com/PP-
                                OCRv3/chinese/ch_PP-OCRv3_det_infer.tar or
                                models/ch_PP-OCRv3_det_infer.tar
        -o SAVE_DIR, --save_dir SAVE_DIR
                                The directory of saving the model.
        -txt_path TXT_PATH, --txt_path TXT_PATH
                                The raw txt url or local txt path, if the model is
                                recognition model.
        ```
   - 示例:
        ```bash {linenos=table}
        # online
        $ paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar \
                            -o models

        $ paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar \
                            -o models \
                            -txt_path https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt

        # offline
        $ paddleocr_convert -p models/ch_PP-OCRv3_det_infer.tar \
                            -o models

        $ paddleocr_convert -p models/ch_PP-OCRv3_rec_infer.tar \
                            -o models \
                            -txt_path models/ppocr_keys_v1.txt
        ```
3. 脚本使用
    - online mode
        ```python {linenos=table}
        from paddleocr_convert import PaddleOCRModelConvert

        converter = PaddleOCRModelConvert()
        save_dir = 'models'
        # online
        url = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar'
        txt_url = 'https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt'

        converter(url, save_dir, txt_path=txt_url)
        ```
    - offline mode
        ```python {linenos=table}
        from paddleocr_convert import PaddleOCRModelConvert

        converter = PaddleOCRModelConvert()
        save_dir = 'models'
        model_path = 'models/ch_PP-OCRv3_rec_infer.tar'
        txt_path = 'models/ppocr_keys_v1.txt'
        converter(model_path, save_dir, txt_path=txt_path)
        ```

#### 使用模型方法
- 假设要用日文识别模型，且已经转好，路径为：`local/models/japan.onnx`
1. 安装`rapidocr_onnxruntime`库
   ```bash {linenos=table}
   pip install rapidocr_onnxruntime
   ```
2. 脚本使用
   ```python {linenos=table}
   from rapidocr_onnxruntime import RapidOCR

   model_path = 'local/models/japan.onnx'
   engine = RapidOCR(rec_model_path=model_path)

   img = '1.jpg'
   result, elapse = engine(img)
   ```
3. 命令行使用
   ```bash {linenos=table}
   $ rapidocr_onnxruntime -img 1.jpg --rec_model_path local/models/japan.onnx
   ```
4. 其他文本检测模型也可同理，通过参数给出。支持的参数列表参见[这里](https://github.com/RapidAI/RapidOCR/tree/main/python#%E6%8E%A8%E8%8D%90pip%E5%AE%89%E8%A3%85%E5%BF%AB%E9%80%9F%E4%BD%BF%E7%94%A8)
   ```python {linenos=table}
   from rapidocr_onnxruntime import RapidOCR

   model_path = 'local/models/japan.onnx'
   engine = RapidOCR(rec_model_path=model_path, det_model_path='xxx.onnx')

   img = '1.jpg'
   result, elapse = engine(img)
   ```
