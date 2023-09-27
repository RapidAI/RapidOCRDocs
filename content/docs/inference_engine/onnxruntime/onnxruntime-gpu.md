---
weight: 403
title: "GPU版推理"
description:
icon: menu_book
date: "2023-09-24"
draft: false
toc: true
---

### onnxruntime-gpu版相关说明
- 目前已知在onnxruntime-gpu上测试过的小伙伴，反映都是GPU推理速度比在CPU上慢很多。关于该问题，已经提了相关issue，具体可参见[onnxruntime issue#13198](https://github.com/microsoft/onnxruntime/issues/13198)

### 有关`onnxruntime-gpu`推理慢的相关帖子
- [Pre-allocating dynamic shaped tensor memory for ONNX runtime inference?](https://stackoverflow.com/questions/75553839/pre-allocating-dynamic-shaped-tensor-memory-for-onnx-runtime-inference)

### 快速查看比较版本
- 国外小伙伴可以基于[Google Colab](https://colab.research.google.com/gist/SWHL/673c39bf07f4cc4ddcb0e196c3e378e6/testortinfer.ipynb)，国内的小伙伴可以基于百度的[AI Studio](https://aistudio.baidu.com/aistudio/projectdetail/4634684?contributionType=1&sUid=57084&shared=1&ts=1664700017761)来查看效果

### 自己折腾版
1. **onnxruntime-gpu**需要严格按照与CUDA、cuDNN版本对应来安装，具体参考[文档](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements)，**这一步关乎后面是否可以成功调用GPU**。
   - 以下是安装示例：
        - 所用机器环境情况：
            - `nvcc-smi`显示**CUDA Driver API**版本：11.7
            - `nccc -V`显示**CUDA Runtime API**版本：11.6
            - 以上两个版本的对应关系，可参考[博客](https://blog.csdn.net/weixin_39518984/article/details/111406728)
        - 具体安装命令如下：
            ```bash {linenos=table}
            conda install cudatoolkit=11.6.0
            conda install cudnn=8.3.2.44
            pip install onnxruntime-gpu==1.12.0
            ```
        - 验证是否可以`onnxruntime-gpu`正常调用GPU
            1. 验证`get_device()`是否可返回GPU
                ```python {linenos=table}
                import onnxruntime as ort

                print(ort.get_device())
                # GPU
                ```
            2. 如果第一步满足了，继续验证`onnxruntime-gpu`加载模型时是否可以调用GPU
                ```python {linenos=table}
                import onnxruntime as ort

                providers = [
                    ('CUDAExecutionProvider', {
                        'device_id': 0,
                        'arena_extend_strategy': 'kNextPowerOfTwo',
                        'gpu_mem_limit': 2 * 1024 * 1024 * 1024,
                        'cudnn_conv_algo_search': 'EXHAUSTIVE',
                        'do_copy_in_default_stream': True,
                    }),
                    'CPUExecutionProvider',
                ]

                # download link: https://github.com/openvinotoolkit/openvino/files/9355419/super_resolution.zip
                model_path = 'super_resolution.onnx'
                session = ort.InferenceSession(model_path, providers=providers)

                print(session.get_providers())
                # 如果输出中含有CUDAExecutionProvider,则证明可以正常调用GPU
                # ['CUDAExecutionProvider', 'CPUExecutionProvider']
                ```
2. 更改[`config.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr_onnxruntime/config.yaml)中对应部分的参数即可，详细参数介绍参见[官方文档](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html)。
    ```yaml
    use_cuda: true
    CUDAExecutionProvider:
        device_id: 0
        arena_extend_strategy: kNextPowerOfTwo
        gpu_mem_limit: 2 * 1024 * 1024 * 1024
        cudnn_conv_algo_search: EXHAUSTIVE
        do_copy_in_default_stream: true
    ```

3. 推理情况
   1. 下载基准测试数据集（`test_images_benchmark`），放到`tests/benchmark`目录下。
        - [百度网盘](https://pan.baidu.com/s/1R4gYtJt2G3ypGkLWGwUCKg?pwd=ceuo) | [Google Drive](https://drive.google.com/drive/folders/1IIOCcUXdWa43Tfpsiy6UQJmPsZLnmgFh?usp=sharing)
        - 最终目录结构如下：
            ```text
            tests/benchmark/
                ├── benchmark.py
                ├── config_gpu.yaml
                ├── config.yaml
                └── test_images_benchmark
            ```
   2. 运行以下代码（`python`目录下运行）：
        ```shell
        # CPU
        python tests/benchmark/benchmark.py --yaml_path config.yaml

        # GPU
        python tests/benchmark/benchmark.py --yaml_path config_gpu.yaml
        ```
   3. 运行相关信息汇总：（以下仅为个人测试情况，具体情况请自行测试）
        - 环境
            |测试者|设备|OS|CPU|GPU|onnxruntime-gpu|
            |:--|:--|:--|:--|:--|:--|
            |[1][zhsunlight](https://github.com/zhsunlight)|宏碁(Acer) 暗影骑士·威N50-N93游戏台式机|Windows|十代i5-10400F 16G 512G SSD|NVIDIA GeForce GTX 1660Super 6G|1.11.0|
            |[2][SWHL](https://github.com/SWHL)|服务器|Linux|AMD R9 5950X|NVIDIA GeForce RTX 3090|1.12.1|
        - 耗时
             |对应上面序号|CPU总耗时(s)|CPU平均耗时(s/img)|GPU总耗时(s)|GPU平均耗时(s/img)||
             |:---:|:---:|:---:|:---:|:---:|:---:|
             |[1]|296.8841|1.18282|646.14667|2.57429|
             |[2]|149.35427|0.50504|250.81760|0.99927|