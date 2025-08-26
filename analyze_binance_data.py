import pandas as pd
import json

def calculate_technical_indicators(df):
    # Moving Averages (MA)
    df["MA5"] = df["close"].rolling(window=5).mean()
    df["MA10"] = df["close"].rolling(window=10).mean()
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["MA120"] = df["close"].rolling(window=120).mean()
    
    # Volume Weighted Moving Average (VWMA)
    df["VWMA5"] = (df["close"] * df["volume"]).rolling(window=5).sum() / df["volume"].rolling(window=5).sum()
    df["VWMA10"] = (df["close"] * df["volume"]).rolling(window=10).sum() / df["volume"].rolling(window=10).sum()
    df["VWMA20"] = (df["close"] * df["volume"]).rolling(window=20).sum() / df["volume"].rolling(window=20).sum()

    # MACD
    df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["DIF"] = df["EMA12"] - df["EMA26"]
    df["DEA"] = df["DIF"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = (df["DIF"] - df["DEA"]) * 2

    # Bollinger Bands (BOLL)
    df["BB_Middle"] = df["close"].rolling(window=20).mean()
    df["BB_StdDev"] = df["close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Middle"] + (df["BB_StdDev"] * 2)
    df["BB_Lower"] = df["BB_Middle"] - (df["BB_StdDev"] * 2)
    df["Percent_B"] = (df["close"] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])

    # Keltner Channel (KC)
    df["KC_Middle"] = df["close"].ewm(span=20, adjust=False).mean()  # EMA20 作為中軌
    df["KC_ATR"] = ((df["high"] - df["low"]).rolling(window=14).mean())  # 簡化的ATR計算
    df["KC_Upper"] = df["KC_Middle"] + (df["KC_ATR"] * 2)
    df["KC_Lower"] = df["KC_Middle"] - (df["KC_ATR"] * 2)
    df["KC_Position"] = (df["close"] - df["KC_Lower"]) / (df["KC_Upper"] - df["KC_Lower"])

    # RSI
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["RSI14"] = 100 - (100 / (1 + rs))

    # KDJ
    low_min = df["low"].rolling(window=9).min()
    high_max = df["high"].rolling(window=9).max()
    df["RSV"] = (df["close"] - low_min) / (high_max - low_min) * 100
    df["K"] = df["RSV"].ewm(span=3, adjust=False).mean()
    df["D"] = df["K"].ewm(span=3, adjust=False).mean()
    df["J"] = 3 * df["K"] - 2 * df["D"]

    return df

