<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RapidAI/RapidOCRWeb/releases/download/v1.0.0/rapidocr_web_logo_v2_dark.png" width="60%" height="60%" class="no-radius">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/RapidAI/RapidOCRWeb/releases/download/v1.0.0/rapidocr_web_logo_v2_white.png" width="60%" height="60%" class="no-radius">
    <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://github.com/RapidAI/RapidOCRWeb/releases/download/v1.0.0/rapidocr_web_logo_v2_white.png" class="no-radius">
  </picture>

  <br/>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
  <a href="https://pepy.tech/project/rapidocr_web"><img src="https://static.pepy.tech/personalized-badge/rapidocr_web?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads%20rapidocr_web"></a>
  <a href="https://pypi.org/project/rapidocr_web/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr_web"></a>
  <a href="https://choosealicense.com/licenses/apache-2.0/"><img src="https://img.shields.io/badge/License-Apache%202-dfd.svg"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

## Introduction

Source code: <https://github.com/RapidAI/RapidOCRWeb>

`rapidocr_web` is a Web-based OCR application built on the `rapidocr` library. It lets you quickly start an OCR service locally, supports clipboard, drag-and-drop and image file uploads for recognition, and provides one-click copying of the recognized text.

The whole project uses a front-end/back-end separation design:

- Front end: HTML + CSS + JavaScript
- Back end: Flask

The UI comes from Cursor and adapts to both mobile and desktop devices. Compared with the older version (v0.x), the current version (v1.x) is more modern.

## Installation

```bash linenums="1"
pip install rapidocr_web
```

## Usage

### Start the service

```bash linenums="1"
rapidocr_web -ip 0.0.0.0 -p 9003
```

After startup, open <http://localhost:9003/> in a browser. It uses `http` by default, not `https`.

Where:

- `-ip 0.0.0.0` allows access from other devices on the local network; change it to `127.0.0.1` when using it on the local machine only.
- `-p 9003` specifies the port. If the port is occupied, switch to another port and access the corresponding address.

!!! note

    If accessing from another device, replace `localhost` with the local-network IP of the device running the service.

<div align="center">
    <img src="https://github.com/RapidAI/RapidOCRWeb/releases/download/v0.0.0/demo.gif" width="100%" height="100%">
</div>
