#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot for Cryptocurrency Buy/Sell Signals
發送虛擬幣買入/賣出訊號到 Telegram Bot
"""

import requests
import json
import os
from datetime import datetime
import pytz

class TelegramBot:
    def __init__(self, bot_token, chat_id):
        """
        初始化 Telegram Bot
        
        Args:
            bot_token (str): Telegram Bot Token
            chat_id (str): Telegram Chat ID (可以是個人或群組)
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message, parse_mode="HTML"):
        """
        發送訊息到 Telegram
        
        Args:
            message (str): 要發送的訊息
            parse_mode (str): 訊息格式 (HTML 或 Markdown)
        
        Returns:
            dict: API 回應結果
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ 發送 Telegram 訊息失敗: {e}")
            return None
    
    def send_buy_signal(self, symbol, price, change_1h, change_4h, change_24h, trend, analysis_data=None, combined_advice="明確看多"):
        """
        發送買入訊號
        
        Args:
            symbol (str): 交易對符號
            price (float): 當前價格
            change_1h (float): 1小時變化百分比
            change_4h (float): 4小時變化百分比  
            change_24h (float): 24小時變化百分比
            trend (str): 趨勢描述
            analysis_data (dict): 詳細分析數據
            combined_advice (str): 綜合建議（如："明確看多"、"謹慎做多"等）
        """
        # 幣種名稱和圖標映射
        symbol_names = {
            "BTCUSDT": {"name": "BTC", "icon": "₿", "emoji": "🟠"},
            "ETHUSDT": {"name": "ETH", "icon": "Ξ", "emoji": "🔵"},
            "SOLUSDT": {"name": "SOL", "icon": "◎", "emoji": "🟣"},
            "DOGEUSDT": {"name": "DOGE", "icon": "🐕", "emoji": "🟡"},
            "XRPUSDT": {"name": "XRP", "icon": "◆", "emoji": "🔷"},
            "ADAUSDT": {"name": "ADA", "icon": "₳", "emoji": "🔵"}
        }
        
        symbol_info = symbol_names.get(symbol, {"name": symbol, "icon": "💰", "emoji": "⚪"})
        
        # 台北時間
        taipei_tz = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        # 格式化價格
        if price >= 1000:
            price_str = f"${price:,.2f}"
        elif price >= 1:
            price_str = f"${price:.2f}"
        else:
            price_str = f"${price:.4f}"
        
        # 構建買入訊號訊息
        message = f"""🚀 <b>{symbol_info['name']} BUY SIGNAL</b> 🚀

{symbol_info['emoji']} <b>{symbol_info['name']} ({symbol})</b>
💰 當前價格: <b>{price_str}</b>

📊 <b>價格變化</b>
• 1小時: <b>{change_1h:+.2f}%</b>
• 4小時: <b>{change_4h:+.2f}%</b>

📈 <b>趨勢分析</b>: {trend}

🟢 <b>綜合建議</b>: {combined_advice}

⏰ 訊號時間: {current_time} (台北時間)

"""

        # 如果有詳細分析數據，添加技術指標信息
        if analysis_data and "technical_indicators_summary" in analysis_data:
            tech_summary = analysis_data["technical_indicators_summary"]
            message += f"""

📊 <b>技術指標摘要</b>
• RSI: {tech_summary.get('RSI', 'N/A')}
• MACD: {tech_summary.get('MACD', 'N/A')}"""
            
            # 添加入場建議
            if "analysis_result" in analysis_data:
                result = analysis_data["analysis_result"]
                message += f"""

💡 <b>入場建議</b>
{result.get('入場時機', 'N/A')}

🎯 <b>目標價位</b>
{result.get('目標價位', 'N/A')}

🛡️ <b>止損設定</b>
{result.get('止損設定', 'N/A')}"""
        
        return self.send_message(message)
    
    def send_sell_signal(self, symbol, price, change_1h, change_4h, change_24h, trend, analysis_data=None):
        """
        發送賣出訊號
        """
        symbol_names = {
            "BTCUSDT": {"name": "BTC", "icon": "₿", "emoji": "🟠"},
            "ETHUSDT": {"name": "ETH", "icon": "Ξ", "emoji": "🔵"},
            "SOLUSDT": {"name": "SOL", "icon": "◎", "emoji": "🟣"},
            "DOGEUSDT": {"name": "DOGE", "icon": "🐕", "emoji": "🟡"},
            "XRPUSDT": {"name": "XRP", "icon": "◆", "emoji": "🔷"},
            "ADAUSDT": {"name": "ADA", "icon": "₳", "emoji": "🔵"}
        }
        
        symbol_info = symbol_names.get(symbol, {"name": symbol, "icon": "💰", "emoji": "⚪"})
        
        taipei_tz = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        if price >= 1000:
            price_str = f"${price:,.2f}"
        elif price >= 1:
            price_str = f"${price:.2f}"
        else:
            price_str = f"${price:.4f}"
        
        message = f"""🔴 <b>賣出訊號 SELL SIGNAL</b> 🔴

