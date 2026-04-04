#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日股评嘴炮生成器
生成各种大师的预测，有理有据，逻辑自洽，但最后全部打脸。
看多了你会发现：所有股评都是废话，但写得比研报还好看。
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

STOCKS = [
    ("贵州茅台", "600519"), ("宁德时代", "300750"), ("比亚迪", "002594"),
    ("中芯国际", "688981"), ("寒武纪", "688256"), ("东方财富", "300059"),
    ("招商银行", "600036"), ("中国平安", "601318"), ("中际旭创", "300308"),
    ("光大证券", "601788"), ("万丰奥威", "002085"), ("漫步者", "002351"),
]

SECTORS = [
    "AI算力", "半导体", "新能源汽车", "军工", "医药",
    "大金融", "消费", "房地产", "低空经济", "固态电池",
]

ANALYST_TYPES = [
    ("技术派大师", "以K线形态和指标为依据"),
    ("价值投资派", "强调护城河和长期持有"),
    ("政策解读派", "擅长从文件中找投资机会"),
    ("游资龙头派", "专注题材炒作和连板逻辑"),
    ("宏观策略派", "从经济周期角度分析市场"),
    ("量化模型派", "用数学模型预测走势"),
]

STYLE_QUOTES = {
    "技术派大师": [
        "从周线级别来看，这里形成了经典的头肩底形态",
        "MACD在零轴上方二次金叉，这是强烈的买入信号",
        "成交量配合股价突破，是有效的突破形态",
        "布林带收口后开口，中期趋势即将展开",
    ],
    "价值投资派": [
        "这家公司的护城河足够宽，足以抵御任何竞争",
        "当前的PE处于历史低位，安全边际极高",
        "管理层优秀，分红率稳定，是典型的价值标的",
        "ROE持续稳定在20%以上，证明了其强大的竞争力",
    ],
    "政策解读派": [
        "从中可以看出，政策正在向科技产业倾斜",
        "这次的文件规格极高，相关板块将直接受益",
        "领导人的讲话透露了明确的产业方向",
        "监管层的最新表态，是板块启动的信号弹",
    ],
    "游资龙头派": [
        "情绪已经到了冰点，明天大概率修复",
        "龙虎榜显示知名游资重仓买入",
        "情绪高涨，连板股打开空间后会有二波",
        "这就是今年的十倍股基因，短线必炒",
    ],
    "宏观策略派": [
        "从美林时钟来看，现在处于衰退到复苏的过渡期",
        "全球流动性拐点已至，A股将迎来系统性机会",
        "PPI和CPI的剪刀差收窄，企业盈利将改善",
        "美债收益率倒挂预示着风险资产面临压力",
    ],
    "量化模型派": [
        "我们的量化模型显示，当前点位上涨概率达78%",
        "从历史数据回测，均值回归的概率超过85%",
        "多因子模型显示，现在是做多的黄金窗口",
        "北向资金流向与技术面形成共振，上涨概率极大",
    ],
}

BEAR_BOTTOM = [
    "但考虑到外围市场不确定性，建议保持谨慎",
    "不过也要注意，结构性行情下要精选个股",
    "当然，具体操作还要结合自身风险承受能力",
    "短期波动在所难免，建议做好仓位控制",
    "但市场永远是对的，我们要尊重市场信号",
]

FUTURE_PREDICTIONS = [
    "保守估计，上证指数年内有望冲击4200点",
    "如果成交量能配合，不排除挑战历史高点的可能",
    "预计三季度将有系统性机会，建议逢低布局",
    "本轮行情有望延续至明年一季度",
    "科技板块将是未来三年的主线行情",
]

GURU_NAMES = [
    "李大霄（但不退休）", "徐晓峰（每天都在）", "但斌（还在守茅台）",
    "任泽平（已改行经济学家）", "叶荣添（天天涨停）",
    "水皮（经常没人知道）", "贺宛男（专业唱空30年）",
    "金岩石（偶尔还会出来）", "侯宁（空军司令）",
    "沙黾农（早晨必发微博）",
]

