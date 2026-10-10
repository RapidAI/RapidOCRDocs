---
title: RapidOCR Image Inputs
description: Supported RapidOCR image types and examples for compressed and raw memory buffers.
comments: true
---

## Supported input types

`RapidOCR` accepts:

- local paths and image URLs: `str`, `pathlib.Path`;
- image data: `numpy.ndarray`, `bytes`, `PIL.Image.Image`;
- memory addresses: `MemoryImage`, `RawMemoryImage` (`rapidocr>=3.10.0`).

Paths, URLs, byte strings and Pillow images support the formats listed in the [Pillow image format reference](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

## Compressed images in memory

Use `MemoryImage` for complete encoded image data such as JPEG or PNG bytes. Pass the first memory address and byte length:

```python
import ctypes
from pathlib import Path

from rapidocr import RapidOCR
from rapidocr.utils.load_image import MemoryImage

encoded = Path("test.jpg").read_bytes()
buffer = ctypes.create_string_buffer(encoded)
memory_image = MemoryImage(
    address=ctypes.addressof(buffer),
    length=len(encoded),
)

engine = RapidOCR()
result = engine(memory_image)
print(result)
```

## Raw pixel buffers in memory

Use `RawMemoryImage` for pixels that have not been encoded as JPEG, PNG or another image format:

```python
import cv2

from rapidocr import RapidOCR
from rapidocr.utils.load_image import RawMemoryImage

image = cv2.imread("test.jpg")
memory_image = RawMemoryImage(
    address=image.ctypes.data,
    length=image.nbytes,
    width=image.shape[1],
    height=image.shape[0],
    pixel_format="BGR",
    stride=image.strides[0],
)

engine = RapidOCR()
result = engine(memory_image)
print(result)
```

`RawMemoryImage` parameters:

| Parameter | Description |
| --- | --- |
| `address` | Address of the first byte in the pixel buffer. |
| `length` | Buffer length; it must be at least `stride * height`. |
| `width`, `height` | Image dimensions in pixels. |
| `pixel_format` | `GRAY`, `GRAY8`, `BGR`, `BGR24`, `RGB`, `RGB24`, `BGRA`, `BGRA32`, `BGRX`, `RGBA`, `RGBA32` or `RGBX`. |
| `stride` | Bytes per row. When omitted, it is calculated from width and channel count. |
| `bottom_up` | Whether rows are stored bottom-to-top. The default is `False`. |

!!! warning

    `MemoryImage` and `RawMemoryImage` store only an address; they do not own the underlying data. Keep `buffer`, `image` or the corresponding owner alive until `engine()` returns. Never pass released memory or an incorrect length.
