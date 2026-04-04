#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓墓碑管理器
把你的亏损持仓当成墓碑展示出来，
每一块墓碑都刻着你的血泪史。
同花顺不会告诉你它们亏了多少，这里会。
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

GRAVEYARD_TEMPLATES = [
    """    ╭──────────────╮
    │              │
    │   RIP        │
    │  {name}  │
    │  亏了{loss}万   │
    │  {date} │
    │              │
    ╰──────────────╯""",
    """    ┌──────────────┐
    │  ×××× ××××  │
    │              │
    │  {name}    │
    │  亏损: {loss}万  │
    │  卒于 {date} │
    └──────────────┘""",
    """    ╔══════════════╗
    ║   HERE LIES    ║
    ║   {name}    ║
    ║              ║
    ║   -{loss}万   ║
    ║  {date}   ║
    ╚══════════════╝""",
    """    ╭─────────────────╮
    │   🪦 R.I.P 🪦     │
    │                 │
    │   {name}       │
    │   亏损: {loss}万     │
    │   死亡日期:      │
    │   {date}       │
    ╰─────────────────╯""",
]

STOCKS = [
    ("中石油", "601857", "亚洲最赚钱的公司，港股投资者20年解套"),
    ("中国平安", "601318", "从90元跌到40元，保险茅的光环已碎"),
    ("格力电器", "000651", "董明珠说不会亏，结果真的亏了"),
    ("中国中免", "601888", "曾经的小甜甜，现在也成了牛夫人"),
    ("海天味业", "603288", "酱油茅跌落神坛，只因太贵了"),
    ("隆基绿能", "601012", "光伏教父也扛不住产能过剩"),
    ("恒瑞医药", "600276", "创新药一哥，集采降价砍到脚踝"),
    ("三一重工", "600031", "机械茅，周期一来跌回原形"),
    ("海康威视", "002415", "被制裁后跌到怀疑人生"),
    ("万科A", "000002", "地产标杆，现在连净资产都守不住"),
    ("中公教育", "002607", "考公茅，退市前最后的挣扎"),
    ("阳光电源", "300274", "逆变器龙头，估值从天上到地下"),
    ("安硕信息", "300380", "曾经的第一高价股，现在已退市"),
    ("全通教育", "300359", "股王全通，现在全通了亏损"),
    ("乐视", "300104", "生态化反，窒息式退市"),
    ("暴风集团", "300431", "DT大娱乐，冯鑫进去了"),
    ("某新能源", "000000", "朋友推荐的，听说有内幕"),
    ("某半导体", "000000", "国产替代黄金赛道，买了就跌"),
    ("某医美", "000000", "颜值经济赛道，结果颜值没了"),
    ("某AI", "000000", "OpenAI沾边概念，蹭完就跌"),
]

FINAL_WORDS = [
    "「我觉得这次不一样」",
    "「只是暂时回撤，长期拿着没问题」",
    "「都跌了30%了，还能跌到哪去」",
    "「我是价值投资，不在乎短期波动」",
    "「等解套了我就卖」",
    "「朋友说这个有内幕消息」",
    "「技术形态已经企稳了」",
    "「我已经加仓摊薄成本了」",
    "「听说公司要回购了」",
    "「行业龙头，不可能倒闭的」",
    "「北向资金在买，我也跟着买」",
    "「牛市来了，这点亏损不算什么」",
    "「我已经不敢看账户了」",
    "「亏太多了，等回本再卖」",
    "「再给我一点时间」",
]

KILL_REASONS = [
    "买入后连续跌停，根本跑不出来",
    "以为抄到了钻石底，结果下面还有地下室",
    "杠杆加太大，爆仓了",
    "听信了「朋友」的内幕消息",
    "以为掌握了K线密码，结果是送钱",
    "高买低卖，完美贡献了手续费",
    "公司突然暴雷，退市了",
    "追涨停板，当日就炸板",
    "以为跌到估值底了，结果是价值陷阱",
    "买了之后遭遇黑天鹅，无法止损",
    "听信了大V荐股，结果是接盘侠",
    "买了自己完全不懂的行业",
    "满仓梭哈，单票押注，all in后归零",
]

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_RED}{'='*60}{C_RESET}")
    print(f"{C_BOLD}{C_RED}  ⚰️  持仓墓碑管理器  |  亏损到此为止（已经止了）{C_RESET}")
    print(f"{C_BOLD}{C_RED}{'='*60}{C_RESET}")

