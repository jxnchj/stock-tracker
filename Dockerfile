FROM python:3.11-slim

LABEL maintainer="StockTracker"

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

COPY web_terminal.py .
COPY templates/ ./templates/
COPY *.py .

RUN pip install --no-cache-dir flask flask-cors gunicorn

EXPOSE 8000

# Railway 注入 PORT 环境变量，用 shell 展开
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 120 web_terminal:app"]
