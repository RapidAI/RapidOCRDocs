---
comments: true
---

<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapidocr-api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr-api"></a>
    <a href="https://pepy.tech/projects/rapidocr_api"><img src="https://static.pepy.tech/personalized-badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

!!! warning

    RapidOCR API now has its own repository, so this changelog is no longer updated. See the latest releases at [RapidOCR API releases](https://github.com/RapidAI/RapidOCRAPI/releases).

#### 2025-01-01 v0.1.5 update

Merged PR [#309](https://github.com/RapidAI/RapidOCR/pull/309).

- Added timestamps to Uvicorn logs.
- Added Vim to the Docker image for temporary editing.
- Added a timezone environment variable when running Docker so timestamps use local time.

#### 2024-12-04 v0.1.4 update

Merged PRs [#282](https://github.com/RapidAI/RapidOCR/pull/282) and [#281](https://github.com/RapidAI/RapidOCR/pull/281). Added support for selecting among multiple RapidOCR inference engines.

#### 2024-11-12 v0.1.2 update

- Merged PR [#263](https://github.com/RapidAI/RapidOCR/pull/253): fixed an incorrect floating-point type that prevented scores from being displayed.

#### 2024-10-28 v0.1.1 update

- Removed the mistakenly used `async` declaration from `def ocr()`. It may be added again in the future if needed.

#### 2024-10-28 v0.1.0 update

- Merged PR [#242](https://github.com/RapidAI/RapidOCR/pull/242).

#### 🍿2024-10-15 v0.0.9 update

- Fixed issue [#223](https://github.com/RapidAI/RapidOCR/issues/223).

#### 2024-07-11 v0.0.7 update

- Merged PR [#200](https://github.com/RapidAI/RapidOCR/pull/200).

#### 🥥2024-03-04 v0.0.6 update

- Improved image loading to match `rapidocr_onnxruntime>=1.3.13`.
- Unified API return values as dictionaries.

#### 🍜2023-05-22 API update

- Decoupled the API from OCRWeb as a separate module; see the [API source](https://github.com/RapidAI/RapidOCR/tree/main/api).
- After `rapidocr_web>0.1.6`, install the API directly with `pip install rapidocr_api` instead of `pip install rapidocr_web[api]`.
