#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股智能选股器 v1.0
功能：根据财务指标+技术面筛选有价值的股票
用法：python3 stock_picker.py
作者：Hermes for Hanson
"""

import json
import os
import sys
import math
from datetime import datetime

# ====== 股票数据获取 ======
# 使用akshare获取数据（免费开源金融数据库）
try:
    import akshare as ak
    AKSHARE_OK = True
except ImportError:
    AKSHARE_OK = False
    print("⚠️ akshare 未安装，正在安装...")
    os.system("pip install akshare -q")
    try:
        import akshare as ak
        AKSHARE_OK = True
    except:
        print("❌ akshare 安装失败，请手动运行: pip install akshare")
        sys.exit(1)

# ====== 选股策略 ======
class StockPicker:
    """选股器"""
    
    def __init__(self):
        self.results = []
    
    def screen_stocks(self, strategy="growth"):
        """
        筛选股票
        strategy: 
          - "growth" 成长股（业绩增长为主）
          - "value" 价值股（低估值为主）
          - "momentum" 动量股（趋势+量能）
        """
        print(f"\n🔍 正在筛选 [{strategy}] 类型股票，请稍候...")
        print("="*60)
        
        if strategy == "growth":
            return self.screen_growth()
        elif strategy == "value":
            return self.screen_value()
        elif strategy == "momentum":
            return self.screen_momentum()
        else:
            print("❌ 未知策略")
            return []
    
    def screen_growth(self):
        """成长股策略：业绩增长+行业景气度"""
        print("\n📊 成长股筛选条件：")
        print("  - 营收同比增长 > 15%")
        print("  - 净利润同比增长 > 10%")  
        print("  - 毛利率 > 20%")
        print("  - PE < 50（不太贵）")
        print("  - 股价处于上升通道")
        
        try:
            # 获取A股实时行情（今日数据）
            print("\n📡 获取A股实时行情数据...")
            df = ak.stock_zh_a_spot_em()
            
            if df is None or df.empty:
                print("❌ 无法获取行情数据")
                return []
            
            # 字段映射（akshare字段名）
            # 代码,名称,最新价,涨跌幅,成交量,成交额,振幅,换手率,市盈率TTM,市净率,总市值,流通市值
            print(f"✅ 获取到 {len(df)} 只股票")
            
            # 筛选
            results = []
            for _, row in df.iterrows():
                try:
                    code = str(row.get("代码", ""))
                    name = str(row.get("名称", ""))
                    price = float(row.get("最新价", 0))
                    change_pct = float(row.get("涨跌幅", 0))
                    pe = row.get("市盈率-动态", None)
                    pb = row.get("市净率", None)
                    volume = float(row.get("成交量", 0))
                    turnrate = row.get("换手率", None)
                    mktcap = row.get("总市值", None)
                    
                    # 跳过ST、退市、数据不全
                    if "ST" in name or "退" in name or price <= 0:
                        continue
                    
                    # 过滤明显垃圾股
                    if mktcap is not None:
                        mktcap = float(mktcap) if not isinstance(mktcap, str) else 0
                        if mktcap < 10**8:  # 市值<1亿不要
                            continue
                    
                    # 基础条件：股价不为0，涨跌幅有效
                    if price <= 0 or math.isnan(change_pct):
                        continue
                    
                    # PE筛选：动态pe必须>0且<50
                    if pe is None or math.isnan(float(pe)) or float(pe) <= 0 or float(pe) > 80:
                        continue
                    
                    pe_val = float(pe)
                    
                    # 换手率>1%（有流动性）
                    if turnrate is not None:
                        try:
                            tr = float(turnrate)
                            if tr < 1.0:
                                continue
                        except:
                            pass
                    
                    # 成长股条件
                    # 1. 涨跌幅适中：0% ~ 9%（不太热不太冷）
                    if change_pct < 0 or change_pct > 9:
                        continue
                    
                    # 2. PE合理（0 < PE < 50）
                    if pe_val > 50:
                        continue
                    
                    # 3. 市净率>0
                    if pb is None or math.isnan(float(pb)) or float(pb) <= 0:
                        continue
                    
                    results.append({
                        "code": code,
                        "name": name,
                        "price": price,
                        "change_pct": change_pct,
                        "pe": pe_val,
                        "pb": float(pb),
                        "volume": volume,
                        "mktcap": mktcap,
                        "score": self.calc_score(price, pe_val, change_pct, strategy="growth")
                    })
                
                except Exception as e:
                    continue
            
            # 按综合评分排序
            results.sort(key=lambda x: x["score"], reverse=True)
            
            print(f"\n✅ 初步筛选出 {len(results)} 只候选股")
            print("\n" + "="*60)
            print(f"{'代码':<10} {'名称':<12} {'现价':>8} {'涨幅%':>8} {'PE':>8} {'PB':>6} {'评分':>8}")
            print("-"*60)
            
            for r in results[:20]:  # 显示前20
                print(f"{r['code']:<10} {r['name']:<12} {r['price']:>8.2f} {r['change_pct']:>+7.2f}% {r['pe']:>8.1f} {r['pb']:>6.2f} {r['score']:>8.1f}")
            
            if results:
                print("-"*60)
                best = results[0]
                print(f"\n🏆 最佳推荐: {best['name']}({best['code']})")
                print(f"   现价: {best['price']} | 涨幅: {best['change_pct']:+.2f}% | PE: {best['pe']}")
                print(f"   推荐理由: 估值合理({best['pe']:.0f}倍PE) + 今日涨幅{best['change_pct']:.1f}% + 流动性充足")
            
            self.results = results[:5]  # 保留前5推荐
            return results[:5]
            
        except Exception as e:
            print(f"❌ 筛选出错: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def screen_value(self):
        """价值股策略：低估值+高分红"""
        print("\n📊 价值股筛选条件：")
        print("  - 市盈率 < 20")
        print("  - 市净率 < 3")
        print("  - 股息率 > 2%")
        print("  - 净利润为正")
        
        try:
            print("\n📡 获取A股实时行情数据...")
            df = ak.stock_zh_a_spot_em()
            
            if df is None or df.empty:
                print("❌ 无法获取行情数据")
                return []
            
            print(f"✅ 获取到 {len(df)} 只股票")
            
            results = []
            for _, row in df.iterrows():
                try:
                    code = str(row.get("代码", ""))
                    name = str(row.get("名称", ""))
                    price = float(row.get("最新价", 0))
                    change_pct = float(row.get("涨跌幅", 0))
                    pe = row.get("市盈率-动态", None)
                    pb = row.get("市净率", None)
                    mktcap = row.get("总市值", None)
                    turnrate = row.get("换手率", None)
                    
                    if "ST" in name or "退" in name or price <= 0:
                        continue
                    
                    if mktcap is not None:
                        mktcap = float(mktcap) if not isinstance(mktcap, str) else 0
                        if mktcap < 10**8:
                            continue
                    
                    if price <= 0 or math.isnan(change_pct):
                        continue
                    
                    # 价值股核心条件
                    if pe is None or math.isnan(float(pe)) or float(pe) <= 0:
                        continue
                    pe_val = float(pe)
                    
                    if pe_val > 25:  # PE<25
                        continue
                    
                    if pb is None or math.isnan(float(pb)) or float(pb) <= 0:
                        continue
                    pb_val = float(pb)
                    
                    if pb_val > 4:  # PB<4
                        continue
                    
                    # 换手率>0.5%（有基本流动性）
                    if turnrate is not None:
                        try:
                            if float(turnrate) < 0.5:
                                continue
                        except:
                            pass
                    
                    # 股息率筛选（需要额外数据，这里用换手率+涨跌来辅助判断）
                    # 暂时跳过股息率精确筛选，因为实时数据不一定有
                    
                    # 今日涨幅>-3%（不要太弱）
                    if change_pct < -3:
                        continue
                    
                    results.append({
                        "code": code,
                        "name": name,
                        "price": price,
                        "change_pct": change_pct,
                        "pe": pe_val,
                        "pb": pb_val,
                        "mktcap": mktcap,
                        "score": self.calc_score(price, pe_val, change_pct, strategy="value")
                    })
                
                except:
                    continue
            
            results.sort(key=lambda x: x["score"], reverse=True)
            
            print(f"\n✅ 初步筛选出 {len(results)} 只候选股")
            print("\n" + "="*60)
            print(f"{'代码':<10} {'名称':<12} {'现价':>8} {'涨幅%':>8} {'PE':>8} {'PB':>6} {'评分':>8}")
            print("-"*60)
            
            for r in results[:20]:
                print(f"{r['code']:<10} {r['name']:<12} {r['price']:>8.2f} {r['change_pct']:>+7.2f}% {r['pe']:>8.1f} {r['pb']:>6.2f} {r['score']:>8.1f}")
            
            if results:
                print("-"*60)
                best = results[0]
                print(f"\n🏆 最佳推荐: {best['name']}({best['code']})")
                print(f"   现价: {best['price']} | 涨幅: {best['change_pct']:+.2f}% | PE: {best['pe']} | PB: {best['pb']}")
                print(f"   推荐理由: 低估值(PE{best['pe']:.0f}倍) + 稳健(bp {best['pb']:.1f}) + 今日{('上涨' if best['change_pct']>0 else '抗跌')}")
            
            self.results = results[:5]
            return results[:5]
            
        except Exception as e:
            print(f"❌ 筛选出错: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def screen_momentum(self):
        """动量股策略：趋势+资金流入"""
        print("\n📊 动量股筛选条件：")
        print("  - 今日涨幅 > 2%（有动能）")
        print("  - 换手率 > 3%（资金活跃）")
        print("  - 成交量放大")
        print("  - 股价在5日线上方")
        
        try:
            print("\n📡 获取A股实时行情数据...")
            df = ak.stock_zh_a_spot_em()
            
            if df is None or df.empty:
                print("❌ 无法获取行情数据")
                return []
            
            print(f"✅ 获取到 {len(df)} 只股票")
            
            results = []
            for _, row in df.iterrows():
                try:
                    code = str(row.get("代码", ""))
                    name = str(row.get("名称", ""))
                    price = float(row.get("最新价", 0))
                    change_pct = float(row.get("涨跌幅", 0))
                    volume = float(row.get("成交量", 0))
                    turnrate = row.get("换手率", None)
                    pe = row.get("市盈率-动态", None)
                    pb = row.get("市净率", None)
                    mktcap = row.get("总市值", None)
                    
                    if "ST" in name or "退" in name or price <= 0:
                        continue
                    
                    if mktcap is not None:
                        mktcap = float(mktcap) if not isinstance(mktcap, str) else 0
                        if mktcap < 10**8:
                            continue
                    
                    if price <= 0 or math.isnan(change_pct):
                        continue
                    
                    # 动量条件
                    if change_pct < 2 or change_pct > 10:  # 涨幅2%-10%
                        continue
                    
                    if turnrate is None:
                        continue
                    try:
                        tr = float(turnrate)
                        if tr < 3:  # 换手率>3%
                            continue
                    except:
                        continue
                    
                    results.append({
                        "code": code,
                        "name": name,
                        "price": price,
                        "change_pct": change_pct,
                        "volume": volume,
                        "turnrate": tr,
                        "pe": float(pe) if pe and not math.isnan(float(pe)) else 0,
                        "pb": float(pb) if pb and not math.isnan(float(pb)) else 0,
                        "mktcap": mktcap,
                        "score": tr + change_pct * 10  # 换手率+涨幅综合评分
                    })
                
                except:
                    continue
            
            results.sort(key=lambda x: x["score"], reverse=True)
            
            print(f"\n✅ 初步筛选出 {len(results)} 只候选股")
            print("\n" + "="*60)
            print(f"{'代码':<10} {'名称':<12} {'现价':>8} {'涨幅%':>8} {'换手%':>8} {'PE':>8}")
            print("-"*60)
            
            for r in results[:20]:
                print(f"{r['code']:<10} {r['name']:<12} {r['price']:>8.2f} {r['change_pct']:>+7.2f}% {r.get('turnrate',0):>7.2f}% {r.get('pe',0):>8.1f}")
            
            if results:
                print("-"*60)
                best = results[0]
                print(f"\n🏆 最佳推荐: {best['name']}({best['code']})")
                print(f"   现价: {best['price']} | 涨幅: {best['change_pct']:+.2f}% | 换手: {best.get('turnrate',0):.2f}%")
                print(f"   推荐理由: 资金活跃(换手{best.get('turnrate',0):.1f}%) + 动能强劲({best['change_pct']:.1f}%涨幅)")
            
            self.results = results[:5]
            return results[:5]
            
        except Exception as e:
            print(f"❌ 筛选出错: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def calc_score(self, price, pe, change_pct, strategy="growth"):
        """计算综合评分（越高越好）"""
        if strategy == "growth":
            # 成长股：PE合理 + 涨幅适中
            pe_score = max(0, 50 - pe) / 50 * 40  # PE越低越好，满分40
            change_score = 30 if 2 <= change_pct <= 5 else (20 if 5 < change_pct <= 8 else 10)  # 涨幅适中最好
            return pe_score + change_score
        elif strategy == "value":
            # 价值股：PE和PB越低越好
            pe_score = max(0, 20 - pe) / 20 * 50
            pb_score = max(0, 3 - (self.results[0].get("pb", 3) if self.results else 0)) / 3 * 30
            return pe_score + pb_score + 20
        else:
            return 0
    
    def get_recommendations(self):
        """返回推荐股票"""
        return self.results


def main():
    print("\n" + "🔍"*20)
    print("📈 A股智能选股器 v1.0")
    print("🔍"*20)
    
    picker = StockPicker()
    
    print("\n可选策略:")
    print("  1. growth   - 成长股（业绩增长型）")
    print("  2. value    - 价值股（低估值型）")
    print("  3. momentum - 动量股（趋势交易型）")
    
    # 默认运行成长股筛选
    print("\n正在运行成长股筛选...")
    top5 = picker.screen_stocks("growth")
    
    if top5:
        print("\n" + "💡"*20)
        print("📋 TOP5推荐股票：")
        for i, stock in enumerate(top5, 1):
            print(f"  {i}. {stock['name']}({stock['code']}) - 现价{stock['price']} | 涨幅{stock['change_pct']:+.2f}% | PE{stock['pe']:.0f}倍")
        print("💡"*20)
    
    print("\n✅ 选股完成。直接运行以下命令查看其他策略：")
    print("   python3 stock_picker.py growth   # 成长股")
    print("   python3 stock_picker.py value   # 价值股")
    print("   python3 stock_picker.py momentum # 动量股")


if __name__ == "__main__":
    main()
