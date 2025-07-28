#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 設定腳本 (根目錄)
Setup script for Telegram Bot (from root directory)
"""

import sys
import os

# 添加 tg 模組到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tg'))

# 簡化的設定腳本
def main():
    print("🔧 Telegram Bot 設定")
    print("=" * 30)
    print("\n請按照以下步驟設定:")
    print("1. 複製配置範例: cp tg/.env.example tg/.env")
    print("2. 編輯 tg/.env 文件，填入您的 Bot Token 和 Chat ID")
    print("3. 測試功能: python tg/test_telegram_integration.py")
    print("4. 執行訊號: python run_telegram_bot.py")
    print("\n📖 詳細說明請查看: tg/README.md")

if __name__ == "__main__":
    main()