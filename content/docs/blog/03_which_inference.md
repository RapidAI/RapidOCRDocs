---
weight: 3400
lastmod: "2022-10-04"
draft: false
author: "SWHL"
title: "选择哪个推理引擎？"
icon: "code"
toc: true
description: ""
---

{{< alert context="warning" text="openvino存在内存不释放的问题，参见[issue #11939](https://github.com/openvinotoolkit/openvino/issues/11939)" />}}

|推理引擎|推理速度更快|占用内存更少|
|:---|:---:|:---:|
|`rapidocr_onnxruntime`||✓|
|`rapidocr_openvino`|✓||

<script src="https://giscus.app/client.js"
        data-repo="RapidAI/RapidOCRDocs"
        data-repo-id="R_kgDOKS1JHQ"
        data-category="Q&A"
        data-category-id="DIC_kwDOKS1JHc4Ce5E0"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>