# 🔐 GitHub Secrets 設定指南

> 🤖 **啟用 Telegram 自動訊號** | 🔒 **安全配置管理**

---

## 🎯 設定目標

讓 GitHub Actions 能夠自動發送 Telegram 買入訊號，需要設定以下 Secrets：

- `TELEGRAM_BOT_TOKEN` - Telegram Bot Token
- `TELEGRAM_CHAT_ID` - 接收訊息的 Chat ID

---

## 📋 設定步驟

### 1. 進入 GitHub 倉庫設定

1. 打開您的 GitHub 倉庫
2. 點擊 **Settings** (設定)
3. 在左側選單找到 **Secrets and variables**
4. 點擊 **Actions**

### 2. 添加 Telegram Bot Token

1. 點擊 **New repository secret**
2. 填入以下資訊：
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Secret**: 您的 Bot Token (格式: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
3. 點擊 **Add secret**

### 3. 添加 Chat ID

1. 再次點擊 **New repository secret**
2. 填入以下資訊：
   - **Name**: `TELEGRAM_CHAT_ID`
   - **Secret**: 您的 Chat ID (格式: `123456789`)
3. 點擊 **Add secret**

---

## 🔍 如何獲取必要資訊

### 📱 獲取 Bot Token

1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/newbot` 創建新 Bot
3. 輸入 Bot 名稱和用戶名
4. 複製獲得的 Token

### 💬 獲取 Chat ID

**方法 1: 使用現有工具**
```bash
# 先向您的 Bot 發送任意訊息
# 然後執行 (需要本地配置)
python tg/setup_telegram_bot.py getchatid YOUR_BOT_TOKEN
```

**方法 2: 手動獲取**
1. 向您的 Bot 發送 `/start`
2. 在瀏覽器打開：
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. 在回應中找到 `"chat":{"id":123456789}`

---

## ✅ 驗證設定

### 檢查 Secrets 是否正確設定

在 GitHub 倉庫的 **Settings → Secrets and variables → Actions** 頁面，您應該看到：

```
Repository secrets
├── TELEGRAM_BOT_TOKEN    ✅ 已設定
└── TELEGRAM_CHAT_ID      ✅ 已設定
```

### 測試 GitHub Actions

1. 進入 **Actions** 頁面
2. 選擇 **Virtual Currency 1h Analysis & README Generator**
3. 點擊 **Run workflow** 手動執行
4. 查看執行日誌中的 Telegram 步驟

---

## 🔄 GitHub Actions 工作流程

設定完成後，工作流程會：

```yaml
1. 📊 獲取市場數據
2. 🔍 執行技術分析  
3. 📝 生成 README 報告
4. 🤖 檢查買入訊號
   ├── 🟢 有買入訊號 → 發送 Telegram 訊息
   └── 📊 無買入訊號 → 跳過發送
5. 📤 提交更新到 GitHub
```

---

## 📱 預期的 Telegram 訊息

### 🟢 買入訊號範例

```
🚀 GitHub Actions 自動訊號 🚀

🟢 發現買入機會！

🟠 Bitcoin (BTCUSDT)
💰 當前價格: $50,123.45
📊 24小時變化: +2.1%
📈 趨勢: 多頭排列，趨勢偏多

🎯 建議操作: 買入 (BUY)
💡 入場建議: 現價50123輕倉試多
🛡️ 止損設定: 49500（-1.2%）

⏰ 分析時間: 2024-01-15 14:00:00 UTC
🤖 由 GitHub Actions 自動生成

#買入訊號 #BTCUSDT #自動化投資
```

### 📊 市場總覽範例

```
📊 虛擬幣市場總覽 📊

⏰ 更新時間: 2024-01-15 14:00:00 UTC

• Bitcoin: $50,123.45 (+2.1%) 🟢買入
• Ethereum: $3,456.78 (+1.5%) 🟢買入
• Solana: $98.76 (-0.8%) ⚪觀望

📈 信號統計
🟢 買入信號: 2 個
🔴 賣出信號: 0 個
⚪ 觀望信號: 1 個

🤖 由 GitHub Actions 自動分析
```

---

## 🛠️ 故障排除

### ❌ 常見錯誤

**1. Bot Token 無效**
```
錯誤: 401 Unauthorized
解決: 檢查 TELEGRAM_BOT_TOKEN 是否正確
```

**2. Chat ID 錯誤**
```
錯誤: 400 Bad Request: chat not found
解決: 確保已向 Bot 發送過訊息，重新獲取 Chat ID
```

**3. Secrets 未設定**
```
日誌: ⚠️ Telegram 配置無效，跳過發送
解決: 檢查 GitHub Secrets 是否正確設定
```

### 🔍 查看執行日誌

1. **GitHub Actions 頁面**
   ```
   您的倉庫 → Actions → 選擇執行記錄
   ```

2. **展開 Telegram 步驟**
   ```
   "Send Telegram signals (if buy signals exist)"
   ```

3. **查看日誌訊息**
   ```bash
   ✅ 成功: Telegram 訊號發送完成！
   📊 跳過: 當前沒有買入訊號，不發送 Telegram 訊息
   ❌ 失敗: Telegram 發送失敗: [錯誤詳情]
   ```

---

## 🎛️ 進階配置

### 自定義觸發條件

您可以添加更多 Secrets 來自定義行為：

| Secret 名稱 | 預設值 | 說明 |
|-------------|--------|------|
| `BUY_SIGNAL_THRESHOLD` | 1.0 | 買入訊號觸發閾值 (%) |
| `SEND_MARKET_SUMMARY` | true | 是否發送市場總覽 |
| `SUPPORTED_SYMBOLS` | 全部 | 監控的幣種列表 |

### 範例設定

```
TELEGRAM_BOT_TOKEN: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID: 123456789
BUY_SIGNAL_THRESHOLD: 2.0
SEND_MARKET_SUMMARY: true
SUPPORTED_SYMBOLS: BTCUSDT,ETHUSDT,SOLUSDT
```

---

## 🎉 完成！

設定完成後，您的 GitHub Actions 將會：

- 🕐 **每30分鐘自動執行** 市場分析
- 🧠 **智能判斷** 是否有買入訊號
- 📱 **自動發送** Telegram 訊息 (僅在有買入訊號時)
- 📊 **更新 README** 投資分析報告

**享受您的全自動化虛擬幣投資助手！** 🚀