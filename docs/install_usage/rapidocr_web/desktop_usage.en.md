---
comments: true
---

#### Introduction

- The desktop edition can be extracted and launched by double-clicking it.
- `rapidocr_web` and its dependencies are packaged into a ZIP archive, so no additional local environment is required.
- The example below uses Windows.

#### Usage

1. Download the corresponding ZIP package.
    - Available packages:
      ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/e60a6411-7d3d-4063-9e0a-6d85df78de7a)
    - Download from [GitHub](https://github.com/RapidAI/RapidOCR/releases/tag/v0.1.5), [Baidu Netdisk](https://pan.baidu.com/s/1Kfk-56I4GoKw8xMZlqUUEw?pwd=rfen), or QQ group files (group `755960114`).

2. Extract the package. The directory looks like this:

    <details>

      ```text linenums="1"
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
      ├── libcrypto-1-1.dll
      ├── libopenblas.XWYDX2IKJW2NMTWSFYNGFUWKQU3LYTCZ.gfortran-win_amd64.dll
      ├── libssl-1-1.dll
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

3. Double-click `RapidOCRWeb.exe`. The interface appears as shown below:
    ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/5ff1d582-bde8-407f-83be-f3a3ec9c9b87)

4. Open `http://localhost:9003/` in a browser to access the RapidOCRWeb interface.
  ![image](https://github.com/RapidAI/RapidOCR/assets/28639377/c113c1c6-376a-48b2-9e52-201e499b1a4f)

    !!! note

        If the interface does not appear, try pressing `Ctrl + C` in the console window.
