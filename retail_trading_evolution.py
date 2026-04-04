#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
散户心态进化史
输入你入市时间，系统生成你的心态进化史
从满怀希望的小白，到老练（破产）的老韭菜。
"""

import random
import os
import datetime

C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_DIM    = "\033[2m"
C_MAGENTA= "\033[95m"

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  散户心态进化史  |  你的A股心路历程{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")

STAGES = [
    {
        "name": "第1阶段：满怀希望的小白",
        "duration": "入市第1个月",
        "psychology": [
            "每天研究K线到凌晨2点",
            "觉得巴菲特也就那样",
            "已经开始计算赚的钱怎么花了",
            "相信自己能跑赢大盘",
            "开户第一天就满仓",
        ],
        "signature_quote": "我觉得这次肯定能赚！",
        "account_status": "刚入市，账户还是红的",
        "color": C_GREEN,
    },
    {
        "name": "第2阶段：被市场教育的嫩韭",
        "duration": "入市1-6个月",
        "psychology": [
            "第一次腰斩，开始怀疑人生",
            "每天看账户脸色吃饭",
            "开始关注各种内幕消息",
            "学会了躺平这个词",
            "对价值投资产生第一次怀疑",
        ],
        "signature_quote": "只是暂时回撤，长期拿着一定能回本",
        "account_status": "亏损20-40%，开始研究解套",
        "color": C_YELLOW,
    },
    {
        "name": "第3阶段：学会技术的半新韭",
        "duration": "6个月-2年",
        "psychology": [
            "开始研究MACD、KDJ、布林带",
            "学会了止损这个词（但从不执行）",
            "关注了30个财经博主",
            "经常说等我解套了就卖",
            "开始给别人推荐股票",
        ],
        "signature_quote": "我懂技术分析了，这次不一样",
        "account_status": "时而大赚（纯属运气）时而大亏",
        "color": C_YELLOW,
    },
    {
        "name": "第4阶段：追涨杀跌的老韭",
        "duration": "2-5年",
        "psychology": [
            "追涨停板是日常",
            "卖了就涨，买入就跌",
            "学会了融资杠杆",
            "对T+0制度恨之入骨",
            "账户有绿K的日子比红K还激动",
        ],
        "signature_quote": "我不信邪，这次肯定能连板！",
        "account_status": "经过不懈努力，账户成功腰斩",
        "color": C_RED,
    },
    {
        "name": "第5阶段：进阶为老油条",
        "duration": "5-10年",
        "psychology": [
            "对市场有了一套自己的玄学理论",
            "开始研究基本面（但还是看图为主）",
            "仓位控制有了概念",
            "学会了等待（虽然经常等来等去）",
            "跟别人聊股票时会说市场永远是对的",
        ],
        "signature_quote": "我不追求暴富了，稳定复利就好",
        "account_status": "回本仍是主要目标",
        "color": C_YELLOW,
    },
    {
        "name": "第6阶段：大师境界（自封的）",
        "duration": "10年以上",
        "psychology": [
            "对中国A股有了深刻的哲学认识",
            "可以云淡风轻地谈论亏损",
            "经常转发各种经济评论",
            "会说悲观者往往正确，乐观者往往赚钱",
            "账户密码都忘了（或者不敢看）",
        ],
        "signature_quote": "活着就是最大的胜利",
        "account_status": "不知道是赚是赔（不敢算）",
        "color": C_CYAN,
    },
    {
        "name": "第7阶段：彻底顿悟的佛系玩家",
        "duration": "15年+",
        "psychology": [
            "卸载了所有证券APP",
            "账户已经不想看了",
            "跟别人聊起股票就说年轻时候也炒过",
            "开始研究养生和钓鱼",
            "偶尔听到牛市来了会心动一下",
        ],
        "signature_quote": "钱是赚不完的，但能亏完",
        "account_status": "要么解套了，要么已经清仓离场",
        "color": C_MAGENTA,
    },
]

def generate_evolution_history(start_year):
    now = datetime.datetime.now()
    years_active = now.year - start_year
    if years_active <= 0:
        active_stages = [STAGES[0]]
    elif years_active < 0.5:
        active_stages = STAGES[:2]
    elif years_active < 2:
        active_stages = STAGES[:3]
    elif years_active < 5:
        active_stages = STAGES[:4]
    elif years_active < 10:
        active_stages = STAGES[:5]
    elif years_active < 15:
        active_stages = STAGES[:6]
    else:
        active_stages = STAGES
    return active_stages

def draw_ascii_person(stage_idx, color):
    people = [
        f"  {C_GREEN}    ∧＿∧\n   (｡･ω･｡)\n   /　  づ{C_RESET}",
        f"  {C_YELLOW}    ∧＿∧\n   (；ω；)\n   /　  づ{C_RESET}",
        f"  {C_YELLOW}    ∧＿∧\n   (？_？)\n   /　  づ{C_RESET}",
        f"  {C_RED}    ∧＿∧\n   (╯°□°)╯\n   /　  づ{C_RESET}",
        f"  {C_YELLOW}    ∧＿∧\n   (￣_￣)\n   /　  づ{C_RESET}",
        f"  {C_CYAN}    ∧＿∧\n   (终南山)\n   /　  づ{C_RESET}",
        f"  {C_MAGENTA}    ∧＿∧\n   (´-ω-`)\n   /　  づ{C_RESET}",
    ]
    return people[min(stage_idx, len(people)-1)]

def main():
    clear()
    header()
    print(f"""
  {C_WHITE}功能说明：{C_RESET}
  输入你入市的时间，系统生成你的心态进化史
  看看你在A股的哪个阶段，以及未来会走向何方
