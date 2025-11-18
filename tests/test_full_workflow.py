#!/usr/bin/env python3
"""
測試完整工作流程
模擬 GitHub Actions 的執行過程
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

def check_file_exists(filename, description):
    """檢查文件是否存在"""
    if os.path.exists(filename):
        print(f"✅ {description} 存在: {filename}")
        return True
    else:
        print(f"❌ {description} 不存在: {filename}")
        return False

def main():
    """主測試流程"""
    print("🚀 開始測試完整的 Binance 分析工作流程")
    print("=" * 60)
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"工作目錄: {os.getcwd()}")
    
    # 步驟 1: 檢查 Python 環境
    if not run_command("python --version", "檢查 Python 版本"):
        return False
    
    # 步驟 2: 安裝依賴
    if not run_command("pip install -r requirements.txt", "安裝 Python 依賴"):
        return False
    
    # 步驟 3: 執行數據獲取
    if not run_command("python get_binance_data.py", "獲取 Binance 數據"):
        return False
    
    # 檢查數據文件
    if not check_file_exists("BTCUSDT_klines_1h.csv", "K線數據文件"):
        return False
    if not check_file_exists("BTCUSDT_ticker_24hr.json", "24小時行情數據文件"):
        return False
    
    # 步驟 4: 執行技術分析
    if not run_command("python analyze_binance_data.py", "執行技術分析"):
        return False
    
    # 檢查分析報告
    if not check_file_exists("investment_report.json", "投資分析報告"):
        return False
    
    # 步驟 5: 生成 README 報告
    if not run_command("python generate_readme_report.py", "生成 README 報告"):
        return False
    
    # 檢查 README 文件
    if not check_file_exists("README.md", "README 報告文件"):
        return False
    
    # 步驟 6: 顯示生成的文件信息
    print("\n📊 生成的文件信息:")
    print("-" * 30)
    
    files_to_check = [
        "BTCUSDT_klines_1h.csv",
        "BTCUSDT_ticker_24hr.json", 
        "investment_report.json",
        "README.md"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            mtime = datetime.fromtimestamp(os.path.getmtime(filename))
            print(f"📄 {filename}: {size} bytes, 修改時間: {mtime.strftime('%H:%M:%S')}")
    
    # 步驟 7: 顯示 README 預覽
    print("\n📖 README.md 預覽 (前20行):")
    print("-" * 40)
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:2d}: {line.rstrip()}")
        if len(lines) > 20:
            print(f"... (還有 {len(lines) - 20} 行)")
    except Exception as e:
        print(f"❌ 讀取 README.md 時發生錯誤: {e}")
    
    print("\n🎉 完整工作流程測試成功完成！")
    print("=" * 60)
    print("📋 下一步:")
    print("1. 將代碼推送到 GitHub 倉庫")
    print("2. 確保 .github/workflows/binance_analysis.yml 文件存在")
    print("3. 在 GitHub Actions 中啟用工作流程")
    print("4. 等待每30分鐘自動執行或手動觸發測試")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