def make_tombstone(name, code, loss, kill_reason, final_quote, date_str):
    """生成墓碑"""
    template = random.choice(GRAVEYARD_TEMPLATES)
    tombstone = template.format(name=name[:10], loss=loss, date=date_str)
    return tombstone

def add_to_graveyard(tombstones, name, code, loss, kill_reason, final_quote):
    """添加到墓园"""
    date_str = datetime.date.today().strftime("%Y.%m")
    tombstone = {
        'name': f"{name}（{code}）",
        'loss': loss,
        'reason': kill_reason,
        'quote': final_quote,
        'date': date_str,
        'template': random.choice(GRAVEYARD_TEMPLATES),
    }
    tombstones.append(tombstone)

def show_graveyard(tombstones):
    """展示墓园"""
    if not tombstones:
        print(f"\n  {C_GREEN}墓园空空如也，你是个幸运儿！{C_RESET}")
        return

    # 总亏损
    total_loss = sum(t['loss'] for t in tombstones)

    clear()
    header()
    print(f"\n  {C_BOLD}🏛️  股民墓园  |  共{tombstones}位冤魂  |  总亏损{total_loss:.1f}万{C_RESET}\n")

    for i, t in enumerate(tombstones, 1):
        template = t['template']
        # 用数据替换占位符
        tomb_text = template.format(name=t['name'][:10], loss=t['loss'], date=t['date'])

        print(f"  {C_RED}{i}.{tomb_text}{C_RESET}")
        print(f"  {C_DIM}死因：{t['reason']}{C_RESET}")
        print(f"  {C_YELLOW}遗言：{t['quote']}{C_RESET}")
        print()

def burial_ceremony():
    """下葬仪式"""
    clear()
    header()
    print(f"""
  {C_BOLD}⚰️  下葬仪式 {C_RESET}

  每个冤魂都值得一个体面的安息。
  让我们为它们上一炷香。
""")

    print(f"  {C_YELLOW}    ☩ ☩ ☩    {C_RESET}")
    print(f"  {C_YELLOW}   ╱   ╲   {C_RESET}")
    print(f"  {C_YELLOW}  ╱  哀  ╲  {C_RESET}")
    print(f"  {C_YELLOW}    悼     {C_RESET}")
    print(f"  {C_YELLOW}  ───────  {C_RESET}")

    print(f"\n  {C_BOLD}请输入持仓信息（或直接回车随机生成）：{C_RESET}\n")

    stock_choice = input(f"  {C_CYAN}选择股票（1-{len(STOCKS)}）: {C_RESET}").strip()
    try:
        idx = int(stock_choice) - 1
        name, code, story = STOCKS[idx]
    except:
        name, code, story = random.choice(STOCKS)

    try:
        loss_str = input(f"  {C_CYAN}亏损金额（万）: {C_RESET}").strip()
        loss = float(loss_str) if loss_str else random.uniform(1, 50)
    except:
        loss = random.uniform(1, 50)

    kill_reason = random.choice(KILL_REASONS)
    final_quote = random.choice(FINAL_WORDS)

    clear()
    header()

    print(f"\n  {C_BOLD}【下葬证书】{C_RESET}\n")
    print(f"  股票名称：{C_RED}{name}（{code}）{C_RESET}")
    print(f"  亏损金额：{C_RED}{loss:.1f}万{C_RESET}")
    print(f"  死亡原因：{C_YELLOW}{kill_reason}{C_RESET}")
    print(f"  临终遗言：{C_CYAN}{final_quote}{C_RESET}")
    print(f"  下葬日期：{datetime.date.today().strftime('%Y年%m月%d日')}{C_RESET}")
    print(f"  墓志铭：{C_GREEN}愿你在另一个市场找到价值{C_RESET}")

    date_str = datetime.date.today().strftime("%Y.%m")
    template = random.choice(GRAVEYARD_TEMPLATES)
    print(f"\n{template.format(name=name[:10], loss=loss, date=date_str)}")

    print(f"\n  {C_DIM}故事：{story}{C_RESET}")

    save = input(f"\n  {C_CYAN}收入墓园？(Y/n): {C_RESET}").strip().lower()
    if save != 'n':
        return {'name': f"{name}（{code}）", 'loss': loss, 'reason': kill_reason,
                'quote': final_quote, 'date': date_str, 'template': template}
    return None

