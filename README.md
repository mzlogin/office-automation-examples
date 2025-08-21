# 办公自动化实例

办公自动化实例，mainly through Python。

**实例列表更新-ing。**

项目里的实例都是我在工作中遇到的一些小需求，最终形成的小工具。有一些是用于简化自己的工作，有一些是帮助同事从重复的机械操作中解放双手，希望能帮助到有同样需求的朋友。

## 实例列表

|序号|实例|语言|
|---|---|---|
|[001](./001.merge-multi-excel-to-one/)|将多个 Excel 文件里的数据合并到一个 Excel 文件中|Python|
|[002](./002.batch-gen-qrcode/)|将网址列表批量生成指定名称的二维码图片|Python|
|[003](./003.batch-gen-xiaoe-qrcode/)|小鹅通系列工具，批量创建课程小节、生成分享二维码、更新关联视频等|JavaScript / Python|
|[004](./004.sticky-chapter-node-title/)|自动组合匹配章节标题|Python|
|[005](./005.batch-copy-files/)|将某一个文件复制多份，并重命名|Python|
|[006](./006.batch-download-wkzj-videos/)|批量下载微课宝视频|JavaScript|
|[007](./007.count-audio-duration/)|统计音频文件总时长|Python|

## Python 实现的小工具使用方法

1. 使用 git 克隆本仓库到本地，或直接在页面找到 Download ZIP 下载本仓库到本地并解压；

2. 使用前请确保已安装 Python 3.x 和实例所需依赖库。

    Python 下载链接：[https://www.python.org/downloads/](https://www.python.org/downloads/)

    依赖库安装方法，以 001 实例为例：

    ```bash
    cd 001.merge-multi-excel-to-one
    python3 -m venv .venv
    ./.venv/bin/pip3 install -r requirements.txt
    ```

3. 运行实例脚本，以 001 实例为例：

    ```bash
    ./.venv/bin/python3 main.py
    ```
