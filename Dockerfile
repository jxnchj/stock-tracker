FROM python:3.11-slim

LABEL maintainer="StockTracker"

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

RUN mkdir -p static templates

# 复制文件
COPY web_terminal.py .
COPY templates/ ./templates/
COPY *.py .

# 安装依赖
RUN pip install --no-cache-dir flask flask-cors gunicorn

# Railway 注入 PORT
EXPOSE $PORT

# 使用 gunicorn 运行（稳定）
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "--threads", "4", "--timeout", "120", "web_terminal:app"]
