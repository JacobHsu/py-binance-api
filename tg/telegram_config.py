#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 配置文件
Configuration file for Telegram Bot
"""

import os
from dotenv import load_dotenv

# 載入 .env 文件
load_dotenv()

class TelegramConfig:
    """Telegram Bot 配置類"""
    
    def __init__(self):
        # 從環境變數讀取配置，如果沒有則使用預設值
        self.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
        
        # 訊號發送設定
        self.SEND_BUY_SIGNALS = os.getenv("SEND_BUY_SIGNALS", "true").lower() == "true"
        self.SEND_SELL_SIGNALS = os.getenv("SEND_SELL_SIGNALS", "true").lower() == "true"
        self.SEND_MARKET_SUMMARY = os.getenv("SEND_MARKET_SUMMARY", "true").lower() == "true"
        
        # 訊號觸發條件
        self.BUY_SIGNAL_THRESHOLD = float(os.getenv("BUY_SIGNAL_THRESHOLD", "1.0"))  # 買入信號閾值 (%)
        self.SELL_SIGNAL_THRESHOLD = float(os.getenv("SELL_SIGNAL_THRESHOLD", "-1.0"))  # 賣出信號閾值 (%)
        
        # 支援的幣種
        self.SUPPORTED_SYMBOLS = os.getenv("SUPPORTED_SYMBOLS", "BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT").split(",")
        
        # 訊息格式設定
        self.MESSAGE_LANGUAGE = os.getenv("MESSAGE_LANGUAGE", "zh-TW")  # zh-TW, en
        self.INCLUDE_TECHNICAL_ANALYSIS = os.getenv("INCLUDE_TECHNICAL_ANALYSIS", "true").lower() == "true"
        
        # 進階設定
        self.MESSAGE_INTERVAL = float(os.getenv("MESSAGE_INTERVAL", "1.0"))  # 發送間隔 (秒)
        self.TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
    def is_valid(self):
        """檢查配置是否有效"""
        return bool(self.BOT_TOKEN and self.CHAT_ID)
    
    def get_missing_config(self):
        """獲取缺失的配置項目"""
        missing = []
        if not self.BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not self.CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")
        return missing

# 預設配置實例
config = TelegramConfig()

# 如果您不想使用環境變數，可以直接在這裡設定：
# config.BOT_TOKEN = "你的Bot Token"
# config.CHAT_ID = "你的Chat ID"

# 自定義設定範例：
# config.BUY_SIGNAL_THRESHOLD = 2.0  # 只有漲幅超過2%才發送買入信號
# config.SELL_SIGNAL_THRESHOLD = -2.0  # 只有跌幅超過2%才發送賣出信號
# config.SUPPORTED_SYMBOLS = ["BTCUSDT", "ETHUSDT"]  # 只監控 BTC 和 ETH