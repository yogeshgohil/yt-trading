"""
Logging utility for the trading application
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class TradingLogger:
    """
    Custom logger for trading application
    Logs to both file and console
    """
    
    def __init__(self, name: str = "TradingApp", log_dir: str = "logs", 
                 level: str = "INFO"):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler - detailed logs
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler - simple logs
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger initialized: {name}")
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def trade(self, action: str, symbol: str, price: float, quantity: int):
        """
        Log a trade action
        
        Args:
            action: Trade action (BUY, SELL)
            symbol: Stock symbol
            price: Trade price
            quantity: Number of shares
        """
        self.logger.info(f"TRADE | {action} | {symbol} | Price: ₹{price} | Qty: {quantity}")
    
    def signal(self, strategy: str, symbol: str, signal_type: str):
        """
        Log a trading signal
        
        Args:
            strategy: Strategy name
            symbol: Stock symbol
            signal_type: Signal type (BUY, SELL, HOLD)
        """
        self.logger.info(f"SIGNAL | {strategy} | {symbol} | {signal_type}")
    
    def performance(self, strategy: str, metrics: dict):
        """
        Log strategy performance
        
        Args:
            strategy: Strategy name
            metrics: Performance metrics dictionary
        """
        self.logger.info(f"PERFORMANCE | {strategy} | Trades: {metrics.get('total_trades', 0)} | "
                        f"Win Rate: {metrics.get('win_rate', 0):.2f}% | "
                        f"Profit: ₹{metrics.get('total_profit', 0):.2f}")


# Global logger instance
_global_logger: Optional[TradingLogger] = None

def get_logger(name: str = "TradingApp") -> TradingLogger:
    """
    Get or create global logger instance
    
    Args:
        name: Logger name
    
    Returns:
        TradingLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = TradingLogger(name)
    return _global_logger


# Test the logger
if __name__ == "__main__":
    print("🧪 Testing Trading Logger...\n")
    
    # Create logger
    logger = TradingLogger("TestLogger")
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test trade logging
    logger.trade("BUY", "RELIANCE", 2500, 10)
    logger.trade("SELL", "TCS", 3500, 5)
    
    # Test signal logging
    logger.signal("MA Crossover", "INFY", "BUY")
    
    # Test performance logging
    metrics = {
        'total_trades': 10,
        'win_rate': 60,
        'total_profit': 5000
    }
    logger.performance("RSI Strategy", metrics)
    
    print("\n✅ Logger test complete!")
    print(f"📁 Check logs in: logs/")

