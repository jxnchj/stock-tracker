#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓诊断工具 v1.0
功能：分析持仓股票，给出持有/加仓/减仓建议
用法：直接运行，按提示输入持仓
"""

import json
import os
import sys
from datetime import datetime

# ====== 硬编码分析规则 ======
# 基于公开信息的股票诊断知识库
# 这些是基于行业逻辑的基本判断，实际决策需结合实时数据

STOCK_ANALYSIS_DB = {
    # 白酒
    "000858": {"name": "五粮液", "industry": "白酒", "risk": "高", "reason": "消费疲软，高端白酒需求承压，短期不建议加仓"},
    "600519": {"name": "贵州茅台", "industry": "白酒", "risk": "中", "reason": "高端龙头，抗跌性强，但弹性不足，适合防守"},
    "000596": {"name": "古井贡酒", "industry": "白酒", "risk": "高", "reason": "区域酒企，受高端酒挤压严重"},
    
    # 新能源
    "300750": {"name": "宁德时代", "industry": "新能源电池", "risk": "中", "reason": "全球龙头，份额稳定，但估值偏高，震荡市"},
    "300274": {"name": "阳光电源", "industry": "光伏逆变器", "risk": "高", "reason": "光伏行业产能过剩，短期承压"},
    "002460": {"name": "赣锋锂业", "industry": "锂矿", "risk": "高", "reason": "锂价下行周期，业绩压力大"},
    
    # 半导体
    "688018": {"name": "乐鑫科技", "industry": "半导体", "risk": "中", "reason": "IoT芯片，AIoT带动需求，有成长性但估值贵"},
    "300757": {"name": "罗博特科", "industry": "半导体设备", "risk": "中", "reason": "半导体设备国产替代，订单可见度高"},
    
    # 光通信
    "601869": {"name": "长飞光纤", "industry": "光通信", "risk": "中", "reason": "AI算力带动光模块需求，景气度上行"},
    "002463": {"name": "沪电股份", "industry": "PCB/光通信", "risk": "低", "reason": "AI服务器PCB龙头，受益算力建设"},
    
    # 科技
    "601127": {"name": "赛力斯", "industry": "新能源汽车", "risk": "高", "reason": "价格战激烈，利润承压，风险较高"},
    "300059": {"name": "东方财富", "industry": "互联网券商", "risk": "中", "reason": "A股情绪指标，行情好时弹性大"},
    
    # 稀有金属/资源
    "002428": {"name": "云南锗业", "industry": "稀有金属", "risk": "高", "reason": "小金属，题材驱动，波动极大，谨慎"},
    
    # 消费电子
    "300476": {"name": "胜宏科技", "industry": "PCB", "risk": "中", "reason": "显卡PCB，AI带动，有订单支撑"},
    
    # 医疗
    "000538": {"name": "云南白药", "industry": "中药", "risk": "低", "reason": "品牌中药，防守性强，弹性一般"},
    "300760": {"name": "迈瑞医疗", "industry": "医疗器械", "risk": "低", "reason": "器械龙头，业绩稳定，适合长持"},
    
    # 银行（债券相关）
    "600036": {"name": "招商银行", "industry": "银行", "risk": "低", "reason": "零售银行龙头，资产质量好，作为打新门票不错"},
    "601398": {"name": "工商银行", "industry": "银行", "risk": "低", "reason": "国有大行，股息率高，适合配置"},
}

# 行业整体判断
INDUSTRY_OUTLOOK = {
    "白酒": {"outlook": "⚠️ 中性偏弱", "reason": "消费疲软，高端酒需求下滑，行业调整期"},
    "新能源电池": {"outlook": "📊 震荡", "reason": "竞争加剧，产能过剩，但龙头份额稳固"},
    "光伏逆变器": {"outlook": "🔴 谨慎", "reason": "产能过剩严重，行业出清中，2026年难有大机会"},
    "锂矿": {"outlook": "🔴 谨慎", "reason": "锂价持续下行，底部未明"},
    "半导体": {"outlook": "📈 看好", "reason": "国产替代加速，AI带动设备需求，景气度上行"},
    "半导体设备": {"outlook": "📈 看好", "reason": "国产替代核心赛道，订单可见度高"},
    "光通信": {"outlook": "📈 看好", "reason": "AI算力建设带动，景气度持续2-3年"},
    "PCB": {"outlook": "📈 看好", "reason": "AI服务器需求爆发，龙头供不应求"},
    "新能源汽车": {"outlook": "⚠️ 中性", "reason": "价格战持续，行业洗牌，机会在分化"},
    "互联网券商": {"outlook": "📊 跟随大盘", "reason": "β属性强，行情好时弹性大"},
    "稀有金属": {"outlook": "⚠️ 高风险", "reason": "题材炒作居多，波动极大，不建议重仓"},
    "中药": {"outlook": "📊 中性", "reason": "防守属性，政策支持，但弹性一般"},
    "医疗器械": {"outlook": "📈 看好", "reason": "老龄化+国产替代，业绩稳定增长"},
    "银行": {"outlook": "🛡️ 防守", "reason": "高股息，稳健，适合债券背景的人配置"},
}


def diagnose_stock(code, shares=None, cost=None):
    """诊断单只股票"""
    code = code.upper().strip()
    
    # 标准化代码
    if not code.startswith(("SH", "SZ", "BJ")):
        if code.startswith("6"):
            code = "SH" + code
        elif code.startswith(("0", "3")):
            code = "SZ" + code
        elif code.startswith("8", "4"):
            code = "BJ" + code
    
    info = STOCK_ANALYSIS_DB.get(code, {})
    
    print("\n" + "="*60)
    print(f"📋 诊断股票: {info.get('name', code)} ({code})")
    if shares:
        print(f"   持仓: {shares}股")
    if cost:
        print(f"   成本: {cost}元")
    print("="*60)
    
    if not info:
        print(f"\n⚠️ 该股票({code})不在知识库中，通用建议：")
        print("   1. 查看所属行业整体前景")
        print("   2. 检查估值是否合理（PE/PB历史分位）")
        print("   3. 看近期是否有机构研报覆盖")
        print("   4. 债券思维：现金流折现角度审视")
        return None
    
    print(f"\n🏭 行业: {info['industry']}")
    ind_info = INDUSTRY_OUTLOOK.get(info['industry'], {})
    if ind_info:
        print(f"📊 行业前景: {ind_info['outlook']}")
        print(f"   原因: {ind_info['reason']}")
    
    print(f"\n📝 个股分析:")
    print(f"   {info['reason']}")
    
    print(f"\n⚠️ 风险等级: {info['risk']}")
    if info['risk'] == "高":
        print("   建议：考虑减仓或止损，不建议加仓")
    elif info['risk'] == "中":
        print("   建议：持有观察，逢低再补")
    else:
        print("   建议：可继续持有，作为防守配置")
    
    # 通用操作建议
    print(f"\n💡 综合建议:")
    if info['risk'] == "高":
        print(f"   建议操作: 减仓/止损 (风险等级: 🔴高)")
    elif info['risk'] == "中":
        print(f"   建议操作: 持有 + 逢低补仓 (风险等级: 🟡中)")
    else:
        print(f"   建议操作: 持有 + 可作为打新门票 (风险等级: 🟢低)")
    
    return info


def diagnose_portfolio(positions):
    """
    诊断整个持仓
    positions: [{"code": "000858", "shares": 100, "cost": 35.5}, ...]
    """
    print("\n" + "🔍"*30)
    print("📊 持仓诊断报告")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("🔍"*30)
    
    if not positions:
        print("\n⚠️ 暂无持仓")
        return
    
    results = []
    for pos in positions:
        info = diagnose_stock(pos.get("code"), pos.get("shares"), pos.get("cost"))
        if info:
            results.append({**pos, **info})
    
    # 汇总
    print("\n" + "="*60)
    print("📊 持仓汇总")
    print("="*60)
    
    high_risk = [r for r in results if r.get("risk") == "高"]
    mid_risk = [r for r in results if r.get("risk") == "中"]
    low_risk = [r for r in results if r.get("risk") == "低"]
    
    print(f"\n🔴 高风险持仓 ({len(high_risk)}只):")
    if high_risk:
        for r in high_risk:
            print(f"   - {r.get('name', r['code'])} ({r['code']}) - {r.get('shares', 0)}股")
    else:
        print("   无")
    
    print(f"\n🟡 中风险持仓 ({len(mid_risk)}只):")
    if mid_risk:
        for r in mid_risk:
            print(f"   - {r.get('name', r['code'])} ({r['code']}) - {r.get('shares', 0)}股")
    else:
        print("   无")
    
    print(f"\n🟢 低风险持仓 ({len(low_risk)}只):")
    if low_risk:
        for r in low_risk:
            print(f"   - {r.get('name', r['code'])} ({r['code']}) - {r.get('shares', 0)}股")
    else:
        print("   无")
    
    # 整体建议
    print("\n" + "="*60)
    print("💡 整体建议")
    print("="*60)
    
    if high_risk:
        print(f"\n⚠️ 你有 {len(high_risk)} 只高风险股票，建议优先处理:")
        for r in high_risk:
            print(f"   - {r.get('name', r['code'])}: {r.get('reason', '风险较高')}")
    
    if low_risk:
        print(f"\n🛡️ 低风险股票可作为压舱石，继续持有:")
        for r in low_risk:
            print(f"   - {r.get('name', r['code'])}: 稳健防守")
    
    # 债券背景建议
    print(f"\n📝 基于你债券背景的建议:")
    print("   1. 股票仓位不宜过高，留足现金流")
    print("   2. 可关注高股息银行股(工行、招行)作为打新门票")
    print("   3. 小市值题材股波动大，债券思维吃不消，慎入")
    print("   4. 考虑配置部分可转债，进可攻退可守")


def interactive_mode():
    """交互模式"""
    print("\n" + "🎯"*20)
    print("📊 持仓诊断工具 v1.0")
    print("🎯"*20)
    
    print("""
