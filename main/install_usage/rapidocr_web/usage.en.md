## Overview

Source repository: <https://github.com/RapidAI/RapidOCRWeb>

`rapidocr_web` wraps RapidOCR in a local browser interface. It supports clipboard input, drag-and-drop, file selection and one-click copying of recognized text. The interface is responsive on desktop and mobile devices.

## Installation

```bash
pip install rapidocr_web
```

## Start the service

```bash
rapidocr_web -ip 0.0.0.0 -p 9003
```

Open <http://localhost:9003/> in a browser.

- `-ip 0.0.0.0` allows access from other devices on the local network. Use `127.0.0.1` for local-only access.
- `-p 9003` selects the port. Choose another port if it is already in use.

!!! note

    The default service uses `http`, not `https`. For access from another device, replace `localhost` with the server's local-network IP address.

<div align="center">
    <img src="https://github.com/RapidAI/RapidOCRWeb/releases/download/v0.0.0/demo.gif" width="100%" height="100%">
</div>
