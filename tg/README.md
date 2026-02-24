# 📱 Telegram Bot 模組

> 🤖 **虛擬幣投資助手** | 🔒 **安全的 .env 配置** | ⚡ **自動訊號發送**

---

## 📁 文件結構

```
tg/
├── 📄 __init__.py                   # Python 模組初始化
├── 📄 README.md                     # 本說明文件
├── 📄 telegram_bot.py               # 核心 Bot 功能
├── 📄 telegram_config.py            # 配置管理 (.env 支援)
├── 📄 run_telegram_signals.py       # 主執行腳本
├── 📄 test_telegram_integration.py  # 測試腳本
└── 📄 .env.example                  # 配置範例
```

---

## 🚀 使用方法

### 從根目錄執行 (推薦)

```bash
# 執行訊號發送
python run_telegram_bot.py

# 測試功能
python tg/test_telegram_integration.py
```

### 進入 tg 目錄執行

```bash
cd tg

# 執行訊號發送
python run_telegram_signals.py

# 測試功能
python test_telegram_integration.py
```

---

## 🔧 配置 .env 文件

1. **複製範例文件**
   ```bash
   cp tg/.env.example tg/.env
   ```

2. **編輯配置**
   ```bash
   # 必需配置
   TELEGRAM_BOT_TOKEN=你的Bot Token
   TELEGRAM_CHAT_ID=你的Chat ID
   
   # 可選配置
   SEND_BUY_SIGNALS=true
   SEND_SELL_SIGNALS=true
   BUY_SIGNAL_THRESHOLD=1.0
   SELL_SIGNAL_THRESHOLD=-1.0
   SUPPORTED_SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT
   ```

---

## 📱 功能特色

- 🟢 **買入訊號**: 自動檢測並發送買入機會
- 🔴 **賣出訊號**: 及時提醒賣出時機  
- 📊 **市場總覽**: 實時多幣種市場狀況
- 🔒 **安全配置**: .env 文件管理敏感信息
- ⚙️ **靈活設定**: 可自定義觸發條件和監控幣種

---

## 🎯 日常使用

```bash
# 1. 確保有分析數據
python get_binance_data.py
python analyze_binance_data.py

# 2. 發送 Telegram 訊號
python run_telegram_bot.py
```

---

**🎉 享受您的 Telegram 虛擬幣投資助手！**