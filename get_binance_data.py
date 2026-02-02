import requests
import pandas as pd
import json

BASE_URL = "https://data-api.binance.vision/api/v3"

def get_klines(symbol, interval, limit=500):
    endpoint = f"{BASE_URL}/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    klines = response.json()
    df = pd.DataFrame(klines, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df = df.astype({
        'open': float, 'high': float, 'low': float, 'close': float, 'volume': float,
        'quote_asset_volume': float, 'number_of_trades': int,
        'taker_buy_base_asset_volume': float, 'taker_buy_quote_asset_volume': float
    })
    return df

def get_ticker_24hr(symbol):
    endpoint = f"{BASE_URL}/ticker/24hr"
    params = {
        "symbol": symbol
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    ticker = response.json()
    return ticker

def fetch_multiple_symbols(symbols, intervals=["1h", "15m"]):
    """獲取多個交易對的多時間框架數據"""
    all_data = {}

    for symbol in symbols:
        try:
            print(f"Fetching data for {symbol}...")

            # 獲取24小時行情數據
            ticker_data = get_ticker_24hr(symbol)

            symbol_data = {
                'ticker': ticker_data,
                'ticker_file': f"data/{symbol}_ticker_24hr.json"
            }

            # 保存ticker數據
            with open(symbol_data['ticker_file'], 'w') as f:
                json.dump(ticker_data, f, indent=4)

            # 獲取多時間框架K線數據
            for interval in intervals:
                print(f"  Fetching {interval} data for {symbol}...")
                klines_df = get_klines(symbol, interval, limit=500 if interval == "1h" else 100)
                
                klines_file = f"data/{symbol}_klines_{interval}.csv"
                klines_df.to_csv(klines_file, index=False)
                
                symbol_data[f'klines_{interval}'] = klines_df
                symbol_data[f'klines_file_{interval}'] = klines_file

            all_data[symbol] = symbol_data
            print(f"✅ {symbol} multi-timeframe data saved successfully")

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
            continue

    return all_data

if __name__ == "__main__":
    # 支援的交易對
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
    intervals = ["1h", "15m"]  # 支援多時間框架

    try:
        print("🚀 開始獲取多幣種多時間框架數據...")
        all_data = fetch_multiple_symbols(symbols, intervals)

        print(f"\n📊 成功獲取 {len(all_data)} 個交易對的多時間框架數據:")
        for symbol in all_data.keys():
            print(f"  ✅ {symbol}: 1h + 15m")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


