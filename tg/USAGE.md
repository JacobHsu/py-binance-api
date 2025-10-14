# 📱 Telegram Bot 使用說明

## 🚀 快速開始

### 1. 配置 .env 文件

```bash
# 複製範例文件
cp tg/.env.example tg/.env

# 編輯配置文件
nano tg/.env  # 或使用其他編輯器
```

### 2. 填入必要配置

```bash
# 必需配置
TELEGRAM_BOT_TOKEN=你的Bot Token
TELEGRAM_CHAT_ID=你的Chat ID

# 可選配置 (可保持預設值)
SEND_BUY_SIGNALS=true
SEND_SELL_SIGNALS=true
SEND_MARKET_SUMMARY=true
BUY_SIGNAL_THRESHOLD=1.0
SELL_SIGNAL_THRESHOLD=-1.0
SUPPORTED_SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT
```

### 3. 執行訊號發送

```bash
# 請先執行數據分析:
python get_binance_data.py
python analyze_binance_data.py
# 從根目錄執行 (推薦)
python run_telegram_bot.py

# 或進入 tg 目錄執行
cd tg && python run_telegram_signals.py
```

---

## 🔧 配置選項說明

| 配置項 | 必需 | 預設值 | 說明 |
|--------|------|--------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | 從 @BotFather 獲取的 Bot Token |
| `TELEGRAM_CHAT_ID` | ✅ | - | 接收訊息的 Chat ID |
| `SEND_BUY_SIGNALS` | ❌ | true | 是否發送買入訊號 |
| `SEND_SELL_SIGNALS` | ❌ | true | 是否發送賣出訊號 |
| `SEND_MARKET_SUMMARY` | ❌ | true | 是否發送市場總覽 |
| `BUY_SIGNAL_THRESHOLD` | ❌ | 1.0 | 買入訊號觸發閾值 (%) |
| `SELL_SIGNAL_THRESHOLD` | ❌ | -1.0 | 賣出訊號觸發閾值 (%) |
| `SUPPORTED_SYMBOLS` | ❌ | 全部 | 監控的幣種列表 |

---

## 📊 訊號邏輯

### 🎯 統一邏輯設計
基於 **15分鐘** 和 **1小時** 多時間框架趨勢分析：

### 📊 市場總覽 (顯示所有狀態)
- **🟢 明確看多**: 15M多頭 + 1H多頭 → 高信心度看多
- **🔴 明確看空**: 15M空頭 + 1H空頭 → 高信心度看空  
- **🟡 謹慎做多**: 15M多頭 + 1H糾結 或 15M糾結 + 1H多頭
- **🟡 謹慎做空**: 15M空頭 + 1H糾結 或 15M糾結 + 1H空頭
- **⚪ 雙重糾結**: 15M糾結 + 1H糾結 → 觀望等待
- **📊 雙重震盪**: 15M震盪 + 1H震盪 → 區間操作

### 🟢 買入訊號 (單幣種推送)
- **觸發條件**: 僅 **🟢 明確看多** (15M多頭 + 1H多頭)
- **包含信息**: 價格、1H/4H變化、技術分析、入場建議、目標價位、止損設定

### 🔴 賣出訊號 (單幣種推送)  
- **觸發條件**: 僅 **🔴 明確看空** (15M空頭 + 1H空頭)
- **包含信息**: 價格、1H/4H變化、趨勢分析、風險警示

### 💡 設計理念
- **市場總覽**: 完整市場狀況，包含謹慎做多/空建議
- **單幣種訊號**: 只推送高信心度交易機會，避免雜訊

---

## 🧪 測試功能

```bash
# 完整功能測試
python tg/test_telegram_integration.py

# 檢查配置是否正確
python -c "from tg.telegram_config import config; print('✅ 配置有效' if config.is_valid() else '❌ 配置無效')"
```

---

## 🔄 自動化執行

### 本地定時執行

```bash
# Linux/Mac - 每30分鐘執行
0 * * * * cd /path/to/project && python run_telegram_bot.py

# Windows - 使用工作排程器
```

### GitHub Actions 整合

```yaml
- name: Send Telegram Signals
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  run: |
    python run_telegram_bot.py
```

---

## 🛠️ 故障排除

### 常見問題

**❌ 找不到 .env 文件**
```bash
cp tg/.env.example tg/.env
```

**❌ 配置無效**
```bash
# 檢查 Bot Token 和 Chat ID 是否正確
# Token 格式: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
# Chat ID 格式: 數字 (可能為負數)
```

**❌ 找不到分析數據**
```bash
python get_binance_data.py
python analyze_binance_data.py
```

**❌ 訊號不一致問題**
```bash
# 確保使用相同數據源和邏輯
# 檢查數據更新時間
ls -la data/multi_investment_report.json

# 重新生成最新數據
python get_binance_data.py && python analyze_binance_data.py

# 確認邏輯統一性
python -c "
from tg.telegram_bot import load_analysis_data
data = load_analysis_data()
if data:
    for symbol, info in data.items():
        trend_15m = info.get('15m', {}).get('trend_type', '糾結')
        trend_1h = info.get('1h', {}).get('trend_type', '糾結')
        print(f'{symbol}: 15M={trend_15m}, 1H={trend_1h}')
"
```

### ⚡ 邏輯統一性檢查
- `telegram_bot.py` 和 `run_telegram_bot.py` 使用相同訊號判斷邏輯
- 市場總覽顯示所有狀態（包括謹慎做多/空）  
- 單幣種訊號僅發送明確看多/空（高信心度）
- 確保資料來源一致，避免使用過時的 JSON 資料

---

## 📱 訊息範例

### 買入訊號 (明確看多才發送)
```
🚀 XRP BUY SIGNAL 🚀

🔷 XRP (XRPUSDT)
💰 當前價格: $3.05

📊 價格變化
• 1小時: -0.10%
• 4小時: -0.81%

📈 趨勢分析: 多頭排列，趨勢偏多(一般)

🟢 綜合建議: 明確看多

⏰ 訊號時間: 2025-08-24 13:07:20 (台北時間)

📊 技術指標摘要
• RSI: 31.68
• MACD: 死叉運行中但收斂

💡 入場建議
激進者：現價3.05輕倉試多，突破3.66加倉
穩健者：等待回踩3.05（MA20）或2.73（S1）企穩後進場

🎯 目標價位
第一目標3.02（24H高點，+1.4%）
第二目標3.05（前波段高點延伸，+2.3%）

🛡️ 止損設定
2.95（-1.1%，低於支撐S1），或浮動止損3%以內
```

### 市場總覽
```
📊 虛擬幣市場總覽 📊

⏰ 更新時間: 2025-08-24 13:07:20 (台北時間)

BTC | $113,186.85 | 1H:-1.04% 4H:-1.44%
15M:📉空頭 | 1H:📉空頭 | 🔴明確看空

ETH | $3,576.86 | 1H:-0.11% 4H:-1.81%
15M:📉空頭 | 1H:📈多頭 | 🟡謹慎做空

XRP | $2.98 | 1H:-1.95% 4H:-3.11%
15M:📉空頭 | 1H:📉空頭 | 🔴明確看空

📈 信號統計
🟢 買入信號: 0 個
🔴 賣出信號: 2 個  
⚪ 觀望信號: 4 個
```