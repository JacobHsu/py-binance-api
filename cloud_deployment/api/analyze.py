from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from get_binance_data import get_klines, get_ticker_24hr
from analyze_binance_data import calculate_technical_indicators, analyze_indicators
import pandas as pd

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 執行分析
            symbol = "BTCUSDT"
            interval = "1h"
            
            # 獲取數據
            ticker_data = get_ticker_24hr(symbol)
            klines_data = get_klines(symbol, interval)
            
            # 確保數據類型正確
            klines_data["close"] = pd.to_numeric(klines_data["close"])
            klines_data["high"] = pd.to_numeric(klines_data["high"])
            klines_data["low"] = pd.to_numeric(klines_data["low"])
            
            # 計算技術指標
            klines_with_indicators = calculate_technical_indicators(klines_data.copy())
            
            # 執行分析
            analysis = analyze_indicators(ticker_data, klines_with_indicators)
            
            # 返回結果
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(analysis, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