BATTLE_GURUS = [
    ("看多派", C_GREEN, "坚定看好，后市必创新高！"),
    ("看空派", C_RED, "我已经减仓，你们随意！"),
    ("滑头派", C_YELLOW, "震荡格局，轻仓应对！"),
    ("神秘派", C_MAGENTA, "我不方便说，但你们懂的..."),
]

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  每日股评嘴炮生成器  |  大师们的表演时间{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*60}{C_RESET}")

def generate_analysis(analyst_type, analyst_name, style_quotes):
    stock, code = random.choice(STOCKS)
    paragraphs = []
    for _ in range(random.randint(2, 3)):
        q = random.choice(style_quotes)
        paragraphs.append(q)
    pred = random.choice(FUTURE_PREDICTIONS)
    paragraphs.append(pred)
    risk = random.choice(BEAR_BOTTOM)
    paragraphs.append(risk)
    return stock, code, paragraphs

def show_battle():
    clear()
    header()
    print(f"\n  {C_BOLD}{'─'*60}{C_RESET}")
    print(f"  {C_BOLD}{C_YELLOW}【大师Battle】{C_RESET} 同一市场，不同声音\n")
    for role, color, declaration in BATTLE_GURUS:
        guru = random.choice(GURU_NAMES)
        print(f"  {color}{role} {guru}{C_RESET}：")
        print(f"  {C_WHITE}「{declaration}」{C_RESET}")
        print()
    print(f"  {C_DIM}散户内心OS：到底该听谁的？？？{C_RESET}")
    input(f"\n  {C_CYAN}[回车继续]{C_RESET}")

def show_single_guru():
    clear()
    header()
    analyst_type, analyst_desc = random.choice(ANALYST_TYPES)
    guru_name = random.choice(GURU_NAMES)
    style_quotes = STYLE_QUOTES[analyst_type]
    print(f"\n  {C_BOLD}{analyst_type} {guru_name}{C_RESET}")
    print(f"  {C_DIM}{analyst_desc}{C_RESET}\n")
    stock, code, paragraphs = generate_analysis(analyst_type, guru_name, style_quotes)
    print(f"  {C_BOLD}【今日市场分析】{C_RESET}\n")
    for p in paragraphs:
        print(f"  {C_WHITE}{p}{C_RESET}\n")
    print(f"  {C_DIM}{'─'*30}{C_RESET}")
    print(f"\n  {C_BOLD}大师金股：{C_RESET}")
    for i in range(random.randint(2, 4)):
        s, c = random.choice(STOCKS)
        target = random.uniform(50, 500)
        pct = random.uniform(10, 50)
        print(f"  {C_CYAN}{i+1}.{C_RESET} {s}（{c}）目标价{target:.2f}元，较当前涨{pct:.0f}%")
    print(f"\n  {C_YELLOW}风险提示：以上分析纯属个人观点，不构成投资建议{C_RESET}")
    input(f"\n  {C_CYAN}[回车继续]{C_RESET}")

def show_prediction_record():
    clear()
    header()
    print(f"\n  {C_BOLD}【历史预测回测】{C_RESET}")
    print(f"  {C_DIM}看看那些大师的历史预测，到底准不准{C_RESET}\n")
    records = []
    for _ in range(8):
        guru = random.choice(GURU_NAMES)
        stock, code = random.choice(STOCKS)
        was_right = random.random() < 0.35
        pred_pct = random.uniform(5, 30)
        if was_right:
            actual_pct = pred_pct * random.uniform(0.8, 1.2)
            result = C_GREEN + f"猜对了！实际涨{actual_pct:.1f}%" + C_RESET
        else:
            actual_pct = -pred_pct * random.uniform(0.5, 1.5)
            result = C_RED + f"打脸了！实际跌{abs(actual_pct):.1f}%" + C_RESET
        records.append((guru, stock, pred_pct, was_right, result))
    print(f"  {'大师':<15} {'股票':<10} {'预测':<8} {'结果'}")
    print(f"  {C_DIM}{'─'*55}{C_RESET}")
    for guru, stock, pred_pct, was_right, result in sorted(records, key=lambda x: x[3]):
        print(f"  {guru:<12} {C_CYAN}{stock:<8}{C_RESET} {C_GREEN if was_right else C_RED}涨{pred_pct:.0f}%{C_RESET}   {result}")
    print(f"\n  {C_BOLD}胜率统计：{C_RED}35%{C_RESET} （市场先生永远是对的）")
    print(f"  {C_DIM}所以，股评看看就行了，别当真{C_RESET}")
    input(f"\n  {C_CYAN}[回车返回]{C_RESET}")

