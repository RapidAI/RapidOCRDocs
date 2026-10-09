## 支持的输入类型

`RapidOCR` 支持传入以下图像类型：

- 本地图像路径或图像 URL：`str`、`pathlib.Path`
- 图像数据：`numpy.ndarray`、`bytes`、`PIL.Image.Image`
- 内存地址：`MemoryImage`、`RawMemoryImage`（`rapidocr>=3.10.0`）

通过文件路径、URL、`bytes` 或 `PIL.Image.Image` 传入图像时，支持的图像格式与 Pillow 保持一致，详情参见 [Pillow 图像格式](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)。

## 从内存地址读取压缩图像

`MemoryImage` 用于读取内存中的完整压缩图像数据，例如 JPEG, PNG 文件的字节内容。初始化时需传入内存首地址和数据长度：

```python linenums="1"
import ctypes
from pathlib import Path

from rapidocr import RapidOCR
from rapidocr.utils.load_image import MemoryImage

encoded = Path("test.jpg").read_bytes()
buffer = ctypes.create_string_buffer(encoded)
memory_img = MemoryImage(
    address=ctypes.addressof(buffer),
    length=len(encoded),
)

engine = RapidOCR()
result = engine(memory_img)
print(result)
```

## 从内存地址读取原始像素缓冲区

`RawMemoryImage` 用于读取未经 JPEG, PNG 等格式编码的原始像素数据。除了内存地址和数据长度，还需提供图像宽高、像素格式等元数据：

```python linenums="1"
import cv2

from rapidocr import RapidOCR
from rapidocr.utils.load_image import RawMemoryImage

img = cv2.imread("test.jpg")
memory_img = RawMemoryImage(
    address=img.ctypes.data,
    length=img.nbytes,
    width=img.shape[1],
    height=img.shape[0],
    pixel_format="BGR",
    stride=img.strides[0],
)

engine = RapidOCR()
result = engine(memory_img)
print(result)
```

`RawMemoryImage` 参数说明：

- `address`：像素缓冲区的内存首地址。
- `length`：缓冲区长度，不能小于 `stride * height`。
- `width`、`height`：图像宽度和高度，单位为像素。
- `pixel_format`：像素格式，支持 `GRAY`、`GRAY8`、`BGR`、`BGR24`、`RGB`、`RGB24`、`BGRA`、`BGRA32`、`BGRX`、`RGBA`、`RGBA32` 和 `RGBX`。
- `stride`：每行数据占用的字节数；不传时按图像宽度和通道数计算。
- `bottom_up`：是否按自底向上的顺序存储图像行，默认为 `False`。

!!! warning

    `MemoryImage` 和 `RawMemoryImage` 只保存内存地址，不持有底层数据。调用 `engine()` 完成前，必须确保示例中的 `buffer` 或 `img` 等底层对象仍然有效；不要传入已经释放或长度不正确的内存地址。
