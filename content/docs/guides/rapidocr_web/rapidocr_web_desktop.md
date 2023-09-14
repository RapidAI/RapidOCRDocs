---
weight: 3
date: "2023-09-08"
draft: false
author: "SWHL"
title: "RapidOCRWeb桌面版使用教程"
icon: "code"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---

#### 引言
- 说明：桌面版指的是可以直接解压，双击即可运行的版本。
- 通俗来说，对`rapidocr_web`做了打包，将相关依赖全部放到一个zip包中，不需要本地有额外的环境，降低使用门槛。
- 下面会以Windows版为例，作简要说明。

#### 使用步骤
1. 下载对应的zip包
    - 目前已有的zip包如下：
         ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/e60a6411-7d3d-4063-9e0a-6d85df78de7a)
    - 下载方式: [Github](https://github.com/RapidAI/RapidOCR/releases/tag/v0.1.5) | [百度网盘](https://pan.baidu.com/s/1Kfk-56I4GoKw8xMZlqUUEw?pwd=rfen) | QQ群共享（群号：755960114）
2. 解压目录如下示例

    <details>

    ```text
    .
    ├── api-ms-win-core-console-l1-1-0.dll
    ├── api-ms-win-core-datetime-l1-1-0.dll
    ├── api-ms-win-core-debug-l1-1-0.dll
    ├── api-ms-win-core-errorhandling-l1-1-0.dll
    ├── api-ms-win-core-file-l1-1-0.dll
    ├── api-ms-win-core-file-l1-2-0.dll
    ├── api-ms-win-core-file-l2-1-0.dll
    ├── api-ms-win-core-handle-l1-1-0.dll
    ├── api-ms-win-core-heap-l1-1-0.dll
    ├── api-ms-win-core-interlocked-l1-1-0.dll
    ├── api-ms-win-core-libraryloader-l1-1-0.dll
    ├── api-ms-win-core-localization-l1-2-0.dll
    ├── api-ms-win-core-memory-l1-1-0.dll
    ├── api-ms-win-core-namedpipe-l1-1-0.dll
    ├── api-ms-win-core-processenvironment-l1-1-0.dll
    ├── api-ms-win-core-processthreads-l1-1-0.dll
    ├── api-ms-win-core-processthreads-l1-1-1.dll
    ├── api-ms-win-core-profile-l1-1-0.dll
    ├── api-ms-win-core-rtlsupport-l1-1-0.dll
    ├── api-ms-win-core-string-l1-1-0.dll
    ├── api-ms-win-core-synch-l1-1-0.dll
    ├── api-ms-win-core-synch-l1-2-0.dll
    ├── api-ms-win-core-sysinfo-l1-1-0.dll
    ├── api-ms-win-core-timezone-l1-1-0.dll
    ├── api-ms-win-core-util-l1-1-0.dll
    ├── api-ms-win-crt-conio-l1-1-0.dll
    ├── api-ms-win-crt-convert-l1-1-0.dll
    ├── api-ms-win-crt-environment-l1-1-0.dll
    ├── api-ms-win-crt-filesystem-l1-1-0.dll
    ├── api-ms-win-crt-heap-l1-1-0.dll
    ├── api-ms-win-crt-locale-l1-1-0.dll
    ├── api-ms-win-crt-math-l1-1-0.dll
    ├── api-ms-win-crt-process-l1-1-0.dll
    ├── api-ms-win-crt-runtime-l1-1-0.dll
    ├── api-ms-win-crt-stdio-l1-1-0.dll
    ├── api-ms-win-crt-string-l1-1-0.dll
    ├── api-ms-win-crt-time-l1-1-0.dll
    ├── api-ms-win-crt-utility-l1-1-0.dll
    ├── _asyncio.pyd
    ├── base_library.zip
    ├── _bz2.pyd
    ├── _ctypes.pyd
    ├── cv2
    ├── _decimal.pyd
    ├── _hashlib.pyd
    ├── importlib_metadata-6.6.0.dist-info
    ├── libcrypto-1_1.dll
    ├── libopenblas.XWYDX2IKJW2NMTWSFYNGFUWKQU3LYTCZ.gfortran-win_amd64.dll
    ├── libssl-1_1.dll
    ├── _lzma.pyd
    ├── markupsafe
    ├── MSVCP140.dll
    ├── _multiprocessing.pyd
    ├── numpy
    ├── onnxruntime
    ├── _overlapped.pyd
    ├── PIL
    ├── pyclipper
    ├── pyexpat.pyd
    ├── python37.dll
    ├── python3.dll
    ├── _queue.pyd
    ├── rapidocr_onnxruntime
    ├── RapidOCRWeb.exe
    ├── select.pyd
    ├── shapely
    ├── Shapely.libs
    ├── _socket.pyd
    ├── _ssl.pyd
    ├── static
    ├── templates
    ├── ucrtbase.dll
    ├── unicodedata.pyd
    ├── VCRUNTIME140_1.dll
    ├── VCRUNTIME140.dll
    └── yaml
    ```
    </details>

3. 双击`RapidOCRWeb.exe`运行，界面如下图所示：

   ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/5ff1d582-bde8-407f-83be-f3a3ec9c9b87)

4. 浏览器中打开`http://localhost:9003/`，即可看到熟悉的RapidOCRWeb界面。
    - ⚠️如果遇到浏览器不显示界面的情况，可以尝试在黑框上按`Ctrl + C`
    - 示例图如下：

        ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/c113c1c6-376a-48b2-9e52-201e499b1a4f)
