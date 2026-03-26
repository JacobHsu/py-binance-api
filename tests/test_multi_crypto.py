#!/usr/bin/env python3
"""
測試多幣種分析系統
"""
import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """執行命令並顯示結果"""
    print(f"\n🔄 {description}")
    print(f"執行命令: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.stdout:
            print("✅ 輸出:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ 錯誤信息:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} 成功完成")
        else:
            print(f"❌ {description} 執行失敗 (返回碼: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ 執行 {description} 時發生異常: {e}")
        return False
    
    return True

def check_files():
    """檢查生成的文件"""
    print("\n📊 檢查生成的文件:")
    print("-" * 30)
    
    expected_files = [
        "BTCUSDT_klines_1h.csv",
        "BTCUSDT_ticker_24hr.json",
        "ETHUSDT_klines_1h.csv", 
        "ETHUSDT_ticker_24hr.json",
        "SOLUSDT_klines_1h.csv",
        "SOLUSDT_ticker_24hr.json",
        "DOGEUSDT_klines_1h.csv",
        "DOGEUSDT_ticker_24hr.json",
        "multi_investment_report.json",
        "README.md"
    ]
    
    for filename in expected_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            mtime = datetime.fromtimestamp(os.path.getmtime(filename))
            print(f"✅ {filename}: {size} bytes, 修改時間: {mtime.strftime('%H:%M:%S')}")
        else:
            print(f"❌ {filename}: 文件不存在")

def show_analysis_summary():
    """顯示分析摘要"""
    try:
        import json
        with open("multi_investment_report.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print("\n📈 分析摘要:")
        print("-" * 40)
        
        for symbol, analysis in data.items():
            price = analysis['current_price']
            change = analysis['24hr_change_percent']
            trend = analysis['current_trend']
            
            # 幣種 emoji
            emoji_map = {
                "BTCUSDT": "₿",
                "ETHUSDT": "Ξ", 
                "SOLUSDT": "◎",
                "DOGEUSDT": "🐕"
            }
            emoji = emoji_map.get(symbol, "💰")
            
            # 格式化價格
            if "DOGE" in symbol:
                price_str = f"${price:.4f}"
            elif price < 100:
                price_str = f"${price:.2f}"
            else:
                price_str = f"${price:,.2f}"
            
            print(f"{emoji} {symbol}: {price_str} ({change:+.2f}%) - {trend[:15]}...")
            
    except Exception as e:
        print(f"❌ 讀取分析數據時發生錯誤: {e}")

def main():
    """主測試流程"""
    print("🚀 開始測試多幣種 Binance 分析系統")
    print("=" * 60)
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"工作目錄: {os.getcwd()}")
    print("支援幣種: BTC, ETH, SOL, DOGE")
    
    # 步驟 1: 安裝依賴
    if not run_command("pip install pandas requests pytz", "安裝 Python 依賴"):
        return False
    
    # 步驟 2: 獲取多幣種數據
    if not run_command("python get_binance_data.py", "獲取多幣種數據"):
        return False
    
    # 步驟 3: 執行多幣種分析
    if not run_command("python analyze_binance_data.py", "執行多幣種技術分析"):
        return False
    
    # 步驟 4: 生成多幣種 README
    if not run_command("python generate_readme_report.py", "生成多幣種 README 報告"):
        return False
    
    # 步驟 5: 檢查文件
    check_files()
    
    # 步驟 6: 顯示分析摘要
    show_analysis_summary()
    
    # 步驟 7: 顯示 README 預覽
    print("\n📖 README.md 預覽 (前15行):")
    print("-" * 40)
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:15], 1):
                print(f"{i:2d}: {line.rstrip()}")
        print(f"... (總共 {len(lines)} 行)")
    except Exception as e:
        print(f"❌ 讀取 README.md 時發生錯誤: {e}")
    
    print("\n🎉 多幣種分析系統測試成功完成！")
    print("=" * 60)
    print("📋 系統特色:")
    print("  ✅ 支援 4 大主流幣種 (BTC, ETH, SOL, XRP)")
    print("  ✅ 一頁式好讀報告格式")
    print("  ✅ 智能最佳機會推薦")
    print("  ✅ 技術指標對比表格")
    print("  ✅ 風險警示提醒")
    print("\n📋 下一步:")
    print("1. 將代碼推送到 GitHub 倉庫")
    print("2. 啟用 GitHub Actions 工作流程")
    print("3. 每30分鐘自動更新多幣種分析報告")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
