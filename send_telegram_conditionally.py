#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
條件式 Telegram 訊號發送腳本
只在有買入訊號時才發送 Telegram 訊息
"""

import sys
import os
import json

# 添加 tg 模組到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tg'))

from telegram_config import config
from telegram_bot import TelegramBot, load_analysis_data

def check_for_buy_signals(analysis_data):
    """檢查是否有買入訊號"""
    buy_signals = []
    
    for symbol in config.SUPPORTED_SYMBOLS:
        if symbol not in analysis_data:
            continue
            
        data = analysis_data[symbol]
        change_24h = data['24hr_change_percent']
        trend = data['current_trend']
        
        # 判斷是否為買入信號 - 改用綜合建議邏輯
        trend_15m = "糾結"
        trend_1h = "糾結"
        
        # 獲取多時間框架趨勢
        if '15m' in data and 'trend_type' in data['15m']:
            trend_15m = data['15m']['trend_type']
        if '1h' in data and 'trend_type' in data['1h']:
            trend_1h = data['1h']['trend_type']
        else:
            trend_1h = data.get('trend_type', '糾結')
        
        # 判斷是否為買入信號
        is_buy_signal = False
        if trend_15m == trend_1h and trend_15m == "多頭":
            is_buy_signal = True  # 雙重看多
        elif (trend_15m == "多頭" and trend_1h == "糾結") or (trend_15m == "糾結" and trend_1h == "多頭"):
            is_buy_signal = True  # 謹慎做多
        
        if is_buy_signal:
            buy_signals.append((symbol, data))
    
    return buy_signals

def main():
    """主函數"""
    print("🔍 檢查是否有買入訊號需要發送...")
    
    # 檢查配置
    if not config.is_valid():
        print("⚠️  Telegram 配置無效，跳過發送")
        print("如需啟用 Telegram 功能，請設定以下 GitHub Secrets:")
        print("- TELEGRAM_BOT_TOKEN")
        print("- TELEGRAM_CHAT_ID")
        return 0
    
    # 載入分析數據
    analysis_data = load_analysis_data()
    if not analysis_data:
        print("❌ 找不到分析數據，跳過 Telegram 發送")
        return 0
    
    # 檢查買入訊號
    buy_signals = check_for_buy_signals(analysis_data)
    
    if not buy_signals:
        print("📊 當前沒有買入訊號，不發送 Telegram 訊息")
        return 0
    
    print(f"🟢 發現 {len(buy_signals)} 個買入訊號，開始發送 Telegram 訊息...")
    
    try:
        # 初始化 Bot
        bot = TelegramBot(config.BOT_TOKEN, config.CHAT_ID)
        
        # 發送市場總覽 (只有在有買入訊號時才發送)
        if config.SEND_MARKET_SUMMARY:
            print("📊 發送市場總覽...")
            bot.send_market_summary(analysis_data)
        
        # 只發送買入訊號
        if config.SEND_BUY_SIGNALS:
            print(f"🟢 發送 {len(buy_signals)} 個買入訊號...")
            for symbol, data in buy_signals:
                print(f"  📤 發送 {symbol} 買入訊號")
                bot.send_buy_signal(
                    symbol=symbol,
                    price=data['current_price'],
                    change_1h=data.get('1h_change_percent', 0),
                    change_4h=data.get('4h_change_percent', 0),
                    change_24h=data['24hr_change_percent'],
                    trend=data['current_trend'],
                    analysis_data=data
                )
        
        print("✅ Telegram 訊號發送完成！")
        return 0
        
    except Exception as e:
        print(f"❌ Telegram 發送失敗: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)