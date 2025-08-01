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
        
        # 統計訊號
        buy_signals = []
        sell_signals = []
        neutral_signals = []
        
        for symbol in config.SUPPORTED_SYMBOLS:
            if symbol not in analysis_data:
                print(f"⚠️  {symbol} 數據不存在，跳過")
                continue
                
            data = analysis_data[symbol]
            change_24h = data['24hr_change_percent']
            trend = data['current_trend']
            
            # 判斷信號
            if change_24h > config.BUY_SIGNAL_THRESHOLD and "多頭" in trend:
                buy_signals.append((symbol, data))
            elif change_24h < config.SELL_SIGNAL_THRESHOLD and "空頭" in trend:
                sell_signals.append((symbol, data))
            else:
                neutral_signals.append((symbol, data))
        
        print(f"\n📊 訊號統計:")
        print(f"🟢 買入訊號: {len(buy_signals)} 個")
        print(f"🔴 賣出訊號: {len(sell_signals)} 個")
        print(f"⚪ 觀望訊號: {len(neutral_signals)} 個")
        
        # 發送市場總覽
        if config.SEND_MARKET_SUMMARY:
            print("\n📊 發送市場總覽...")
            bot.send_market_summary(analysis_data)
        
        # 發送買入訊號
        if config.SEND_BUY_SIGNALS and buy_signals:
            print(f"\n🟢 發送 {len(buy_signals)} 個買入訊號...")
            for symbol, data in buy_signals:
                print(f"  📤 {symbol} 買入訊號")
                bot.send_buy_signal(
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
        
        # 發送賣出訊號
        if config.SEND_SELL_SIGNALS and sell_signals:
            print(f"\n🔴 發送 {len(sell_signals)} 個賣出訊號...")
            for symbol, data in sell_signals:
                print(f"  📤 {symbol} 賣出訊號")
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