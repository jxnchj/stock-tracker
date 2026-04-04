#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主力资金流向博弈图
用ASCII艺术可视化展示，散户/庄家/北向资金 三方在同一张图上的博弈态势。
实时模拟资金流入流出的战场，看谁在买谁在卖。
"""

import random
import os
import sys
import time
import datetime

C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_DIM    = "\033[2m"
C_MAGENTA= "\033[95m"

WIDTH = 70
HEIGHT = 22
DECIMAL_PLACES = 2  # 保留小数位数

def clear():
    os.system("clear")

def header():
    now = datetime.datetime.now()
    print(f"{C_BOLD}{C_CYAN}{'='*WIDTH}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  主力资金流向博弈图  |  {now.strftime('%Y-%m-%d %H:%M:%S')}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*WIDTH}{C_RESET}")

def generate_battle(ticks=60):
    """生成60个时间点的资金流向数据"""
    times = []
    retail = []   # 散户资金 (散户永远追涨杀跌)
    institutional = []  # 机构资金 (低买高卖)
    north = []    # 北向资金 (聪明钱)

    r, inst, n = 0.0, 0.0, 0.0
    for i in range(ticks):
        times.append(i)

        # 散户：跟涨跟跌，永远慢半拍
        if i > 0:
            prev = retail[-1] if retail else 0
            if institutional[-1] > 5:  # 机构买入后散户才反应过来
                r += random.uniform(1, 4)
            elif institutional[-1] < -5:
                r -= random.uniform(2, 5)  # 恐慌抛售
            else:
                r += random.uniform(-1.5, 2)
        r = max(-20, min(20, r))
        retail.append(r)

        # 机构：反向操作，低位吸筹，高位派发
        if i < 10:
            inst += random.uniform(1, 3)  # 开盘吸筹
        elif i < 20 and inst < 10:
            inst += random.uniform(2, 4)
        elif i > 40:
            inst -= random.uniform(2, 5)  # 尾盘派发
        else:
            inst += random.uniform(-1, 2)
        inst = max(-25, min(25, inst))
        institutional.append(inst)

        # 北向资金：相对稳定，偶尔大进大出
        if random.random() < 0.05:
            n += random.uniform(-8, 8)  # 偶尔大幅波动
        else:
            n += random.uniform(-1.5, 2)
        n = max(-20, min(20, n))
        north.append(n)

    return times, retail, institutional, north

def draw_battlefield(times, retail, institutional, north, current_idx):
    """绘制资金博弈战场"""
    mid = HEIGHT // 2

    # 准备列：每个tick一列
    max_ticks = min(len(times), WIDTH - 10)

    # 计算各列数值对应的Y位置
    def val_to_y(val, baseline=mid):
        # val范围 [-25, 25]，映射到 [1, HEIGHT-2]
        y = int((val + 25) / 50 * (HEIGHT - 3) + 1.5)
        return max(1, min(HEIGHT - 2, y))

    # 初始化网格
    grid = [[" " for _ in range(max_ticks + 8)] for _ in range(HEIGHT)]

    # 中轴线
    for x in range(max_ticks + 8):
        grid[mid][x] = "─"

    # 纵轴标签
    for y in [1, mid, HEIGHT-2]:
        grid[y][0] = "│"

    # 绘制三条线（从右向左绘制，后画的覆盖先画的）
    # 散户线
    for i in range(min(current_idx+1, max_ticks)):
        tick_idx = len(times) - max_ticks + i if len(times) > max_ticks else i
        y = val_to_y(retail[tick_idx])
        arrow = "↗" if i > 0 and retail[tick_idx] > retail[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "↘" if i > 0 and retail[tick_idx] < retail[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "•"
        grid[y][i+8] = C_RED + arrow + C_RESET

    # 机构线
    for i in range(min(current_idx+1, max_ticks)):
        tick_idx = len(times) - max_ticks + i if len(times) > max_ticks else i
        y = val_to_y(institutional[tick_idx])
        arrow = "↗" if i > 0 and institutional[tick_idx] > institutional[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "↘" if i > 0 and institutional[tick_idx] < institutional[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "•"
        grid[y][i+8] = C_GREEN + arrow + C_RESET

    # 北向线
    for i in range(min(current_idx+1, max_ticks)):
        tick_idx = len(times) - max_ticks + i if len(times) > max_ticks else i
        y = val_to_y(north[tick_idx])
        arrow = "↗" if i > 0 and north[tick_idx] > north[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "↘" if i > 0 and north[tick_idx] < north[times.index(times[tick_idx-1]) if tick_idx>0 else tick_idx] else "•"
        grid[y][i+8] = C_YELLOW + arrow + C_RESET

    # 现在位置标记
    if current_idx < max_ticks:
        y_marker = mid
        grid[y_marker][current_idx + 8] = C_CYAN + C_BOLD + "◆" + C_RESET

    # 输出
    for y, row in enumerate(grid):
        # 左轴标注
        label = ""
        if y == 1: label = "+25 "
        elif y == mid: label = "  0 "
        elif y == HEIGHT-2: label = "-25 "
        elif y == HEIGHT//4: label = "+12 "
        elif y == 3*HEIGHT//4: label = "-12 "
        else: label = "    "

        print(f"  {C_DIM}{label}{C_RESET}" + "".join(row))

def draw_legend():
    print(f"\n  {C_BOLD}{'─'*WIDTH}{C_RESET}")
    print(f"  {C_BOLD}资金流向图例：{C_RESET}")
    print(f"  {C_RED}散户资金  → 追涨杀跌，永远慢半拍{C_RESET}")
    print(f"  {C_GREEN}机构资金  → 低吸高抛，反向操作{C_RESET}")
    print(f"  {C_YELLOW}北向资金  → 相对稳定，偶尔大幅波动{C_RESET}")
    print(f"  {C_CYAN}◆ 现在位置{C_RESET}")

def draw_stats(times, retail, institutional, north, current_idx):
    """底部实时统计"""
    idx = min(current_idx, len(times)-1)
    r = retail[idx]
    inst = institutional[idx]
    n = north[idx]

    total_net = r + inst + n
    battle_status = "多空僵持" if abs(total_net) < 5 else ("多头占优" if total_net > 0 else "空头肆虐")

    print(f"  {C_BOLD}{'─'*WIDTH}{C_RESET}")
    print(f"  散户: {C_RED}{r:+.1f}{C_RESET}   机构: {C_GREEN}{inst:+.1f}{C_RESET}   北向: {C_YELLOW}{n:+.1f}{C_RESET}   "
          f"净流向: {C_CYAN}{total_net:+.1f}{C_RESET}  态势: {C_BOLD}{battle_status}{C_RESET}")

    # 买卖信号
    signals = []
    if inst > 10 and r < -5:
        signals.append((C_GREEN, "机构建仓信号↑"))
    if inst < -10 and r > 5:
        signals.append((C_RED, "机构派发信号↓"))
    if n > 10:
        signals.append((C_YELLOW, "北向抄底信号"))
    if n < -10:
        signals.append((C_YELLOW, "北向出逃信号"))
    if r > 15:
        signals.append((C_RED, "散户接盘警告⚠"))
    if inst > 0 and r < 0 and n > 0:
        signals.append((C_GREEN, "三方共振做多！"))
    if inst < 0 and r > 0 and n < 0:
        signals.append((C_RED, "三方共振做空！"))

    if signals:
        sig_text = "  ".join([f"{c}{s}{C_RESET}" for c,s in signals])
        print(f"  {C_BOLD}信号：{sig_text}{C_RESET}")

def simulate(ticks=60, speed=0.15):
    """实时模拟资金流向博弈"""
    times, retail, institutional, north = generate_battle(ticks)

    for i in range(ticks):
        clear()
        header()
        print(f"\n  {C_BOLD}【实时资金博弈 · 模拟交易时段】{C_RESET}")
        print(f"  {C_DIM}模拟第 {i+1}/{ticks} 分钟  (共60分钟，相当于一个交易日){C_RESET}\n")
        draw_battlefield(times, retail, institutional, north, i)
        draw_legend()
        draw_stats(times, retail, institutional, north, i)
        print(f"\n  {C_DIM}Ctrl+C 退出 | 每 {speed*1000:.0f}ms 更新{C_RESET}")
        time.sleep(speed)

    # 最终结算
    clear()
    header()
    print(f"\n  {C_BOLD}【收盘博弈报告】{C_RESET}\n")
    draw_battlefield(times, retail, institutional, north, ticks-1)
    draw_legend()
    draw_stats(times, retail, institutional, north, ticks-1)

    print(f"\n  {C_BOLD}{'─'*WIDTH}{C_RESET}")
    idx = ticks - 1
    r, inst, n = retail[idx], institutional[idx], north[idx]

    if inst > 0 and n > 0 and r < 0:
        verdict = f"{C_GREEN}完美配合！机构+北向做多，散户在抛——这是拉升前兆！{C_RESET}"
    elif inst < 0 and r > 10:
        verdict = f"{C_RED}机构在跑！散户在接盘！典型的派发行情！{C_RESET}"
    elif inst > 10 and r > 10:
        verdict = f"{C_YELLOW}机构建仓但散户也进了——可能是震荡行情{C_RESET}"
    else:
        verdict = f"{C_CYAN}多方博弈，暂无明确方向，建议观望{C_RESET}"

    print(f"\n  {C_BOLD}收盘判断：{verdict}{C_RESET}")
    print(f"  {C_DIM}提示：这是模拟数据，仅供娱乐，不代表真实市场{C_RESET}\n")

def main():
    clear()
    header()
    print(f"""
  {C_BOLD}{C_WHITE}┌─── 功能说明 ──────────────────────────────────┐{C_RESET}
  {C_WHITE}│                                                    │{C_RESET}
  {C_WHITE}│  用ASCII图形象征性展示A股市场三类主要资金的           │{C_RESET}
  {C_WHITE}│  资金流向博弈：散户(红)·机构(绿)·北向(黄)            │{C_RESET}
  {C_WHITE}│                                                    │{C_RESET}
  {C_WHITE}│  三条线的互动关系揭示市场博弈本质：                  │{C_RESET}
  {C_WHITE}│  ·机构低吸高抛 vs 散户追涨杀跌                       │{C_RESET}
  {C_WHITE}│  ·北向资金相对领先，可作为情绪参考                   │{C_RESET}
  {C_WHITE}│  ·观察三者共振判断行情方向                          │{C_RESET}
  {C_WHITE}│                                                    │{C_RESET}
  {C_BOLD}{C_WHITE}└────────────────────────────────────────────────────┘{C_RESET}
""")
    input(f"  {C_CYAN}[回车开始模拟实时博弈]{C_RESET}")
    try:
        simulate(ticks=60, speed=0.2)
    except KeyboardInterrupt:
        print("\n\n  退出博弈图")
    print(f"\n  {C_CYAN}[回车返回]{C_RESET}")
    input()

if __name__ == "__main__":
    main()
