---
weight: 3
date: "2023-09-11"
draft: false
author: "SWHL"
title: "rapidocr_api"
icon: "update"
toc: true
description: ""
publishdate: "2023-09-08"
tags:
categories:
---

#### 🍜2023-05-22 api update:
- 将API从ocrweb中解耦出来，作为单独模块维护，详情参见[API](https://github.com/RapidAI/RapidOCR/tree/main/api)
- `rapidocr_web>0.1.6`之后，将不支持`pip install rapidocr_web[api]`方式安装，可直接`pip install rapidocr_api`安装使用。
