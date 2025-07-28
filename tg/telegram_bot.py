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
    
    def send_buy_signal(self, symbol, price, change_1h, change_4h, change_24h, trend, analysis_data=None):
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
        """
        # 幣種名稱和圖標映射
        symbol_names = {
            "BTCUSDT": {"name": "Bitcoin", "icon": "₿", "emoji": "🟠"},
            "ETHUSDT": {"name": "Ethereum", "icon": "Ξ", "emoji": "🔵"},
            "SOLUSDT": {"name": "Solana", "icon": "◎", "emoji": "🟣"},
            "DOGEUSDT": {"name": "Dogecoin", "icon": "🐕", "emoji": "🟡"},
            "XRPUSDT": {"name": "Ripple", "icon": "◆", "emoji": "🔷"},
            "ADAUSDT": {"name": "Cardano", "icon": "₳", "emoji": "🔵"}
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
        message = f"""🚀 <b>買入訊號 BUY SIGNAL</b> 🚀

{symbol_info['emoji']} <b>{symbol_info['name']} ({symbol})</b>
💰 當前價格: <b>{price_str}</b>

📊 <b>價格變化</b>
• 1小時: <b>{change_1h:+.2f}%</b>
• 4小時: <b>{change_4h:+.2f}%</b>
• 24小時: <b>{change_24h:+.2f}%</b>

📈 <b>趨勢分析</b>: {trend}

🟢 <b>建議操作</b>: 買入 (BUY)
⚠️ <b>風險提醒</b>: 請做好風險管理，設定止損

⏰ 訊號時間: {current_time} (台北時間)

#買入訊號 #{symbol} #虛擬幣投資"""

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
            "BTCUSDT": {"name": "Bitcoin", "icon": "₿", "emoji": "🟠"},
            "ETHUSDT": {"name": "Ethereum", "icon": "Ξ", "emoji": "🔵"},
            "SOLUSDT": {"name": "Solana", "icon": "◎", "emoji": "🟣"},
            "DOGEUSDT": {"name": "Dogecoin", "icon": "🐕", "emoji": "🟡"},
            "XRPUSDT": {"name": "Ripple", "icon": "◆", "emoji": "🔷"},
            "ADAUSDT": {"name": "Cardano", "icon": "₳", "emoji": "🔵"}
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
• 24小時: <b>{change_24h:+.2f}%</b>

📉 <b>趨勢分析</b>: {trend}

🔴 <b>建議操作</b>: 賣出 (SELL)
⚠️ <b>風險提醒</b>: 謹慎操作，注意市場變化

⏰ 訊號時間: {current_time} (台北時間)

#賣出訊號 #{symbol} #虛擬幣投資"""

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
            trend = data['current_trend']
            
            # 判斷信號
            if change_24h > 1 and "多頭" in trend:
                signal = "🟢買入"
                buy_signals.append(symbol)
            elif change_24h < -1 and "空頭" in trend:
                signal = "🔴賣出"
                sell_signals.append(symbol)
            else:
                signal = "⚪觀望"
                neutral_signals.append(symbol)
            
            # 格式化價格
            if price >= 1000:
                price_str = f"${price:,.2f}"
            elif price >= 1:
                price_str = f"${price:.2f}"
            else:
                price_str = f"${price:.4f}"
            
            symbol_names = {
                "BTCUSDT": "Bitcoin",
                "ETHUSDT": "Ethereum", 
                "SOLUSDT": "Solana",
                "DOGEUSDT": "Dogecoin",
                "XRPUSDT": "Ripple",
                "ADAUSDT": "Cardano"
            }
            
            name = symbol_names.get(symbol, symbol)
            message += f"• <b>{name}</b>: {price_str} ({change_24h:+.2f}%) {signal}\n"
        
        # 添加統計信息
        message += f"""
📈 <b>信號統計</b>
🟢 買入信號: {len(buy_signals)} 個
🔴 賣出信號: {len(sell_signals)} 個  
⚪ 觀望信號: {len(neutral_signals)} 個

#市場總覽 #虛擬幣投資 #技術分析"""
        
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
        
        # 判斷是否發送買入信號
        if change_24h > 1 and "多頭" in trend:
            print(f"🟢 發送 {symbol} 買入訊號...")
            bot.send_buy_signal(
                symbol=symbol,
                price=price,
                change_1h=change_1h,
                change_4h=change_4h,
                change_24h=change_24h,
                trend=trend,
                analysis_data=data
            )
        
        # 判斷是否發送賣出信號
        elif change_24h < -1 and "空頭" in trend:
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