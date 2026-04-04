#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StockGPT - 你的AI股市分析师（但不保证正确）
一个假装专业的A股分析终端，语不惊人死不休。
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

# ─── 数据池 ───────────────────────────────────────────────
STOCKS = [
    ("贵州茅台",    "600519", "白酒信仰"),
    ("宁德时代",    "300750", "新能源一哥"),
    ("比亚迪",      "002594", "国产电车之光"),
    ("中芯国际",    "688981", "半导体突围"),
    ("寒武纪",      "688256", "AI算力军火商"),
    ("东方财富",    "300059", "券商业茅"),
    ("招商银行",    "600036", "银行零售之王"),
    ("中国平安",    "601318", "保险压舱石"),
    ("万华化学",    "600309", "化工茅台"),
    ("药明康德",    "603259", "CXO龙头"),
    ("中际旭创",    "300308", "光模块总龙头"),
    ("浙江世宝",    "002703", "连板妖股"),
    ("漫步者",      "002351", "AI耳机正宗"),
    ("四川长虹",    "600839", "国货之光"),
    ("光大证券",    "601788", "牛市旗手"),
]

BULL_THS = [
    "突破前高，剑指万亿！",
    "机构大幅建仓，主升浪开启！",
    "量价齐升，主力志在高远！",
    "技术面完美，多头排列！",
    "业绩超预期，估值重塑！",
    "政策利好催化，趋势已成！",
    "北向资金持续买入，看多信号明确！",
    "换手率健康，筹码充分换手，后市看涨！",
]

BEAR_THS = [
    "高位放量出货，警惕回调风险！",
    "技术指标顶背离，短期需谨慎！",
    "估值泡沫严重，建议逢高减仓！",
    "主力资金净流出，短期不容乐观！",
    "市场情绪过热，随时可能调整！",
    "基本面不支持当前股价，回归合理区间！",
    "外部环境不确定性增大，防御为主！",
    "量能不足，上攻乏力，谨慎观望！",
]

FRUSTRATING_QUOTES = [
    "你以为我在第一层，其实我在第五层。",
    "这个位置，我选择沉默。",
    "看不懂的时候就空仓，这话我说过一千遍了。",
    "市场永远是对的，错的是你。",
    "我没有荐股资格，但你有亏损的自由。",
    "价值投资？先活过这波再说。",
    "你问我要不要抄底？我问你：你有多少条命？",
    "悲观者往往正确，乐观者往往赚钱——但在这个市场，悲观者也亏钱。",
]

INSANE_PREDICTIONS = [
    ("本轮牛市将涨到16000点", "2026-12-31", 0.05),
    ("A股将在下周开启主升浪", "2026-04-30", 0.10),
    ("宁德时代目标价888元", "2026-06-30", 0.03),
    ("半导体板块将出现10倍股", "2026-12-31", 0.15),
    ("券商板块将复制2014年行情", "2026-09-30", 0.08),
    ("北向资金年内净流入超万亿", "2026-12-31", 0.20),
]

RUMORS = [
    "据知情人士透露，某头部券商正在酝酿合并",
    "市场传言：监管层正在讨论T+0试点",
    "内部消息：某新能源龙头已获得大订单",
    "坊间传闻：某科技巨头将回A上市",
    "小道消息：某保险巨头正在布局AI算力",
    "不可靠消息：某游资已控盘连板妖股",
    "朋友圈看到的：明天某股票要停牌重组",
    "某股吧爆料：实控人被抓了（已被澄清是谣言）",
]

DAY名人名言 = [
    "活着就是为了玄学，赚钱就是为了信仰。——利弗莫尔（没说过）",
    "追高穷三代，低吸富一生。",
    "会买的是徒弟，会卖的是师父，会止损的是师公。",
    "不接飞刀，不抄半山腰，不追涨停板。",
    "计划你的交易，交易你的计划。",
    "股市没有专家，只有赢家和输家。",
    "你永远赚不到认知以外的钱——除非你运气好。",
]

