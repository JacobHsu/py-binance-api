# 🚀 Telegram Bot 快速開始指南

> 📱 **5分鐘設定完成** | 🤖 **自動投資訊號** | 🔒 **安全配置**

---

## ⚡ 超快速設定 (推薦)

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 配置 .env 文件
cp tg/.env.example tg/.env
# 編輯 tg/.env 填入您的 Bot Token 和 Chat ID

# 3. 執行訊號發送
python run_telegram_bot.py
```

**就這麼簡單！** 🎉

---

## 📋 詳細步驟

### 步驟 1: 創建 Telegram Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/newbot`
3. 輸入 Bot 名稱: `虛擬幣投資助手`
4. 輸入用戶名: `your_crypto_bot`
5. 複製 Bot Token
6. 向您的 Bot 發送 `/start`

### 步驟 2: 配置 .env 文件

```bash
# 複製範例文件
cp tg/.env.example tg/.env

# 編輯配置文件，填入您的資訊
nano tg/.env  # 或使用其他編輯器
```

需要填入：
- ✅ TELEGRAM_BOT_TOKEN (從 @BotFather 獲取)
- ✅ TELEGRAM_CHAT_ID (您的 Chat ID)
- ⚙️ 其他可選配置 (可保持預設值)

### 步驟 3: 開始使用

```bash
# 發送投資訊號
python run_telegram_bot.py
```

---

## 📱 您將收到的訊息

### 🟢 買入訊號範例
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

⏰ 訊號時間: 2024-01-15 14:30:00
```

### 📊 市場總覽範例
```
📊 虛擬幣市場總覽 📊

• Bitcoin: $50,123.45 (+2.1%) 🟢買入
• Ethereum: $3,456.78 (+1.5%) 🟢買入
• Solana: $98.76 (-0.8%) ⚪觀望

📈 信號統計
🟢 買入信號: 2 個
🔴 賣出信號: 0 個
⚪ 觀望信號: 1 個
```

---

## 🎯 支援的幣種

| 幣種 | 符號 | 圖標 |
|------|------|------|
| Bitcoin | BTCUSDT | ₿ |
| Ethereum | ETHUSDT | Ξ |
| Binance Coin | BNBUSDT | 🔶 |
| Solana | SOLUSDT | ◎ |
| Ripple | XRPUSDT | ◆ |

---

## ⚙️ 自定義設定

編輯 `tg/.env` 文件來自定義：

```bash
# 只監控 BTC 和 ETH
SUPPORTED_SYMBOLS=BTCUSDT,ETHUSDT

# 提高觸發閾值
BUY_SIGNAL_THRESHOLD=2.0
SELL_SIGNAL_THRESHOLD=-2.0

# 只發送買入訊號
SEND_BUY_SIGNALS=true
SEND_SELL_SIGNALS=false
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

在 `.github/workflows/binance_analysis.yml` 添加：

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
cd tg
python setup_env.py
```

**❌ Bot Token 無效**
- 檢查 Token 格式是否正確
- 重新從 @BotFather 獲取

**❌ 找不到分析數據**
```bash
python get_binance_data.py
python analyze_binance_data.py
```

### 🧪 測試功能

```bash
# 完整測試
python tg/test_telegram_integration.py

# 基本測試
python tg/setup_telegram_bot.py test YOUR_TOKEN YOUR_CHAT_ID
```

---

## 📁 文件結構

```
📁 專案根目錄
├── 📄 setup_telegram.py          # 設定入口 (從根目錄執行)
├── 📄 run_telegram_bot.py        # 執行入口 (從根目錄執行)
└── 📁 tg/                        # Telegram Bot 模組
    ├── 📄 telegram_bot.py         # 核心功能
    ├── 📄 telegram_config.py      # 配置管理
    ├── 📄 .env                    # 您的配置 (自動生成)
    └── 📄 ...                     # 其他工具腳本
```

---

## 🎉 完成！

現在您的 Telegram Bot 已準備就緒！

### 日常使用

```bash
# 發送投資訊號
python run_telegram_bot.py

# 查看配置
cat tg/.env

# 測試功能
python tg/test_telegram_integration.py
```

### 進階功能

- 📊 查看詳細指南: `tg/README_TELEGRAM.md`
- 🔧 自定義配置: 編輯 `tg/.env`
- 🧪 功能演示: `python tg/demo_telegram_bot.py`

---

**🚀 享受您的自動化虛擬幣投資助手！**