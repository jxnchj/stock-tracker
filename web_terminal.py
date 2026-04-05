#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Terminal Service for Stock Tracker Apps
Flask + threading 后端，SSE 输出
"""

import os
import sys
import select
import termios
import tty
import pty
import fcntl
import errno
import signal
import threading
import queue as ThreadQueue

from flask import Flask, render_template, Response

app = Flask(__name__, static_folder='static', template_folder='templates')

# 程序目录
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# 支持的程序列表
APPS = {
    "1-fund-flow": {
        "name": "主力资金流向博弈图",
        "file": "fund_flow_battle.py",
        "desc": "散户/机构/北向资金三方博弈实时模拟",
    },
    "2-limit-up": {
        "name": "涨停敢死队模拟器",
        "file": "limit_up_warrior.py",
        "desc": "体验打板的快感，35%概率当日亏20%",
    },
    "3-kline-run": {
        "name": "K线跑酷游戏",
        "file": "kline_run.py",
        "desc": "你就是蜡烛图，在K线丛林里跑酷躲闪",
    },
    "4-minesweeper": {
        "name": "财报排雷大师",
        "file": "financial_minesweeper.py",
        "desc": "扫雷游戏，但扫的是财报地雷",
    },
    "5-sector-radar": {
        "name": "板块轮动窥探器",
        "file": "sector_radar.py",
        "desc": "雷达图展示资金在板块间的轮动节奏",
    },
    "6-break-even": {
        "name": "解套倒计时",
        "file": "break_even_countdown.py",
        "desc": "输入成本和现价，算你还要多少年回本",
    },
    "7-evolution": {
        "name": "散户心态进化史",
        "file": "retail_trading_evolution.py",
        "desc": "根据入市年份生成你的心态进化血泪史",
    },
    "8-guru": {
        "name": "每日股评嘴炮生成器",
        "file": "stock_guru_generator.py",
        "desc": "大师预测报告，次日自动打脸",
    },
    "9-graveyard": {
        "name": "持仓墓碑管理器",
        "file": "portfolio_graveyard.py",
        "desc": "把亏钱的持仓当墓碑展示",
    },
    "10-sentiment": {
        "name": "市场情绪温度计",
        "file": "market_sentiment_gauge.py",
        "desc": "6维度综合计算市场情绪温度",
    },
}


def run_app_streaming(app_id, out_queue):
    """通过 pty 运行程序，输出放入队列"""
    if app_id not in APPS:
        out_queue.put(("stderr", "未知程序: " + app_id + "\n"))
        out_queue.put(("done", ""))
        return

    app_info = APPS[app_id]
    app_path = os.path.join(APP_DIR, app_info["file"])

    if not os.path.exists(app_path):
        out_queue.put(("stderr", "文件不存在: " + app_path + "\n"))
        out_queue.put(("done", ""))
        return

    master_fd, slave_fd = pty.openpty()
    old_settings = termios.tcgetattr(slave_fd)
    try:
        tty.setraw(slave_fd)
        termios.tcsetattr(slave_fd, termios.TCSADRAIN, old_settings)
    except Exception:
        pass

    pid = os.fork()
    if pid == 0:
        # 子进程
        os.close(master_fd)
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        os.close(slave_fd)
        os.environ["TERM"] = "xterm-256color"
        os.environ["COLUMNS"] = "120"
        os.environ["LINES"] = "30"
        try:
            os.execvp("python3", ["python3", app_path])
        except Exception:
            os.execvp("python", ["python", app_path])
        os._exit(1)

    # 父进程
    os.close(slave_fd)
    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    try:
        while True:
            r, _, _ = select.select([master_fd], [], [], 0.5)
            if master_fd in r:
                try:
                    data = os.read(master_fd, 4096)
                    if data:
                        out_queue.put(("stdout", data.decode("utf-8", errors="replace")))
                    else:
                        break
                except OSError as e:
                    if e.errno != errno.EIO:
                        break
                    break
            result, _ = os.waitpid(pid, os.WNOHANG)
            if result != 0:
                break
    finally:
        os.close(master_fd)
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass

    out_queue.put(("done", ""))


@app.route("/")
def index():
    return render_template("index.html", apps=APPS)


@app.route("/terminal/<app_id>")
def terminal_page(app_id):
    if app_id not in APPS:
        return "未知程序", 404
    return render_template(
        "terminal.html",
        app_id=app_id,
        app_name=APPS[app_id]["name"],
        app_desc=APPS[app_id]["desc"]
    )


@app.route("/stream/<app_id>")
def stream(app_id):
    """SSE 端点"""
    if app_id not in APPS:
        return "未知程序", 404

    def generate():
        out_queue = ThreadQueue.Queue()
        t = threading.Thread(target=run_app_streaming, args=(app_id, out_queue))
        t.daemon = True
        t.start()

        while True:
            try:
                msg_type, data = out_queue.get(timeout=30)
                if msg_type == "done":
                    break
                # SSE 格式
                yield "data: " + data + "\n\n"
            except ThreadQueue.Empty:
                # 超时发送空行保持连接
                yield "data: \n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 50)
    print("Stock Tracker Web Terminal Service")
    print("Port:", port)
    print("=" * 50)

    # Railway 用 gunicorn 或直接运行
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
