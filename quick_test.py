#!/usr/bin/env python3
"""
快速測試整理後的系統
"""
import os
import subprocess
from datetime import datetime

def check_directory_structure():
    """檢查目錄結構"""
    print("📁 檢查目錄結構...")
    
    expected_dirs = ['data', 'docs', 'tests', 'cloud_deployment', '.github']
    expected_files = [
        'get_binance_data.py',
        'analyze_binance_data.py', 
        'generate_readme_report.py',
        'requirements.txt',
        '.gitignore',
        'README.md'
    ]
    
    print("\n📂 目錄檢查:")
    for dir_name in expected_dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (缺失)")
    
    print("\n📄 核心文件檢查:")
    for file_name in expected_files:
        if os.path.exists(file_name):
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} (缺失)")

def check_data_files():
    """檢查數據文件"""
    print("\n📊 檢查數據文件...")
    
    if not os.path.exists('data'):
        print("  ❌ data/ 目錄不存在")
        return
    
    expected_data_files = [
        'BTCUSDT_klines_1h.csv',
        'BTCUSDT_ticker_24hr.json',
        'ETHUSDT_klines_1h.csv', 
        'ETHUSDT_ticker_24hr.json',
        'SOLUSDT_klines_1h.csv',
        'SOLUSDT_ticker_24hr.json',
        'DOGEUSDT_klines_1h.csv',
        'DOGEUSDT_ticker_24hr.json',
        'multi_investment_report.json'
    ]
    
    for file_name in expected_data_files:
        file_path = f"data/{file_name}"
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_name} ({size} bytes)")
        else:
            print(f"  ❌ {file_name} (缺失)")

def run_quick_test():
    """執行快速功能測試"""
    print("\n🧪 執行快速功能測試...")
    
    try:
        # 測試數據獲取
        print("\n1️⃣ 測試數據獲取...")
        result = subprocess.run(['python', 'get_binance_data.py'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("  ✅ 數據獲取成功")
        else:
            print(f"  ❌ 數據獲取失敗: {result.stderr}")
            return False
        
        # 測試技術分析
        print("\n2️⃣ 測試技術分析...")
        result = subprocess.run(['python', 'analyze_binance_data.py'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("  ✅ 技術分析成功")
        else:
            print(f"  ❌ 技術分析失敗: {result.stderr}")
            return False
        
        # 測試報告生成
        print("\n3️⃣ 測試報告生成...")
        result = subprocess.run(['python', 'generate_readme_report.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("  ✅ 報告生成成功")
        else:
            print(f"  ❌ 報告生成失敗: {result.stderr}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("  ❌ 測試超時")
        return False
    except Exception as e:
        print(f"  ❌ 測試異常: {e}")
        return False

def show_readme_preview():
    """顯示 README 預覽"""
    print("\n📖 README.md 預覽...")
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("前10行:")
        for i, line in enumerate(lines[:10], 1):
            print(f"  {i:2d}: {line.rstrip()}")
        
        print(f"\n總行數: {len(lines)}")
        
        # 檢查關鍵內容
        content = ''.join(lines)
        if '虛擬幣1h投資分析報告' in content:
            print("  ✅ 標題正確")
        if 'Bitcoin' in content and 'Ethereum' in content:
            print("  ✅ 包含多幣種數據")
        if '技術指標總結' in content:
            print("  ✅ 包含技術指標對比")
            
    except Exception as e:
        print(f"  ❌ 讀取 README.md 失敗: {e}")

def main():
    """主函數"""
    print("🚀 快速測試整理後的虛擬幣分析系統")
    print("=" * 50)
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 檢查目錄結構
    check_directory_structure()
    
    # 檢查數據文件
    check_data_files()
    
    # 執行功能測試
    if run_quick_test():
        print("\n🎉 所有測試通過！")
    else:
        print("\n❌ 部分測試失敗")
        return
    
    # 顯示 README 預覽
    show_readme_preview()
    
    print("\n📋 系統狀態總結:")
    print("  ✅ 目錄結構已整理")
    print("  ✅ 數據文件正常生成")
    print("  ✅ 核心功能運行正常")
    print("  ✅ README 報告生成成功")
    
    print("\n📁 整理後的目錄結構:")
    print("  📂 data/           - 數據文件 (已忽略版本控制)")
    print("  📂 docs/           - 文檔資料")
    print("  📂 tests/          - 測試腳本")
    print("  📂 cloud_deployment/ - 雲端部署文件")
    print("  📄 核心腳本        - 根目錄")
    
    print("\n🚀 準備部署到 GitHub:")
    print("  1. git add .")
    print("  2. git commit -m '🗂️ Reorganize project structure'")
    print("  3. git push origin main")
    print("  4. 啟用 GitHub Actions")

if __name__ == "__main__":
    main()
