#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批处理网页版入口。
放弃在 PaaS 上不稳定的 PTY 终端，改成：网页输入 -> 后端一次性执行 -> 返回真实输出。
"""

import os
import re
import sys
import subprocess
from pathlib import Path

from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static', template_folder='templates')
APP_DIR = Path(__file__).resolve().parent

ANSI_RE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
CLEAR_RE = re.compile(r'(\x1bc|\x1b\[2J|\x1b\[H|\x1b\[3J)')


def strip_ansi(text: str) -> str:
    """清理 ANSI 颜色和清屏控制符，避免网页出现乱码。"""
    text = CLEAR_RE.sub('', text or '')
    return ANSI_RE.sub('', text)


APPS = {
    "6-break-even": {
        "name": "解套倒计时",
        "file": "break_even_countdown.py",
        "desc": "输入成本、现价和股息率，直接给你回本年限和绝望指数。",
        "status": "ready",
        "badge": "已落地",
        "input_help": "按顺序输入 3 行：成本价 / 当前价 / 预估股息率。最后留一个空行结束。",
        "example_input": "10\n8\n3\n\n",
        "featured": True,
    },
    "7-evolution": {
        "name": "散户心态进化史",
        "file": "retail_trading_evolution.py",
        "desc": "输入入市年份，生成你的 A 股心态进化报告。",
        "status": "ready",
        "badge": "已落地",
        "input_help": "输入 1 行入市年份，例如 2018。最后留一个空行结束。",
        "example_input": "2018\n\n",
        "featured": True,
    },
    "8-guru": {
        "name": "每日股评嘴炮生成器",
        "file": "stock_guru_generator.py",
        "desc": "用菜单方式生成嘴炮股评、打脸回测和大师 Battle。",
        "status": "ready",
        "badge": "已落地",
        "input_help": "输入菜单操作序列。例子里先看大师 Battle，再回车继续，最后输入 0 退出。",
        "example_input": "1\n\n0\n",
        "featured": True,
    },
    "9-graveyard": {
        "name": "持仓墓碑管理器",
        "file": "portfolio_graveyard.py",
        "desc": "给亏损持仓立墓碑，生成下葬证书和墓园统计。",
        "status": "ready",
        "badge": "已落地",
        "input_help": "示例：随机选股、亏 12 万、收入墓园。依次输入：股票序号 / 亏损金额 / 是否收入墓园。",
        "example_input": "\n12\ny\n0\n",
        "featured": True,
    },
    "10-sentiment": {
        "name": "市场情绪温度计",
        "file": "market_sentiment_gauge.py",
        "desc": "原版是持续刷新型终端，不适合网页批处理，先暂停重构。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
    "1-fund-flow": {
        "name": "主力资金流向博弈图",
        "file": "fund_flow_battle.py",
        "desc": "原版偏实时终端玩法，先暂停重构。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
    "2-limit-up": {
        "name": "涨停敢死队模拟器",
        "file": "limit_up_warrior.py",
        "desc": "原版偏多轮交互，先暂停重构。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
    "3-kline-run": {
        "name": "K线跑酷游戏",
        "file": "kline_run.py",
        "desc": "原版需要连续按键，不适合 Railway 网页终端。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
    "4-minesweeper": {
        "name": "财报排雷大师",
        "file": "financial_minesweeper.py",
        "desc": "原版是逐步扫雷玩法，先暂停重构。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
    "5-sector-radar": {
        "name": "板块轮动窥探器",
        "file": "sector_radar.py",
        "desc": "原版偏终端动态展示，先暂停重构。",
        "status": "rebuild",
        "badge": "重构中",
        "input_help": "这个版本暂不开放网页运行。",
        "example_input": "",
        "featured": False,
    },
}


@app.route('/')
def index():
    featured_apps = {k: v for k, v in APPS.items() if v.get('featured')}
    rebuilding_apps = {k: v for k, v in APPS.items() if not v.get('featured')}
    return render_template('index.html', featured_apps=featured_apps, rebuilding_apps=rebuilding_apps)


@app.route('/terminal/<app_id>')
def old_terminal_redirect(app_id):
    return redirect(url_for('play_app', app_id=app_id))


@app.route('/play/<app_id>')
def play_app(app_id):
    app_info = APPS.get(app_id)
    if not app_info:
        return '未知程序', 404
    return render_template('terminal.html', app_id=app_id, app_info=app_info)


@app.route('/run/<app_id>', methods=['POST'])
def run_app_once(app_id):
    app_info = APPS.get(app_id)
    if not app_info:
        return jsonify({'ok': False, 'error': '未知程序'}), 404

    if app_info.get('status') != 'ready':
        return jsonify({'ok': False, 'error': '这个程序还在重构中，暂不开放网页运行。'}), 400

    payload = request.get_json(silent=True) or {}
    user_input = payload.get('user_input', '')
    app_path = APP_DIR / app_info['file']
    if not app_path.exists():
        return jsonify({'ok': False, 'error': f'脚本不存在：{app_info["file"]}'}), 500

    try:
        result = subprocess.run(
            [sys.executable, str(app_path)],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=45,
            cwd=str(APP_DIR),
            env={**os.environ, 'TERM': 'xterm-256color'},
        )
    except subprocess.TimeoutExpired:
        return jsonify({'ok': False, 'error': '运行超时了。这个程序更适合改造成真正网页，不适合继续假装终端。'}), 504
    except Exception as exc:
        return jsonify({'ok': False, 'error': f'运行失败：{exc}'}), 500

    merged = (result.stdout or '') + ('\n' + result.stderr if result.stderr else '')
    cleaned = strip_ansi(merged).strip() or '程序没有返回内容。'
    return jsonify({
        'ok': result.returncode == 0,
        'returncode': result.returncode,
        'output': cleaned,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