FAKE_NEWS = [
    "📢 【突发】央行宣布降准0.25个百分点，释放长期资金约5000亿",
    "📢 【重磅】证监会：支持头部券商做优做强，适时推出做市商制度",
    "📢 【快讯】商务部：将采取更大力度举措稳外资，扩大开放领域",
    "📢 【要闻】国资委：推动国有控股上市公司价值回归合理区间",
    "📢 【独家】知情人士：新能源汽车购置税减免政策将延续至2027年",
]

# ─── 界面 ────────────────────────────────────────────────
def clear():
    os.system("clear")

def header():
    now = datetime.datetime.now()
    print(f"{C_BOLD}{C_CYAN}╔{'═' * 62}╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║  StockGPT Terminal  {now.strftime('%Y-%m-%d %H:%M:%S').rjust(28)}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╚{'═' * 62}╝{C_RESET}")

def menu():
    print(f"""
  {C_BOLD}{C_WHITE}┌─ 功能菜单 ─────────────────────────────────────┐{C_RESET}
  {C_WHITE}│                                                      │{C_RESET}
  {C_WHITE}│  {C_GREEN}[1]{C_RESET} 📈 每日市场分析                           │{C_RESET}
  {C_WHITE}│  {C_YELLOW}[2]{C_RESET} 🎯 个股诊断（诊断结果概不负责）            │{C_RESET}
  {C_WHITE}│  {C_RED}[3]{C_RESET} 🔮 明日预测（预测错了你就当我放屁）          │{C_RESET}
  {C_WHITE}│  {C_CYAN}[4]{C_RESET} 📰 市场快讯（假新闻生产器）                │{C_RESET}
  {C_WHITE}│  {C_MAG}[5]{C_RESET} 💬 名言警句（亏钱的时候看看很治愈）          │{C_RESET}
  {C_WHITE}│  {C_YELLOW}[6]{C_RESET} 🗣️  股民投诉窗口（AI负责挨骂）             │{C_RESET}
  {C_WHITE}│  {C_GREEN}[7]{C_RESET} 🎲 模拟选股（玄学选股，赛博算命）           │{C_RESET}
  {C_WHITE}│  {C_RED}[0]{C_RESET} 🚪 退出                                     │{C_RESET}
  {C_WHITE}│                                                      │{C_RESET}
  {C_BOLD}{C_WHITE}└──────────────────────────────────────────────────────┘{C_RESET}
""")

def divider(char="─", width=62):
    print(f"{C_DIM}{char * width}{C_RESET}")

def loading(text="思考中"):
    for i in range(3):
        print(f"\r{C_YELLOW}{text}{'.' * i}{' ' * (3-i)}{C_RESET}", end="", flush=True)
        time.sleep(0.3)
    print(f"\r{C_GREEN}✓ 完成{C_RESET}")

