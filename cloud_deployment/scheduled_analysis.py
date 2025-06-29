#!/usr/bin/env python3
"""
Heroku Scheduler 執行腳本
"""
import os
import json
import requests
from datetime import datetime
import pandas as pd
from get_binance_data import get_klines, get_ticker_24hr
from analyze_binance_data import calculate_technical_indicators, analyze_indicators

def send_webhook_notification(analysis_data):
    """
    發送 Webhook 通知 (例如 Discord, Slack, Telegram)
    """
    webhook_url = os.environ.get('WEBHOOK_URL')
    if not webhook_url:
        return
    
    message = f"""
🚀 **Binance 分析報告**

💰 **當前價格**: ${analysis_data['current_price']:,.2f}
📈 **24小時變化**: {analysis_data['24hr_change_percent']:.3f}%
📊 **趨勢**: {analysis_data['current_trend']}

🔍 **技術指標摘要**:
• 均線系統: {analysis_data['technical_indicators_summary']['均線系統'][:50]}...
• MACD: {analysis_data['technical_indicators_summary']['MACD'][:50]}...
• RSI: {analysis_data['technical_indicators_summary']['RSI'][:50]}...

⏰ 分析時間: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
    """
    
    # Discord Webhook 格式
    payload = {
        "content": message,
        "embeds": [{
            "title": "BTCUSDT 技術分析",
            "color": 0x00ff00 if analysis_data['24hr_change_percent'] > 0 else 0xff0000,
            "fields": [
                {
                    "name": "交易建議",
                    "value": analysis_data['analysis_result']['方向'],
                    "inline": False
                },
                {
                    "name": "入場時機",
                    "value": analysis_data['analysis_result']['入場時機'][:100] + "...",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("通知發送成功")
    except Exception as e:
        print(f"通知發送失敗: {e}")

def main():
    """
    主執行函數
    """
    try:
        print("開始執行 Binance 分析...")
        
        # 執行分析
        symbol = "BTCUSDT"
        interval = "1h"
        
        # 獲取數據
        ticker_data = get_ticker_24hr(symbol)
        klines_data = get_klines(symbol, interval)
        
        # 數據預處理
        klines_data["close"] = pd.to_numeric(klines_data["close"])
        klines_data["high"] = pd.to_numeric(klines_data["high"])
        klines_data["low"] = pd.to_numeric(klines_data["low"])
        
        # 計算技術指標
        klines_with_indicators = calculate_technical_indicators(klines_data.copy())
        
        # 執行分析
        analysis = analyze_indicators(ticker_data, klines_with_indicators)
        analysis["analysis_time"] = datetime.utcnow().isoformat()
        
        # 保存結果
        with open("investment_report.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=4, ensure_ascii=False)
        
        # 發送通知
        send_webhook_notification(analysis)
        
        print("分析完成！")
        print(f"當前價格: ${analysis['current_price']:,.2f}")
        print(f"24小時變化: {analysis['24hr_change_percent']:.3f}%")
        print(f"趨勢: {analysis['current_trend']}")
        
    except Exception as e:
        print(f"執行錯誤: {e}")
        # 發送錯誤通知
        webhook_url = os.environ.get('WEBHOOK_URL')
        if webhook_url:
            error_payload = {
                "content": f"❌ **Binance 分析執行失敗**\n\n錯誤信息: {str(e)}\n時間: {datetime.utcnow().isoformat()}"
            }
            requests.post(webhook_url, json=error_payload)

if __name__ == "__main__":
    main()
