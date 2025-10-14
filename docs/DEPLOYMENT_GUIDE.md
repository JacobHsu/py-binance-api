# 🚀 GitHub Actions 自動化部署指南

## 📋 功能說明

這個 GitHub Actions 工作流程會：
- ⏰ **每30分鐘自動執行**（UTC 時間每個整點和半點）
- 📊 **獲取最新 Binance 數據**
- 🔍 **執行技術分析**
- 📝 **生成美觀的 README.md 投資報告**
- 🔄 **自動提交並推送到 GitHub**

## 🛠️ 部署步驟

### 1. 準備 GitHub 倉庫

```bash
# 1. 創建新的 GitHub 倉庫
# 2. 克隆到本地
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 3. 複製所有專案文件到倉庫目錄
```

### 2. 確保文件結構

```
your-repo/
├── .github/
│   └── workflows/
│       └── binance_analysis.yml     # GitHub Actions 工作流程
├── get_binance_data.py              # 數據獲取腳本
├── analyze_binance_data.py          # 技術分析腳本
├── generate_readme_report.py       # README 生成器
├── requirements.txt                 # Python 依賴
└── README.md                        # 將被自動更新
```

### 3. 推送到 GitHub

```bash
git add .
git commit -m "🚀 Initial commit: Binance auto analysis system"
git push origin main
```

### 4. 啟用 GitHub Actions

1. 進入 GitHub 倉庫頁面
2. 點擊 **Actions** 標籤
3. 如果看到工作流程，點擊 **Enable workflow**
4. 或者手動觸發：點擊 **Run workflow**

## ⚙️ 自定義設置

### 修改執行頻率

編輯 `.github/workflows/binance_analysis.yml`：

```yaml
on:
  schedule:
    # 每30分鐘執行
    - cron: '0,30 * * * *'
    
    # 每30分鐘執行
    # - cron: '*/30 * * * *'
    
    # 每天早上8點執行
    # - cron: '0 8 * * *'
    
    # 每週一早上9點執行
    # - cron: '0 9 * * 1'
```

### 修改分析的交易對

編輯 `get_binance_data.py` 和 `analyze_binance_data.py`：

```python
# 將 BTCUSDT 改為其他交易對
symbol = "ETHUSDT"  # 或 "SOLUSDT", "XRPUSDT" 等
```

### 自定義 README 樣式

編輯 `generate_readme_report.py` 中的 `generate_readme_content` 函數來修改報告格式。

## 🔧 故障排除

### 常見問題

1. **Actions 沒有執行**
   - 檢查倉庫是否為公開倉庫（私有倉庫有分鐘限制）
   - 確認 `.github/workflows/` 目錄結構正確

2. **推送失敗**
   - 確保倉庫有寫入權限
   - 檢查 `GITHUB_TOKEN` 權限設置

3. **Python 錯誤**
   - 檢查 `requirements.txt` 是否包含所有依賴
   - 查看 Actions 日誌中的錯誤信息

### 查看執行日誌

1. 進入 GitHub 倉庫
2. 點擊 **Actions** 標籤
3. 點擊具體的工作流程運行
4. 查看詳細日誌

## 📊 效果展示

執行成功後，您的 README.md 會自動更新為：

- 📈 實時市場數據表格
- 🔍 詳細技術指標分析
- 💡 專業交易建議
- ⏰ 自動時間戳記
- 🎨 美觀的 emoji 和格式

## 🎯 進階功能

### 添加通知功能

可以在工作流程中添加 Discord/Slack 通知：

```yaml
- name: Send Discord Notification
  run: |
    curl -H "Content-Type: application/json" \
         -d '{"content":"📊 BTCUSDT 分析報告已更新！"}' \
         ${{ secrets.DISCORD_WEBHOOK_URL }}
```

### 添加多交易對支持

修改腳本支持分析多個交易對並生成綜合報告。

### 歷史數據追蹤

可以將分析結果保存到 GitHub Issues 或 Discussions 中進行歷史追蹤。

## 🔒 安全注意事項

- 不要在代碼中硬編碼 API 密鑰
- 使用 GitHub Secrets 存儲敏感信息
- 定期檢查依賴包的安全更新

## 📞 支持

如果遇到問題：
1. 查看 GitHub Actions 執行日誌
2. 檢查本指南的故障排除部分
3. 在 GitHub Issues 中提問

---

**🎉 現在您就有了一個全自動的 Binance 投資分析系統！**