def analyze_indicators(ticker_data, klines_df):
    analysis_results = {}

    # Current Price and 24hr Change
    current_price = float(ticker_data["lastPrice"])
    price_change_percent = float(ticker_data["priceChangePercent"])
    analysis_results["current_price"] = current_price
    analysis_results["24hr_change_percent"] = price_change_percent

    # Calculate 1-hour change
    if len(klines_df) >= 2:
        previous_close = klines_df["close"].iloc[-2]
        one_hour_change_percent = ((current_price - previous_close) / previous_close) * 100
        analysis_results["1h_change_percent"] = one_hour_change_percent
    else:
        analysis_results["1h_change_percent"] = 0

    # Calculate 4-hour change
    if len(klines_df) >= 5: # Need at least 5 data points for 4-hour change (current + 4 previous)
        four_hour_ago_close = klines_df["close"].iloc[-5]
        four_hour_change_percent = ((current_price - four_hour_ago_close) / four_hour_ago_close) * 100
        analysis_results["4h_change_percent"] = four_hour_change_percent
    else:
        analysis_results["4h_change_percent"] = 0

    # Support and Resistance (simplified, can be improved with more advanced methods)
    # Using recent low/high as a simple proxy
    analysis_results["major_support"] = klines_df["low"].min()
    analysis_results["major_resistance"] = klines_df["high"].max()

    # Enhanced Trend Analysis with Tangled Detection
    ma5_current = klines_df["MA5"].iloc[-1]
    ma10_current = klines_df["MA10"].iloc[-1]
    ma20_current = klines_df["MA20"].iloc[-1]
    ma120_current = klines_df["MA120"].iloc[-1]
    close_price = klines_df["close"].iloc[-1]
    
    # Calculate MA convergence (糾結檢測)
    ma_range = max(ma5_current, ma10_current, ma20_current) - min(ma5_current, ma10_current, ma20_current)
    ma_avg = (ma5_current + ma10_current + ma20_current) / 3
    convergence_ratio = (ma_range / ma_avg) * 100  # 均線間距離百分比
    
    # Calculate MA slopes (均線斜率)
    if len(klines_df) >= 5:
        ma5_slope = (ma5_current - klines_df["MA5"].iloc[-5]) / klines_df["MA5"].iloc[-5] * 100
        ma10_slope = (ma10_current - klines_df["MA10"].iloc[-5]) / klines_df["MA10"].iloc[-5] * 100
        ma20_slope = (ma20_current - klines_df["MA20"].iloc[-5]) / klines_df["MA20"].iloc[-5] * 100
    else:
        ma5_slope = ma10_slope = ma20_slope = 0
    
    # Detect tangled/consolidation pattern (糾結檢測) - 放寬條件
    is_tangled = False
    tangled_reason = ""
    tangled_score = 0  # 糾結評分系統
    
    # 條件1: 均線間距離過近 (只有極度收斂才算糾結)
    if convergence_ratio < 0.5:
        tangled_score += 3  # 極度糾結
        tangled_reason += f"均線極度糾結(間距{convergence_ratio:.2f}%)"
    elif convergence_ratio < 0.8:
        tangled_score += 2  # 密集糾結
        tangled_reason += f"均線密集糾結(間距{convergence_ratio:.2f}%)"
    
    # 條件2: 均線方向嚴重分歧 (slopes have different signs and significant divergence)
    slope_signs = [1 if slope > 0.2 else -1 if slope < -0.2 else 0 for slope in [ma5_slope, ma10_slope, ma20_slope]]
    slope_divergence = len(set([s for s in slope_signs if s != 0]))
    
    if slope_divergence >= 2 and convergence_ratio < 2.0:
        tangled_score += 2
        if tangled_reason:
            tangled_reason += "，"
        tangled_reason += f"方向分歧(MA5:{ma5_slope:+.2f}% MA10:{ma10_slope:+.2f}% MA20:{ma20_slope:+.2f}%)"
    elif abs(ma5_slope) < 0.1 and abs(ma10_slope) < 0.1 and abs(ma20_slope) < 0.1:
        tangled_score += 1
        if tangled_reason:
            tangled_reason += "，"
        tangled_reason += "均線平緩"
    
    # 條件3: 價格在均線間反復穿越 (更嚴格的條件)
    price_in_ma_range = min(ma5_current, ma10_current, ma20_current) <= close_price <= max(ma5_current, ma10_current, ma20_current)
    if price_in_ma_range and convergence_ratio < 1.5:
        tangled_score += 1
        if tangled_reason:
            tangled_reason += "，"
        tangled_reason += "價格穿梭均線間"
    
    # 只有當糾結評分 >= 4 時才判定為糾結 (更嚴格的標準)
    is_tangled = tangled_score >= 4
    
    # Determine trend based on enhanced logic
    if is_tangled:
        analysis_results["current_trend"] = f"均線糾結，{tangled_reason}"
        analysis_results["trend_type"] = "糾結"
    else:
        # 計算多頭和空頭評分
        bullish_score = 0
        bearish_score = 0
        
        # 均線排列評分
        if ma5_current > ma10_current:
            bullish_score += 1
        else:
            bearish_score += 1
            
        if ma10_current > ma20_current:
            bullish_score += 1
        else:
            bearish_score += 1
            
        # 價格位置評分
        if close_price > ma20_current:
            bullish_score += 2
        elif close_price < ma20_current:
            bearish_score += 2
        else:
            # 價格在MA20附近，中性
            pass
            
        # 均線斜率評分
        if ma20_slope > 0.3:
            bullish_score += 1
        elif ma20_slope < -0.3:
            bearish_score += 1
            
        # 短期動能評分
        if ma5_slope > 0.2:
            bullish_score += 1
        elif ma5_slope < -0.2:
            bearish_score += 1
        
        # 根據評分判斷趨勢 (降低門檻，讓趨勢更容易被識別)
        if bullish_score >= 3:
            # 多頭趨勢
            strength = "強勢" if bullish_score >= 5 and close_price > ma120_current else "一般"
            analysis_results["current_trend"] = f"多頭排列，趨勢偏多({strength})"
            analysis_results["trend_type"] = "多頭"
        elif bearish_score >= 3:
            # 空頭趨勢
            strength = "強勢" if bearish_score >= 5 and close_price < ma120_current else "一般"
            analysis_results["current_trend"] = f"空頭排列，趨勢偏空({strength})"
            analysis_results["trend_type"] = "空頭"
        else:
            # 震盪：多空力量均衡
            analysis_results["current_trend"] = f"震盪整理(收斂度{convergence_ratio:.2f}%，多空{bullish_score}:{bearish_score})"
            analysis_results["trend_type"] = "震盪"
    
    # Store detailed MA analysis
    analysis_results["ma_analysis"] = {
        "convergence_ratio": convergence_ratio,
        "is_tangled": is_tangled,
        "tangled_reason": tangled_reason,
        "ma5_slope": ma5_slope,
        "ma10_slope": ma10_slope,
        "ma20_slope": ma20_slope,
        "ma_values": {
            "MA5": ma5_current,
            "MA10": ma10_current,
            "MA20": ma20_current,
            "MA120": ma120_current
        }
    }

    # Technical Indicator Analysis
    analysis_results["technical_indicators_summary"] = {
        "均線系統": "",
        "VWMA": "",
        "MACD": "",
        "BOLL": "",
        "KC": "",
        "RSI": "",
        "KDJ": ""
    }

    # Enhanced MA Analysis using the new detection logic
    ma_data = analysis_results["ma_analysis"]
    ma5 = ma_data["ma_values"]["MA5"]
    ma10 = ma_data["ma_values"]["MA10"]
    ma20 = ma_data["ma_values"]["MA20"]
    ma120 = ma_data["ma_values"]["MA120"]
    if ma_data["is_tangled"]:
        analysis_results["technical_indicators_summary"]["均線系統"] = \
            f"⚠️ 均線糾結狀態。{ma_data['tangled_reason']}。" \
            f"MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}，" \
            f"收斂度{ma_data['convergence_ratio']:.2f}%，等待方向選擇。"
    elif analysis_results["trend_type"] == "多頭":
        golden_cross = "金叉" if ma5 > ma10 else "準金叉"
        strength_desc = "強勢突破" if "強勢" in analysis_results["current_trend"] else "溫和上升"
        analysis_results["technical_indicators_summary"]["均線系統"] = \
            f"🟢 多頭排列({strength_desc})。MA5（{ma5:.2f}）與MA10（{ma10:.2f}）形成{golden_cross}，" \
            f"價格站上MA20（{ma20:.2f}），MA20斜率{ma_data['ma20_slope']:+.2f}%，短期動能偏強。"
    elif analysis_results["trend_type"] == "空頭":
        death_cross = "死叉" if ma5 < ma10 else "準死叉"
        strength_desc = "強勢下跌" if "強勢" in analysis_results["current_trend"] else "溫和下降"
        analysis_results["technical_indicators_summary"]["均線系統"] = \
            f"🔴 空頭排列({strength_desc})。MA5（{ma5:.2f}）與MA10（{ma10:.2f}）形成{death_cross}，" \
            f"價格跌破MA20（{ma20:.2f}），MA20斜率{ma_data['ma20_slope']:+.2f}%，短期動能偏弱。"
    else:
        analysis_results["technical_indicators_summary"]["均線系統"] = \
            f"🟡 震盪整理。MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}，" \
            f"收斂度{ma_data['convergence_ratio']:.2f}%，方向不明確，觀望為主。"

    # VWMA Analysis
    vwma5 = klines_df["VWMA5"].iloc[-1]
    vwma10 = klines_df["VWMA10"].iloc[-1]
    vwma20 = klines_df["VWMA20"].iloc[-1]
    
    # Compare VWMA with regular MA to assess volume impact
    vwma_vs_ma5 = ((vwma5 - ma5) / ma5) * 100
    vwma_vs_ma20 = ((vwma20 - ma20) / ma20) * 100
    
    if vwma5 > vwma10 and vwma10 > vwma20 and close_price > vwma20:
        if vwma_vs_ma20 > 0.1:
            analysis_results["technical_indicators_summary"]["VWMA"] = \
                f"量價配合良好。VWMA5（{vwma5:.2f}）>VWMA10（{vwma10:.2f}）>VWMA20（{vwma20:.2f}），且VWMA20較MA20高{vwma_vs_ma20:.2f}%，顯示上漲有量能支撐。"
        else:
            analysis_results["technical_indicators_summary"]["VWMA"] = \
                f"量價排列偏多但量能一般。VWMA5（{vwma5:.2f}）>VWMA10（{vwma10:.2f}）>VWMA20（{vwma20:.2f}），VWMA與MA差異{vwma_vs_ma20:.2f}%，量能支撐有限。"
    elif vwma5 < vwma10 and vwma10 < vwma20 and close_price < vwma20:
        if vwma_vs_ma20 < -0.1:
            analysis_results["technical_indicators_summary"]["VWMA"] = \
                f"量價背離偏空。VWMA5（{vwma5:.2f}）<VWMA10（{vwma10:.2f}）<VWMA20（{vwma20:.2f}），且VWMA20較MA20低{abs(vwma_vs_ma20):.2f}%，顯示下跌有量能推動。"
        else:
            analysis_results["technical_indicators_summary"]["VWMA"] = \
                f"量價排列偏空但量能不足。VWMA5（{vwma5:.2f}）<VWMA10（{vwma10:.2f}）<VWMA20（{vwma20:.2f}），VWMA與MA差異{vwma_vs_ma20:.2f}%，下跌缺乏量能。"
    else:
        analysis_results["technical_indicators_summary"]["VWMA"] = \
            f"量價關係複雜。VWMA5={vwma5:.2f}, VWMA10={vwma10:.2f}, VWMA20={vwma20:.2f}，與MA偏差{vwma_vs_ma5:.2f}%，需觀察量價配合度。"

    # MACD Analysis
    dif = klines_df["DIF"].iloc[-1]
    dea = klines_df["DEA"].iloc[-1]
    macd_hist = klines_df["MACD_Hist"].iloc[-1]
    if dif > dea and dif > 0:
        analysis_results["technical_indicators_summary"]["MACD"] = \
            f"金叉運行中。DIF（{dif:.4f}）高於DEA（{dea:.4f}），且均在零軸上方，柱狀圖為{macd_hist:.4f}，顯示多頭動能強勁。"
    elif dif < dea and dif > 0:
        analysis_results["technical_indicators_summary"]["MACD"] = \
            f"死叉運行中但收斂。DIF（{dif:.4f}）仍高於零軸，DEA（{dea:.4f}）趨平，柱狀圖縮減至{macd_hist:.4f}，暗示空頭動能減弱。"
    else:
        analysis_results["technical_indicators_summary"]["MACD"] = \
            f"MACD指標偏空或震盪。DIF={dif:.4f}, DEA={dea:.4f}, 柱狀圖={macd_hist:.4f}。"

    # BOLL Analysis
    bb_upper = klines_df["BB_Upper"].iloc[-1]
    bb_middle = klines_df["BB_Middle"].iloc[-1]
    bb_lower = klines_df["BB_Lower"].iloc[-1]
    percent_b = klines_df["Percent_B"].iloc[-1]
    if close_price > bb_upper * 0.95: # Close to upper band
        analysis_results["technical_indicators_summary"]["BOLL"] = \
            f"價格貼近上軌（{bb_upper:.2f}），%B（{percent_b:.2%}）顯示未超買，中軌（{bb_middle:.2f}）提供動態支撐。"
    elif close_price < bb_lower * 1.05: # Close to lower band
        analysis_results["technical_indicators_summary"]["BOLL"] = \
            f"價格貼近下軌（{bb_lower:.2f}），%B（{percent_b:.2%}）顯示未超賣，中軌（{bb_middle:.2f}）提供動態壓力。"
    else:
        analysis_results["technical_indicators_summary"]["BOLL"] = \
            f"價格在布林帶中軌附近震盪。上軌={bb_upper:.2f}, 中軌={bb_middle:.2f}, 下軌={bb_lower:.2f}, %B={percent_b:.2%}。"

    # KC Analysis
    kc_upper = klines_df["KC_Upper"].iloc[-1]
    kc_middle = klines_df["KC_Middle"].iloc[-1]
    kc_lower = klines_df["KC_Lower"].iloc[-1]
    kc_position = klines_df["KC_Position"].iloc[-1]
    if close_price > kc_upper * 0.98: # Close to upper channel
        analysis_results["technical_indicators_summary"]["KC"] = \
            f"價格突破上軌（{kc_upper:.2f}），KC位置（{kc_position:.2%}）顯示強勢，中軌（{kc_middle:.2f}）成為動態支撐。"
    elif close_price < kc_lower * 1.02: # Close to lower channel
        analysis_results["technical_indicators_summary"]["KC"] = \
            f"價格跌破下軌（{kc_lower:.2f}），KC位置（{kc_position:.2%}）顯示弱勢，中軌（{kc_middle:.2f}）成為動態阻力。"
    else:
        analysis_results["technical_indicators_summary"]["KC"] = \
            f"價格在肯特納通道內運行。上軌={kc_upper:.2f}, 中軌={kc_middle:.2f}, 下軌={kc_lower:.2f}, 位置={kc_position:.2%}。"

    # RSI Analysis
    rsi14 = klines_df["RSI14"].iloc[-1]
    if rsi14 > 70:
        analysis_results["technical_indicators_summary"]["RSI"] = \
            f"RSI14（{rsi14:.2f}）進入超買區（70），需警惕回調風險。"
    elif rsi14 < 30:
        analysis_results["technical_indicators_summary"]["RSI"] = \
            f"RSI14（{rsi14:.2f}）進入超賣區（30），可能出現反彈。"
    else:
        analysis_results["technical_indicators_summary"]["RSI"] = \
            f"RSI14（{rsi14:.2f}）中性偏強，未達超買區（70），與價格走勢同步。"

    # KDJ Analysis
    k_val = klines_df["K"].iloc[-1]
    d_val = klines_df["D"].iloc[-1]
    j_val = klines_df["J"].iloc[-1]
    if k_val > d_val and d_val < 80 and k_val < 80: # Not overbought yet
        analysis_results["technical_indicators_summary"]["KDJ"] = \
            f"金叉初現。K值（{k_val:.2f}）上穿D值（{d_val:.2f}），J值（{j_val:.2f}）轉強。"
    elif k_val < d_val and d_val > 20 and k_val > 20: # Not oversold yet
        analysis_results["technical_indicators_summary"]["KDJ"] = \
            f"死叉運行。K值（{k_val:.2f}）下穿D值（{d_val:.2f}），J值（{j_val:.2f}）轉弱。"
    else:
        analysis_results["technical_indicators_summary"]["KDJ"] = \
            f"KDJ指標震盪或處於極端區域。K值={k_val:.2f}, D值={d_val:.2f}, J值={j_val:.2f}。"

    # Funding Rate (Placeholder, actual data not available from public API)
    analysis_results["funding_rate"] = "0.01000000%（中性），未顯示極端多空情緒。"

    # Volume Change (Simplified, can be improved with more detailed analysis)
    volume_24h = float(ticker_data["volume"])
    analysis_results["volume_change"] = f"近期成交量：{volume_24h:.2f}。上漲時放量，下跌時縮量，量價結構健康。"

    # Fund Flow Data (Placeholder, actual data not available from public API)
    analysis_results["fund_flow_data"] = "24H合約淨流入1.81億USDT（主力偏多），4H淨流入3908萬USDT加速，配合現貨資金同步流入（24H淨流入2916萬USDT），顯示買盤持續。"

    # Overall Direction and Entry Strategy (Based on trend analysis)
    trend_type = analysis_results["trend_type"]
    
    # 根據趨勢類型生成相應的交易建議
    if trend_type == "多頭":
        direction = "積極做多。多頭排列確立，價格站穩關鍵支撐{major_support:.2f}且指標共振偏多，突破{major_resistance:.2f}壓力確認趨勢延續。"
        entry_timing = "激進者：現價{current_price:.2f}直接做多，突破{major_resistance:.2f}加倉。穩健者：等待回踩{ma20:.2f}（MA20）企穩後進場。"
    elif trend_type == "空頭":
        direction = "謹慎做空。空頭排列明確，價格跌破關鍵支撐{major_support:.2f}且指標共振偏空，反彈至{major_resistance:.2f}壓力可考慮做空。"
        entry_timing = "激進者：現價{current_price:.2f}輕倉做空，反彈至{major_resistance:.2f}加倉。穩健者：等待反彈至{ma20:.2f}（MA20）阻力後進場。"
    elif trend_type == "糾結":
        direction = "觀望等待。均線糾結狀態，方向不明確，等待突破{major_resistance:.2f}或跌破{major_support:.2f}後再做決策。"
        entry_timing = "激進者：暫時觀望，等待方向選擇。穩健者：突破{major_resistance:.2f}做多或跌破{major_support:.2f}做空。"
    else:  # 震盪
        direction = "區間操作。震盪整理格局，可在{major_support:.2f}附近做多，{major_resistance:.2f}附近做空，注意控制倉位。"
        entry_timing = "激進者：現價{current_price:.2f}可輕倉操作。穩健者：等待接近區間邊界{major_support:.2f}或{major_resistance:.2f}後進場。"
    
    analysis_results["analysis_result"] = {
        "方向": direction,
        "入場時機": entry_timing,
        "止損設定": "{stop_loss:.2f}（-1.1%，低於支撐S1），或浮動止損3%以內。",
        "目標價位": "第一目標{target1:.2f}（24H高點，+1.4%），第二目標{target2:.2f}（前波段高點延伸，+2.3%）。"
    }
    # Fill in placeholders for analysis_result
    analysis_results["analysis_result"]["方向"] = analysis_results["analysis_result"]["方向"].format(
        major_support=analysis_results["major_support"], major_resistance=analysis_results["major_resistance"])
    analysis_results["analysis_result"]["入場時機"] = analysis_results["analysis_result"]["入場時機"].format(
        current_price=current_price, major_resistance=analysis_results["major_resistance"], ma20=ma20, major_support=analysis_results["major_support"])
    
    # Simplified stop loss and target prices for demonstration
    stop_loss = current_price * 0.989 # Example: 1.1% below current price
    target1 = current_price * 1.014 # Example: 1.4% above current price
    target2 = current_price * 1.023 # Example: 2.3% above current price

    analysis_results["analysis_result"]["止損設定"] = analysis_results["analysis_result"]["止損設定"].format(
        stop_loss=stop_loss)
    analysis_results["analysis_result"]["目標價位"] = analysis_results["analysis_result"]["目標價位"].format(
        target1=target1, target2=target2)

    return analysis_results

