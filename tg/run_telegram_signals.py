#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
執行 Telegram 訊號發送的主腳本
Main script to run Telegram signal sending
"""

import sys
import os
import time

try:
    from .telegram_config import config
    from .telegram_bot import TelegramBot, load_analysis_data
except ImportError:
    # 如果從 tg 目錄內執行
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
            
            # 判斷信號 - 使用與 README 相同的綜合建議邏輯
            trend_15m = "糾結"
            trend_1h = "糾結"
            signal_15m = "⚪觀望"
            signal_1h = "⚪觀望"
            
            # 獲取多時間框架趨勢和信號
            if '15m' in data and 'trend_type' in data['15m']:
                trend_type_15m = data['15m']['trend_type']
                trend_15m = trend_type_15m
                if trend_type_15m == "多頭":
                    signal_15m = "🟢買入" if not data['15m'].get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
                elif trend_type_15m == "空頭":
                    signal_15m = "🔴賣出" if not data['15m'].get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
            
            if '1h' in data and 'trend_type' in data['1h']:
                trend_type_1h = data['1h']['trend_type']
                trend_1h = trend_type_1h
                if trend_type_1h == "多頭":
                    signal_1h = "🟢買入" if not data['1h'].get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
                elif trend_type_1h == "空頭":
                    signal_1h = "🔴賣出" if not data['1h'].get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
            else:
                # 向後兼容：使用根層級的趨勢數據
                trend_type = data.get('trend_type', '糾結')
                trend_1h = trend_type
                if trend_type == "多頭":
                    signal_1h = "🟢買入" if not data.get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
                elif trend_type == "空頭":
                    signal_1h = "🔴賣出" if not data.get('ma_analysis', {}).get('is_tangled', True) else "⚪觀望"
            
            # 綜合建議 - 與 README 完全相同的邏輯
            combined_advice = ""
            if trend_15m == trend_1h and "糾結" not in trend_15m:
                if "多頭" in trend_15m:
                    combined_advice = "🟢明確看多"
                    buy_signals.append((symbol, data))
                elif "空頭" in trend_15m:
                    combined_advice = "🔴明確看空"
                    sell_signals.append((symbol, data))
                else:
                    combined_advice = "📊雙重震盪"
                    neutral_signals.append((symbol, data))
            elif "糾結" in trend_15m and "糾結" in trend_1h:
                combined_advice = "⚪雙重糾結"
                neutral_signals.append((symbol, data))
            else:
                # 時框分歧時給出具體操作建議
                if "多頭" in trend_15m and "糾結" in trend_1h:
                    combined_advice = "🟡謹慎做多"
                    buy_signals.append((symbol, data))
                elif "糾結" in trend_15m and "多頭" in trend_1h:
                    combined_advice = "🟡謹慎做多"
                    buy_signals.append((symbol, data))
                elif "空頭" in trend_15m and "糾結" in trend_1h:
                    combined_advice = "🟡謹慎做空"
                    sell_signals.append((symbol, data))
                elif "糾結" in trend_15m and "空頭" in trend_1h:
                    combined_advice = "🟡謹慎做空"
                    sell_signals.append((symbol, data))
                elif "多頭" in trend_15m and "空頭" in trend_1h:
                    combined_advice = "⚪觀望等待"
                    neutral_signals.append((symbol, data))
                elif "空頭" in trend_15m and "多頭" in trend_1h:
                    combined_advice = "⚪觀望等待"
                    neutral_signals.append((symbol, data))
                else:
                    combined_advice = "⚪觀望等待"
                    neutral_signals.append((symbol, data))
            
            # 儲存綜合建議到數據中，供後續使用
            data['combined_advice'] = combined_advice
            data['signal_15m'] = signal_15m
            data['signal_1h'] = signal_1h
        
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
                # 從數據中獲取正確的綜合建議
                combined_advice = data.get('combined_advice', '明確看多').replace('🟢', '').replace('🟡', '').strip()
                
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