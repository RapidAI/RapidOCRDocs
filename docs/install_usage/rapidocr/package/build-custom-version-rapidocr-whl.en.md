---
title: How to Build a rapidocr Wheel for a Specific Version
date:
  created: 2026-06-12
authors:
  - SWHL
slug: build-custom-version-rapidocr-whl
comments: true
hide:
  - toc
---

<!-- more -->

RapidOCR now uses `pyproject.toml` + `setuptools-scm` to build wheels. The build environment requires Python `>=3.9`; the resulting wheel can be installed on Python `>=3.8`.

### 1. Enter the Python package directory

```bash linenums="1"
git clone https://github.com/RapidAI/RapidOCR.git
cd RapidOCR/python
```

### 2. Install the build tools and asset preparation dependencies

```bash linenums="1"
python -m pip install --upgrade pip
python -m pip install build setuptools wheel setuptools-scm PyYAML
```

If you also need to run tests or prepare the default models, you can install the full dependencies:

```bash linenums="1"
python -m pip install -r requirements.txt
```

### 3. Prepare the default model assets

```bash linenums="1"
python tools/prepare_wheel_assets.py
```

This step will:

- Derive the default Det / Cls / Rec models from `rapidocr/config.yaml`
- Read the download URLs and SHA256 values from `rapidocr/default_models.yaml`
- Download or verify the model files
- Generate `MANIFEST.in` to make sure these models are included in the wheel

If you only want to check whether the models are ready:

```bash linenums="1"
python tools/prepare_wheel_assets.py --check
```

### 4. Specify the version and build the wheel

```bash linenums="1"
SETUPTOOLS_SCM_PRETEND_VERSION_FOR_RAPIDOCR=3.1.0 python -m build --wheel
```

The build output is written to:

```text
dist/
```

For example:

```text
dist/rapidocr-3.1.0-py3-none-any.whl
```

### 5. Verify the wheel version

```bash linenums="1"
unzip -p dist/rapidocr-3.1.0-py3-none-any.whl "*/METADATA" | grep "^Version:"
```

Expected output:

```text
Version: 3.1.0
```

### 6. Verify that the models are included in the wheel

```bash linenums="1"
python -m zipfile -l dist/rapidocr-3.1.0-py3-none-any.whl | grep "rapidocr/models"
```

You should see the default model files.

If you do not specify a version manually, you can also build from a Git tag:

```bash linenums="1"
git tag v3.1.0
python tools/prepare_wheel_assets.py
python -m build --wheel
```

When the current commit is exactly on the `v3.1.0` tag, `setuptools-scm` derives version `3.1.0`. If the current commit is not on a tag, a development version is generated.
