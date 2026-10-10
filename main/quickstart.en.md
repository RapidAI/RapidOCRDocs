### 1. Installation

```bash
pip install rapidocr onnxruntime
```

### 2. Usage

=== "CLI"

    ```bash
    rapidocr -img "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg" --vis_res
    ```

=== "Python"

    ```python
    from rapidocr import RapidOCR

    engine = RapidOCR()
    img_url = "https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/master/resources/test_files/ch_en_num.jpg"
    result = engine(img_url)

    print(result.txts)
    print(result.scores)
    result.vis("vis_result.jpg")
    ```

!!! note

    `result.vis()` downloads the font required for visualization on first use. In an offline environment, omit this line or configure `font_path` in advance.

### 3. View the visualization result

![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-09-14-1fc6ada8.png)

### 4. Inspect the `result`

`result` is a `RapidOCROutput` data class. The most commonly used fields are:

| Field | Type | Description |
| --- | --- | --- |
| `boxes` | `np.ndarray` | Four-point coordinates for each text line, shaped `(N, 4, 2)` |
| `txts` | `Tuple[str]` | Recognized text, in the same order as `boxes` |
| `scores` | `Tuple[float]` | Confidence score for each text line |
| `elapse` | `float` | Total inference time in seconds |

```python
print(result.boxes.shape)
print(result.txts)
print(result.scores)
```

See the [usage guide](install_usage/rapidocr/usage.md) for the complete output structure and stage-specific results.

### Recommended reading

#### [Support for other programming languages](https://rapidai.github.io/RapidOCRDocs/blog/posts/other_programing_lan/)
