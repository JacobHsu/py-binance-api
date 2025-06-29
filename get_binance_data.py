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

def fetch_multiple_symbols(symbols, interval="1h"):
    """獲取多個交易對的數據"""
    all_data = {}

    for symbol in symbols:
        try:
            print(f"Fetching data for {symbol}...")

            # 獲取24小時行情數據
            ticker_data = get_ticker_24hr(symbol)

            # 獲取K線數據
            klines_df = get_klines(symbol, interval)

            # 保存數據到 data 目錄
            ticker_file = f"data/{symbol}_ticker_24hr.json"
            klines_file = f"data/{symbol}_klines_{interval}.csv"

            with open(ticker_file, 'w') as f:
                json.dump(ticker_data, f, indent=4)

            klines_df.to_csv(klines_file, index=False)

            all_data[symbol] = {
                'ticker': ticker_data,
                'klines': klines_df,
                'ticker_file': ticker_file,
                'klines_file': klines_file
            }

            print(f"✅ {symbol} data saved successfully")

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
            continue

    return all_data

if __name__ == "__main__":
    # 支援的交易對
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]
    interval = "1h"

    try:
        print("🚀 開始獲取多幣種數據...")
        all_data = fetch_multiple_symbols(symbols, interval)

        print(f"\n📊 成功獲取 {len(all_data)} 個交易對的數據:")
        for symbol in all_data.keys():
            print(f"  ✅ {symbol}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


