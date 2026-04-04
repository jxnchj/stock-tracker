#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涨停敢死队模拟器
你是一个专门打板的散户，每天在涨停板上追板。
体验一下什么是"涨停板上买，当日亏20%"的快感。
"""

import random
import os
import sys
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

STOCKS = [
    ("浙江世宝", "002703", "汽车零部件", 8.88),
    ("漫步者",   "002351", "AI耳机",     12.34),
    ("四川长虹", "600839", "国货家电",   5.67),
    ("光大证券", "601788", "券商",       15.20),
    ("中际旭创", "300308", "光模块",     88.88),
    ("药明康德", "603259", "CXO",        68.50),
    ("寒武纪",   "688256", "AI算力",     150.0),
    ("万丰奥威", "002085", "低空经济",   18.99),
    ("拓维信息", "002261", "华为算力",   22.50),
    ("大众交通", "600611", "网约车",     7.33),
]

BOARDS = [
    ("AI算力", ["寒武纪","海光信息","光模块","铜缆高速连"]),
    ("低空经济", ["万丰奥威","卧龙电驱","莱斯信息","川大智胜"]),
    ("半导体", ["中芯国际","华虹半导体","拓荆科技"]),
    ("新能源汽车", ["比亚迪","赛力斯","理想汽车"]),
    ("券商", ["光大证券","中国银河","中建投"]),
]

def clear():
    os.system("clear")

def print_banner():
    print(f"{C_RED}{C_BOLD}")
    print("  ██████╗██████╗  █████╗ ███████╗██╗  ██╗    ██╗      █████╗ ███████╗████████╗")
    print(" ██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║    ██║     ██╔══██╗██╔════╝╚══██╔══╝")
    print(" ██║     ██████╔╝███████║███████╗███████║    ██║     ███████║███████╗   ██║   ")
    print(" ██║     ██╔══██╗██╔══██║╚════██║██╔══██║    ██║     ██╔══██║╚════██║   ██║   ")
    print(" ╚██████╗██║  ██║██║  ██║███████║██║  ██║    ███████╗██║  ██║███████║   ██║   ")
    print("  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ")
    print(f"{C_RESET}")
    print(f"  {C_YELLOW}「在涨停板上追板，是散户最快的亏钱方式」{C_RESET}\n")

def show_board(stock, board_name, board_stocks):
    """显示涨停板"""
    clear()
    print_banner()
    print(f"  {C_BOLD}【{board_name}板块 · 涨停板】{C_RESET}\n")

    print(f"  {C_GREEN}✓{C_RESET} {C_BOLD}{stock[0]}{C_RESET}（{stock[1]}）{C_CYAN}{stock[2]}{C_RESET}  现价 ¥{stock[3]:.2f}")

    for i, s in enumerate(board_stocks[:4], 1):
        print(f"  {C_GREEN}✓{C_RESET} {s}  {C_YELLOW}涨停中...{C_RESET}")

    print(f"\n  {C_RED}封单量：{random.randint(5000, 50000):,}手{C_RESET}")
    print(f"  {C_YELLOW}换手率：{random.uniform(5, 25):.1f}%{C_RESET}")
    print(f"  {C_DIM}市场情绪：{random.choice(['极度亢奋','抢筹','疯狂'])}{C_RESET}")

def simulate_trade(account=100_0000, days=5):
    """模拟打板体验"""
    total = account
    results = []

    for day in range(1, days+1):
        board_name, board_stocks = random.choice(BOARDS)
        stock = random.choice(STOCKS)

        show_board(stock, board_name, board_stocks)

        print(f"\n  {C_BOLD}第{day}天 | 账户：{total/10000:.1f}万{C_RESET}")
        print(f"\n  你盯着{stock[0]}的涨停板...")
        time.sleep(1.5)

        # 追板决策
        print(f"\n  {C_YELLOW}封单开始撤了！{C_RESET}")
        time.sleep(0.8)
        print(f"  {C_RED}炸板了！！！{C_RESET}")
        time.sleep(0.5)

        # 当日结果
        board_type = random.random()

        if board_type < 0.35:
            # 大面 -20%
            loss_pct = random.uniform(12, 20)
            change = total * loss_pct / 100
            total -= change
            result = ("BIG_LOSS", f"当日亏损{loss_pct:.1f}%", f"-{change/10000:.1f}万", C_RED)
            desc = random.choice([
                "你涨停价买入，炸板后封死跌停，当日亏光本金20%",
                "你追进去的瞬间，封单全部撤单，你被套在高位",
                "你买入后直接炸板，次日一字跌停，你根本跑不出来",
            ])
        elif board_type < 0.60:
            # 小面 -5%
            loss_pct = random.uniform(3, 8)
            change = total * loss_pct / 100
            total -= change
            result = ("SMALL_LOSS", f"当日亏损{loss_pct:.1f}%", f"-{change/10000:.1f}万", C_YELLOW)
            desc = random.choice([
                "还好炸板后拉回去了，你只亏了手续费和一点亏损",
                "勉强封住涨停，但你买高了，次日低开割肉",
            ])
        elif board_type < 0.75:
            # 次日溢价
            gain_pct = random.uniform(3, 8)
            change = total * gain_pct / 100
            total += change
            result = ("NEXT_DAY", f"次日高开+{gain_pct:.1f}%", f"+{change/10000:.1f}万", C_GREEN)
            desc = random.choice([
                "炸板后强势回封，次日高开，你成功吃肉！",
                "你运气好，次日情绪延续，小赚一笔",
            ])
        else:
            # 成功连板
            gain_pct = random.uniform(10, 20)
            change = total * gain_pct / 100
            total += change
            result = ("CONTINUE", f"连板行情+{gain_pct:.1f}%", f"+{change/10000:.1f}万", C_GREEN + C_BOLD)
            desc = random.choice([
                "你买到了妖股！连续涨停，你封神了！",
                "龙头战法成功，你吃到了连板！",
            ])

        clear()
        print_banner()
        print(f"  {C_BOLD}第{day}天交易报告{C_RESET}\n")
        print(f"  标的：{stock[0]}（{board_name}板块）")
        print(f"  结果：{result[3]}{result[1]}{C_RESET}  账户变化：{result[3]}{result[2]}{C_RESET}\n")
        print(f"  {C_WHITE}{desc}{C_RESET}\n")
        print(f"  {C_BOLD}当前账户：{C_CYAN}{total/10000:.2f}万{C_RESET}  "
              f"{'(+' if total > account else '('}{abs((total-account)/10000):.2f}万){C_RESET}")

        results.append(result)

        if day < days:
            print(f"\n  {C_DIM}按回车继续下一天...{C_RESET}")
            input()

    # 最终报告
    clear()
    print_banner()
    print(f"  {C_BOLD}【敢死队生涯报告】{C_RESET}\n")

    profit_loss = total - account
    roi = profit_loss / account * 100

    print(f"  初始资金：{account/10000:.0f}万")
    print(f"  最终资金：{total/10000:.2f}万")
    print(f"  盈亏：{C_GREEN if profit_loss>0 else C_RED}{profit_loss/10000:+.2f}万{C_RESET}  ({roi:+.1f}%)\n")

    big_losses = sum(1 for r in results if r[0] == "BIG_LOSS")
    wins = sum(1 for r in results if r[0] in ("NEXT_DAY", "CONTINUE"))

    print(f"  交易天数：{days}天")
    print(f"  大面次数：{C_RED}{big_losses}次{C_RESET}")
    print(f"  盈利次数：{C_GREEN}{wins}次{C_RESET}")
    print(f"  胜率：{C_YELLOW}{wins/days*100:.0f}%{C_RESET}\n")

    if big_losses >= 3:
        print(f"  {C_RED}{C_BOLD}你已经成为合格的「韭菜」了！{C_RESET}")
        print(f"  {C_DIM}市场评价：连面都不知道是什么颜色的人{C_RESET}")
    elif wins >= 4:
        print(f"  {C_GREEN}{C_BOLD}恭喜！你已经成为涨停敢死队成员！{C_RESET}")
        print(f"  {C_DIM}市场评价：刀尖上跳舞的勇士{C_RESET}")
    else:
        print(f"  {C_YELLOW}你是一个普通的散户，不赚不亏（或者小亏）{C_RESET}")
        print(f"  {C_DIM}市场评价：活着就是最大的胜利{C_RESET}")

    print(f"\n  {C_MAGENTA}「打板这条路，九死一生。你不是第一个爆仓的，也不会是最后一个。」{C_RESET}\n")

    print(f"  {C_CYAN}[回车退出]{C_RESET}")
    input()

def main():
    clear()
    print_banner()
    print(f"  {C_BOLD}{C_WHITE}┌─── 游戏规则 ────────────────────────────────────┐{C_RESET}")
    print(f"  {C_WHITE}│                                                       │{C_RESET}")
    print(f"  {C_WHITE}│  你有10万块，进入涨停敢死队模拟器，                    │{C_RESET}")
    print(f"  {C_WHITE}│  每天在涨停板上追板，体验炸板的快感。                  │{C_RESET}")
    print(f"  {C_WHITE}│                                                       │{C_RESET}")
    print(f"  {C_WHITE}│  35%概率大面（当日亏12-20%）                           │{C_RESET}")
    print(f"  {C_WHITE}│  25%概率小面（当日亏3-8%）                             │{C_RESET}")
    print(f"  {C_WHITE}│  15%概率次日溢价（赚3-8%）                             │{C_RESET}")
    print(f"  {C_WHITE}│  25%概率连板（赚10-20%）                               │{C_RESET}")
    print(f"  {C_WHITE}│                                                       │{C_RESET}")
    print(f"  {C_BOLD}{C_WHITE}└───────────────────────────────────────────────────────┘{C_RESET}")
    print()
    days = input(f"  {C_CYAN}模拟几天？(默认5天，最多20天): {C_RESET}").strip()
    days = int(days) if days.isdigit() else 5
    days = min(days, 20)

    try:
        simulate_trade(account=100_0000, days=days)
    except KeyboardInterrupt:
        print("\n\n  提前退出敢死队")

if __name__ == "__main__":
    main()
