#!/usr/bin/env python3
"""
生成 README.md 投資報告
"""
import json
import os
from datetime import datetime
import pytz

def load_analysis_data():
    """載入多幣種分析數據"""
    try:
        with open("data/multi_investment_report.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: data/multi_investment_report.json not found")
        return None

def get_trend_emoji(trend):
    """根據趨勢返回對應的 emoji"""
    if "多頭" in trend or "偏多" in trend:
        return "📈"
    elif "空頭" in trend or "偏空" in trend:
        return "📉"
    else:
        return "📊"

def get_change_emoji(change_percent):
    """根據漲跌幅返回對應的 emoji"""
    if change_percent > 2:
        return "🚀"
    elif change_percent > 0:
        return "📈"
    elif change_percent > -2:
        return "📉"
    else:
        return "💥"

def format_price(price, symbol="BTCUSDT"):
    """格式化價格顯示"""
    if "DOGE" in symbol:
        return f"${price:.4f}"  # DOGE 顯示4位小數
    elif "XRP" in symbol or "ADA" in symbol:
        return f"${price:.4f}"  # XRP, ADA 顯示4位小數
    elif price < 1:
        return f"${price:.6f}"  # 小於1的幣種顯示6位小數
    elif price < 100:
        return f"${price:.2f}"  # ETH, SOL 等顯示2位小數
    else:
        return f"${price:,.2f}"  # BTC 等大價格顯示千分位

def get_tradingview_icon_url(symbol):
    """獲取 TradingView 圖標 URL"""
    icon_map = {
        "BTCUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCBTC--big.svg",
        "ETHUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCETH--big.svg", 
        "SOLUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCSOL--big.svg",
        "DOGEUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCDOGE--big.svg",
        "XRPUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCXRP--big.svg",
        "ADAUSDT": "https://s3-symbol-logo.tradingview.com/crypto/XTVCADA--big.svg"
    }
    return icon_map.get(symbol, "")

def get_symbol_with_icon(symbol, name):
    """生成帶 TradingView 圖標的符號（用於 GitHub README）"""
    icon_url = get_tradingview_icon_url(symbol)
    if icon_url:
        # GitHub README 支援 HTML img 標籤
        return f'<img src="{icon_url}" width="16" height="16" alt="{name}"> **{name}**'
    else:
        # 備用 emoji 方案
        emoji_map = {
            "BTCUSDT": "₿",      # Bitcoin 官方 Unicode 符號
            "ETHUSDT": "Ξ",      # Ethereum 官方 Unicode 符號
            "SOLUSDT": "◎",      # Solana 專業符號 (圓形設計)
            "DOGEUSDT": "Ð",     # Dogecoin 官方 Unicode 符號
            "XRPUSDT": "✕",      # XRP 專業符號 (X 設計)
            "ADAUSDT": "₳"       # Cardano 官方 Unicode 符號
        }
        emoji = emoji_map.get(symbol, "💰")
        return f"{emoji} **{name}**"

def get_symbol_emoji(symbol):
    """根據幣種返回對應的 emoji（備用方案）"""
    emoji_map = {
        "BTCUSDT": "₿",      # Bitcoin 官方 Unicode 符號
        "ETHUSDT": "Ξ",      # Ethereum 官方 Unicode 符號
        "SOLUSDT": "◎",      # Solana 專業符號 (圓形設計)
        "DOGEUSDT": "Ð",     # Dogecoin 官方 Unicode 符號
        "XRPUSDT": "✕",      # XRP 專業符號 (X 設計)
        "ADAUSDT": "₳"       # Cardano 官方 Unicode 符號
    }
    return emoji_map.get(symbol, "💰")

def get_symbol_name(symbol):
    """獲取幣種全名"""
    name_map = {
        "BTCUSDT": "Bitcoin",
        "ETHUSDT": "Ethereum",
        "SOLUSDT": "Solana",
        "DOGEUSDT": "Dogecoin",
        "XRPUSDT": "Ripple",
        "ADAUSDT": "Cardano"
    }
    return name_map.get(symbol, symbol)