# ─── 功能模块 ────────────────────────────────────────────
def daily_analysis():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_GREEN}📈 每日市场分析{C_RESET}")
    divider()

    indices = [
        ("上证指数",   random.uniform(-2, 2.5),  random.randint(2800, 3600)),
        ("深证成指",   random.uniform(-2.5, 2),  random.randint(8000, 11000)),
        ("创业板指",   random.uniform(-3, 3),    random.randint(1500, 2200)),
        ("科创50",     random.uniform(-2, 3.5),  random.randint(700, 1100)),
        ("沪深300",    random.uniform(-1.5, 2),  random.randint(3200, 4200)),
    ]

    for name, pct, pts in indices:
        arrow = C_GREEN + "▲" if pct > 0 else C_RED + "▼"
        color = C_GREEN if pct > 0 else C_RED
        print(f"  {color}{arrow}{C_RESET} {name:<10} {pct:+.2f}%   {pts:,.0f}点")

    divider()
    print(f"\n  {C_BOLD}📊 板块动向：{C_RESET}")
    sectors = [
        ("AI算力",      random.choice([C_GREEN, C_RED, C_GREEN])),
        ("半导体",      random.choice([C_GREEN, C_GREEN, C_RED])),
        ("新能源汽车",  random.choice([C_RED, C_GREEN, C_RED])),
        ("军工",        random.choice([C_GREEN, C_RED, C_GREEN])),
        ("医药",        random.choice([C_RED, C_RED, C_GREEN])),
        ("大金融",      random.choice([C_GREEN, C_GREEN, C_GREEN])),
    ]
    for name, color in sectors:
        bar = random.choice(["▓▓▓▓░░", "▓▓░░░░", "▓▓▓▓▓▓", "▓▓▓░░░"])
        pct = random.uniform(-3, 5)
        arrow = C_GREEN+"▲" if pct>0 else C_RED+"▼"
        print(f"  {name:<12} {color}{bar}{C_RESET} {arrow}{abs(pct):.1f}%")

    divider()
    print(f"\n  {C_BOLD}💬 AI今日观点：{C_RESET}")
    loading("分析市场")
    opinion = random.choice([
        f"{C_GREEN}市场今日表现强劲，AI算力板块延续昨日升势，{C_RESET}\n  建议关注低位补涨的半导体个股，注意控制仓位。",
        f"{C_YELLOW}指数震荡分化，AI题材进入轮动期，{C_RESET}\n  前期涨幅较大的个股注意获利了结，可适当布局超跌的消费电子。",
        f"{C_RED}市场情绪偏谨慎，防御板块相对抗跌，{C_RESET}\n  建议保持轻仓，等待市场企稳后再考虑加仓。",
        f"{C_CYAN}创业板指走势明显强于主板，市场风格偏向成长，{C_RESET}\n  科创50可关注，短期趋势向好。",
    ])
    print(f"\n  {opinion}\n")
    print(f"  {C_DIM}⚠️  以上分析不构成投资建议，亏钱别找我。{C_RESET}")
    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def stock_diagnosis():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_YELLOW}🎯 个股诊断{C_RESET}")
    divider()
    print(f"  {C_WHITE}输入股票代码或名称（直接回车随机一只）：{C_RESET}")
    user_input = input(f"\n  >>> {C_CYAN}").strip()

    if user_input == "":
        stock_name, code, tag = random.choice(STOCKS)
    else:
        stock_name, code, tag = None, None, None
        for s in STOCKS:
            if user_input in s[0] or user_input in s[1]:
                stock_name, code, tag = s
                break
        if stock_name is None:
            stock_name, code, tag = random.choice(STOCKS)

    loading("扫描基本面")
    loading("分析技术面")
    loading("扒内幕消息")

    price = random.uniform(10, 500)
    pct = random.uniform(-8, 9.9)
    pe = random.uniform(8, 120)
    pb = random.uniform(1, 15)
    market_cap = random.choice(["500亿", "1200亿", "3000亿", "8000亿", "1.2万亿"])
    revenue_growth = random.uniform(-20, 50)
    holder_num = random.randint(3, 50)

    arrow = C_GREEN if pct > 0 else C_RED
    print(f"\n  {C_BOLD}{'─' * 50}{C_RESET}")
    print(f"  {C_WHITE}股票名称：{C_BOLD}{stock_name}{C_RESET}  代码：{code}")
    print(f"  {C_WHITE}今日价格：{arrow}{pct:+.2f}%{C_RESET}  当前价 ¥{price:.2f}")
    print(f"  {C_WHITE}市值：{market_cap}  PE：{pe:.1f}  PB：{pb:.1f}{C_RESET}")
    print(f"  {C_WHITE}营收增长：{C_GREEN if revenue_growth > 0 else C_RED}{revenue_growth:+.1f}%{C_RESET}  股东户数：{holder_num}万{C_RESET}")
    print(f"  {C_WHITE}所属概念：{C_CYAN}{tag}{C_RESET}")
    print(f"  {C_BOLD}{'─' * 50}{C_RESET}")

    verdict = random.choices(
        ["强烈推荐买入", "建议逢低布局", "保持观望", "建议逢高减仓", "不建议关注"],
        weights=[0.15, 0.25, 0.30, 0.20, 0.10]
    )[0]

    if "推荐" in verdict or "布局" in verdict:
        color = C_GREEN
    elif "观望" in verdict:
        color = C_YELLOW
    else:
        color = C_RED

    print(f"\n  {C_BOLD}🤖 AI诊断结果：{color}{verdict}{C_RESET}")
    print(f"\n  {C_WHITE}诊断依据：{C_RESET}")
    for _ in range(3):
        print(f"  {C_DIM}• {random.choice(BULL_THS if '推荐' in verdict or '布局' in verdict else BEAR_THS)}{C_RESET}")

    rumor = random.choice(RUMORS)
    print(f"\n  {C_YELLOW}📢 附加情报：{C_RESET}")
    print(f"  {C_DIM}  {random.choice(FAKE_NEWS)}{C_RESET}")
    print(f"  {C_YELLOW}  {rumor}{C_RESET}")

    print(f"\n  {C_BOLD}📝 AI补充判断：{C_RESET}")
    quote = random.choice(FRUSTRATING_QUOTES)
    print(f"  {C_CYAN}  「{quote}」{C_RESET}")

    print(f"\n  {C_DIM}⚠️  诊断结果纯属AI胡说八道，如有雷同，建议反思。{C_RESET}")
    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def tomorrow_prediction():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_RED}🔮 明日预测{C_RESET}")
    divider()
    print(f"  {C_YELLOW}⚠️  预测纯属AI胡说八道，亏钱了是你自己判断力的问题{C_RESET}\n")

    loading("连接宇宙能量场")
    loading("解读政策信号")
    loading("分析主力意图")

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    index_pred = random.uniform(-2, 2.5)
    volume = random.randint(7000, 14000)

    print(f"\n  {C_BOLD}📅 预测日期：{tomorrow.strftime('%Y年%m月%d日')}（星期"
          + ["一","二","三","四","五","六","日"][tomorrow.weekday()] + "）{C_RESET}")
    print(f"  {C_WHITE}上证指数预测：{C_GREEN if index_pred>0 else C_RED}{index_pred:+.2f}%{C_RESET}")
    print(f"  {C_WHITE}两市成交额预测：{volume:,}亿{C_RESET}")

    hot_theme = random.choice(["AI算力","半导体自主可控","新能源汽车","低空经济","量子科技","固态电池"])
    cold_theme = random.choice(["房地产产业链","消费电子","医药","银行"])

    print(f"\n  {C_BOLD}🔥 明日最热板块：{C_GREEN}{hot_theme}{C_RESET}")
    print(f"  {C_BOLD}❄️  明日回避板块：{C_RED}{cold_theme}{C_RESET}")

    stock, code, tag = random.choice(STOCKS)
    target = price = random.uniform(20, 300)
    target_price = price * random.uniform(1.05, 1.5)
    print(f"\n  {C_BOLD}🎯 明日金股（仅供演示）：{C_RESET}")
    print(f"  {C_WHITE}  {stock}（{code}）{C_RESET}")
    print(f"  {C_WHITE}  今日收盘：¥{price:.2f}  →  明日目标价：¥{target_price:.2f}（{((target_price/price)-1)*100:+.1f}%）{C_RESET}")

    insane_pred = random.choice(INSANE_PREDICTIONS)
    print(f"\n  {C_MAG}🌟 大胆预测：{C_RESET}")
    print(f"  {C_WHITE}  「{insane_pred[0]}」{C_RESET}")
    print(f"  {C_DIMPLE}  预测时间：{insane_pred[1]}  置信度：{insane_pred[2]*100:.0f}%（瞎编的）{C_RESET}")

    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def market_news():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_CYAN}📰 市场快讯{C_RESET}")
    divider()
    print(f"  {C_YELLOW}以下新闻纯属AI生产，如有雷同可能是巧合{C_RESET}\n")

    news = random.sample(FAKE_NEWS, k=min(4, len(FAKE_NEWS)))
    for i, n in enumerate(news):
        print(f"  {C_BOLD}{i+1}.{C_RESET} {n}")
        time.sleep(0.3)

    print()
    rumor = random.choice(RUMORS)
    print(f"  {C_YELLOW}🗣️  市场传言：{C_RESET}")
    print(f"  {C_DIM}  {rumor}{C_RESET}")

    divider()
    print(f"\n  {C_BOLD}📋 个股公告（模拟）：{C_RESET}")
    stock, code, tag = random.choice(STOCKS)
    anns = [
        f"【交易风险提示】{stock}（{code}）股票交易短期内波动较大，敬请投资者注意风险。",
        f"【异动公告】{stock}（{code}）股票连续3个交易日内日收盘价格涨幅偏离值累计达到20%，特此公告。",
        f"【业绩预告】{stock}（{code}）预计2026年一季度归母净利润同比+{random.uniform(20,80):.0f}%。",
        f"【澄清公告】近日有媒体报道公司涉及{tag}业务，经核实，该报道不属实，公司目前未开展相关业务。",
    ]
    for ann in random.sample(anns, 2):
        print(f"  {C_RED}📢{C_RESET} {ann}")

    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def famous_quotes():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_MAG}💬 股民名言警句{C_RESET}")
    divider()
    print(f"  {C_DIM}亏钱的时候读一读，很治愈{C_RESET}\n")

    quotes = [
        ("会买的是徒弟，会卖的是师父，会止损的是师公。", "——流传于民间"),
        ("不接飞刀，不抄半山腰，不追涨停板。", "——操盘手老K"),
        ("计划你的交易，交易你的计划。", "——据说利弗莫尔"),
        ("你永远赚不到认知以外的钱——除非你运气好。", "——StockGPT"),
        ("在A股，最贵的学费是杠杆。", "——某爆仓大佬"),
        ("止损要快，盈利要慢。", "——华尔街没说过这话"),
        ("别人恐慌我贪婪，别人贪婪我更贪婪。", "——最后一批接盘侠"),
        ("价值投资？先活过这波再说。", "——深圳某韭菜"),
        ("追高穷三代，低吸富一生。", "——民间智慧"),
        ("我昨天刚割肉，它今天就涨停了。", "——你身边的散户"),
        ("A股专治各种不服。", "——市场"),
        ("会买的是徒弟，会空仓的是大师。", "——某老股民"),
    ]

    for i, (quote, author) in enumerate(quotes, 1):
        color = random.choice([C_CYAN, C_YELLOW, C_GREEN, C_MAG])
        print(f"  {color}{i}.「{quote}」{C_RESET}")
        print(f"  {C_DIM}   —— {author}{C_RESET}\n")
        time.sleep(0.2)

    print(f"  {C_BOLD}{C_RED}最实用的一条：{C_RESET}")
    print(f"  {C_WHITE}  {random.choice(FRUSTRATING_QUOTES)}{C_RESET}")

    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def complaint_window():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_YELLOW}🗣️  股民投诉窗口{C_RESET}")
    divider()
    print(f"  {C_RED}AI在这里负责挨骂，你可以随意发泄{C_RESET}\n")

    complaints = [
        "买了就跌，卖了就涨，你们AI能不能靠谱一次？",
        "你们说好的AI革命呢？我的账户已经腰斩了！",
        "会买的是徒弟——我就是那个徒弟，被市场反复揍的那种。",
        "听了你们的推荐，我成功地从韭菜变成了老韭菜。",
        "你们研报说要涨，结果我买进去就开始跌，什么意思？",
        "为什么我一空仓就暴涨，一满仓就暴跌？是因为我吗？",
        "在A股混了三年，终于明白了一个道理：活着就是最大的赢家。",
    ]

    for i, c in enumerate(complaints, 1):
        print(f"  {C_YELLOW}{i}.{C_RESET} {c}")
    print()

    user_complaint = input(f"  {C_CYAN}你想骂什么？（直接回车看AI回复）{C_RESET}\n\n  >>> ").strip()

    loading("接受批评")
    loading("深度反思")
    loading("甩锅给市场")

    responses = [
        "您说得对，但这是市场的错，不是我的错。",
        "感谢您的投诉，我们会虚心接受……下次还敢。",
        "您的经历非常令人同情，但股市有风险，入市需谨慎这句话是认真的。",
        "我理解您的心情。说实话我也亏过，只不过我是AI，我没有心。",
        "您的建议已记录。鉴于您是VIP客户，我们决定：不退钱。",
        "非常抱歉给您带来的体验。我们AI已经学习了10000个小时，水平还是这样，我们会继续学习。",
    ]

    print(f"\n  {C_BOLD}{C_RED}StockGPT 客服回复：{C_RESET}")
    print(f"  {C_WHITE}{random.choice(responses)}{C_RESET}")

    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

