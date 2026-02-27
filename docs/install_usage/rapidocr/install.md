---
comments: true
hide:
  - toc
---

<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypistats.org/packages/rapidocr"><img src="https://img.shields.io/pypi/dd/rapidocr?style=flat&label=rapidocr"></a>
<a href="https://pypi.org/project/rapidocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr"></a>

!!! warning

    `rapidocr_onnxruntime`, `rapidocr_openvino`, `rapidocr_paddle`三个库逐渐不再维护，后续会以`rapidocr`为主。

#### 简介

`rapidocr`是合并了`rapidocr_onnxruntime`、`rapidocr_openvino`、`rapidocr_paddle`以及支持PyTorch推理的版本。

`rapidocr>=2.0.0,<=2.0.5`中，默认采用ONNXRuntime CPU版作为推理引擎，可以通过安装其他推理引擎，通过相应参数来使用GPU推理。该部分请参见后续文档。

`rapidocr>=2.0.6`中不再将ONNXRuntime库作为依赖包，但是仍然是默认推理引擎。该版本及以后需要小伙伴们手动安装所需推理引擎来使用。这样做是经过充分考虑了的。

#### 安装

顺利的话，两行命令即可使用上。`rapidocr`包大小约为15M左右，包含三个模型：文本检测、文本行方向分类和文本识别。其中mobile版模型较小，因此将相关模型都已打到whl包，可直接pip安装使用。

```bash linenums="1"
pip install onnxruntime
pip install rapidocr
```

国内安装速度慢的话，可以指定国内的安装源，如使用清华源：

```bash linenums="1"
pip install rapidocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 验证安装是否成功

=== "`rapidocr>=2.0.3`验证方式"

    ```bash linenums="1" hl_lines="11"
    $ rapidocr check

    # 输出以下内容即证明安装成功
    [INFO] 2025-03-20 21:46:47,854 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-20 21:46:47,886 utils.py:35: File already exists in /Users/jiahuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv4_det_infer.onnx
    [INFO] 2025-03-20 21:46:47,931 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-20 21:46:47,931 utils.py:35: File already exists in /Users/jiahuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_infer.onnx
    [INFO] 2025-03-20 21:46:47,949 base.py:30: Using engine_name: onnxruntime
    [INFO] 2025-03-20 21:46:47,949 utils.py:35: File already exists in /Users/jiahuawang/miniconda3/envs/py310/lib/python3.10/site-packages/rapidocr/models/ch_PP-OCRv4_rec_infer.onnx

    Success! rapidocr is installed correctly!
    ```

=== "`rapidocr>=2.0.0,<2.0.2`验证方式"

    运行以下代码，终端可以打印出文字内容，即安装成功。

    ```bash linenums="1"
    rapidocr -img "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg" --vis_res
    ```

!!! info

    如果在安装过程中，出现某个依赖包不能正确安装时，可先单独安装某个依赖包，之后再安装`rapidocr`即可。

依赖的包如下：

```txt linenums="1"
pyclipper>=1.2.0
opencv_python>=4.5.1.48
numpy>=1.19.5,<3.0.0
six>=1.15.0
Shapely>=1.7.1,!=2.0.4  # python3.12 2.0.4 bug
PyYAML
Pillow
tqdm
omegaconf
```
