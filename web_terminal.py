#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Terminal Service for Stock Tracker Apps
Flask + websockets 后端，在浏览器里运行终端程序
"""

from flask import Flask, render_template, request, Response
from flask_sock import Sock
import subprocess
import asyncio
import uuid
import os
import sys
import select
import termios
import tty
import pty
import struct
import fcntl
import errno
import signal

app = Flask(__name__, static_folder='static', template_folder='templates')
sock = Sock(app)

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


def run_app(app_id, write_fn):
    """通过pty运行程序，实时回传输出到websocket"""
    if app_id not in APPS:
        write_fn(f"未知程序: {app_id}\n".encode())
        return

    app_info = APPS[app_id]
    app_path = os.path.join(APP_DIR, app_info["file"])

    if not os.path.exists(app_path):
        write_fn(f"文件不存在: {app_path}\n".encode())
        return

    # 创建伪终端
    master_fd, slave_fd = pty.openpty()
    old_settings = termios.tcgetattr(slave_fd)

    # 设置终端
    try:
        tty.setraw(slave_fd)
        termios.tcsetattr(slave_fd, termios.TCSADRAIN, old_settings)
    except:
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
        except:
            os.execvp("python", ["python", app_path])
        os._exit(1)
    else:
        # 父进程
        os.close(slave_fd)

        # 设置stdout为非阻塞
        flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        try:
            while True:
                # 等待数据
                r, _, _ = select.select([master_fd], [], [], 0.5)

                if master_fd in r:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            write_fn(data)
                        else:
                            break
                    except OSError as e:
                        if e.errno != errno.EIO:
                            break
                        # EIO means EOF on some systems
                        break

                # 检查子进程是否结束
                result, _ = os.waitpid(pid, os.WNOHANG)
                if result != 0:
                    break

        finally:
            os.close(master_fd)
            # 确保子进程被终止
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass


@app.route("/")
def index():
    """首页：程序列表"""
    return render_template("index.html", apps=APPS)


@app.route("/terminal/<app_id>")
def terminal_page(app_id):
    """终端页面"""
    if app_id not in APPS:
        return "未知程序", 404
    try:
        return render_template("terminal.html", app_id=app_id, app_name=APPS[app_id]["name"], app_desc=APPS[app_id]["desc"])
    except Exception as e:
        import traceback
        import sys
        sys.stderr.write(f"render_template error: {e}\n")
        sys.stderr.write(traceback.format_exc())
        return f"Template error: {e}", 500


@sock.route("/ws/<app_id>")
def websocket_terminal(ws, app_id):
    """WebSocket终端"""
    import traceback

    def write(data):
        try:
            ws.send(data.decode("utf-8", errors="replace"))
        except:
            pass

    try:
        run_app(app_id, write)
    except Exception as e:
        err_msg = f"\n\x1b[31m[ERROR] {type(e).__name__}: {e}\x1b[0m\n"
        try:
            ws.send(err_msg)
        except:
            pass
        # 打印到 stderr 让 Railway 日志能看到
        import sys
        sys.stderr.write(f"run_app error: {type(e).__name__}: {e}\n")
        sys.stderr.write(traceback.format_exc())


if __name__ == "__main__":
    # 允许跨域，方便开发
    from flask_cors import CORS
    CORS(app)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=5000, help="监听端口")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    args = parser.parse_args()

    print(f"")
    print(f"  ╔══════════════════════════════════════════╗")
    print(f"  ║   Stock Tracker Web Terminal Service      ║")
    print(f"  ║   浏览器访问: http://{args.host}:{args.port}   ║")
    print(f"  ╚══════════════════════════════════════════╝")
    print(f"")
    print(f"  支持的程序：")
    for k, v in APPS.items():
        print(f"  {k}: {v['name']}")
    print(f"")

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        threaded=True,
        extra_files=[],  # 不监听额外文件变化
    )