{symbol_info['emoji']} <b>{symbol_info['name']} ({symbol})</b>
💰 當前價格: <b>{price_str}</b>

📊 <b>價格變化</b>
• 1小時: <b>{change_1h:+.2f}%</b>
• 4小時: <b>{change_4h:+.2f}%</b>

📉 <b>趨勢分析</b>: {trend}

🔴 <b>建議操作</b>: 賣出 (SELL)
⚠️ <b>風險提醒</b>: 謹慎操作，注意市場變化

⏰ 訊號時間: {current_time} (台北時間)

"""

        return self.send_message(message)
    
    def send_market_summary(self, analysis_data):
        """
        發送市場總覽訊息
        
        Args:
            analysis_data (dict): 所有幣種的分析數據
        """
        taipei_tz = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"""📊 <b>虛擬幣市場總覽</b> 📊

⏰ 更新時間: {current_time} (台北時間)

"""
        
        buy_signals = []
        sell_signals = []
        neutral_signals = []
        
        for symbol, data in analysis_data.items():
            price = data['current_price']
            change_24h = data['24hr_change_percent']
            change_1h = data.get('1h_change_percent', 0)
            change_4h = data.get('4h_change_percent', 0)
            trend = data['current_trend']
            
            # 使用與 README 相同的多時間框架信號判斷邏輯
            trend_15m = "糾結"
            trend_1h = "糾結"
            
            # 獲取多時間框架趨勢
            if '15m' in data and 'trend_type' in data['15m']:
                trend_15m = data['15m']['trend_type']
            if '1h' in data and 'trend_type' in data['1h']:
                trend_1h = data['1h']['trend_type']
            else:
                trend_1h = data.get('trend_type', '糾結')
            
            # 綜合建議邏輯 - 與 README 完全相同
            if trend_15m == trend_1h and "糾結" not in trend_15m:
                if "多頭" in trend_15m:
                    signal = "🟢明確看多"
                    buy_signals.append(symbol)
                elif "空頭" in trend_15m:
                    signal = "🔴明確看空"
                    sell_signals.append(symbol)
                else:
                    signal = "📊雙重震盪"
                    neutral_signals.append(symbol)
            elif "糾結" in trend_15m and "糾結" in trend_1h:
                signal = "⚪雙重糾結"
                neutral_signals.append(symbol)
            else:
                # 時框分歧時的具體建議
                if ("多頭" in trend_15m and "糾結" in trend_1h) or ("糾結" in trend_15m and "多頭" in trend_1h):
                    signal = "🟡謹慎做多"
                    buy_signals.append(symbol)
                elif ("空頭" in trend_15m and "糾結" in trend_1h) or ("糾結" in trend_15m and "空頭" in trend_1h):
                    signal = "🟡謹慎做空"
                    sell_signals.append(symbol)
                else:
                    signal = "⚪觀望等待"
                    neutral_signals.append(symbol)
            
            # 格式化價格
            if price >= 1000:
                price_str = f"${price:,.2f}"
            elif price >= 1:
                price_str = f"${price:.2f}"
            else:
                price_str = f"${price:.4f}"
            
            symbol_names = {
                "BTCUSDT": "BTC",
                "ETHUSDT": "ETH", 
                "SOLUSDT": "SOL",
                "DOGEUSDT": "DOGE",
                "XRPUSDT": "XRP",
                "ADAUSDT": "ADA"
            }
            
            name = symbol_names.get(symbol, symbol)
            
            # 獲取趨勢顯示
            trend_15m_display = "🔄糾結"
            trend_1h_display = "🔄糾結"
            
            if '15m' in data and 'trend_type' in data['15m']:
                trend_type_15m = data['15m']['trend_type']
                if trend_type_15m == "多頭":
                    trend_15m_display = "📈多頭"
                elif trend_type_15m == "空頭":
                    trend_15m_display = "📉空頭"
                elif trend_type_15m == "震盪":
                    trend_15m_display = "📊震盪"
            
            if '1h' in data and 'trend_type' in data['1h']:
                trend_type_1h = data['1h']['trend_type']
                if trend_type_1h == "多頭":
                    trend_1h_display = "📈多頭"
                elif trend_type_1h == "空頭":
                    trend_1h_display = "📉空頭"
                elif trend_type_1h == "震盪":
                    trend_1h_display = "📊震盪"
            else:
                # 向後兼容
                trend_type = data.get('trend_type', '糾結')
                if trend_type == "多頭":
                    trend_1h_display = "📈多頭"
                elif trend_type == "空頭":
                    trend_1h_display = "📉空頭"
                elif trend_type == "震盪":
                    trend_1h_display = "📊震盪"
            
            # 格式化顯示 - 類似 README 表格格式
            message += f"<b>{name}</b> | {price_str} | 1H:{change_1h:+.2f}% 4H:{change_4h:+.2f}%\n"
            message += f"15M:{trend_15m_display} | 1H:{trend_1h_display} | {signal}\n\n"
        
        # 添加統計信息
        message += f"""
