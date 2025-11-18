import json
import boto3
from datetime import datetime
import pandas as pd
from get_binance_data import get_klines, get_ticker_24hr
from analyze_binance_data import calculate_technical_indicators, analyze_indicators

def lambda_handler(event, context):
    """
    AWS Lambda 函數處理器
    """
    try:
        # 執行 Binance 分析
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
        
        # 添加時間戳
        analysis["analysis_time"] = datetime.utcnow().isoformat()
        
        # 保存到 S3 (可選)
        s3_client = boto3.client('s3')
        bucket_name = 'your-binance-analysis-bucket'
        file_key = f"reports/{datetime.utcnow().strftime('%Y/%m/%d')}/investment_report_{datetime.utcnow().strftime('%H%M%S')}.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(analysis, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
        # 發送通知 (可選)
        sns_client = boto3.client('sns')
        topic_arn = 'arn:aws:sns:region:account:binance-analysis-alerts'
        
        message = f"""
Binance 分析報告已生成

當前價格: ${analysis['current_price']:,.2f}
24小時漲跌: {analysis['24hr_change_percent']:.3f}%
趨勢: {analysis['current_trend']}

報告位置: s3://{bucket_name}/{file_key}
        """
        
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=f"Binance {symbol} 分析報告"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '分析完成',
                'report_location': f's3://{bucket_name}/{file_key}',
                'analysis_summary': {
                    'price': analysis['current_price'],
                    'change': analysis['24hr_change_percent'],
                    'trend': analysis['current_trend']
                }
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"錯誤: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
