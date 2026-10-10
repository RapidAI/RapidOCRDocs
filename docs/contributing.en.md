---
comments: true
title: RapidOCR Python Contribution Guide
hide:
  - navigation
---

!!! tip

    This document is synchronized with [CONTRIBUTING.md in the GitHub repository](https://github.com/RapidAI/RapidOCR/blob/main/docs/CONTRIBUTING.md). The upstream repository is authoritative; this copy may not always be current.

Thank you for your interest in RapidOCR Python. This guide explains how to prepare an environment, develop code, run tests and submit contributions in the Python directory.

## Prerequisites

- Python >= 3.6 (3.8+ recommended)
- Git
- A registered GitHub account

## 1. Clone the source

```bash
git clone https://github.com/RapidAI/RapidOCR.git
cd RapidOCR
```

If the network is restricted, use a mirror or proxy, or fork the repository first and clone your fork as described below.

## 2. Enter the Python directory and configure the environment

```bash
cd python
```

Use a virtual environment to avoid conflicts with the system Python:

```bash
# venv
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# or conda
conda create -n rapidocr python=3.10
conda activate rapidocr
```

Install dependencies. Editable installation is recommended during development:

```bash
pip install -r requirements.txt
pip install pytest
pip install -e .
```

For ONNX Runtime and other inference backends, follow the [installation guide](install_usage/rapidocr/install.md) and [inference engine guide](install_usage/rapidocr/how_to_use_infer_engine.md).

## 3. Install formatting tools and pre-commit hooks

```bash
pip install pre-commit
cd ..
pre-commit install
```

The configured formatters, such as Black and autoflake, run automatically on `git commit`. You can run them manually from the repository root:

```bash
pre-commit run --all-files
```

## 4. Run unit tests

Run these commands from the `python` directory:

```bash
pytest tests/ -v
pytest tests/test_input.py -v
pytest tests/test_det_cls_rec.py -v
pytest tests/ -v --cov=rapidocr
```

The coverage command requires `pytest-cov`. Confirm that the baseline branch passes locally before making changes.

## 5. Reproduce issues or add features

### Reproduce a bug

1. Select or create an issue in [Issues](https://github.com/RapidAI/RapidOCR/issues).
2. Reproduce it locally using the code under `python`.
3. Locate the issue in `rapidocr/` or `tests/` and modify the code until it is resolved.

### Add a feature

1. Discuss the requirement and implementation with a maintainer or in an existing issue when practical.
2. Implement the logic under `rapidocr/`, following the project style (including [Black](https://github.com/psf/black)).
3. Add unit-test coverage for the new behavior.

## 6. Write corresponding unit tests

- Put tests in `python/tests/` and use the `test_*.py` naming convention.
- Test images and other resources belong in `tests/test_files/`.
- Tests should reliably reproduce the bug or feature and should not depend on undocumented external services. Use mocks or skips when necessary.

Example:

```python
# tests/test_xxx.py
import pytest
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
tests_dir = root_dir / "tests" / "test_files"

@pytest.fixture()
def engine():
    from rapidocr import RapidOCR
    return RapidOCR()

def test_your_new_feature(engine):
    img_path = tests_dir / "ch_en_num.jpg"
    result = engine(img_path)
    assert result is not None
```

## 7. Run all unit tests again

```bash
pytest tests/ -v
```

If tests are skipped because an inference backend is unavailable, confirm that your modified or new tests actually ran and passed in the current environment.

## 8. Prepare a submission

### 8.1 Fork the RapidOCR repository

Open the [RapidOCR repository](https://github.com/RapidAI/RapidOCR) and click **Fork**.

### 8.2 Commit and push to your fork

```bash
git remote add myfork https://github.com/your-name/RapidOCR.git
git checkout -b fix/xxx
git add python/
git status
git commit -m "fix(python): short description"
git push myfork fix/xxx
```

Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

```text
<type>[optional scope]: <short description>

[optional body]
[optional footer]
```

Common types include `feat`, `fix`, `docs`, `style`, `refactor`, `test` and `chore`.

### 8.3 Open a pull request

1. Open your fork and click **Compare & pull request**, or create a pull request from the **Branches** page.
2. Set the base repository to `RapidAI/RapidOCR`, base branch to `main`, and the head to your fork and branch.
3. Include the issue number, reason for the change, main modifications and verification steps in the description.
4. Submit the pull request and push follow-up changes to the same branch after review.

## Summary

| Step | Description |
|---|---|
| 1 | Clone RapidOCR |
| 2 | Configure the Python environment and install dependencies |
| 3 | Install pre-commit |
| 4 | Run the baseline tests |
| 5 | Reproduce an issue or implement a feature |
| 6 | Add or update tests |
| 7 | Run the full test suite again |
| 8 | Fork, commit and push, then open a pull request |

## Additional notes

- **Code style:** use Black, autoflake and the configured pre-commit hooks. Run `pre-commit run --all-files` before submitting.
- **Documentation:** see the [RapidOCR documentation](https://rapidai.github.io/RapidOCRDocs/latest/) for installation and usage details.
- **Issues and discussions:** report bugs and feature requests through [GitHub Issues](https://github.com/RapidAI/RapidOCR/issues).
