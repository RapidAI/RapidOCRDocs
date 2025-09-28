---
comments: true
hide:
  - toc
---

使用方法同样也是有两种：一是通过配置文件传入；二是通过初始化参数传入。

⚠️注意：Paddle格式模型需要使用`model_dir`来传入。原因是Paddle格式模型为多个文件组成，需要在程序中拼接为对应完整路径。

下面以通过初始化参数传入为例：

```python linenums="1" hl_lines="4"
from rapidocr import RapidOCR

engine = RapidOCR(
    params={"Det.model_path": "models/ch_PP-OCRv4_det_infer.onnx"}
)

img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
```

上面第4行通过`Det.model_path`指定了本地已经下载好的文本检测模型。文本方向分类和文本识别模型也可同样指定。(`Cls.model_path`和`Rec.model_path`同理)
