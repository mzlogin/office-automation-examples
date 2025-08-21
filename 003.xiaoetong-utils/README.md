# 003. 批量生成小鹅通课程分享二维码

批量生成小鹅通课程及里面的小节的分享二维码。

## 环境配置

1. 安装 Python 3，注意安装时勾选 `Add Python to PATH` 选项；

2. 安装依赖库：

    ```sh
    pip install -r requirements.txt
    ```

    Windows 下可直接双击 `安装依赖库.CMD`。

## 使用方法

1. 在浏览器打开需要生成二维码的小鹅通课程，按 F12 打开开发者工具，切到 网络（or Network）选项卡；

2. 刷新页面；

3. 执行脚本

    ```sh
    python batch-gen-course-node-qrcode.py
    ```

    Windows 下可直接双击执行 `批量生成课程二维码.CMD`。

4. 此时会弹出一个窗口，提示输入 Cookie，在浏览器开发者工具中点击一个请求，切到 Headers 选项卡，找到 Cookie，复制整个 Cookie 字符串，粘贴到弹出的窗口中，点 OK；

5. 此时提示输入课程 ID，从浏览器地址栏复制最后一段，如 `course_xxxx`，粘贴到弹出的窗口中，点 OK；

6. 等待执行完成。