使用方式:
  1. 输入单只股票诊断: 输入股票代码 (如: 000858)
  2. 输入持仓诊断: 输入 'portfolio'
  3. 退出: 输入 'q'
""")
    
    while True:
        try:
            cmd = input("\n>>> ").strip()
            if not cmd:
                continue
            
            if cmd.lower() in ["q", "quit", "exit"]:
                print("👋 再见!")
                break
            
            if cmd.lower() in ["portfolio", "p"]:
                # 加载持仓
                portfolio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio.json")
                if os.path.exists(portfolio_file):
                    with open(portfolio_file) as f:
                        data = json.load(f)
                    positions = data.get("positions", [])
                    if positions:
                        diagnose_portfolio(positions)
                    else:
                        print("📭 暂无持仓，请先添加持仓")
                else:
                    print("📭 暂无持仓文件")
                continue
            
            if cmd.lower() in ["help", "h"]:
                print("""
命令:
  000858      - 诊断单只股票(五粮液)
  600519      - 诊断单只股票(茅台)
  portfolio   - 诊断所有持仓
  q           - 退出
""")
                continue
            
            # 诊断单只
            diagnose_stock(cmd)
        
        except KeyboardInterrupt:
            print("\n👋 退出")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    # 如果有命令行参数，直接诊断
    if len(sys.argv) > 1:
        for code in sys.argv[1:]:
            diagnose_stock(code)
    else:
        interactive_mode()
