#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 主執行腳本 (根目錄)
Main execution script for Telegram Bot (from root directory)
"""

import sys
import os
import time

# 添加 tg 模組到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tg'))

# 直接導入模組
from telegram_config import config
from telegram_bot import TelegramBot, load_analysis_data

def main():
    """主函數"""
    print("🤖 虛擬幣 Telegram 訊號系統")
    print("=" * 40)
    
    # 檢查配置
    if not config.is_valid():
        missing = config.get_missing_config()
        print(f"❌ 配置不完整，缺少: {', '.join(missing)}")
        print("\n請設定 .env 文件:")
        print("1. cp tg/.env.example tg/.env")
        print("2. 編輯 tg/.env 填入 Bot Token 和 Chat ID")
        return 1
    
    print(f"✅ 配置檢查通過")
    print(f"📱 Bot Token: {config.BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {config.CHAT_ID}")
    print(f"📊 監控幣種: {', '.join(config.SUPPORTED_SYMBOLS)}")
    
    # 檢查分析數據是否存在
    analysis_data = load_analysis_data()
    if not analysis_data:
        print("❌ 找不到分析數據，請先執行數據分析:")
        print("python get_binance_data.py")
        print("python analyze_binance_data.py")
        return 1
    
    print(f"📈 找到 {len(analysis_data)} 個幣種的分析數據")
    
    # 執行訊號檢查和發送
    try:
        print("\n🔍 開始檢查交易訊號...")
        
        # 初始化 Bot
        bot = TelegramBot(config.BOT_TOKEN, config.CHAT_ID)
        
        # 先發送市場總覽，並從中獲取訊號判斷結果
        print("\n📊 分析市場訊號...")
        
        # 使用與 send_market_summary 相同的邏輯來判斷訊號
        buy_signals = []
        sell_signals = []
        neutral_signals = []
        market_signals = {}  # 儲存每個幣種的訊號結果
        
        for symbol, data in analysis_data.items():
            if symbol not in config.SUPPORTED_SYMBOLS:
                continue
                
            trend_15m = "糾結"
            trend_1h = "糾結"
            
            # 獲取多時間框架趨勢（與市場總覽邏輯完全相同）
            if '15m' in data and 'trend_type' in data['15m']:
                trend_15m = data['15m']['trend_type']
            if '1h' in data and 'trend_type' in data['1h']:
                trend_1h = data['1h']['trend_type']
            else:
                trend_1h = data.get('trend_type', '糾結')
            
            # 綜合建議邏輯（與 send_market_summary 完全相同）
            if trend_15m == trend_1h and "糾結" not in trend_15m:
                if "多頭" in trend_15m:
                    signal = "🟢明確看多"
                    buy_signals.append((symbol, data))
                    print(f"✅ {symbol} 明確看多 - 加入買入訊號")
                elif "空頭" in trend_15m:
                    signal = "🔴明確看空"
                    sell_signals.append((symbol, data))
                    print(f"✅ {symbol} 明確看空 - 加入賣出訊號")
                else:
                    signal = "📊雙重震盪"
                    neutral_signals.append((symbol, data))
                    print(f"❌ {symbol} 雙重震盪 - 不發送訊號")
            elif "糾結" in trend_15m and "糾結" in trend_1h:
                signal = "⚪雙重糾結"
                neutral_signals.append((symbol, data))
                print(f"❌ {symbol} 雙重糾結 - 不發送訊號")
            else:
                # 時框分歧時的具體建議
                if ("多頭" in trend_15m and "糾結" in trend_1h) or ("糾結" in trend_15m and "多頭" in trend_1h):
                    signal = "🟡謹慎做多"
                    print(f"❌ {symbol} 謹慎做多 - 僅在總覽顯示，不發送單幣種訊號")
                elif ("空頭" in trend_15m and "糾結" in trend_1h) or ("糾結" in trend_1h and "空頭" in trend_1h):
                    signal = "🟡謹慎做空"
                    print(f"❌ {symbol} 謹慎做空 - 僅在總覽顯示，不發送單幣種訊號")
                else:
                    signal = "⚪觀望等待"
                    print(f"❌ {symbol} 觀望等待 - 不發送訊號")
                neutral_signals.append((symbol, data))
            
            market_signals[symbol] = signal
        
        print(f"\n📊 訊號統計:")
        print(f"🟢 買入訊號: {len(buy_signals)} 個")
        print(f"🔴 賣出訊號: {len(sell_signals)} 個")
        print(f"⚪ 觀望訊號: {len(neutral_signals)} 個")
        
        # 只有在有買入訊號時才發送市場總覽
        if config.SEND_MARKET_SUMMARY and buy_signals:
            print("\n📊 發送市場總覽...")
            bot.send_market_summary(analysis_data)
        
        # 發送買入訊號
        if config.SEND_BUY_SIGNALS and buy_signals:
            print(f"\n🟢 發送 {len(buy_signals)} 個買入訊號...")
            for symbol, data in buy_signals:
                print(f"  📤 {symbol} 買入訊號")
                
                # 從市場訊號判斷結果獲取正確的 combined_advice
                signal = market_signals.get(symbol, "明確看多")
                combined_advice = signal.replace("🟢", "").strip()  # 移除emoji，只保留文字
                
                bot.send_buy_signal(
                    symbol=symbol,
                    price=data['current_price'],
                    change_1h=data.get('1h_change_percent', 0),
                    change_4h=data.get('4h_change_percent', 0),
                    change_24h=data['24hr_change_percent'],
                    trend=data['current_trend'],
                    analysis_data=data,
                    combined_advice=combined_advice
                )
                # 添加發送間隔
                if config.MESSAGE_INTERVAL > 0:
                    time.sleep(config.MESSAGE_INTERVAL)
        
        # 發送賣出訊號
        if config.SEND_SELL_SIGNALS and sell_signals:
            print(f"\n🔴 發送 {len(sell_signals)} 個賣出訊號...")
            for symbol, data in sell_signals:
                print(f"  📤 {symbol} 賣出訊號")
                
                # 從市場訊號判斷結果獲取正確的訊號狀態（用於調試）
                signal = market_signals.get(symbol, "明確看空")
                print(f"    💡 {symbol} 訊號狀態: {signal}")
                
                bot.send_sell_signal(
                    symbol=symbol,
                    price=data['current_price'],
                    change_1h=data.get('1h_change_percent', 0),
                    change_4h=data.get('4h_change_percent', 0),
                    change_24h=data['24hr_change_percent'],
                    trend=data['current_trend'],
                    analysis_data=data
                )
                # 添加發送間隔
                if config.MESSAGE_INTERVAL > 0:
                    time.sleep(config.MESSAGE_INTERVAL)
        
        print("\n✅ 所有訊號發送完成！")
        return 0
        
    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)