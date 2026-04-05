FROM python:3.11-slim

LABEL maintainer="StockTracker"
LABEL description="Stock Tracker Web Terminal"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales curl \
    && localedef -i zh_CN -f UTF-8 zh_CN.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
ENV TERM=xterm-256color

WORKDIR /app

# 先建目录避免空目录问题
RUN mkdir -p static templates

# 复制应用文件
COPY web_terminal.py .
COPY templates/ ./templates/
COPY *.py .

# 安装Python依赖
RUN pip install --no-cache-dir flask flask-sock flask-cors gevent

# Railway 注入 PORT 环境变量
EXPOSE $PORT

# 启动命令 - 用 gevent WSGI 服务器运行
CMD python3 -c "from gevent.pywsgi import WSGIServer; import os; from web_terminal import app; WSGIServer(('0.0.0.0', int(os.environ.get('PORT',5000))), app).serve_forever()"
