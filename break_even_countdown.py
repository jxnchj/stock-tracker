#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解套倒计时
输入你的持仓成本和当前亏损，系统计算：
- 靠分红/债券收益解套要多少年
- 靠股价涨回去要多少年
- 最绝望情况和最乐观情况
让你清楚看到：回本到底有多远。
"""

import random
import os
import math

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
    print(f"{C_BOLD}{C_CYAN}  解套倒计时  |  距离回本还有多远{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")

def calc_years_to_breakeven(buy_price, current_price, annual_return_pct=8):
    """计算靠自然增长回本需要多少年"""
    if current_price >= buy_price:
        return 0.0
    loss_pct = (buy_price - current_price) / buy_price * 100
    # 需要的年化收益
    annual_gain = annual_return_pct / 100
    years = math.log(buy_price / current_price) / math.log(1 + annual_gain)
    return years

def calc_with_dividend(buy_price, current_price, dividend_yield=3, annual_return_pct=5):
    """计算靠分红+股价增长回本"""
    if current_price >= buy_price:
        return 0.0, 0.0
    annual_gain = annual_return_pct / 100
    years = math.log(buy_price / current_price) / math.log(1 + annual_gain)
    return years, dividend_yield

def draw_breakeven_chart(buy_price, current_price):
    """绘制解套进度条"""
    loss_pct = (buy_price - current_price) / buy_price * 100
    recovered_pct = max(0, (current_price / buy_price - 1) * -100 + 100)

    bar_total = 40
    recovered_blocks = int(recovered_pct / 100 * bar_total)
    lost_blocks = bar_total - recovered_blocks

    recovered_bar = C_GREEN + "▓" * recovered_blocks + C_RESET
    lost_bar = C_RED + "▓" * lost_blocks + C_RESET

    print(f"\n  {C_BOLD}持仓状态：{buy_price:.2f} → 当前 {current_price:.2f}{C_RESET}")
    print(f"  {C_RED}亏损：{loss_pct:.1f}%{C_RESET}  |{recovered_bar}{lost_bar}|  "
          f"{C_GREEN}已恢复：{recovered_pct:.1f}%{C_RESET}")

def draw_timeline(buy_price, current_price):
    """绘制时间轴"""
    print(f"\n  {C_BOLD}回本路径时间轴：{C_RESET}")
    print(f"  {C_DIM}{'─'*60}{C_RESET}")

    scenarios = [
        ("靠股价自然增长(年化8%)", 8),
        ("靠股价+分红综合(年化10%)", 10),
        ("靠高分红股(年化6%股息)", 6),
        ("靠账户天天涨停(乐观)", 10),  # 每天10%，几乎不可能
        ("靠每月定投补仓摊薄(中性)", 12),
        ("靠大牛市普涨(历史平均)", 15),
    ]

    for name, annual_pct in scenarios:
        years = calc_years_to_breakeven(buy_price, current_price, annual_pct)
        if years > 100:
            desc = f"{C_RED}约{years:.0f}年 ({C_BOLD}下辈子吧{C_RED}){C_RESET}"
        elif years > 20:
            desc = f"{C_YELLOW}约{years:.1f}年{C_RESET}"
        elif years > 5:
            desc = f"{C_YELLOW}{years:.1f}年{C_RESET}"
        else:
            desc = f"{C_GREEN}{years:.1f}年{C_RESET}"

        # 时间轴可视化
        timeline_pos = min(1.0, years / 30)
        pos_chars = int(timeline_pos * 50)
        timeline_bar = C_DIM + "─" * pos_chars + C_CYAN + "●" + C_RESET + C_DIM + "─" * (50 - pos_chars) + C_RESET

        print(f"  {name:<35} {timeline_bar} {desc}")

def draw_recovery_table(buy_price, current_price):
    """显示在不同年化收益下的回本年限表"""
    print(f"\n  {C_BOLD}回本年限速查表（需要多少年化收益才能回本）:{C_RESET}\n")
    print(f"  {'年化收益':>8}  {'需要年数':>8}  {'届时股价':>10}  {'压力评估'}")
    print(f"  {C_DIM}{'─'*56}{C_RESET}")

    for annual in [3, 5, 8, 10, 15, 20, 30]:
        years = calc_years_to_breakeven(buy_price, current_price, annual)
        future_price = buy_price * ((1 + annual/100) ** years)
        if years == 0:
            years_str = f"{C_GREEN}已回本{C_RESET}"
            pressure = C_GREEN + "无" + C_RESET
        elif years > 50:
            years_str = f"{C_RED}不可能{C_RESET}"
            pressure = C_RED + "绝望" + C_RESET
        elif years > 20:
            years_str = f"{C_YELLOW}{years:.1f}年{C_RESET}"
            pressure = C_YELLOW + "巨大" + C_RESET
        elif years > 10:
            years_str = f"{C_YELLOW}{years:.1f}年{C_RESET}"
            pressure = C_YELLOW + "较大" + C_RESET
        else:
            years_str = f"{C_GREEN}{years:.1f}年{C_RESET}"
            pressure = C_GREEN + "可接受" + C_RESET

        print(f"  {annual:>6}%  {years_str}  ¥{future_price:>9.2f}  {pressure}")

def draw_desperation_meter(buy_price, current_price):
    """绝望指数"""
    loss_pct = (buy_price - current_price) / buy_price * 100

    if loss_pct >= 70:
        level = "极度绝望"
        color = C_RED + C_BOLD
        emoji = "💀"
    elif loss_pct >= 50:
        level = "深度套牢"
        color = C_RED
        emoji = "😢"
    elif loss_pct >= 30:
        level = "中等套牢"
        color = C_YELLOW
        emoji = "😰"
    elif loss_pct >= 15:
        level = "轻度套牢"
        color = C_YELLOW
        emoji = "😐"
    else:
        level = "小套一下"
        color = C_GREEN
        emoji = "🙂"

    meter_len = 20
    filled = int(loss_pct / 100 * meter_len)
    meter = color + "▓" * filled + C_RESET + C_DIM + "░" * (meter_len - filled) + C_RESET

    print(f"\n  {C_BOLD}{emoji} 绝望指数：{meter} {loss_pct:.1f}%  [{level}]{C_RESET}")

    quotes = {
        "极度绝望": ["在A股，亏70%不叫亏，叫价值投资者。", "你以为的钻石底，下面还有地下室。"],
        "深度套牢": ["腰斩之后还有腰斩，这就是A股。", "时间是你的朋友？前提是你能活到回本那天。"],
        "中等套牢": ["还好没加杠杆，还能等到牛市。", "别看了，去滑个雪吧。"],
        "轻度套牢": ["小场面，这点波动不算什么。", "放心，牛市来了很快就能解套。"],
        "小套一下": ["恭喜你，跑赢了大多数韭菜。", "这点回撤，风控合格。"],
    }

    quote = random.choice(quotes[level])
    print(f"  {C_DIM}「{quote}」{C_RESET}")

def main():
    clear()
    header()
    print(f"""
  {C_WHITE}功能说明：{C_RESET}
  输入持仓成本和当前股价，系统计算回本所需时间
  以及不同策略下的解套路径