def generate_readme_content(all_analysis_data):
    """生成多幣種 README.md 內容"""

    # 獲取當前時間 (UTC 和台北時間)
    utc_now = datetime.now(pytz.UTC)
    taipei_tz = pytz.timezone('Asia/Taipei')
    taipei_time = utc_now.astimezone(taipei_tz)

    # 生成多幣種 README 內容
    readme_content = f"""# 🚀 虛擬幣1h投資分析報告

> 📊 **實時技術分析** | 🤖 **自動化生成** | ⏰ **每小時更新** | 💰 **₿BTC·ΞETH·◎SOL·ÐDOGE·✕XRP·₳ADA**

---

## 📈 市場總覽

| 幣種 | 價格 | 1H變化 | 4H變化 | 24H變化 | 趨勢 | 信號 |
|------|------|--------|--------|---------|------|------|"""

    # 添加每個幣種的市場概況
    for symbol, analysis in all_analysis_data.items():
        price = analysis['current_price']
        one_hour_change = analysis.get('1h_change_percent', 0)
        four_hour_change = analysis.get('4h_change_percent', 0) # 获取 4H 变化
        change = analysis['24hr_change_percent']
        trend = analysis['current_trend']
        name = get_symbol_name(symbol)
        symbol_with_icon = get_symbol_with_icon(symbol, name)

        trend_short = "📈多頭" if "多頭" in trend else "📉空頭" if "空頭" in trend else "📊震盪"
        signal = "🟢買入" if change > 1 and "多頭" in trend else "🔴賣出" if change < -1 and "空頭" in trend else "⚪觀望"

        readme_content += f"""
| {symbol_with_icon} | {format_price(price, symbol)} | {one_hour_change:+.2f}% | {four_hour_change:+.2f}% | {change:+.2f}% | {trend_short} | {signal} |"""

    readme_content += f"""

**最後更新時間**: {taipei_time.strftime('%Y-%m-%d %H:%M:%S')} 台北時間

---

## 🔍 詳細分析

"""

    # 為每個幣種添加詳細分析
    for symbol, analysis in all_analysis_data.items():
        name = get_symbol_name(symbol)
        detail_symbol_with_icon = get_symbol_with_icon(symbol, name)  # 為詳細分析重新生成圖標
        price = analysis['current_price']
        one_hour_change = analysis.get('1h_change_percent', 0)
        change = analysis['24hr_change_percent']
        indicators = analysis['technical_indicators_summary']

        readme_content += f"""### {detail_symbol_with_icon} ({symbol})
"""
        # 移除图表引用

        # 避免 f-string 語法錯誤，分別格式化
        price_info = f"**價格**: {format_price(price, symbol)} | **1H**: {one_hour_change:+.2f}% | **24H**: {change:+.2f}% | **趨勢**: {analysis['current_trend']}"
        
        readme_content += f"""
{price_info}

**📊 均線系統**: {indicators['均線系統']}

**📈 MACD指標**: {indicators['MACD']}

**🎯 RSI指標**: {indicators['RSI']}

**🔄 KDJ指標**: {indicators['KDJ']}

**🎢 BOLL指標**: {indicators.get('BOLL', 'N/A')}

**💡 交易建議**: {analysis['analysis_result']['方向']}

**⏰ 入場時機**: {analysis['analysis_result']['入場時機']}

**🛡️ 風險管理**: {analysis['analysis_result']['止損設定']}

---

"""

    readme_content += f"""## 🎯 今日重點

### 🔥 最佳機會"""

    # 找出最佳機會（漲幅最大且趨勢向上）
    best_opportunity = None
    best_score = -999
    for symbol, analysis in all_analysis_data.items():
        change = analysis['24hr_change_percent']
        trend_score = 2 if "多頭" in analysis['current_trend'] else -2 if "空頭" in analysis['current_trend'] else 0
        score = change + trend_score
        if score > best_score:
            best_score = score
            best_opportunity = (symbol, analysis)

    if best_opportunity:
        symbol, analysis = best_opportunity
        name = get_symbol_name(symbol)
        symbol_with_icon = get_symbol_with_icon(symbol, name)
        readme_content += f"""
**{symbol_with_icon}** - {format_price(analysis['current_price'], symbol)} ({analysis['24hr_change_percent']:+.2f}%)

**🎯 方向判斷**: {analysis['analysis_result']['方向']}

**⏰ 入場時機**: {analysis['analysis_result']['入場時機']}

**🎯 目標價位**: {analysis['analysis_result']['目標價位']}"""

    readme_content += f"""

### ⚠️ 風險警示"""

    # 找出風險最大的幣種（跌幅最大或趨勢向下）
    highest_risk = None
    worst_score = 999
    for symbol, analysis in all_analysis_data.items():
        change = analysis['24hr_change_percent']
        trend_score = -2 if "空頭" in analysis['current_trend'] else 2 if "多頭" in analysis['current_trend'] else 0
        score = change + trend_score
        if score < worst_score:
            worst_score = score
            highest_risk = (symbol, analysis)

    if highest_risk:
        symbol, analysis = highest_risk
        name = get_symbol_name(symbol)
        symbol_with_icon = get_symbol_with_icon(symbol, name)
        readme_content += f"""
**{symbol_with_icon}** - {format_price(analysis['current_price'], symbol)} ({analysis['24hr_change_percent']:+.2f}%)

**⚠️ 趨勢狀況**: {analysis['current_trend']}，建議謹慎操作

**🛡️ 風險管理**: {analysis['analysis_result']['止損設定']}

**📊 技術狀況**: 當前指標顯示需要密切關注市場變化"""

    readme_content += f"""

---

## 📊 技術指標總結

| 指標 | BTC | ETH | SOL | DOGE | XRP | ADA |
|------|-----|-----|-----|------|-----|-----|"""

    # 創建技術指標對比表
    btc_data = all_analysis_data.get('BTCUSDT', {})
    eth_data = all_analysis_data.get('ETHUSDT', {})
    sol_data = all_analysis_data.get('SOLUSDT', {})
    doge_data = all_analysis_data.get('DOGEUSDT', {})
    xrp_data = all_analysis_data.get('XRPUSDT', {})
    ada_data = all_analysis_data.get('ADAUSDT', {})

    def get_indicator_status(analysis, indicator_key):
        if not analysis or 'technical_indicators_summary' not in analysis:
            return "N/A"
        indicator = analysis['technical_indicators_summary'].get(indicator_key, "")

        if indicator_key == 'BOLL':
            if "接近下軌" in indicator or "位於中軌下方" in indicator:
                return "🔴" # 价格偏弱/低位
            elif "接近上軌" in indicator or "位於中軌上方" in indicator:
                return "🟢" # 价格偏强/高位
            else:
                return "⚪" # 中性/震荡
        elif indicator_key == 'RSI':
            if "超買區" in indicator or "中性偏強" in indicator:
                return "🟢" # 偏强
            elif "超賣區" in indicator or "中性偏弱" in indicator:
                return "🔴" # 偏弱
            else:
                return "⚪" # 中性
        elif "金叉" in indicator or "多頭" in indicator or "偏強" in indicator:
            return "🟢"
        elif "死叉" in indicator or "空頭" in indicator or "偏弱" in indicator:
            return "🔴"
        else:
            return "⚪"

    indicators_list = ['均線系統', 'MACD', 'RSI', 'KDJ', 'BOLL'] # 新增 BOLL 到列表
    for indicator in indicators_list:
        btc_status = get_indicator_status(btc_data, indicator)
        eth_status = get_indicator_status(eth_data, indicator)
        sol_status = get_indicator_status(sol_data, indicator)
        doge_status = get_indicator_status(doge_data, indicator)
        xrp_status = get_indicator_status(xrp_data, indicator)
        ada_status = get_indicator_status(ada_data, indicator)
        readme_content += f"""
| **{indicator}** | {btc_status} | {eth_status} | {sol_status} | {doge_status} | {xrp_status} | {ada_status} |"""

    readme_content += f"""

---

## 🤖 系統信息

- **📊 數據來源**: Binance API
- **🔄 更新頻率**: 每小時自動更新
- **⏰ 最後更新**: {taipei_time.strftime('%Y-%m-%d %H:%M:%S')} 台北時間
- **🌍 UTC 時間**: {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC
- **📈 分析幣種**: BTC, ETH, SOL, DOGE, XRP, ADA
- **🎯 技術指標**: MA, MACD, BOLL, RSI, KDJ

---

## ⚠️ 免責聲明

> **投資有風險，入市需謹慎**
>
> 本報告僅供參考，不構成投資建議。加密貨幣市場波動極大，請做好風險管理，切勿投入超過承受能力的資金。

---

<div align="center">

**🚀 由 GitHub Actions 自動生成 | ⭐ 如果覺得有用請給個 Star**

*📊 實時監控 6 大主流幣種 | 🤖 專業技術分析 | 💡 智能交易建議*

</div>
"""
    
    return readme_content

def main():
    """主函數"""
    print("開始生成多幣種 README.md 投資報告...")

    # 載入分析數據
    all_analysis_data = load_analysis_data()
    if not all_analysis_data:
        print("無法載入分析數據，退出程序")
        return

    # 生成 README 內容
    readme_content = generate_readme_content(all_analysis_data)

    # 寫入 README.md
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("SUCCESS: 多幣種 README.md 投資報告生成成功！")

        # 顯示關鍵信息
        print(f"\n📊 成功分析 {len(all_analysis_data)} 個幣種:")
        for symbol, analysis in all_analysis_data.items():
            price = analysis['current_price']
            change = analysis['24hr_change_percent']
            trend = analysis['current_trend'][:10]
            emoji = get_symbol_emoji(symbol)
            print(f"  {emoji} {symbol}: {format_price(price, symbol)} ({change:+.2f}%) - {trend}")

    except Exception as e:
        print(f"ERROR: 生成 README.md 時發生錯誤: {e}")

if __name__ == "__main__":
    main()