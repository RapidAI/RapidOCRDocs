---
weight: 400
date: "2022-09-15"
draft: false
author: "SWHL"
title: "Nuitka打包"
icon: "code"
toc: true
description: ""
---

--by [DeadWood8](https://github.com/DeadWood8)

#### 打包环境
- `OS`: Windows11
- `Python`: 3.8.10
- `rapidocr_onnxruntime`: 1.2.0
- `nuitka`: 1.5.3
- `onnxruntime`: 1.14.0

#### 打包步骤
1. 安装`Nuitka`
    ```bash {linenos=table}
    pip install nuitka
    ```
   注：第一次安装会自动下载mingw和ccache，也可以手动配置，自行某度。
2. 修改`rapidocr-onnxruntime`源码（修改后可以将所有依赖打包进文件）
    {{< alert context="info" text="`rapidocr_onnxruntime>=1.2.8`以后不用再手动修改下面代码，已经做了修改。可以跳过该步。" />}}
   - 进入`rapidocr-onnxruntime`安装位置，一般在`Lib\site-packages\rapidocr_onnxruntime`或者你设置的虚拟环境下。
   - 用编辑器打开`rapid_ocr_api.py`，对**39-52行**进行修改，如下图：

    ![image](https://user-images.githubusercontent.com/28639377/227765049-357c6670-56cb-44a4-a32c-f2dde479838e.png)
3. `nuitka`打包
    ```bash {linenos=table}
    cd rapidocr_web
    nuitka --mingw64 --standalone --show-memory --show-progress --nofollow-import-to=tkinter --output-dir=out ocrweb.py
    ```
   - 如下图所示：

    ![image](https://user-images.githubusercontent.com/28639377/227765149-4ba15340-6199-49df-be85-6ef3263f5d2c.png)
4. 拷贝静态文件
   - 打包后的文件位于当前位置的`out\ocrweb.dist`目录下，需要将`web`项目和`rapidocr-onnxruntime`相关文件拷贝到此目录。

    ![image](https://user-images.githubusercontent.com/28639377/227765238-f7015ebc-5d71-45bc-9482-9b38c9cc8835.png)
   - 拷贝`rapidocr_web`目录`static`和`templates`两个文件夹全部拷贝到`out\ocrweb.dist`下
   - 在`out\ocrweb.dist`创建`rapidocr_onnxruntime`文件夹，将`Lib\site-packages\rapidocr_onnxruntime`目录下的`config.yaml`和`models`文件夹拷贝到`out\ocrweb.dist\rapidocr_onnxruntime`文件夹内
5. 运行程序
   - 进入`out\ocrweb.dist`，直接双击`ocrweb.exe`运行。

    ![image](https://user-images.githubusercontent.com/28639377/227765308-c37eba5f-78e9-479e-a289-cbc3e3463618.png)
6. 打包好的exe下载：[百度网盘](https://pan.baidu.com/s/1nj_1rjuVu76drKBZDY9Bww?pwd=xnu7) | [Google Drive](https://drive.google.com/drive/folders/1okQj22XxLUptyhjKQcRU25eI8Ya693gf?usp=share_link) | [Gitee](https://gitee.com/RapidAI/RapidOCR/releases/download/v1.2.0/ocrweb.dist.rar)

#### 补充
- 如果不想运行程序后有黑框，可以在打包命令中加入以下参数
 `--windows-disable-console`
- 完整命令为：
    ```bash {linenos=table}
    nuitka --mingw64 --standalone --show-memory --show-progress --nofollow-import-to=tkinter --windows-disable-console --output-dir=out ocrweb.py
    ```