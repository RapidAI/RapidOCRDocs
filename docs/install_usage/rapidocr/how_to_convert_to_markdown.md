---
comments: true
hide:
  - toc
---

在`rapidocr>=3.2.0`中粗略支持了导出markdown格式排版，后续会逐步优化。使用方法：

```python linenums="1" hl_lines="10"
from rapidocr import RapidOCR

engine = RapidOCR()

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url, return_word_box=True, return_single_char_box=True)
print(result)

result.vis("vis_result.jpg")
print(result.to_markdown())
```