def graveyard_statistics(tombstones):
    """墓园统计"""
    if not tombstones:
        return

    total_loss = sum(t['loss'] for t in tombstones)
    avg_loss = total_loss / len(tombstones)
    max_loss_stock = max(tombstones, key=lambda x: x['loss'])
    oldest = min(tombstones, key=lambda x: x['date'])

    print(f"\n  {C_BOLD}{'─'*60}{C_RESET}")
    print(f"  {C_BOLD}墓园统计：{C_RESET}")
    print(f"  入园数量：{C_RED}{len(tombstones)}只{C_RESET}")
    print(f"  总亏损：{C_RED}{total_loss:.1f}万{C_RESET}")
    print(f"  平均每只亏损：{C_YELLOW}{avg_loss:.1f}万{C_RESET}")
    print(f"  最大亏损：{C_RED}{max_loss_stock['loss']:.1f}万{C_RESET}（{max_loss_stock['name']}）")
    print(f"  入园最早：{oldest['name']}（{oldest['date']}）")

    if total_loss > 100:
        print(f"\n  {C_RED}{C_BOLD}你已经成功亏掉了一套房子首付{C_RESET}")
        print(f"  {C_DIM}但放心，你还活着，活着就有希望——虽然希望也不大{C_RESET}")
    elif total_loss > 50:
        print(f"\n  {C_YELLOW}你已经成功亏掉了一辆车{C_RESET}")
    elif total_loss > 10:
        print(f"\n  {C_YELLOW}你已经成功亏掉了好几个包{C_RESET}")
    else:
        print(f"\n  {C_GREEN}还好，亏得不算多，当交学费了{C_RESET}")

def main():
    tombstones = []

    # 预填一些示例墓碑
    sample_tombstones = [
        {'name': '中石油（601857）', 'loss': 12.3, 'reason': '亚洲最赚钱的公司，结果亏成最赔钱',
         'quote': '「我就不信邪，长期持有一定能回本」', 'date': '2024.03', 'template': GRAVEYARD_TEMPLATES[0]},
        {'name': '某新能源', 'loss': 8.5, 'reason': '听了朋友说内幕，结果朋友自己都亏了',
         'quote': '「朋友说这个绝对没问题」', 'date': '2024.08', 'template': GRAVEYARD_TEMPLATES[1]},
    ]
    tombstones.extend(sample_tombstones)

    while True:
        clear()
        header()
        print(f"""
  {C_BOLD}{C_WHITE}┌─── 功能菜单 ────────────────────────────────────┐{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_WHITE}│  {C_GREEN}[1]{C_RESET} 🪦 参观墓园（已有{tombstones}块墓碑）                  │{C_RESET}
  {C_WHITE}│  {C_YELLOW}[2]{C_RESET} ⚰️  下葬新持仓（添加亏损记录）                  │{C_RESET}
  {C_WHITE}│  {C_RED}[3]{C_RESET} 📊 墓园统计                                        │{C_RESET}
  {C_WHITE}│  {C_CYAN}[4]{C_RESET} 🕯️  点蜡烛祭奠                                      │{C_RESET}
  {C_WHITE}│  {C_RED}[0]{C_RESET} 🚪 离开墓园                                         │{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_BOLD}{C_WHITE}└───────────────────────────────────────────────────────┘{C_RESET}
""")

        choice = input(f"  {C_CYAN}请选择: {C_RESET}").strip()

        if choice == "1":
            show_graveyard(tombstones)
            input(f"\n  {C_CYAN}[回车返回]{C_RESET}")
        elif choice == "2":
            new_tomb = burial_ceremony()
            if new_tomb:
                tombstones.append(new_tomb)
            input(f"\n  {C_CYAN}[回车返回]{C_RESET}")
        elif choice == "3":
            clear()
            header()
            graveyard_statistics(tombstones)
            input(f"\n  {C_CYAN}[回车返回]{C_RESET}")
        elif choice == "4":
            clear()
            header()
            print(f"\n  {C_YELLOW}    🕯️      🕯️      🕯️    {C_RESET}")
            print(f"  {C_YELLOW}    ╱        ╲    ╱      {C_RESET}")
            print(f"  {C_YELLOW}   ╱   逝者    ╲╱    安息  {C_RESET}")
            print(f"  {C_YELLOW}     永垂不朽        {C_RESET}")
            print(f"\n  {C_BOLD}为所有在A股牺牲的战友默哀{C_RESET}")
            print(f"  {C_DIM}愿你们来世不碰杠杆，不追涨停，不听内幕{C_RESET}")
            print(f"  {C_DIM}愿你们的账户在天上永远是红的{C_RESET}")
            print(f"\n  {C_YELLOW}🕯️  一路走好 🕯️{C_RESET}")
            input(f"\n  {C_CYAN}[回车返回]{C_RESET}")
        elif choice == "0":
            break
        else:
            import time
            time.sleep(1)

if __name__ == "__main__":
    main()