""")

    try:
        year_str = input(f"  {C_CYAN}你哪一年入市的？（如2015）: {C_RESET}").strip()
        start_year = int(year_str) if year_str.isdigit() else 2021
    except:
        start_year = 2021

    now = datetime.datetime.now()
    years_active = now.year - start_year

    clear()
    header()

    print(f"\n  {C_BOLD}【{now.year}年 股民心态评估报告】{C_RESET}")
    print(f"  入市时间：{start_year}年（距今{years_active}年）")
    print(f"  初始资金：{random.choice(['5万','10万','20万','50万'])}元")
    print(f"  当前状态：{random.choice(['还在市场中','已经躺平','偶尔看看','已经佛系'])}\n")

    stages = generate_evolution_history(start_year)

    for i, stage in enumerate(stages):
        color = stage['color']
        is_current = (i == len(stages) - 1)

        print(f"{C_BOLD}{'═'*60}{C_RESET}")
        if is_current:
            print(f"  {color}{C_BOLD}★ {stage['name']} ★（当前阶段）{C_RESET}")
        else:
            print(f"  {color}{stage['name']}{C_RESET}")
        print(f"  {C_DIM}{stage['duration']}{C_RESET}")
        print()
        print(draw_ascii_person(i, color))
        print(f"\n  {C_BOLD}心理特征：{C_RESET}")
        for p in random.sample(stage['psychology'], min(3, len(stage['psychology']))):
            print(f"  {color}·{C_RESET} {p}")
        print(f"\n  {C_BOLD}经典语录：{C_RESET}")
        print(f"  {C_CYAN}「{stage['signature_quote']}」{C_RESET}")
        print(f"\n  账户状态：{stage['account_status']}")

        if is_current:
            print(f"\n  {C_BOLD}{'─'*60}{C_RESET}")
            print(f"  {C_BOLD}{C_YELLOW}下一个阶段预告：{C_RESET}")
            if i < len(STAGES) - 1:
                next_stage = STAGES[i + 1]
                print(f"  再过几年，你将成为：{next_stage['color']}{next_stage['name']}{C_RESET}")
                print(f"  标志：{next_stage['signature_quote']}")
            else:
                print(f"  {C_MAGENTA}你已经到达最终形态：佛系玩家{C_RESET}")
                print(f"  {C_DIM}你已经看透了A股的本质：活着就是为了玄学{C_RESET}")

    print(f"\n{C_BOLD}{'═'*60}{C_RESET}")
    print(f"\n  {C_BOLD}【进化总结】{C_RESET}")

    losses = [
        ("还没怎么亏", C_GREEN),
        ("小亏怡情", C_GREEN),
        ("亏了一套首付", C_YELLOW),
        ("亏了一辆车", C_YELLOW),
        ("亏了一辆车还搭上油钱", C_RED),
        ("可以在深圳付个首付了", C_RED + C_BOLD),
        ("已经能影响阶层叙事", C_RED + C_BOLD),
    ]

    loss_idx = min(len(losses) - 1, years_active)
    loss_text, loss_color = losses[loss_idx]

    print(f"  A股年龄：{years_active}年 -> {loss_color}{loss_text}{C_RESET}")

    lessons = [
        "学会了敬畏市场（虽然经常忘）",
        "学会了仓位管理（虽然经常满仓）",
        "学会了止损（但执行力约等于0）",
        "学会了研究基本面（但还是看图为主）",
        "学会了耐心等待（但经常等来等去）",
        "学会了接受亏损（因为亏太多了）",
        "学会了不看账户（眼不见为净）",
        "学会了退出市场（或者被市场退出）",
    ]

    print(f"\n  {C_BOLD}血泪教训：{C_RESET}")
    for lesson in random.sample(lessons, min(3, len(lessons))):
        print(f"  {C_RED}×{C_RESET} {lesson}")

    print(f"\n  {C_BOLD}最终评价：{C_RESET}")
    if years_active < 1:
        print(f"  {C_GREEN}你还是个新手，账户还完整，好好珍惜。{C_RESET}")
    elif years_active < 3:
        print(f"  {C_YELLOW}你已经完成了初步的投资者教育，代价是部分本金。{C_RESET}")
    elif years_active < 7:
        print(f"  {C_YELLOW}你是中国A股市场的资深参与者，见过大场面。{C_RESET}")
    else:
        print(f"  {C_MAGENTA}你是A股的老战士，活着就是最大的胜利。{C_RESET}")

    print(f"\n  {C_DIM}「在A股，活得久的才是赢家。活得短的不是输了，是重在参与。」{C_RESET}")
    print(f"\n  {C_CYAN}[回车退出]{C_RESET}")
    input()

if __name__ == "__main__":
    main()
