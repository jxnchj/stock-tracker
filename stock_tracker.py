#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票持仓追踪工具 v1.0
功能：管理持仓、计算盈亏、分析涨跌
作者：Hermes for Hanson
"""

import json
import os
import sys
from datetime import datetime

# ====== 配置文件 ======
PORTFOLIO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio.json")

# ====== 核心数据操作 ======
def load_portfolio():
    """加载持仓数据"""
    if not os.path.exists(PORTFOLIO_FILE):
        return {"positions": [], "cash": 0.0, "last_updated": None}
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_portfolio(portfolio):
    """保存持仓数据"""
    portfolio["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

# ====== 持仓操作 ======
def add_position(stock_code, shares, cost_per_share):
    """
    添加或更新持仓
    stock_code: 股票代码，如 "000858" 或 "600519"
    shares: 股数（正数买入，负数卖出）
    cost_per_share: 成本价
    """
    portfolio = load_portfolio()
    
    # 查找是否已有该持仓
    found = False
    for pos in portfolio["positions"]:
        if pos["code"] == stock_code:
            # 更新现有持仓
            old_shares = pos["shares"]
            old_cost = pos["cost"]
            total_cost = old_shares * old_cost + shares * cost_per_share
            new_shares = old_shares + shares
            
            if new_shares <= 0:
                print(f"⚠️ 卖出后持仓为0或负数，删除该记录")
                portfolio["positions"].remove(pos)
            else:
                pos["shares"] = new_shares
                pos["cost"] = total_cost / new_shares  # 新平均成本
            found = True
            break
    
    if not found and shares > 0:
        # 新增持仓
        portfolio["positions"].append({
            "code": stock_code,
            "shares": shares,
            "cost": cost_per_share,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        })
    
    save_portfolio(portfolio)
    print(f"✅ 已更新持仓: {stock_code} x {shares}股 @ {cost_per_share}元")

def remove_position(stock_code, shares=None):
    """删除持仓（全部或部分）"""
    portfolio = load_portfolio()
    for pos in portfolio["positions"]:
        if pos["code"] == stock_code:
            if shares is None or shares >= pos["shares"]:
                portfolio["positions"].remove(pos)
                print(f"🗑️ 已删除持仓: {stock_code}")
            else:
                pos["shares"] -= shares
                print(f"✂️ 已减持: {stock_code} x {shares}股，剩余 {pos['shares']}股")
            save_portfolio(portfolio)
            return
    print(f"⚠️ 未找到持仓: {stock_code}")

# ====== 展示分析 ======
def show_portfolio():
    """展示当前持仓和盈亏"""
    portfolio = load_portfolio()
    positions = portfolio.get("positions", [])
    cash = portfolio.get("cash", 0.0)
    
    print("\n" + "="*60)
    print(f"📊 持仓报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    if not positions:
        print("📭 当前无持仓")
    else:
        print(f"{'代码':<10} {'股数':>8} {'成本价':>10} {'现价':>10} {'盈亏额':>12} {'盈亏%':>10}")
        print("-"*60)
        
        total_cost = 0.0
        total_value = 0.0
        
        for pos in positions:
            code = pos["code"]
            shares = pos["shares"]
            cost = pos["cost"]
            
            # 计算盈亏（这里用成本模拟现价，实际使用时需要接入实时行情）
            # 用户需要手动更新现价
            current_price = pos.get("current_price", cost)  # 默认=成本价
            pnl = (current_price - cost) * shares
            pnl_pct = (current_price / cost - 1) * 100 if cost > 0 else 0
            
            total_cost += cost * shares
            total_value += current_price * shares
            
            pnl_str = f"{pnl:+.2f}"
            pnl_pct_str = f"{pnl_pct:+.2f}%"
            sign = "🟢" if pnl >= 0 else "🔴"
            
            print(f"{code:<10} {shares:>8} {cost:>10.2f} {current_price:>10.2f} {pnl_str:>12} {pnl_pct_str:>10} {sign}")
    
    print("-"*60)
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_value / total_cost - 1) * 100 if total_cost > 0 else 0
    print(f"{'总成本':>20} {'总市值':>20} {'总盈亏':>20}")
    print(f"{'':>20} {total_value:>20.2f} {total_pnl:>+20.2f} ({total_pnl_pct:+.2f}%)")
    print(f"{'现金':>20} {cash:>20.2f}")
    print(f"{'总资产':>20} {total_value + cash:>20.2f}")
    print("="*60)
    
    # 温馨提醒
    if positions:
        print("\n💡 提示: 当前显示的是成本价，需手动更新现价才能计算真实盈亏")
        print("   命令: update_price <股票代码> <现价>")
    
    return portfolio

def update_price(stock_code, current_price):
    """更新股票现价"""
    portfolio = load_portfolio()
    for pos in portfolio["positions"]:
        if pos["code"] == stock_code:
            pos["current_price"] = current_price
            save_portfolio(portfolio)
            print(f"✅ 已更新 {stock_code} 现价: {current_price}")
            return
    print(f"⚠️ 未找到持仓: {stock_code}")

def show_watchlist():
    """展示自选股"""
    portfolio = load_portfolio()
    watchlist = portfolio.get("watchlist", [])
    print("\n⭐ 自选股:")
    if not watchlist:
        print("  暂无自选股")
    else:
        for code in watchlist:
            print(f"  - {code}")
    return watchlist

def add_watchlist(stock_code):
    """添加自选股"""
    portfolio = load_portfolio()
    watchlist = portfolio.setdefault("watchlist", [])
    if stock_code not in watchlist:
        watchlist.append(stock_code)
        save_portfolio(portfolio)
        print(f"✅ 已添加自选: {stock_code}")
    else:
        print(f"⚠️ {stock_code} 已在自选股中")

def remove_watchlist(stock_code):
    """删除自选股"""
    portfolio = load_portfolio()
    watchlist = portfolio.get("watchlist", [])
    if stock_code in watchlist:
        watchlist.remove(stock_code)
        save_portfolio(portfolio)
        print(f"🗑️ 已删除自选: {stock_code}")
    else:
        print(f"⚠️ {stock_code} 不在自选股中")

# ====== 命令行接口 ======
def print_help():
    print("""
