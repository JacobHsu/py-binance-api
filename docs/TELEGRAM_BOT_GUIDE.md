# 📱 Telegram Bot 買入訊號設定指南

> 🤖 **自動發送虛擬幣買入/賣出訊號到 Telegram**

---

## 🚀 快速開始

### 步驟 1: 創建 Telegram Bot

1. **找到 BotFather**
   - 在 Telegram 中搜尋 `@BotFather`
   - 點擊開始對話

2. **創建新 Bot**
   ```
   發送: /newbot
   輸入 Bot 名稱: 虛擬幣投資助手
   輸入 Bot 用戶名: your_crypto_bot (必須以 _bot 結尾)
   ```

3. **獲取 Bot Token**
   - BotFather 會給您一個 Token，格式如: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **請妥善保管此 Token！**

### 步驟 2: 獲取 Chat ID

**方法 A - 個人聊天 (推薦)**
```bash
# 1. 向您的 Bot 發送任意訊息 (例如: /start)
# 2. 執行以下命令獲取 Chat ID
python setup_telegram_bot.py getchatid YOUR_BOT_TOKEN
```

**方法 B - 群組聊天**
```bash
# 1. 將 Bot 加入群組
# 2. 在群組中發送 /start
# 3. 執行上述命令獲取群組 Chat ID
```

### 步驟 3: 配置 .env 文件

```bash
# 方法 A: 互動式設定 (推薦)
python setup_env.py

# 方法 B: 快速設定
python quick_setup.py

# 方法 C: 手動設定
cp .env.example .env
# 然後編輯 .env 文件填入您的配置
```

### 步驟 4: 測試連接

```bash
# 測試 Bot 是否正常工作
python setup_telegram_bot.py test YOUR_BOT_TOKEN YOUR_CHAT_ID
```

---

## 🔧 詳細配置

### 環境變數設定

| 變數名 | 必需 | 預設值 | 說明 |
|--------|------|--------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | ✅ | - | 接收訊息的 Chat ID |
| `SEND_BUY_SIGNALS` | ❌ | true | 是否發送買入訊號 |
| `SEND_SELL_SIGNALS` | ❌ | true | 是否發送賣出訊號 |
| `SEND_MARKET_SUMMARY` | ❌ | true | 是否發送市場總覽 |
| `BUY_SIGNAL_THRESHOLD` | ❌ | 1.0 | 買入訊號觸發閾值 (%) |
| `SELL_SIGNAL_THRESHOLD` | ❌ | -1.0 | 賣出訊號觸發閾值 (%) |

### 配置文件設定

編輯 `telegram_config.py`:

```python
# 直接設定 (不使用環境變數)
config.BOT_TOKEN = "您的Bot Token"
config.CHAT_ID = "您的Chat ID"

# 自定義閾值
config.BUY_SIGNAL_THRESHOLD = 2.0   # 漲幅超過2%才發送買入訊號
config.SELL_SIGNAL_THRESHOLD = -2.0 # 跌幅超過2%才發送賣出訊號

# 選擇監控的幣種
config.SUPPORTED_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
```

---

## 🚀 使用方法

### 方法 1: 完整工作流程

```bash
# 1. 獲取數據
python get_binance_data.py

# 2. 執行分析
python analyze_binance_data.py

# 3. 發送 Telegram 訊號
python run_telegram_signals.py
```

### 方法 2: 直接使用

```bash
# 一鍵執行 (需要先有分析數據)
python run_telegram_signals.py
```

### 方法 3: 程式化調用

```python
from telegram_bot import TelegramBot, check_and_send_signals

# 方式 A: 使用配置文件
check_and_send_signals(bot_token, chat_id)

# 方式 B: 手動發送
bot = TelegramBot(bot_token, chat_id)
bot.send_buy_signal(
    symbol="BTCUSDT",
    price=50000,
    change_1h=0.5,
    change_4h=1.2,
    change_24h=2.1,
    trend="多頭排列，趨勢偏多"
)
```

---

## 📊 訊號類型

### 🟢 買入訊號
- **觸發條件**: 24小時漲幅 > 1% 且趨勢為多頭
- **包含信息**: 價格、變化百分比、技術分析、入場建議

### 🔴 賣出訊號
- **觸發條件**: 24小時跌幅 > 1% 且趨勢為空頭
- **包含信息**: 價格、變化百分比、風險警示

