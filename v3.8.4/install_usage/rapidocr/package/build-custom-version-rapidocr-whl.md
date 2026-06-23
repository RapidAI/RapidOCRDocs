<!-- more -->

RapidOCR 现在使用 `pyproject.toml` + `setuptools-scm` 构建 wheel。构建环境要求 Python `>=3.9`；构建出的 wheel 支持安装到 Python `>=3.8`。

### 1. 进入 Python 包目录

```bash linenums="1"
git clone https://github.com/RapidAI/RapidOCR.git
cd RapidOCR/python
```

### 2. 安装构建工具和资源准备依赖

```bash linenums="1"
python -m pip install --upgrade pip
python -m pip install build setuptools wheel setuptools-scm PyYAML
```

如果还需要运行测试或准备默认模型，也可以安装完整依赖：

```bash linenums="1"
python -m pip install -r requirements.txt
```

### 3. 准备默认模型资源

```bash linenums="1"
python tools/prepare_wheel_assets.py
```

这一步会：

- 根据 `rapidocr/config.yaml` 推导默认 Det / Cls / Rec 模型
- 从 `rapidocr/default_models.yaml` 读取下载地址和 SHA256
- 下载或校验模型文件
- 生成 `MANIFEST.in`，确保这些模型被打进 wheel

如果只想检查模型是否已准备好：

```bash linenums="1"
python tools/prepare_wheel_assets.py --check
```

### 4. 指定版本号并构建 wheel

```bash linenums="1"
SETUPTOOLS_SCM_PRETEND_VERSION_FOR_RAPIDOCR=3.1.0 python -m build --wheel
```

构建产物会生成到：

```text
dist/
```

例如：

```text
dist/rapidocr-3.1.0-py3-none-any.whl
```

### 5. 验证 wheel 版本

```bash linenums="1"
unzip -p dist/rapidocr-3.1.0-py3-none-any.whl "*/METADATA" | grep "^Version:"
```

期望输出：

```text
Version: 3.1.0
```

### 6. 验证模型是否打进 wheel

```bash linenums="1"
python -m zipfile -l dist/rapidocr-3.1.0-py3-none-any.whl | grep "rapidocr/models"
```

应该能看到默认模型文件。

如果不手动指定版本，也可以通过 git tag 构建：

```bash linenums="1"
git tag v3.1.0
python tools/prepare_wheel_assets.py
python -m build --wheel
```

当当前 commit 正好位于 `v3.1.0` tag 上时，`setuptools-scm` 会推导出版本 `3.1.0`。如果当前 commit 不在 tag 上，会生成 dev 版本。
