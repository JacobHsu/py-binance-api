# 📁 專案結構說明

## 🗂️ 目錄結構

```
Binance_py/
├── 📁 .github/workflows/          # GitHub Actions 工作流程
│   └── binance_analysis.yml       # 自動化分析工作流程
│
├── 📁 data/                       # 數據文件目錄 (自動生成，已忽略版本控制)
│   ├── BTCUSDT_klines_1h.csv     # Bitcoin K線數據
│   ├── BTCUSDT_ticker_24hr.json  # Bitcoin 24小時行情
│   ├── ETHUSDT_klines_1h.csv     # Ethereum K線數據
│   ├── ETHUSDT_ticker_24hr.json  # Ethereum 24小時行情
│   ├── SOLUSDT_klines_1h.csv     # Solana K線數據
│   ├── SOLUSDT_ticker_24hr.json  # Solana 24小時行情
│   ├── DOGEUSDT_klines_1h.csv    # Dogecoin K線數據
│   ├── DOGEUSDT_ticker_24hr.json # Dogecoin 24小時行情
│   ├── XRPUSDT_klines_1h.csv     # Ripple K線數據
│   ├── XRPUSDT_ticker_24hr.json  # Ripple 24小時行情
│   ├── ADAUSDT_klines_1h.csv     # Cardano K線數據
│   ├── ADAUSDT_ticker_24hr.json  # Cardano 24小時行情
│   └── multi_investment_report.json # 綜合分析報告
│
├── 📁 docs/                       # 文檔目錄
│   ├── DEPLOYMENT_GUIDE.md        # 部署指南
│   ├── MULTI_CRYPTO_GUIDE.md      # 多幣種系統指南
│   ├── deploy_to_github.md        # GitHub 部署說明
│   └── PROJECT_SUMMARY.md         # 專案總結
│
├── 📁 tests/                      # 測試腳本目錄
│   ├── test_full_workflow.py      # 完整工作流程測試
│   └── test_multi_crypto.py       # 多幣種系統測試
│
├── 📁 tg/                          # Telegram Bot 模組
│   ├── telegram_bot.py            # 核心 Bot 功能
│   ├── telegram_config.py         # 配置管理 (.env 支援)
│   ├── run_telegram_signals.py    # 主執行腳本
│   ├── test_telegram_integration.py # 測試腳本
│   ├── .env.example               # 配置範例
│   ├── README.md                  # 模組說明
│   └── USAGE.md                   # 使用說明
│
├── 📁 cloud_deployment/           # 雲端部署文件
│   ├── 📁 api/                    # Vercel API 目錄
│   │   └── analyze.py             # Vercel 分析 API
│   ├── lambda_function.py         # AWS Lambda 函數
│   ├── main.py                    # Google Cloud Function
│   ├── scheduled_analysis.py      # Heroku 排程腳本
│   ├── Procfile                   # Heroku 配置
│   └── vercel.json               # Vercel 配置
│
├── 📄 核心腳本 (根目錄)
│   ├── get_binance_data.py        # 數據獲取腳本
│   ├── analyze_binance_data.py    # 技術分析腳本
│   ├── generate_readme_report.py  # README 報告生成器
│   ├── run_telegram_bot.py        # Telegram Bot 執行入口
│   ├── setup_telegram.py          # Telegram Bot 設定入口
│   ├── requirements.txt           # Python 依賴清單
│   └── .gitignore                 # Git 忽略文件配置
│
└── 📄 README.md                   # 自動生成的投資分析報告
```

## 📋 文件分類說明

### 🔧 核心功能文件 (根目錄)
- **`get_binance_data.py`**: 從 Binance API 獲取多幣種數據
- **`analyze_binance_data.py`**: 執行技術分析 (MA, MACD, BOLL, RSI, KDJ)
- **`generate_readme_report.py`**: 生成虛擬幣1h投資分析報告
- **`run_telegram_bot.py`**: Telegram Bot 執行入口 (從根目錄)
- **`setup_telegram.py`**: Telegram Bot 設定入口 (從根目錄)
- **`requirements.txt`**: Python 依賴包清單 (包含 python-dotenv)
- **`.gitignore`**: 版本控制忽略配置 (已排除 .env 文件)

