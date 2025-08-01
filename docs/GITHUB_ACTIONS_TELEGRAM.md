# 🤖 GitHub Actions Telegram 整合指南

> 📊 **自動化報告** + 📱 **智能訊號** = 🚀 **完美整合**

---

## 🎯 功能說明

GitHub Actions 工作流程現在會：
1. ✅ 獲取市場數據
2. ✅ 執行技術分析  
3. ✅ 生成 README 報告
4. 🆕 **檢查買入訊號並發送到 Telegram**

### 🔍 智能發送邏輯

- 📊 **有買入訊號** → 發送 Telegram 訊息
- 📈 **無買入訊號** → 跳過發送，節省資源
- ⚠️ **配置無效** → 跳過發送，不影響主流程

---

## ⚙️ 設定 GitHub Secrets

### 1. 進入 GitHub 倉庫設定

```
您的倉庫 → Settings → Secrets and variables → Actions
```

### 2. 添加必要的 Secrets

| Secret 名稱 | 說明 | 範例 |
|-------------|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TELEGRAM_CHAT_ID` | 接收訊息的 Chat ID | `123456789` |

### 3. 設定步驟

1. **點擊 "New repository secret"**
2. **添加 TELEGRAM_BOT_TOKEN**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Secret: 您的 Bot Token
3. **添加 TELEGRAM_CHAT_ID**
   - Name: `TELEGRAM_CHAT_ID`  
   - Secret: 您的 Chat ID

---

## 🔄 工作流程詳解

### 📋 完整流程

```yaml
name: Binance Analysis with Telegram

on:
  schedule:
    - cron: '0 * * * *'  # 每小時執行
  workflow_dispatch:

jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      # 1. 獲取數據
      - name: Get Binance data
        run: python get_binance_data.py
      
      # 2. 執行分析
      - name: Analyze data
        run: python analyze_binance_data.py
      
      # 3. 生成報告
      - name: Generate README report
        run: python generate_readme_report.py
      
      # 4. 🆕 智能 Telegram 發送
      - name: Send Telegram signals (if buy signals exist)
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python send_telegram_conditionally.py
      
      # 5. 提交更新
      - name: Commit and push
        run: |
          git add .
          git commit -m "📊 Update analysis report"
          git push
```

### 🧠 智能發送邏輯

```python
# 檢查買入訊號
buy_signals = check_for_buy_signals(analysis_data)

if buy_signals:
    # 🟢 有買入訊號 → 發送 Telegram
    send_telegram_signals(buy_signals)
else:
    # 📊 無買入訊號 → 跳過發送
    print("當前沒有買入訊號，不發送 Telegram 訊息")
```

---

## 📱 Telegram 訊息範例

### 🟢 買入訊號訊息

```
🚀 GitHub Actions 自動訊號 🚀

🟢 發現買入機會！

🟠 Bitcoin (BTCUSDT)
💰 當前價格: $50,123.45
📊 24小時變化: +2.1%
📈 趨勢: 多頭排列，趨勢偏多

🎯 建議操作: 買入 (BUY)
💡 入場時機: 現價50123輕倉試多
🛡️ 止損設定: 49500（-1.2%）

⏰ 分析時間: 2024-01-15 14:00:00 UTC
🤖 由 GitHub Actions 自動生成

#買入訊號 #BTCUSDT #自動化投資
```

### 📊 市場總覽訊息

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

## 🛠️ 自定義配置

### 📋 環境變數選項

您可以在 GitHub Secrets 中添加更多配置：

| 變數名 | 預設值 | 說明 |
|--------|--------|------|
| `SEND_BUY_SIGNALS` | true | 是否發送買入訊號 |
| `SEND_SELL_SIGNALS` | false | 是否發送賣出訊號 |
| `SEND_MARKET_SUMMARY` | true | 是否發送市場總覽 |
| `BUY_SIGNAL_THRESHOLD` | 1.0 | 買入訊號觸發閾值 |

### 🎛️ 自定義範例

```yaml
- name: Send Telegram signals
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
    SEND_MARKET_SUMMARY: true
    BUY_SIGNAL_THRESHOLD: 2.0  # 只有漲幅超過2%才發送
  run: python send_telegram_conditionally.py
```

---

## 🔍 監控和調試

### 📊 查看執行日誌

1. **進入 GitHub Actions 頁面**
   ```
   您的倉庫 → Actions → 選擇工作流程執行
   ```

2. **查看 Telegram 步驟日誌**
   ```
   展開 "Send Telegram signals" 步驟
   ```

### 🧪 測試配置

```yaml
# 手動觸發測試
on:
  workflow_dispatch:  # 允許手動執行
```

### 📋 常見日誌訊息

```bash
✅ 成功訊息:
🔍 檢查是否有買入訊號需要發送...
🟢 發現 2 個買入訊號，開始發送 Telegram 訊息...
✅ Telegram 訊號發送完成！

⚠️ 跳過訊息:
📊 當前沒有買入訊號，不發送 Telegram 訊息

❌ 錯誤訊息:
⚠️ Telegram 配置無效，跳過發送
❌ Telegram 發送失敗: [錯誤詳情]
```

---

## 🚀 進階功能

### 🎯 條件式發送

```python
# 只在特定條件下發送
if len(buy_signals) >= 2:  # 至少2個買入訊號
    send_telegram_signals()
```

### 📈 自定義訊號邏輯

```python
# 自定義買入條件
def is_strong_buy_signal(data):
    return (
        data['24hr_change_percent'] > 3.0 and  # 漲幅超過3%
        "多頭" in data['current_trend'] and     # 趨勢向上
        data.get('1h_change_percent', 0) > 0.5  # 1小時也在上漲
    )
```

### 🔄 多頻率發送

```yaml
# 不同時間發送不同內容
- name: Send morning summary
  if: github.event.schedule == '0 0 * * *'  # 每天早上
  run: python send_daily_summary.py

- name: Send hourly signals  
  if: github.event.schedule == '0 * * * *'  # 每小時
  run: python send_telegram_conditionally.py
```

---

## 🛡️ 安全最佳實踐

### 🔒 保護敏感信息

1. ✅ **使用 GitHub Secrets** 存儲 Token
2. ✅ **不在代碼中硬編碼** 敏感信息
3. ✅ **定期更換** Bot Token
4. ✅ **限制 Bot 權限** 只給必要權限

### 📊 監控使用情況

1. **定期檢查** GitHub Actions 使用量
2. **監控 Telegram** 訊息發送頻率
3. **設定合理的** 觸發條件

---

## 🎉 完成！

現在您的 GitHub Actions 工作流程已經完美整合了 Telegram 功能：

- 🤖 **全自動化**: 無需手動干預
- 🧠 **智能發送**: 只在有買入訊號時發送
- 🔒 **安全可靠**: 使用 GitHub Secrets 保護敏感信息
- 📊 **詳細日誌**: 完整的執行記錄

**享受您的自動化虛擬幣投資助手！** 🚀