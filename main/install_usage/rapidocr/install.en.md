<a href=""><img src="https://img.shields.io/badge/Python->=3.8,<4-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pepy.tech/project/rapidocr"><img src="https://static.pepy.tech/personalized-badge/rapidocr?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20rapidocr"></a>
<a href="https://pypi.org/project/rapidocr/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr"></a>

!!! warning

    The three packages `rapidocr_onnxruntime`, `rapidocr_openvino` and `rapidocr_paddle` are gradually being retired. Development continues on `rapidocr`.

#### Introduction

`rapidocr` merges `rapidocr_onnxruntime`, `rapidocr_openvino` and `rapidocr_paddle`, and adds support for PyTorch inference.

In `rapidocr>=2.0.0,<=2.0.5`, the ONNX Runtime CPU build is used as the default inference engine. You can install another inference engine and switch to GPU inference through the corresponding parameters, which later pages describe in detail.

Starting from `rapidocr>=2.0.6`, ONNX Runtime is no longer a dependency, although it remains the default inference engine. From that version onwards you need to install the inference engine you want to use yourself.

`rapidocr>=3.10.0`: The dependent `opencv` library has been changed from `opencv-python` to `opencv-python-headless`.

Server-side, Docker, headless environment: use `opencv-python-headless` — simply install it directly.

If you need GUI features such as `imshow` and window display: switch to `opencv-python`. Do not install both packages at the same time to avoid cv2 conflicts.

```bash linenums="1"
pip uninstall opencv-python-headless
pip install opencv-python
```

#### Installation

If all goes well, a single command is enough to get started. The `rapidocr` package is about 27.2 MB and contains three models: text detection, text line orientation classification and text recognition. The small models are compact enough to be bundled into the wheel, so pip install is all that is needed.

```bash linenums="1"
pip install rapidocr onnxruntime
```

If the download is slow in your region, specify a closer mirror. For example, using the Tsinghua mirror:

```bash linenums="1"
pip install rapidocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### Install Additional Dependencies as Needed

> Supported for `rapidocr>=3.10.0`

If you need to use right-to-left languages such as Arabic, install RTL support:

```bash linenums="1"
pip install "rapidocr[rtl]" onnxruntime
```

If rapidocr and the inference engine are already installed, just install the extra dependency:

```bash linenums="1"
pip install "rapidocr[rtl]"
```

The `rtl` extra installs `python-bidi`, which adjusts the display order for right-to-left languages.

#### Verify the installation

=== "`rapidocr>=2.0.3`"

    ```bash linenums="1" hl_lines="11"
    $ rapidocr check

    # The installation is correct when you see the following output
    [INFO] 2026-06-23 12:51:43,979 [RapidOCR] base.py:23: Using engine_name: onnxruntime
    [INFO] 2026-06-23 12:51:44,045 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_det_small.onnx
    [INFO] 2026-06-23 12:51:44,046 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_det_small.onnx
    [INFO] 2026-06-23 12:51:44,127 [RapidOCR] base.py:23: Using engine_name: onnxruntime
    [INFO] 2026-06-23 12:51:44,129 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_mobile.onnx
    [INFO] 2026-06-23 12:51:44,129 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/ch_ppocr_mobile_v2.0_cls_mobile.onnx
    [INFO] 2026-06-23 12:51:44,190 [RapidOCR] base.py:23: Using engine_name: onnxruntime
    [INFO] 2026-06-23 12:51:44,260 [RapidOCR] download_file.py:60: File exists and is valid: /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_rec_small.onnx
    [INFO] 2026-06-23 12:51:44,260 [RapidOCR] main.py:63: Using /usr/local/lib/python3.12/dist-packages/rapidocr/models/PP-OCRv6_rec_small.onnx
    Success! rapidocr is installed correctly!
    ```

=== "`rapidocr>=2.0.0,<2.0.2`"

    Run the following command. The installation succeeded if the recognized text is printed in the terminal.

    ```bash linenums="1"
    rapidocr -img "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg" --vis_res
    ```

!!! info

    If a dependency fails to install, install that dependency on its own first and then install `rapidocr`.

The dependencies are:

```txt linenums="1"
pyclipper>=1.2.0
opencv-python-headless>=4.5.1.48
numpy>=1.19.5,<3.0.0
six>=1.15.0
Shapely>=1.7.1,!=2.0.4  # python3.12 2.0.4 bug
PyYAML
Pillow
tqdm
omegaconf!=2.2.1 # https://github.com/omry/omegaconf/issues/934
requests
colorlog
```
