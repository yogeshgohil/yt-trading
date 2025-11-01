"""
Base Data Fetcher Interface
This interface ensures both Free and Kite fetchers work the same way
"""
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class BaseFetcher(ABC):
    """
    Abstract base class for data fetchers
    Both FreeFetcher and KiteFetcher implement this interface
    """
    
    @abstractmethod
    def get_historical_data(self, symbol: str, from_date: str, to_date: str, interval: str = "day") -> pd.DataFrame:
        """
        Get historical OHLCV data
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE')
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            interval: Data interval (day, minute, etc.)
        
        Returns:
            DataFrame with columns: Date, Open, High, Low, Close, Volume
        """
        pass
    
    @abstractmethod
    def get_live_price(self, symbol: str) -> float:
        """
        Get current/latest price of a symbol
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Current price as float
        """
        pass
    
    @abstractmethod
    def get_quote(self, symbol: str) -> dict:
        """
        Get detailed quote information
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Dictionary with quote details (last_price, open, high, low, volume, etc.)
        """
        pass
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate if data has required columns
        
        Args:
            data: DataFrame to validate
        
        Returns:
            True if valid, False otherwise
        """
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in data.columns for col in required_columns)
    
    def format_symbol(self, symbol: str) -> str:
        """
        Format symbol for the data source
        Override in child classes if needed
        
        Args:
            symbol: Original symbol
        
        Returns:
            Formatted symbol
        """
        return symbol.upper()