def generate_daily_prediction():
    clear()
    header()
    now = datetime.datetime.now()
    print(f"\n  {C_BOLD}【{now.strftime('%Y年%m月%d日')} 市场展望】{C_RESET}\n")
    for role, color, _ in BATTLE_GURUS:
        guru = random.choice(GURU_NAMES)
        stock, code = random.choice(STOCKS)
        if role == "看多派":
            view = f"{C_GREEN}震荡上行，建议积极布局{C_RESET}"
            target = random.randint(3200, 3800)
            action = f"目标上证 {target}点，看好{stock}"
        elif role == "看空派":
            view = f"{C_RED}谨慎观望，控制仓位为宜{C_RESET}"
            target = random.randint(2700, 3100)
            action = f"警惕回调，下方支撑 {target}点，建议减仓"
        elif role == "滑头派":
            view = f"{C_YELLOW}区间震荡，高抛低吸{C_RESET}"
            action = f"在{random.randint(2900,3200)}-{random.randint(3300,3600)}点之间波动"
        else:
            view = f"{C_MAGENTA}我说了你们也不信{C_RESET}"
            action = f"{C_DIM}（大师神秘一笑，不愿多说）{C_RESET}"
        print(f"  {color}{C_BOLD}{role} {guru}{C_RESET}：")
        print(f"  {C_WHITE}「{view}」{C_RESET}")
        print(f"  {action}\n")
    print(f"  {C_BOLD}【收盘结果（第二天的真实情况）】{C_RESET}")
    actual_pct = random.uniform(-2, 2.5)
    actual_points = random.randint(2800, 3600)
    if actual_pct > 0:
        print(f"  {C_GREEN}实际上证指数：{actual_pct:+.2f}%  {actual_points}点{C_RESET}")
        print(f"  {C_RED}多方大师：猜对了  看空大师：打脸了{C_RESET}")
    else:
        print(f"  {C_RED}实际上证指数：{actual_pct:+.2f}%  {actual_points}点{C_RESET}")
        print(f"  {C_GREEN}看空大师：猜对了  多方大师：打脸了{C_RESET}")
    print(f"\n  {C_DIM}【次日大师们的反应】{C_RESET}")
    print(f"  {random.choice(GURU_NAMES)}：我说了是结构性行情，指数不重要")
    print(f"  {random.choice(GURU_NAMES)}：短期波动不改长期趋势，我的逻辑依然成立")
    print(f"  {random.choice(GURU_NAMES)}：我是预测大盘，不是预测每天的涨跌")
    input(f"\n  {C_CYAN}[回车返回]{C_RESET}")

def main():
    while True:
        clear()
        header()
        print(f"""
  {C_BOLD}{C_WHITE}┌─── 功能菜单 ────────────────────────────────────┐{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {C_WHITE}│  {C_GREEN}[1]{C_RESET} 观摩大师Battle（看多vs看空）                     │{C_RESET}
  {C_WHITE}│  {C_YELLOW}[2]{C_RESET} 拜读大师每日分析（认真你就输了）              │{C_RESET}
  {C_WHITE}│  {C_RED}[3]{C_RESET} 历史预测回测（看看谁被打脸最多）                │{C_RESET}
  {C_WHITE}│  {C_CYAN}[4]{C_RESET} 生成今日预测报告（次日自动打脸）              │{C_RESET}
  {C_WHITE}│  {C_RED}[0]{C_RESET} 退出                                             │{C_RESET}
  {C_WHITE}│                                                       │{C_RESET}
  {BOLD}{C_WHITE}└───────────────────────────────────────────────────────┘{C_RESET}
""")
        choice = input(f"  {C_CYAN}请选择: {C_RESET}").strip()
        if choice == "1":
            show_battle()
        elif choice == "2":
            show_single_guru()
        elif choice == "3":
            show_prediction_record()
        elif choice == "4":
            generate_daily_prediction()
        elif choice == "0":
            break
        else:
            import time
            time.sleep(1)

if __name__ == "__main__":
    main()