📈 股票持仓追踪工具 v1.0
======================
命令:
  add <代码> <股数> <成本>      添加/更新持仓 (如: add 000858 100 35.5)
  remove <代码> [股数]         删除持仓（不填股数则全部删除）
  update <代码> <现价>         更新现价 (如: update 000858 38.5)
  show                        显示持仓报告
  watch                       显示自选股
  watch_add <代码>             添加自选股 (如: watch_add 600519)
  watch_remove <代码>          删除自选股
  help                        显示本帮助
  quit                        退出
======================
""")

def main():
    print("\n" + "🏃"*20)
    print("📈 股票持仓追踪工具 v1.0 启动")
    print("🏃"*20 + "\n")
    
    # 启动时显示当前持仓
    show_portfolio()
    print()
    show_watchlist()
    print_help()
    
    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == "quit" or action == "exit" or action == "q":
                print("👋 再见!")
                break
            elif action == "help" or action == "h":
                print_help()
            elif action == "show" or action == "s":
                show_portfolio()
            elif action == "watch" or action == "w":
                show_watchlist()
            elif action == "add" or action == "a":
                if len(parts) >= 4:
                    add_position(parts[1], int(parts[2]), float(parts[3]))
                else:
                    print("⚠️ 格式: add <代码> <股数> <成本>")
            elif action == "remove" or action == "rm":
                if len(parts) >= 2:
                    shares = int(parts[2]) if len(parts) >= 3 else None
                    remove_position(parts[1], shares)
                else:
                    print("⚠️ 格式: remove <代码> [股数]")
            elif action == "update" or action == "up":
                if len(parts) >= 3:
                    update_price(parts[1], float(parts[2]))
                else:
                    print("⚠️ 格式: update <代码> <现价>")
            elif action == "watch_add" or action == "wa":
                if len(parts) >= 2:
                    add_watchlist(parts[1])
                else:
                    print("⚠️ 格式: watch_add <代码>")
            elif action == "watch_remove" or action == "wr":
                if len(parts) >= 2:
                    remove_watchlist(parts[1])
                else:
                    print("⚠️ 格式: watch_remove <代码>")
            else:
                print(f"⚠️ 未知命令: {action}，输入 help 查看帮助")
        
        except KeyboardInterrupt:
            print("\n👋 退出")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
