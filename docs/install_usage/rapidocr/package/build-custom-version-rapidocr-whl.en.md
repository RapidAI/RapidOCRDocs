---
title: Build a Custom RapidOCR Wheel Version
description: Build a RapidOCR wheel with an explicit version and bundled default models.
date:
  created: 2026-06-12
authors:
  - SWHL
comments: true
hide:
  - toc
---

RapidOCR uses `pyproject.toml` and `setuptools-scm` to build wheels. The build environment requires Python `>=3.9`; the resulting wheel supports Python `>=3.8`.

### 1. Enter the Python package directory

```bash
git clone https://github.com/RapidAI/RapidOCR.git
cd RapidOCR/python
```

### 2. Install build dependencies

```bash
python -m pip install --upgrade pip
python -m pip install build setuptools wheel setuptools-scm PyYAML
```

Install the complete requirements if you also need to run tests:

```bash
python -m pip install -r requirements.txt
```

### 3. Prepare bundled model assets

```bash
python tools/prepare_wheel_assets.py
```

This command resolves the default Det, Cls and Rec models, verifies their SHA256 checksums and generates `MANIFEST.in`. To verify already prepared assets without downloading them:

```bash
python tools/prepare_wheel_assets.py --check
```

### 4. Set the version and build

```bash
SETUPTOOLS_SCM_PRETEND_VERSION_FOR_RAPIDOCR=3.1.0 python -m build --wheel
```

The wheel is written to `dist/`, for example:

```text
dist/rapidocr-3.1.0-py3-none-any.whl
```

### 5. Verify the wheel

Check its version:

```bash
unzip -p dist/rapidocr-3.1.0-py3-none-any.whl "*/METADATA" | grep "^Version:"
```

Check that the default models are included:

```bash
python -m zipfile -l dist/rapidocr-3.1.0-py3-none-any.whl | grep "rapidocr/models"
```

Alternatively, build from a Git tag. When the current commit is exactly at `v3.1.0`, `setuptools-scm` derives version `3.1.0`; otherwise it generates a development version.
