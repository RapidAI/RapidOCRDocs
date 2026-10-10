--by [DeadWood8](https://github.com/DeadWood8)

### Packaging environment

- `OS`: Windows 11
- `Python`: 3.8.10
- `rapidocr_onnxruntime`: 1.2.0
- `nuitka`: 1.5.3
- `onnxruntime`: 1.14.0

### Packaging steps

#### Step 1: Install `Nuitka`

```bash linenums="1"
pip install nuitka
```

The first installation automatically downloads MinGW and ccache. You can also configure them manually.

#### Step 2: Modify the source

!!! note

    Starting with `rapidocr_onnxruntime>=1.2.8`, the source below is already fixed and this step can be skipped.

Modify the `rapidocr-onnxruntime` source so all dependencies can be packaged. Open `rapid_ocr_api.py` in the installed package (usually under `Lib\\site-packages\\rapidocr_onnxruntime`) and edit lines **39-52** as shown:

![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-43-17-2196674a.png)

Package `nuitka`:

```bash linenums="1"
cd rapidocr_web
nuitka --mingw64 --standalone --show-memory --show-progress --nofollow-import-to=tkinter --output-dir=out ocrweb.py
```

![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-43-37-1b48293b.png)

#### Step 3: Copy static files

The packaged files are in `out\\ocrweb.dist`. Copy the Web project and the required `rapidocr-onnxruntime` files into this directory.

![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-45-56-5fadb69c.png)

Copy the `static` and `templates` directories from `rapidocr_web` into `out\\ocrweb.dist`. Create `out\\ocrweb.dist\\rapidocr_onnxruntime` and copy `config.yaml` and the `models` directory from the installed package into it.

#### Step 4: Run the program

Open `out\\ocrweb.dist` and double-click `ocrweb.exe`.

![](https://raw.githubusercontent.com/RapidAI/RapidOCRDocs-Assets/main/images/2026/2026-10-08_11-44-01-23818d58.png)

Download the packaged executable: [Baidu Netdisk](https://pan.baidu.com/s/1nj_1rjuVu76drKBZDY9Bww?pwd=xnu7) | [Google Drive](https://drive.google.com/drive/folders/1okQj22XxLUptyhjKQcRU25eI8Ya693gf?usp=share_link) | [Gitee](https://gitee.com/RapidAI/RapidOCR/releases/download/v1.2.0/ocrweb.dist.rar)

#### Additional note

To prevent a console window from appearing, add `--windows-disable-console` to the packaging command:

```bash linenums="1"
nuitka --mingw64 --standalone --show-memory --show-progress --nofollow-import-to=tkinter --windows-disable-console --output-dir=out ocrweb.py
```