""")

    try:
        buy_str = input(f"  {C_CYAN}持仓成本价（如20.5）: {C_RESET}").strip()
        buy_price = float(buy_str)

        curr_str = input(f"  {C_CYAN}当前股价（如12.3）: {C_RESET}").strip()
        current_price = float(curr_str)

        div_str = input(f"  {C_CYAN}预估股息率%（直接回车默认3%）: {C_RESET}").strip()
        dividend_yield = float(div_str) if div_str else 3.0
    except:
        print(f"  {C_RED}输入无效，使用示例数据{C_RESET}")
        buy_price, current_price, dividend_yield = 50.0, 30.0, 3.0

    clear()
    header()
    print(f"\n  {C_BOLD}【解套诊断报告】{C_RESET}\n")
    print(f"  持仓成本：¥{buy_price:.2f}")
    print(f"  当前股价：¥{current_price:.2f}")
    loss_pct = (buy_price - current_price) / buy_price * 100
    print(f"  亏损幅度：{C_RED}{loss_pct:.1f}%{C_RESET}")
    print(f"  需涨回：¥{buy_price:.2f}（还需涨{(buy_price/current_price-1)*100:.1f}%）")

    draw_breakeven_chart(buy_price, current_price)
    draw_timeline(buy_price, current_price)
    draw_recovery_table(buy_price, current_price)
    draw_desperation_meter(buy_price, current_price)

    print(f"\n  {C_BOLD}{'─'*60}{C_RESET}")
    print(f"  {C_BOLD}实操建议：{C_RESET}")
    if loss_pct >= 50:
        print(f"  {C_YELLOW}1. 确认基本面是否发生变化，如恶化建议止损换股{C_RESET}")
        print(f"  {C_YELLOW}2. 如果坚信逻辑，等待下一轮牛市（历史平均7-10年一轮）{C_RESET}")
        print(f"  {C_YELLOW}3. 切勿加杠杆补仓，风险收益比极差{C_RESET}")
        print(f"  {C_RED}4. A股退市新规下，50%以上亏损存在退市风险{C_RESET}")
    elif loss_pct >= 30:
        print(f"  {C_GREEN}1. 回本需要较长时间，考虑是否值得持有机会成本{C_RESET}")
        print(f"  {C_YELLOW}2. 如基本面良好，可定投摊薄成本{C_RESET}")
        print(f"  {C_YELLOW}3. 关注板块轮动，抓住反弹机会分批减仓{C_RESET}")
    else:
        print(f"  {C_GREEN}1. 亏损可控，保持耐心持有{C_RESET}")
        print(f"  {C_YELLOW}2. 趁反弹可适当减仓降低损失{C_RESET}")

    print(f"\n  {C_CYAN}[回车退出]{C_RESET}")
    input()

if __name__ == "__main__":
    main()