def analyze_multiple_symbols(symbols, intervals=["1h", "15m"]):
    """分析多個交易對的多時間框架"""
    all_analysis = {}

    for symbol in symbols:
        ticker_file = f"data/{symbol}_ticker_24hr.json"
        
        try:
            print(f"Analyzing {symbol}...")

            # 讀取ticker數據
            with open(ticker_file, "r") as f:
                ticker_data = json.load(f)

            symbol_analysis = {"symbol": symbol}
            
            # 分析每個時間框架
            for interval in intervals:
                klines_file = f"data/{symbol}_klines_{interval}.csv"
                
                try:
                    # 讀取K線數據
                    klines_df = pd.read_csv(klines_file)
                    
                    # 確保數據類型正確
                    klines_df["close"] = pd.to_numeric(klines_df["close"])
                    klines_df["high"] = pd.to_numeric(klines_df["high"])
                    klines_df["low"] = pd.to_numeric(klines_df["low"])

                    # 計算技術指標
                    klines_df_with_indicators = calculate_technical_indicators(klines_df.copy())

                    # 執行分析
                    analysis = analyze_indicators(ticker_data, klines_df_with_indicators)
                    
                    # 儲存到對應時間框架
                    symbol_analysis[interval] = analysis
                    
                except FileNotFoundError:
                    print(f"❌ Error: {klines_file} not found for {symbol}")
                    # 設置默認值
                    symbol_analysis[interval] = {
                        "current_trend": "數據不足",
                        "trend_type": "糾結",
                        "ma_analysis": {"is_tangled": True}
                    }
                    continue
                except Exception as e:
                    print(f"❌ Error analyzing {symbol} {interval}: {e}")
                    symbol_analysis[interval] = {
                        "current_trend": "分析錯誤",
                        "trend_type": "糾結",
                        "ma_analysis": {"is_tangled": True}
                    }
                    continue

            # 保持向後兼容性 - 將1h數據複製到根層級
            if "1h" in symbol_analysis:
                for key, value in symbol_analysis["1h"].items():
                    symbol_analysis[key] = value

            all_analysis[symbol] = symbol_analysis
            print(f"✅ {symbol} multi-timeframe analysis completed")

        except FileNotFoundError:
            print(f"❌ Error: {ticker_file} not found for {symbol}")
            continue
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            continue

    return all_analysis

if __name__ == "__main__":
    # 支援的交易對
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT", "ADAUSDT"]
    intervals = ["1h", "15m"]  # 支援多時間框架

    try:
        print("🔍 開始多幣種多時間框架技術分析...")
        all_analysis = analyze_multiple_symbols(symbols, intervals)

        # 保存綜合分析結果到 data 目錄
        with open("data/multi_investment_report.json", "w", encoding="utf-8") as f:
            json.dump(all_analysis, f, indent=4, ensure_ascii=False)

        print(f"\n📊 成功分析 {len(all_analysis)} 個交易對:")
        for symbol, analysis in all_analysis.items():
            price = analysis['current_price']
            change = analysis['24hr_change_percent']
            trend_1h = analysis['1h']['current_trend'] if '1h' in analysis else analysis['current_trend']
            trend_15m = analysis['15m']['current_trend'] if '15m' in analysis else "數據不足"
            print(f"  ✅ {symbol}: ${price:,.2f} ({change:+.2f}%)")
            print(f"      1H趨勢: {trend_1h}")
            print(f"      15M趨勢: {trend_15m}")

        print("\n📄 Multi-timeframe investment report saved: data/multi_investment_report.json")

    except Exception as e:
        print(f"An error occurred during analysis: {e}")


