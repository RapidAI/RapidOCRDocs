---
title: Exporting OCR Results to Markdown
description: Convert RapidOCR output into a basic Markdown representation.
comments: true
hide:
  - toc
---

Basic Markdown export is available in `rapidocr>=3.2.0`. Enable word and character boxes when running OCR, then call `to_markdown()`:

```python
from rapidocr import RapidOCR

engine = RapidOCR()
image_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"

result = engine(
    image_url,
    return_word_box=True,
    return_single_char_box=True,
)

result.vis("vis_result.jpg")
markdown = result.to_markdown()
print(markdown)
```

The generated Markdown is a lightweight layout approximation. Complex document reconstruction may require additional layout-analysis and table-recognition components.
