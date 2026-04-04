#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场情绪温度计
综合多个维度：涨跌停家数、北向资金、两融数据、期权PCR、
股债收益差、恐慌指数，实时计算市场情绪。
比同花顺的情绪温度更直观，更有深度。
"""

import random
import os
import math
import time

C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_DIM    = "\033[2m"
C_MAGENTA= "\033[95m"

DIMENSIONS = [
    ("涨跌停家数比", "涨停/跌停比例"),
    ("北向资金", "当日净流入方向和力度"),
    ("两融余额变化", "融资融券余额变动"),
    ("股债收益差", "股票vs债券的相对吸引力"),
    ("恐慌指数VIX", "期权市场对未来波动的预期"),
    ("成交量能", "量能是否配合趋势"),
]

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  市场情绪温度计  |  多维综合情绪分析  |  每秒更新{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")

def calc_overall_sentiment(dimensions):
    """计算综合情绪"""
    return sum(d['score'] * d['weight'] for d in dimensions) / sum(d['weight'] for d in dimensions)

def draw_gauge(score, width=50):
    """绘制温度计"""
    filled = int(score / 100 * width)
    empty = width - filled

    # 颜色
    if score >= 80:
        color = C_RED + C_BOLD
        label = "极度贪婪"
        emoji = "🤑"
    elif score >= 65:
        color = C_YELLOW + C_BOLD
        label = "贪婪"
        emoji = "😈"
    elif score >= 50:
        color = C_WHITE
        label = "中性"
        emoji = "😐"
    elif score >= 35:
        color = C_CYAN
        label = "恐惧"
        emoji = "😰"
    else:
        color = C_BLUE if 'C_BLUE' in dir() else "\033[94m"
        label = "极度恐惧"
        emoji = "😱"

    bar = color + "▓" * filled + C_DIM + "░" * empty + C_RESET

    print(f"\n  {C_BOLD}{emoji} 市场情绪：{bar} {score:.0f}/100{C_RESET}")
    print(f"  {C_BOLD}状态：{color}{label}{C_RESET}")

    # 刻度
    print(f"  {C_DIM}0{C_RESET}          {C_DIM}25{C_RESET}          {C_DIM}50{C_RESET}          {C_DIM}75{C_RESET}          {C_DIM}100{C_RESET}")
    print(f"  {C_RED}极度恐惧{C_RESET}  {C_CYAN}恐惧{C_RESET}  {C_WHITE}中性{C_RESET}  {C_YELLOW}贪婪{C_RESET}  {C_RED}极度贪婪{C_RESET}")

def draw_needle(score):
    """绘制指针"""
    # 指针角度范围：-90度（0）到+90度（100）
    angle = (score / 100 - 0.5) * 180  # -90到+90
    print(f"\n  {C_BOLD}仪表盘指针：{C_RESET}")
    print(f"  {C_DIM}       北(N)       {C_RESET}")
    print(f"  {C_DIM}      /  |  \\      {C_RESET}")
    print(f"  {C_DIM}   西--{C_RESET}{C_WHITE}o{C_RESET}{C_DIM}--东     (当前: {score:.0f}°){C_RESET}")
    print(f"  {C_DIM}      \\  |  /      {C_RESET}")
    print(f"  {C_DIM}       南(S)       {C_RESET}")

def draw_radar_chart(dimensions):
    """绘制雷达图"""
    n = len(dimensions)
    R = 12
    print(f"\n  {C_BOLD}多维情绪雷达图：{C_RESET}\n")

    # 简单文本雷达图
    labels = [d['name'][:4] for d in dimensions]
    scores = [d['score'] for d in dimensions]

    # 绘制条形图风格的雷达
    max_len = max(len(l) for l in labels)
    for i, (label, score) in enumerate(zip(labels, scores)):
        bar_len = int(score / 100 * 30)
        bar = C_GREEN + "▓" * bar_len + C_DIM + "░" * (30 - bar_len) + C_RESET
        score_color = C_GREEN if score > 65 else (C_YELLOW if score > 35 else C_RED)
        print(f"  {label:<{max_len}} {bar} {score_color}{score:.0f}{C_RESET}")

def draw_indicators(dimensions, total_score):
    """绘制各指标详情"""
    print(f"\n  {C_BOLD}指标详情：{C_RESET}")

    sorted_dims = sorted(dimensions, key=lambda x: x['score'], reverse=True)

    for i, d in enumerate(sorted_dims, 1):
        bar_len = int(d['score'] / 100 * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        score_color = C_GREEN if d['score'] > 65 else (C_YELLOW if d['score'] > 35 else C_RED)
        desc_color = C_GREEN if d['signal'] == '看多' else (C_RED if d['signal'] == '看空' else C_WHITE)

        print(f"  {i}. {d['name']:<10} {score_color}{bar}{C_RESET} {d['score']:.0f}  "
              f"{desc_color}{d['signal']}{C_RESET}  {C_DIM}{d['desc']}{C_RESET}")

def generate_dimensions():
    """生成各维度情绪数据"""
    dimensions = []

    # 涨跌停比
    up = random.randint(30, 150)
    down = random.randint(10, 80)
    ratio = up / max(down, 1)
    score = min(100, int(ratio * 25 + 25))
    dimensions.append({
        'name': '涨跌停比',
        'score': score,
        'weight': 1.2,
        'signal': '看多' if score > 60 else ('看空' if score < 40 else '中性'),
        'desc': f'涨停{up}家/跌停{down}家'
    })

    # 北向资金
    north = random.uniform(-100, 200)
    score = int((north + 100) / 300 * 100)
    score = max(0, min(100, score))
    dimensions.append({
        'name': '北向资金',
        'score': score,
        'weight': 1.0,
        'signal': '看多' if north > 50 else ('看空' if north < -30 else '中性'),
        'desc': f'净流入{north:+.0f}亿'
    })

    # 两融余额变化
    margin_change = random.uniform(-5, 8)
    score = int((margin_change + 5) / 13 * 100)
    score = max(0, min(100, score))
    dimensions.append({
        'name': '两融变化',
        'score': score,
        'weight': 0.9,
        'signal': '看多' if margin_change > 2 else ('看空' if margin_change < -1 else '中性'),
        'desc': f'两融余额{margin_change:+.1f}%'
    })

    # 股债收益差（FED模型）
    spread = random.uniform(-2, 4)  # 股票ERP
    score = int((spread + 2) / 6 * 100)
    score = max(0, min(100, score))
    dimensions.append({
        'name': '股债收益差',
        'score': score,
        'weight': 1.1,
        'signal': '看多' if spread > 2 else ('看空' if spread < 0 else '中性'),
        'desc': f'股票ERP {spread:.1f}%'
    })

    # 恐慌指数
    vix = random.uniform(10, 40)
    score = int(max(0, min(100, (40 - vix) / 30 * 100)))  # VIX越高越恐惧
    dimensions.append({
        'name': '恐慌指数',
        'score': score,
        'weight': 1.0,
        'signal': '看多' if vix < 20 else ('看空' if vix > 28 else '中性'),
        'desc': f'VIX = {vix:.1f}'
    })

    # 量能
    volume_ratio = random.uniform(0.6, 1.6)
    score = int(volume_ratio / 1.6 * 100)
    score = max(0, min(100, score))
    dimensions.append({
        'name': '成交量能',
        'score': score,
        'weight': 0.8,
        'signal': '看多' if volume_ratio > 1.2 else ('看空' if volume_ratio < 0.8 else '中性'),
        'desc': f'量比 {volume_ratio:.2f}'
    })

    return dimensions

def generate_market_interpretation(total_score, dimensions):
    """生成市场解读"""
    bull_count = sum(1 for d in dimensions if d['signal'] == '看多')
    bear_count = sum(1 for d in dimensions if d['signal'] == '看空')

    if total_score >= 80:
        return [
            "市场情绪极度亢奋，贪婪情绪达到顶峰",
            "所有人都在买，市场即将见顶",
            "建议：开始减仓，别接最后一棒",
            C_RED + "⚠️ 极度贪婪信号：历史上极度贪婪后往往伴随大幅回调" + C_RESET,
        ]
    elif total_score >= 65:
        return [
            "市场情绪偏暖，但未到极致",
            f"{bull_count}个指标看多，{bear_count}个指标看空",
            "建议：可以参与，但注意止损",
            C_YELLOW + "市场机会与风险并存，控制仓位" + C_RESET,
        ]
    elif total_score >= 50:
        return [
            "市场情绪中性，多空僵持",
            f"看多{bull_count}个，看空{bear_count}个，势均力敌",
            "建议：轻仓等待方向明确",
            C_WHITE + "震荡市，高抛低吸为主" + C_RESET,
        ]
    elif total_score >= 35:
        return [
            "市场情绪偏冷，恐慌开始蔓延",
            f"{bull_count}个指标看多，{bear_count}个指标看空，空头占优",
            "建议：控制仓位，等待超跌机会",
            C_CYAN + "市场情绪低迷，但可能酝酿反弹" + C_RESET,
        ]
    else:
        return [
            "市场情绪极度恐慌，人气冰点",
            "历史大底往往在极度恐惧中出现",
            "建议：逆向布局优质资产，但做好仓位控制",
            C_BLUE if hasattr(C_BLUE, '__call__') else "\033[94m" + "⚠️ 极度恐惧信号：长线资金可以分批布局" + C_RESET,
        ]

def simulate_sentiment(seconds=15):
    """实时模拟情绪变化"""
    for sec in range(seconds):
        clear()
        header()
        print(f"\n  {C_BOLD}市场情绪实时监测 · 第{sec+1}秒/共{seconds}秒{C_RESET}")
        print(f"  {C_DIM}Ctrl+C 退出{C_RESET}\n")

        dimensions = generate_dimensions()
        total_score = calc_overall_sentiment(dimensions)

        draw_gauge(total_score)
        draw_radar_chart(dimensions)
        draw_indicators(dimensions, total_score)

        print(f"\n  {C_BOLD}综合判断：{C_RESET}")
        interpretation = generate_market_interpretation(total_score, dimensions)
        for line in interpretation:
            print(f"  {C_WHITE}{line}{C_RESET}")

        print(f"\n  {C_BOLD}历史类比：{C_RESET}")
        analogies = {
            (80, 100): ("2020年7月牛市高潮", C_RED),
            (65, 79): ("2023年一季度春季行情", C_YELLOW),
            (50, 64): ("2022年大部分时间", C_WHITE),
            (35, 49): ("2022年10月市场底", C_CYAN),
            (0, 34): ("2018年贸易战底部", C_BLUE if hasattr(C_BLUE, '__call__') else "\033[94m"),
        }

        for (low, high), (text, color) in analogies.items():
            if low <= total_score < high:
                print(f"  {color}类似：{text}{C_RESET}")
                break

        time.sleep(1)

    # 最终报告
    clear()
    header()
    print(f"\n  {C_BOLD}【情绪监测报告】{C_RESET}\n")

    dimensions = generate_dimensions()
    total_score = calc_overall_sentiment(dimensions)

    draw_gauge(total_score)
    draw_radar_chart(dimensions)
    draw_indicators(dimensions, total_score)

    print(f"\n  {C_BOLD}综合判断：{C_RESET}")
    interpretation = generate_market_interpretation(total_score, dimensions)
    for line in interpretation:
        print(f"  {C_WHITE}{line}{C_RESET}")

    print(f"\n  {C_DIM}注：以上指标均为模拟数据，仅供娱乐，不代表真实市场判断{C_RESET}")

    input(f"\n  {C_CYAN}[回车退出]{C_RESET}")

def main():
    clear()
    header()
    print(f"""
  {C_WHITE}功能说明：{C_RESET}
  综合6个维度的量化指标，实时计算市场情绪温度
  比单一指标更全面，比同花顺的"情绪温度"更深层

  {C_BOLD}指标维度：{C_RESET}
  · 涨跌停家数比（市场赚钱效应）
  · 北向资金（外资情绪）
  · 两融余额变化（杠杆资金动向）
  · 股债收益差（估值吸引力）
  · 恐慌指数VIX（波动率预期）
  · 成交量能（资金活跃度）

  {C_BOLD}解读规则：{C_RESET}
  80-100：极度贪婪（风险积聚）
  65-79：贪婪（可以参与）
  50-64：中性（轻仓观望）
  35-49：恐惧（控制仓位）
  0-34：极度恐惧（逆向布局）
""")

    input(f"  {C_CYAN}[回车开始实时监测]{C_RESET}")

    duration = input(f"  监测时长秒数（默认15秒，最多60秒）: {C_RESET}").strip()
    duration = int(duration) if duration.isdigit() else 15
    duration = min(duration, 60)

    try:
        simulate_sentiment(seconds=duration)
    except KeyboardInterrupt:
        print("\n\n  退出监测")

if __name__ == "__main__":
    main()
