import functions_framework
import json
from datetime import datetime
import pandas as pd
from get_binance_data import get_klines, get_ticker_24hr
from analyze_binance_data import calculate_technical_indicators, analyze_indicators
from google.cloud import storage
from google.cloud import pubsub_v1

@functions_framework.http
def binance_analysis(request):
    """
    Google Cloud Function 入口點
    """
    try:
        # 執行分析
        symbol = "BTCUSDT"
        interval = "1h"
        
        print(f"開始分析 {symbol} {interval} 數據...")
        
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
        
        # 保存到 Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket('your-binance-analysis-bucket')
        blob_name = f"reports/{datetime.utcnow().strftime('%Y/%m/%d')}/investment_report_{datetime.utcnow().strftime('%H%M%S')}.json"
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(
            json.dumps(analysis, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        
        # 發布到 Pub/Sub (可選)
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path('your-project-id', 'binance-analysis')
        
        message_data = {
            'symbol': symbol,
            'price': analysis['current_price'],
            'change': analysis['24hr_change_percent'],
            'trend': analysis['current_trend'],
            'report_url': f'gs://your-binance-analysis-bucket/{blob_name}'
        }
        
        publisher.publish(topic_path, json.dumps(message_data).encode('utf-8'))
        
        return {
            'status': 'success',
            'message': '分析完成',
            'report_location': f'gs://your-binance-analysis-bucket/{blob_name}',
            'analysis_summary': {
                'price': analysis['current_price'],
                'change': analysis['24hr_change_percent'],
                'trend': analysis['current_trend']
            }
        }
        
    except Exception as e:
        print(f"錯誤: {str(e)}")
        return {'status': 'error', 'message': str(e)}, 500

@functions_framework.cloud_event
def scheduled_analysis(cloud_event):
    """
    Cloud Scheduler 觸發的函數
    """
    return binance_analysis(None)