📈 <b>信號統計</b>
🟢 買入信號: {len(buy_signals)} 個
🔴 賣出信號: {len(sell_signals)} 個  
⚪ 觀望信號: {len(neutral_signals)} 個

"""
        
        return self.send_message(message)

def load_analysis_data():
    """
    載入分析數據
    """
    # 嘗試多個可能的路徑
    possible_paths = [
        "data/multi_investment_report.json",
        "../data/multi_investment_report.json",
        "../../data/multi_investment_report.json"
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            continue
    
    print("❌ 找不到分析數據文件，請先執行 analyze_binance_data.py")
    print("   嘗試的路徑:", possible_paths)
    return None

def check_and_send_signals(bot_token, chat_id, send_summary=True):
    """
    檢查並發送交易訊號
    
    Args:
        bot_token (str): Telegram Bot Token
        chat_id (str): Telegram Chat ID
        send_summary (bool): 是否發送市場總覽
    """
    # 載入分析數據
    analysis_data = load_analysis_data()
    if not analysis_data:
        return
    
    # 初始化 Telegram Bot
    bot = TelegramBot(bot_token, chat_id)
    
    # 發送市場總覽
    if send_summary:
        print("📊 發送市場總覽...")
        bot.send_market_summary(analysis_data)
    
    # 檢查每個幣種的信號
    for symbol, data in analysis_data.items():
        price = data['current_price']
        change_24h = data['24hr_change_percent']
        change_1h = data.get('1h_change_percent', 0)
        change_4h = data.get('4h_change_percent', 0)
        trend = data['current_trend']
        
        # 使用與 README 相同的多時間框架信號判斷邏輯
        trend_15m = "糾結"
        trend_1h = "糾結"
        
        # 獲取多時間框架趨勢
        if '15m' in data and 'trend_type' in data['15m']:
            trend_15m = data['15m']['trend_type']
        if '1h' in data and 'trend_type' in data['1h']:
            trend_1h = data['1h']['trend_type']
        else:
            # 向後兼容：如果沒有1h數據，使用根層級的趨勢數據
            trend_1h = data.get('trend_type', '糾結')
        
        # 綜合建議邏輯判斷是否發送信號
        should_send_buy = False
        should_send_sell = False
        
        # 調試信息：顯示實際的趨勢判斷
        print(f"📊 {symbol} 趨勢判斷: 15M={trend_15m}, 1H={trend_1h}")
        
        # 只有明確看多時才發送買入信號
        if trend_15m == trend_1h and "糾結" not in trend_15m:
            if "多頭" in trend_15m:
                should_send_buy = True  # 明確看多
                print(f"✅ {symbol} 符合明確看多條件")
            elif "空頭" in trend_15m:
                should_send_sell = True  # 明確看空
                print(f"✅ {symbol} 符合明確看空條件")
        else:
            print(f"❌ {symbol} 不符合明確看多/空條件")
        
        # 發送買入信號
        if should_send_buy:
            print(f"🟢 發送 {symbol} 買入訊號...")
            bot.send_buy_signal(
                symbol=symbol,
                price=price,
                change_1h=change_1h,
                change_4h=change_4h,
                change_24h=change_24h,
                trend=trend,
                analysis_data=data,
                combined_advice="明確看多"
            )
        
        # 發送賣出信號
        elif should_send_sell:
            print(f"🔴 發送 {symbol} 賣出訊號...")
            bot.send_sell_signal(
                symbol=symbol,
                price=price,
                change_1h=change_1h,
                change_4h=change_4h,
                change_24h=change_24h,
                trend=trend,
                analysis_data=data
            )

if __name__ == "__main__":
    # 從環境變數或配置文件讀取 Bot Token 和 Chat ID
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ 請設定環境變數:")
        print("   TELEGRAM_BOT_TOKEN=你的Bot Token")
        print("   TELEGRAM_CHAT_ID=你的Chat ID")
        print("\n或者直接在代碼中設定:")
        print('   BOT_TOKEN = "你的Bot Token"')
        print('   CHAT_ID = "你的Chat ID"')
        exit(1)
    
    print("🤖 開始檢查交易訊號...")
    check_and_send_signals(BOT_TOKEN, CHAT_ID)
    print("✅ 訊號檢查完成!")