### 📱 Telegram Bot 模組 (`tg/`)
- **`telegram_bot.py`**: 核心 Bot 功能 (發送訊號、市場總覽)
- **`telegram_config.py`**: 配置管理 (支援 .env 文件)
- **`run_telegram_signals.py`**: 主執行腳本
- **`test_telegram_integration.py`**: 完整功能測試
- **`.env.example`**: 配置範例文件
- **`USAGE.md`**: 詳細使用說明
- **注意**: 精簡的執行模組，專注於核心功能

### 📊 數據文件 (`data/`)
- **K線數據**: `*_klines_1h.csv` - 500根1小時K線數據
- **行情數據**: `*_ticker_24hr.json` - 24小時行情統計
- **分析報告**: `multi_investment_report.json` - 綜合技術分析結果
- **注意**: 此目錄已加入 `.gitignore`，數據會自動生成

### 📚 文檔資料 (`docs/`)
- **`DEPLOYMENT_GUIDE.md`**: GitHub Actions 部署完整指南
- **`MULTI_CRYPTO_GUIDE.md`**: 多幣種系統使用說明
- **`deploy_to_github.md`**: 快速部署步驟
- **`PROJECT_SUMMARY.md`**: 專案功能總結

### 🧪 測試腳本 (`tests/`)
- **`test_full_workflow.py`**: 測試完整分析流程
- **`test_multi_crypto.py`**: 測試多幣種功能
- **執行方式**: `python tests/test_multi_crypto.py`

### ☁️ 雲端部署 (`cloud_deployment/`)
- **AWS Lambda**: `lambda_function.py`
- **Google Cloud**: `main.py`
- **Vercel**: `vercel.json` + `api/analyze.py`
- **Heroku**: `Procfile` + `scheduled_analysis.py`

### 🤖 GitHub Actions (`.github/workflows/`)
- **`binance_analysis.yml`**: 每小時自動執行工作流程
- 自動獲取數據 → 分析 → 生成報告 → 推送更新

## 🔄 工作流程

### 1. 數據獲取
```bash
python get_binance_data.py
# 輸出: data/ 目錄中的 CSV 和 JSON 文件
```

### 2. 技術分析
```bash
python analyze_binance_data.py
# 輸出: data/multi_investment_report.json
```

### 3. 報告生成
```bash
python generate_readme_report.py
# 輸出: README.md (虛擬幣1h投資分析報告)
```

### 4. Telegram 訊號發送 (新功能)
```bash
# 配置 .env 文件
cp tg/.env.example tg/.env
# 編輯 tg/.env 填入 Bot Token 和 Chat ID

# 發送投資訊號
python run_telegram_bot.py
# 輸出: 自動發送買入/賣出訊號到 Telegram
```

### 5. 自動化執行
- GitHub Actions 每小時自動執行上述流程
- 自動提交並推送更新的 README.md
- 可選: 同時發送 Telegram 訊號

## 🎯 使用建議

### 本地開發
1. 執行 `python tests/test_multi_crypto.py` 測試系統
2. 查看 `data/` 目錄確認數據生成
3. 檢查 `README.md` 報告內容

### 部署到 GitHub
1. 參考 `docs/DEPLOYMENT_GUIDE.md`
2. 推送代碼到 GitHub 倉庫
3. 啟用 GitHub Actions
4. 每小時自動更新投資分析報告

### 雲端部署
1. 選擇適合的雲端平台
2. 使用 `cloud_deployment/` 中對應的配置文件
3. 參考各平台的部署說明

## 📝 維護說明

### 添加新幣種
1. 修改 `get_binance_data.py` 和 `analyze_binance_data.py` 中的 `symbols` 列表
2. 更新 `generate_readme_report.py` 中的 emoji 和名稱映射

### 修改執行頻率
1. 編輯 `.github/workflows/binance_analysis.yml`
2. 修改 `cron` 表達式

### 自定義報告格式
1. 編輯 `generate_readme_report.py` 中的 `generate_readme_content` 函數
2. 調整 README 模板和樣式

---

**🎉 現在您的專案結構清晰有序，便於維護和擴展！**
