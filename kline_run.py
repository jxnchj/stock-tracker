#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K线跑酷游戏
K线就是赛道，你控制一个蜡烛图在K线上跑。
跳着躲闪下跌的K线形态，抓住上涨的K线。
同花顺上没有的体验——你就是K线本身。
"""

import random
import os
import sys
import time
import math

C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_DIM    = "\033[2m"

SCREEN_W = 80
SCREEN_H = 20
PLAYER_X = 10  # 固定X位置

KLINE_CHARS = {
    'up':   ('│', '━'),   # 阳线：实体上下影线
    'down': ('│', '━'),   # 阴线：实体上下影线
}

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*SCREEN_W}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  K线跑酷  |  蜡烛躲躲躲  |  WASD/方向键操作  |  Q退出{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*SCREEN_W}{C_RESET}")

def draw_kline(canvas, x, open_p, close_p, high, low, max_h=SCREEN_H-2):
    """在canvas指定列绘制一根K线"""
    # max_h是最高可见位置，min_h是最低可见位置
    open_y  = int((open_p  / 100) * (max_h - 1)) + 1
    close_y = int((close_p / 100) * (max_h - 1)) + 1
    high_y  = int((high     / 100) * (max_h - 1)) + 1
    low_y   = int((low      / 100) * (max_h - 1)) + 1

    open_y  = max(1, min(max_h - 1, open_y))
    close_y = max(1, min(max_h - 1, close_y))
    high_y  = max(1, min(max_h - 1, high_y))
    low_y   = max(1, min(max_h - 1, low_y))

    is_up = close_p >= open_p
    body_char = C_GREEN + '█' + C_RESET if is_up else C_RED + '█' + C_RESET

    # 画上下影线
    for y in range(min(high_y, low_y), max(high_y, low_y) + 1):
        if 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
            if y == high_y or y == low_y:
                canvas[y][x] = C_YELLOW + '│' + C_RESET
            else:
                canvas[y][x] = C_YELLOW + '│' + C_RESET

    # 画实体
    for y in range(min(open_y, close_y), max(open_y, close_y) + 1):
        if 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
            canvas[y][x] = body_char

    return is_up

def generate_klines(count=50):
    """生成count根K线数据"""
    klines = []
    price = 50.0
    for i in range(count):
        # 模拟价格走势：趋势+震荡
        trend = random.uniform(-3, 3)
        noise = random.uniform(-1.5, 1.5)
        close = price + trend + noise

        open_p = price
        high = max(open_p, close) + random.uniform(0, 2)
        low  = min(open_p, close) - random.uniform(0, 2)

        open_p = max(1, min(99, open_p))
        close_p = max(1, min(99, close_p))
        high_p = max(open_p, close_p) + random.uniform(0, 3)
        low_p = min(open_p, close_p) - random.uniform(0, 3)

        klines.append({
            'open': open_p, 'close': close_p,
            'high': min(99, high_p), 'low': max(1, low_p),
            'is_up': close_p >= open_p
        })
        price = close_p
    return klines

class Player:
    def __init__(self):
        self.y = SCREEN_H // 2
        self.lives = 3
        self.coins = 0
        self.shield_time = 0

    def move_up(self):
        self.y = max(1, self.y - 1)

    def move_down(self):
        self.y = min(SCREEN_H - 2, self.y + 1)

    def draw(self, canvas):
        if self.shield_time > 0:
            char = C_YELLOW + C_BOLD + "@" + C_RESET
            self.shield_time -= 1
        else:
            char = C_CYAN + C_BOLD + "@" + C_RESET
        if 0 <= self.y < len(canvas) and 0 <= PLAYER_X < len(canvas[0]):
            canvas[self.y][PLAYER_X] = char

def draw_game(canvas, score, lives, coins, speed, msg=None):
    clear()
    header()

    # 左上角信息
    score_str = f"分数: {score}  命: {lives}❤  金币: {coins}🪙  速度: {speed:.1f}x"
    print(f"  {C_BOLD}{C_WHITE}{score_str}{C_RESET}")
    print(f"  {C_DIM}{'─'*SCREEN_W}{C_RESET}")

    for row in canvas:
        print("  " + "".join(row))

    print(f"  {C_DIM}{'─'*SCREEN_W}{C_RESET}")

    # 价格区间图例
    print(f"  {C_DIM}价格区间: 顶部=高价 底部=低价{C_RESET}")
    print(f"  {C_YELLOW}│{C_RESET}=K线影线  {C_GREEN}█{C_RESET}=阳线(涨)  {C_RED}█{C_RESET}=阴线(跌)  "
          f"{C_CYAN}@{C_RESET}=你(蜡烛人)")

    if msg:
        print(f"\n  {C_BOLD}{msg}{C_RESET}")

def run_game():
    score = 0
    lives = 3
    coins = 0
    speed = 1.0
    tick = 0

    player = Player()
    klines = generate_klines(200)  # 预生成足够多K线
    kline_index = 0

    canvas = [[" " for _ in range(SCREEN_W - 4)] for _ in range(SCREEN_H)]

    running = True
    msg = None
    msg_timer = 0

    try:
        import tty, termios, sys
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        has_tty = True
    except:
        has_tty = False
        old_settings = None

    try:
        while running and lives > 0:
            tick += 1
            speed = 1.0 + tick / 100  # 逐渐加速

            # 每隔几帧移动K线
            move_every = max(1, int(3 / speed))

            if tick % move_every == 0 and kline_index < len(klines):
                # 整体左移
                for row in canvas:
                    row.pop(0)
                    row.append(" ")

                # 绘制新K线
                kl = klines[kline_index]
                x = len(canvas[0]) - 1
                draw_kline(canvas, x, kl['open'], kl['close'], kl['high'], kl['low'])

                kline_index += 1

                # 检测碰撞
                player_y = player.y
                player_col = [PLAYER_X]

                if player_col[0] < len(canvas[0]):
                    cell = canvas[player_y][PLAYER_X]
                    # 检测K线实体（绿色或红色█）
                    if C_GREEN + '█' in cell or C_RED + '█' in cell:
                        if player.shield_time == 0:
                            lives -= 1
                            player.shield_time = 30
                            msg = C_RED + f"💥 撞到K线了！命-1，剩余{lives}条命" + C_RESET
                            msg_timer = 60
                            if lives <= 0:
                                running = False
                    # 检测上影线顶部（高价区）
                    elif C_YELLOW + '│' in cell:
                        # 检查是否在高价区（y较小=高价）
                        if player_y < SCREEN_H // 3:
                            coins += 1
                            score += 5
                            msg = C_YELLOW + f"🪙 抓住高价能量+5分！" + C_RESET
                            msg_timer = 30

            # 更新消息
            if msg_timer > 0:
                msg_timer -= 1
                if msg_timer == 0:
                    msg = None

            # 计分
            if tick % 10 == 0:
                score += 1

            # 玩家碰撞检测：高价区奖励
            player.draw(canvas)

            draw_game(canvas, score, lives, coins, speed, msg)

            # 键盘输入
            if has_tty:
                import select
                if select.select([sys.stdin], [], [], 0)[0]:
                    ch = sys.stdin.read(1)
                    if ch in ('q', 'Q'):
                        running = False
                    elif ch == '\x1b':  # 方向键
                        more = sys.stdin.read(2)
                        if more == '[A': player.move_up()
                        elif more == '[B': player.move_down()
                    elif ch in ('w', 'W'): player.move_up()
                    elif ch in ('s', 'S'): player.move_down()

            time.sleep(0.05)

    finally:
        if old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    # 游戏结束
    clear()
    header()
    print(f"\n  {C_BOLD}【游戏结束】{C_RESET}\n")
    print(f"  最终分数：{C_CYAN}{score}{C_RESET}")
    print(f"  收集金币：{C_YELLOW}{coins}{C_RESET}")
    print(f"  存活时间：{tick * 0.05:.1f}秒")
    print(f"\n  {C_DIM}你是A股市场里一根顽强奔跑的蜡烛，")
    print(f"  在涨跌的K线丛林里永不停歇。{C_RESET}\n")

    if score > 200:
        print(f"  {C_GREEN}评价：股神级跑酷选手！{C_RESET}")
    elif score > 100:
        print(f"  {C_YELLOW}评价：不错的跑酷水平！{C_RESET}")
    else:
        print(f"  {C_RED}评价：需要多跑两圈磨练一下{C_RESET}")

    return score

def main():
    clear()
    header()
    print(f"""
  {C_BOLD}{C_WHITE}┌─── 游戏说明 ────────────────────────────────────┐{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_WHITE}│  K线从右向左滚动，你要操控蜡烛人@躲闪K线实体           │{C_RESET}
  {C_WHITE}│  W/↑ = 上移  |  S/↓ = 下移                             │{C_RESET}
  {C_WHITE}│  Q = 退出                                             │{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_WHITE}│  躲避红色/绿色K线实体（撞到-1命）                     │{C_RESET}
  {C_WHITE}│  进入高价区顶部收集黄色能量（+金币+分）                │{C_RESET}
  {C_WHITE}│  速度会随时间越来越快                                 │{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_BOLD}{C_WHITE}└───────────────────────────────────────────────────────┘{C_RESET}
""")
    input(f"  {C_CYAN}[回车开始跑酷]{C_RESET}")
    try:
        run_game()
    except Exception as e:
        print(f"游戏出错: {e}")
    print(f"\n  {C_CYAN}[回车退出]{C_RESET}")
    input()

if __name__ == "__main__":
    main()
