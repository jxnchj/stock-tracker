#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块轮动窥探器
用雷达图展示各板块的轮动节奏，时间轴显示热点切换。
看一眼就知道现在是什么风格的市场，以及下一个可能轮到谁。
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

SECTORS = [
    ("AI算力",     C_CYAN),
    ("半导体",     C_GREEN),
    ("新能源汽车", C_YELLOW),
    ("军工",       C_MAGENTA),
    ("医药",       C_RED),
    ("大金融",     C_WHITE),
    ("消费",       C_YELLOW),
    ("地产",       C_RED),
]

R = 18  # 雷达图半径

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  板块轮动窥探器  |  雷达图展示资金分布  |  每秒更新{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")

def intensity_to_radius(intensity, max_intensity=100):
    """强度值转雷达图半径"""
    return int(intensity / 100 * R)

def draw_radar(intensities, names, colors):
    """绘制雷达图"""
    n = len(names)
    angles = [2 * math.pi * i / n - math.pi / 2 for i in range(n)]

    # 计算雷达图边界点
    def get_point(i, r):
        angle = angles[i]
        x = int(r * math.cos(angle)) + R + 4
        y = int(r * math.sin(angle)) + R + 2
        return x, y

    # 初始化画布
    W = (R + 4) * 2 + 10
    H = (R + 3) * 2 + 4
    canvas = [[" " for _ in range(W)] for _ in range(H)]
    cx, cy = R + 4, R + 2

    # 绘制同心圆
    for radius in [R//3, 2*R//3, R]:
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(cx + radius * math.cos(rad))
            y = int(cy + radius * math.sin(rad))
            if 0 <= x < W and 0 <= y < H:
                canvas[y][x] = C_DIM + "·" + C_RESET

    # 绘制轴线
    for i in range(n):
        x, y = get_point(i, R)
        ax, ay = get_point(i, 0)
        for r in range(R + 1):
            px, py = get_point(i, r)
            if 0 <= px < W and 0 <= py < H:
                canvas[py][px] = C_DIM + "─" + C_RESET

    # 绘制数据区域（多边形）
    # 先找各点
    points = []
    for i in range(n):
        intensity = intensities[i]
        r = intensity_to_radius(intensity)
        x, y = get_point(i, r)
        points.append((x, y))

    # 填充多边形（用字符模拟）
    min_x = max(0, min(p[0] for p in points) - 1)
    max_x = min(W - 1, max(p[0] for p in points) + 1)
    min_y = max(0, min(p[1] for p in points) - 1)
    max_y = min(H - 1, max(p[1] for p in points) + 1)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # 简单的多边形填充：射线法
            inside = False
            crossings = 0
            for i in range(n):
                j = (i + 1) % n
                p1 = points[i]
                p2 = points[j]
                # 检查水平射线是否与边相交
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    if p2[1] != p1[1]:
                        x_cross = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                        if x_cross < x:
                            inside = not inside
            if inside and 0 <= x < W and 0 <= y < H:
                canvas[y][x] = C_DIM + "▒" + C_RESET

    # 绘制数据点
    for i, (x, y) in enumerate(points):
        if 0 <= y < H and 0 <= x < W:
            canvas[y][x] = colors[i] + C_BOLD + "●" + C_RESET

    # 绘制标签
    for i, (name, color) in enumerate(zip(names, colors)):
        intensity = intensities[i]
        r_label = R + 3
        x, y = get_point(i, r_label)
        # 调整标签位置
        if abs(math.sin(angles[i])) < 0.3:
            ha = "center"
        elif math.cos(angles[i]) > 0:
            ha = "left"
        else:
            ha = "right"

        label = f"{color}{name}{C_RESET} {intensity:.0f}%"
        print(f"  {label}")

    # 绘制画布（仅绘制有内容的部分）
    for row in canvas:
        line = "  " + "".join(row)
        if any(c != " " for c in line):
            print(line)

def generate_intensities():
    """生成板块强度（带轮动特征）"""
    intensities = []
    hot_zone = random.randint(0, len(SECTORS) - 1)

    for i, (name, color) in enumerate(SECTORS):
        if i == hot_zone:
            # 热门板块：高位强势
            intensity = random.uniform(75, 98)
        elif abs(i - hot_zone) <= 1:
            # 跟风板块
            intensity = random.uniform(40, 70)
        else:
            # 其他板块：低位
            intensity = random.uniform(5, 35)
        intensities.append(intensity)

    return intensities

def simulate_rotation(seconds=20):
    """模拟板块轮动"""
    current_intensities = [random.uniform(20, 60) for _ in SECTORS]
    hot_sector = None

    for sec in range(seconds):
        clear()
        header()
        print(f"\n  {C_BOLD}板块轮动 · 第{sec+1}秒 / 共{seconds}秒{C_RESET}")
        print(f"  {C_DIM}实时资金分布（强度=资金活跃度）{C_RESET}\n")

        # 更新：轮动切换
        if sec % random.randint(3, 6) == 0:
            old_hot = hot_sector
            hot_sector = random.randint(0, len(SECTORS) - 1)
            if old_hot is not None:
                # 旧的冷却
                current_intensities[old_hot] *= random.uniform(0.3, 0.6)
            # 新的加热
            current_intensities[hot_sector] = random.uniform(80, 98)
            # 带动相邻板块
            for adj in [(hot_sector - 1) % len(SECTORS), (hot_sector + 1) % len(SECTORS)]:
                if adj != old_hot:
                    current_intensities[adj] = min(100, current_intensities[adj] + random.uniform(10, 25))

        # 自然波动
        current_intensities = [max(5, min(98, i + random.uniform(-5, 5))) for i in current_intensities]

        names = [s[0] for s in SECTORS]
        colors = [s[1] for s in SECTORS]

        draw_radar(current_intensities, names, colors)

        # 市场解读
        print(f"\n  {C_BOLD}市场解读：{C_RESET}")
        hot_idx = current_intensities.index(max(current_intensities))
        cold_idx = current_intensities.index(min(current_intensities))
        print(f"  最热板块：{colors[hot_idx]}{names[hot_idx]}{C_RESET}（{max(current_intensities):.0f}%）")
        print(f"  最冷板块：{colors[cold_idx]}{names[cold_idx]}{C_RESET}（{min(current_intensities):.0f}%）")

        # 轮动预判
        warm_sectors = [i for i, v in enumerate(current_intensities) if v > 50]
        if len(warm_sectors) >= 3:
            print(f"  {C_GREEN}轮动信号：{C_RESET}多个板块资金活跃，{C_YELLOW}市场情绪较高{C_RESET}")
        elif len(warm_sectors) == 1:
            print(f"  {C_YELLOW}轮动信号：{C_RESET}资金高度集中{ names[hot_idx]} ，{C_RED}警惕热点切换{C_RESET}")
        else:
            print(f"  {C_YELLOW}轮动信号：{C_RESET}资金分散，暂无明确主线")

        print(f"\n  {C_DIM}每3秒板块强度会自动轮动切换...{C_RESET}")
        print(f"  {C_CYAN}Ctrl+C 退出{C_RESET}")

        time.sleep(1)

    # 最终报告
    clear()
    header()
    print(f"\n  {C_BOLD}【板块轮动报告】{C_RESET}\n")
    draw_radar(current_intensities, names, colors)

    print(f"\n  {C_BOLD}板块排序：{C_RESET}")
    sorted_sectors = sorted(zip(current_intensities, names, colors), reverse=True)
    for rank, (intensity, name, color) in enumerate(sorted_sectors, 1):
        bar_len = int(intensity / 100 * 20)
        bar = "▓" * bar_len + "░" * (20 - bar_len)
        print(f"  {rank}. {color}{name}{C_RESET} {bar} {intensity:.0f}%")

    print(f"\n  {C_DIM}提示：板块轮动是A股最重要的规律之一，{C_RESET}")
    print(f"  {C_DIM}抓住主线板块，在轮动到高位时撤退，是盈利的关键。{C_RESET}")

    input(f"\n  {C_CYAN}[回车退出]{C_RESET}")

def main():
    clear()
    header()
    print(f"""
  {C_WHITE}功能说明：{C_RESET}
  雷达图展示8个主要板块的资金活跃度（强度）
  强度越高 → 资金越集中 → 板块越热
  通过观察轮动节奏，判断市场主线和切换时机

  {C_BOLD}板块列表：{C_RESET}
""")
    for i, (name, color) in enumerate(SECTORS):
        print(f"  {color}{i+1}. {name}{C_RESET}")

    input(f"\n  {C_CYAN}[回车开始轮动窥探]{C_RESET}")

    duration = input(f"  持续秒数 (默认20秒，最多60秒): {C_RESET}").strip()
    duration = int(duration) if duration.isdigit() else 20
    duration = min(duration, 60)

    try:
        simulate_rotation(seconds=duration)
    except KeyboardInterrupt:
        print("\n\n  退出轮动窥探器")

if __name__ == "__main__":
    main()
