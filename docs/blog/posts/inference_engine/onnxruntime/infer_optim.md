---
title: ONNXRuntime CPU推理优化
date: 2022-09-23
authors: [SWHL]
categories:
  - 推理引擎
comments: true
---


<!-- more -->

#### 引言

- 平时推理用的最多是ONNXRuntime，推理引擎的合适调配对推理性能有着至关重要的影响。但是有关于ONNXRuntime参数设置的资料却散落在各个地方，不能形成有效的指导意见。
- 因此，决定在这一篇文章中来梳理一下相关的设置。
- 以下参数都是来自`SessionOptions`中
- 相关测试代码可以前往[AI Studio](https://aistudio.baidu.com/aistudio/projectdetail/6109918?sUid=57084&shared=1&ts=1683438418669)查看
- 欢迎补充和指出不足之处。

#### 推荐常用设置

```python linenums="1"
import onnxruntime as rt

sess_options = rt.SessionOptions()
sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.log_severity_level = 4
sess_options.enable_cpu_mem_arena = False

# 其他参数，采用默认即可
```

#### [`enable_cpu_mem_arena`](https://onnxruntime.ai/docs/api/python/api_summary.html#onnxruntime.SessionOptions.enable_cpu_mem_arena)

- 作用：启用CPU上的**memory arena**。Arena可能会为将来预先申请很多内存。如果不想使用它，可以设置为`enable_cpu_mem_area=False`，默认是`True`
- 结论：建议关闭
  - 开启之后，占用内存会剧增（5618.3M >> 5.3M），且持续占用，不释放；推理时间只有大约13%提升

- 测试环境：
  - Python: 3.7.13
  - ONNXRuntime: 1.14.1
- 测试代码（来自[issue 11627](https://github.com/microsoft/onnxruntime/issues/11627)，[enable_cpu_memory_area_example.zip](https://github.com/microsoft/onnxruntime/files/8772315/enable_cpu_memory_area_example.zip)）

    ```python linenums="1"
    # pip install onnxruntime==1.14.1
    # pip install memory_profiler

    import numpy as np
    import onnxruntime as ort
    from memory_profiler import profile


    @profile
    def onnx_prediction(model_path, input_data):
        ort_sess = ort.InferenceSession(model_path, sess_options=sess_options)
        preds = ort_sess.run(output_names=["predictions"],
                             input_feed={"input_1": input_data})[0]
        return preds


    sess_options = ort.SessionOptions()
    sess_options.enable_cpu_mem_arena = False

    input_data = np.load('enable_cpu_memory_area_example/input.npy')
    print(f'input_data shape: {input_data.shape}')
    model_path = 'enable_cpu_memory_area_example/model.onnx'

    onnx_prediction(model_path, input_data)
    ```

- Windows端 | Mac端 | Linux端 测试情况都大致相同
    <details>

  - `enable_cpu_mem_arena=True`

        ```bash linenums="1"
        (demo) PS G:> python .\test_enable_cpu_mem_arena.py
        enable_cpu_mem_arena: True
        input_data shape: (32, 200, 200, 1)
        Filename: .\test_enable_cpu_mem_arena.py

        Line #    Mem usage    Increment  Occurrences   Line Contents
        =============================================================
            7     69.1 MiB     69.1 MiB           1   @profile
            8                                         def onnx_prediction(model_path, input_data):
            9     77.2 MiB      8.1 MiB           1       ort_sess = ort.InferenceSession(model_path, sess_options=sess_options)
            10     77.2 MiB      0.0 MiB           1       preds = ort_sess.run(output_names=["predictions"],
            11   5695.5 MiB   5618.3 MiB           1                            input_feed={"input_1": input_data})[0]
            12   5695.5 MiB      0.0 MiB           1       return preds
        ```

  - `enable_cpu_mem_arena=False`

        ```bash linenums="1"
        (demo) PS G:> python .\test_enable_cpu_mem_arena.py
        enable_cpu_mem_arena: False
        input_data shape: (32, 200, 200, 1)
        Filename: .\test_enable_cpu_mem_arena.py

        Line #    Mem usage    Increment  Occurrences   Line Contents
        =============================================================
            7     69.1 MiB     69.1 MiB           1   @profile
            8                                         def onnx_prediction(model_path, input_data):
            9     76.9 MiB      7.8 MiB           1       ort_sess = ort.InferenceSession(model_path, sess_options=sess_options)
            10     76.9 MiB      0.0 MiB           1       preds = ort_sess.run(output_names=["predictions"],
            11     82.1 MiB      5.3 MiB           1                            input_feed={"input_1": input_data})[0]
            12     82.1 MiB      0.0 MiB           1       return preds
        ```

    </details>

#### `enable_profiling`

- 开启这个参数，在推理时，会生成一个类似`onnxruntime_profile__2023-05-07_09-02-15.json`的日志文件，包含详细的性能数据（线程、每个运算符的延迟等）。
- 建议开启
- 示例代码：

    ```python linenums="1"
    import onnxruntime as rt

    sess_options = rt.SessionOptions()
    sess_options.enable_profiling = True
    ```

#### `execution_mode`

- 设置运行模型的模式，包括`rt.ExecutionMode.ORT_SEQUENTIAL`和`rt.ExecutionMode.ORT_PARALLEL`。一个序列执行，一个并行。默认是序列执行
- **通常来说，当一个模型中有许多分支时，可以设置该参数为`ORT_PARALLEL`来达到更好的表现**
- 当设置`sess_options.execution_mode = rt.ExecutionMode.ORT_PARALLEL`时，可以设置`sess_options.inter_op_num_threads`来控制使用线程的数量，来并行化执行（模型中各个节点之间）

#### `inter_op_num_threads`

- 设置并行化执行图（跨节点）时，使用的线程数。默认是0，交由onnxruntime自行决定。
- 示例代码：

    ```python linenums="1"
    import onnxruntime as rt

    sess_options = rt.SessionOptions()
    sess_options.inter_op_num_threads = 2
    ```

#### `intra_op_num_threads`

- 设置并行化执行图（内部节点）时，使用的线程数。默认是0，交由onnxruntime自行决定，一般会选择使用设备上所有的核。
- ⚠️ 这个值并不是越大越好，具体参考[AI Studio](https://aistudio.baidu.com/aistudio/projectdetail/6109918?sUid=57084&shared=1&ts=1683438418669)中的消融实验。
- 示例代码：

    ```python linenums="1"
    import onnxruntime as rt

    sess_options = rt.SessionOptions()
    sess_options.intra_op_num_threads = 2
    ```

#### [`graph_optimization_level`](https://github.com/microsoft/onnxruntime-openenclave/blob/openenclave-public/docs/ONNX_Runtime_Graph_Optimizations.md)

- 运行图时，对图中算子的优化水平。默认是开启全部算子的优化。建议采用默认值即可。
- 可选的枚举值有：`ORT_DISABLE_ALL | ORT_ENABLE_BASIC | ORT_ENABLE_EXTENDED | ORT_ENABLE_ALL`
- 示例代码：

    ```python linenums="1"
    import onnxruntime as rt

    sess_options = rt.SessionOptions()
    sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL
    ```

#### 参考资料

- [ONNX Runtime Performance Tuning](https://github.com/microsoft/onnxruntime-openenclave/blob/openenclave-public/docs/ONNX_Runtime_Perf_Tuning.md)
- [Python API](https://onnxruntime.ai/docs/api/python/api_summary.html)