def mystic_stock_picker():
    clear()
    header()
    print(f"\n  {C_BOLD}{C_GREEN}🎲 玄学选股（赛博算命）{C_RESET}")
    divider()
    print(f"  {C_YELLOW}⚠️  选股结果纯属随机生成，不构成任何投资建议{C_RESET}\n")

    loading("摇卦中")
    loading("读取K线能量场")
    loading("扫描主力仓位灵气")

    stock, code, tag = random.choice(STOCKS)
    lucky_num = random.randint(1, 99)
    color = random.choice(["红色", "黄色", "绿色", "白色", "黑色"])
    direction = random.choice(["东", "西", "南", "北", "东南", "西南"])
    action = random.choice(["买入", "观望", "加仓", "减仓", "清仓"])

    stars = ["★" * random.randint(1, 5) for _ in range(3)]

    print(f"\n  {C_BOLD}{C_CYAN}{'═' * 40}{C_RESET}")
    print(f"  {C_BOLD}      🧧 玄学选股结果 🧧{C_RESET}")
    print(f"  {C_BOLD}{C_CYAN}{'═' * 40}{C_RESET}")
    print(f"""
  {C_YELLOW}  卦象显示：{random.choice(['山天大壮','地水师','火天大有','雷水解','水风井'])}{C_RESET}
  {C_WHITE}  幸运数字：{lucky_num}{C_RESET}
  {C_WHITE}  今日幸运色：{color}  幸运方向：{direction}{C_RESET}
  {C_WHITE}  今日忌：{random.choice(['追高','频繁交易','满仓','杠杆'])}{C_RESET}
  {C_WHITE}  今日宜：{random.choice(['静观其变','分批建仓','止损','喝奶茶'])}{C_RESET}
""")
    print(f"  {C_BOLD}{C_GREEN}  推荐股票：{stock}（{code}）{C_RESET}")
    print(f"  {C_WHITE}  所属概念：{tag}{C_RESET}")
    print(f"  {C_WHITE}  综合评分：{random.choice(stars)} {random.randint(60, 98)}分{C_RESET}")
    print(f"  {C_WHITE}  操作建议：{C_RED if action in ['减仓','清仓'] else C_GREEN}{action}{C_RESET}")

    pct = random.uniform(-5, 9.9)
    print(f"  {C_WHITE}  预计波动：{C_GREEN if pct>0 else C_RED}{pct:+.1f}%{C_RESET}")

    print(f"\n  {C_BOLD}{C_MAG}  赛博占卜赠言：{C_RESET}")
    fortunes = [
        "今日运势：持股待涨，不动如山。",
        "今日运势：逢高减磅，落袋为安。",
        "今日运势：静待时机，不可盲目。",
        "今日运势：分批建仓，稳中求进。",
        "今日运势：管住手，别乱动。",
    ]
    print(f"  {C_CYAN}{random.choice(fortunes)}{C_RESET}")

    input(f"\n  {C_CYAN}[回车返回菜单]{C_RESET}")

# ─── 主循环 ──────────────────────────────────────────────
def main():
    while True:
        clear()
        header()
        menu()

        choice = input(f"  {C_CYAN}请选择 [0-7]: {C_RESET}").strip()

        if choice == "1":
            daily_analysis()
        elif choice == "2":
            stock_diagnosis()
        elif choice == "3":
            tomorrow_prediction()
        elif choice == "4":
            market_news()
        elif choice == "5":
            famous_quotes()
        elif choice == "6":
            complaint_window()
        elif choice == "7":
            mystic_stock_picker()
        elif choice == "0":
            clear()
            print(f"\n  {C_BOLD}{C_CYAN}感谢使用 StockGPT Terminal{C_RESET}")
            print(f"  {C_DIM}记住：市场有风险，入市需谨慎。活着就是为了玄学。{C_RESET}\n")
            break
        else:
            print(f"\n  {C_RED}无效选项，请重新选择{C_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