### 📊 市場總覽
- **發送時機**: 每次執行時
- **包含信息**: 所有幣種概況、信號統計

---

## 🔄 自動化部署

### GitHub Actions 整合

編輯 `.github/workflows/binance_analysis.yml`:

```yaml
- name: Send Telegram Signals
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  run: |
    python run_telegram_signals.py
```

### 設定 GitHub Secrets

1. 進入您的 GitHub 倉庫
2. 點擊 `Settings` → `Secrets and variables` → `Actions`
3. 添加以下 Secrets:
   - `TELEGRAM_BOT_TOKEN`: 您的 Bot Token
   - `TELEGRAM_CHAT_ID`: 您的 Chat ID

### 本地定時執行

```bash
# 使用 cron (Linux/Mac)
# 每30分鐘執行一次
0 * * * * cd /path/to/your/project && python run_telegram_signals.py

# 使用 Windows 工作排程器
# 創建基本工作 → 設定觸發程序 → 設定動作
```

---

## 🛠️ 故障排除

### 常見問題

**1. Bot Token 無效**
```
❌ 錯誤: 401 Unauthorized
✅ 解決: 檢查 Bot Token 是否正確，重新從 BotFather 獲取
```

**2. Chat ID 錯誤**
```
❌ 錯誤: 400 Bad Request: chat not found
✅ 解決: 確保已向 Bot 發送過訊息，重新獲取 Chat ID
```

**3. 找不到分析數據**
```
❌ 錯誤: 找不到 data/multi_investment_report.json
✅ 解決: 先執行 get_binance_data.py 和 analyze_binance_data.py
```

**4. 網路連接問題**
```
❌ 錯誤: requests.exceptions.ConnectionError
✅ 解決: 檢查網路連接，確認可以訪問 api.telegram.org
```

### 調試模式

```python
# 在 telegram_bot.py 中啟用調試
import logging
logging.basicConfig(level=logging.DEBUG)

# 測試單個功能
from telegram_bot import TelegramBot
bot = TelegramBot("YOUR_TOKEN", "YOUR_CHAT_ID")
result = bot.send_message("測試訊息")
print(result)
```

---

## 📱 訊息範例

### 買入訊號範例
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
⚠️ 風險提醒: 請做好風險管理，設定止損

⏰ 訊號時間: 2024-01-15 14:30:00 (台北時間)

#買入訊號 #BTCUSDT #虛擬幣投資
```

### 市場總覽範例
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

#市場總覽 #虛擬幣投資 #技術分析
```

---

## 🔒 安全建議

1. **保護 Bot Token**
   - 不要在代碼中硬編碼 Token
   - 使用環境變數或配置文件
   - 定期更換 Token

2. **限制 Bot 權限**
   - 只給 Bot 發送訊息的權限
   - 不要給予管理員權限

3. **監控使用情況**
   - 定期檢查 Bot 發送的訊息
   - 設定合理的發送頻率限制

---

## 🎯 進階功能

### 自定義訊息模板

編輯 `telegram_bot.py` 中的訊息模板:

```python
def send_buy_signal(self, ...):
    message = f"""🚀 自定義買入訊號 🚀
    
{symbol_info['emoji']} {symbol_info['name']}
價格: {price_str}
變化: {change_24h:+.2f}%

您的自定義內容...
"""
```

### 添加新的訊號類型

```python
def send_alert_signal(self, symbol, message):
    """發送自定義警報"""
    alert_message = f"""⚠️ 市場警報 ⚠️
    
{symbol}: {message}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return self.send_message(alert_message)
```

### 整合其他指標

```python
# 在 analyze_binance_data.py 中添加新指標
def calculate_custom_indicator(df):
    # 您的自定義指標邏輯
    pass

# 在訊號判斷中使用
if custom_indicator > threshold:
    # 發送特殊訊號
    pass
```

---

## 📞 支援與反饋

如果您在設定過程中遇到問題，請：

1. 檢查本指南的故障排除部分
2. 確認所有依賴已正確安裝
3. 驗證 Bot Token 和 Chat ID 的正確性
4. 查看控制台輸出的錯誤訊息

---

**🎉 恭喜！您的 Telegram 虛擬幣投資助手已準備就緒！**