---
comments: true
hide:
  - navigation
  - toc
---

### 1. 安装
```bash linenums="1"
pip install rapidocr_onnxruntime
```

### 2. 使用

=== "命令行使用"

    ```bash linenums="1"
    rapidocr_onnxruntime -img tests/test_files/ch_en_num.jpg
    ```

=== "Python使用"

    ```python linenums="1"
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()

    img_path = 'tests/test_files/ch_en_num.jpg'
    result, elapse = engine(img_path)
    print(result)
    ```


### 3. 查看效果

```python linenums="1"
[
    [[[9.0, 2.0], [321.0, 11.0], [318.0, 102.0], [6.0, 93.0]], '正品促销', '0.7986101984977723'],
    [[[70.0, 98.0], [251.0, 98.0], [251.0, 125.0], [70.0, 125.0]], '大桶装更划算', '0.7368737288883754'],
    [[[69.0, 144.0], [255.0, 144.0], [255.0, 164.0], [69.0, 164.0]], '强力去污符合国标', '0.8172478278477987'],
    [[[107.0, 170.0], [219.0, 170.0], [219.0, 182.0], [107.0, 182.0]], '-40深度防冻不结冰', '0.8655969283797524'],
    [[[35.0, 227.0], [63.0, 227.0], [63.0, 236.0], [35.0, 236.0]], '日常价?', '0.6502826035022735'],
    [[[141.0, 223.0], [187.0, 225.0], [185.0, 249.0], [139.0, 247.0]], '直击', '0.596031109491984'],
    [[[34.0, 234.0], [81.0, 236.0], [80.0, 254.0], [33.0, 252.0]], '10.0起', '0.8231529593467712'],
    [[[257.0, 234.0], [304.0, 236.0], [303.0, 253.0], [256.0, 251.0]], '10.0起', '0.8304102122783661'],
    [[[258.0, 227.0], [287.0, 226.0], [287.0, 236.0], [258.0, 237.0]], '日常价?', '0.5725070595741272'],
    [[[140.0, 245.0], [186.0, 246.0], [186.0, 272.0], [139.0, 271.0]], '底价', '0.5142453710238138'],
    [[[129.0, 290.0], [207.0, 292.0], [206.0, 339.0], [128.0, 337.0]], '5.8', '0.6341951936483383'],
    [[[98.0, 320.0], [129.0, 320.0], [129.0, 331.0], [98.0, 331.0]], '券后价?', '0.6209247708320618'],
    [[[114.0, 343.0], [210.0, 343.0], [210.0, 355.0], [114.0, 355.0]], '惊喜福利不容错过', '0.8640043867958916'],
    [[[69.0, 363.0], [151.0, 363.0], [151.0, 383.0], [69.0, 383.0]], '极速发货', '0.7552512288093567'],
    [[[201.0, 363.0], [285.0, 363.0], [285.0, 383.0], [201.0, 383.0]], '冰点标准', '0.7194759607315063'],
    [[[68.0, 392.0], [151.0, 392.0], [151.0, 412.0], [68.0, 412.0]], '破损就赔', '0.7711991906166077'],
    [[[202.0, 391.0], [285.0, 391.0], [285.0, 413.0], [202.0, 413.0]], '假一赔十', '0.6546663284301758']
]
```

### [其他编程语言支持](./blog/posts/other_programing_lan.md)