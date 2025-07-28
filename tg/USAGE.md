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
SUPPORTED_SYMBOLS=BTCUSDT,ETHUSDT,SOLUSDT,DOGEUSDT,XRPUSDT,ADAUSDT
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

## 📊 訊號類型

### 🟢 買入訊號
- **觸發條件**: 24小時漲幅 > 閾值 且趨勢為多頭
- **包含信息**: 價格、變化百分比、技術分析、入場建議

### 🔴 賣出訊號  
- **觸發條件**: 24小時跌幅 > 閾值 且趨勢為空頭
- **包含信息**: 價格、變化百分比、風險警示

### 📊 市場總覽
- **發送時機**: 每次執行時
- **包含信息**: 所有幣種概況、信號統計

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
# Linux/Mac - 每小時執行
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

---

## 📱 訊息範例

### 買入訊號
```
🚀 買入訊號 BUY SIGNAL 🚀

🟠 Bitcoin (BTCUSDT)
💰 當前價格: $50,123.45

📊 價格變化
• 1小時: +0.5%
• 4小時: +1.2%
• 24小時: +2.1%

📈 趨勢分析: 多頭排列，趨勢偏多
🟢 建議操作: 買入 (BUY)

💡 入場建議: 現價50123輕倉試多
🎯 目標價位: 第一目標51000（+1.7%）
🛡️ 止損設定: 49500（-1.2%）

⏰ 訊號時間: 2024-01-15 14:30:00 (台北時間)
```

### 市場總覽
```
📊 虛擬幣市場總覽 📊

⏰ 更新時間: 2024-01-15 14:30:00 (台北時間)

• Bitcoin: $50,123.45 (+2.1%) 🟢買入
• Ethereum: $3,456.78 (+1.5%) 🟢買入
• Solana: $98.76 (-0.8%) ⚪觀望

📈 信號統計
🟢 買入信號: 2 個
🔴 賣出信號: 0 個
⚪ 觀望信號: 1 個
```