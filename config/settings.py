"""
Configuration settings for the Trading Application
Toggle between FREE and KITE data sources easily
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    """Application Settings"""
    
    # ========================================
    # DATA SOURCE CONFIGURATION
    # ========================================
    # Toggle between "FREE" and "KITE"
    # FREE = Use NSEpy/yfinance (no cost)
    # KITE = Use Kite Connect API (₹2,000/month)
    DATA_SOURCE = "FREE"  # Change to "KITE" when ready for live trading
    
    # ========================================
    # FREE DATA SOURCE SETTINGS
    # ========================================
    USE_NSEPY = True
    USE_YFINANCE = True
    
    # ========================================
    # KITE CONNECT API SETTINGS
    # ========================================
    # Get these from: https://developers.kite.trade/
    KITE_API_KEY = ""  # Add your API key when you subscribe
    KITE_API_SECRET = ""  # Add your API secret
    KITE_ACCESS_TOKEN = ""  # Generated after login
    
    # ========================================
    # TRADING SETTINGS
    # ========================================
    # Default capital for backtesting
    INITIAL_CAPITAL = 100000  # ₹1,00,000
    
    # Position sizing
    POSITION_SIZE_PERCENT = 0.1  # Use 10% of capital per trade
    
    # Risk management
    STOP_LOSS_PERCENT = 0.02  # 2% stop loss
    TARGET_PERCENT = 0.05  # 5% target
    
    # Trading hours (IST)
    MARKET_OPEN_TIME = "09:15"
    MARKET_CLOSE_TIME = "15:30"
    
    # ========================================
    # STRATEGY SETTINGS
    # ========================================
    # Moving Average periods
    MA_SHORT_PERIOD = 20
    MA_LONG_PERIOD = 50
    
    # RSI settings
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    # MACD settings
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # Bollinger Bands
    BB_PERIOD = 20
    BB_STD = 2
    
    # ========================================
    # DATABASE SETTINGS
    # ========================================
    DATABASE_PATH = BASE_DIR / "data" / "trading.db"
    
    # ========================================
    # LOGGING SETTINGS
    # ========================================
    LOG_DIR = BASE_DIR / "logs"
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # ========================================
    # BACKTESTING SETTINGS
    # ========================================
    BACKTEST_START_DATE = "2023-01-01"
    BACKTEST_END_DATE = "2024-12-31"
    
    # ========================================
    # STOCK WATCHLIST
    # ========================================
    # Top Indian stocks for trading
    WATCHLIST = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "BHARTIARTL",
        "ITC",
        "KOTAKBANK",
        "LT"
    ]
    
    @classmethod
    def is_kite_configured(cls):
        """Check if Kite API credentials are configured"""
        return bool(cls.KITE_API_KEY and cls.KITE_API_SECRET)
    
    @classmethod
    def get_data_source(cls):
        """Get the current data source"""
        if cls.DATA_SOURCE == "KITE" and not cls.is_kite_configured():
            print("⚠️  Warning: Kite selected but not configured. Using FREE data.")
            return "FREE"
        return cls.DATA_SOURCE
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        directories = [
            BASE_DIR / "data",
            BASE_DIR / "data" / "historical",
            BASE_DIR / "logs",
            BASE_DIR / "reports"
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Create directories on import
Settings.create_directories()

