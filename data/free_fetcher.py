"""
Free Data Fetcher using NSEpy and yfinance
No API costs - Perfect for development and backtesting
"""
import pandas as pd
from datetime import datetime, date, timedelta
import yfinance as yf
from typing import Optional
import warnings
warnings.filterwarnings('ignore')

from data.base_fetcher import BaseFetcher

class FreeFetcher(BaseFetcher):
    """
    Free data fetcher using NSEpy and yfinance
    No API key required - completely FREE!
    """
    
    def __init__(self):
        """Initialize free data fetcher"""
        self.source = "yfinance"  # Primary source
        print("✅ Free Data Fetcher initialized (using yfinance)")
        print("💡 Note: Data may be delayed by 15-20 minutes")
    
    def get_historical_data(self, symbol: str, from_date: str, to_date: str, interval: str = "day") -> pd.DataFrame:
        """
        Get historical OHLCV data from yfinance
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE')
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            interval: Data interval (1d, 1h, 1m, etc.)
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Format symbol for NSE
            formatted_symbol = self._format_nse_symbol(symbol)
            
            # Map interval
            interval_map = {
                'day': '1d',
                'hour': '1h',
                'minute': '1m',
                '1d': '1d',
                '1h': '1h',
                '1m': '1m'
            }
            yf_interval = interval_map.get(interval, '1d')
            
            # Download data
            data = yf.download(
                formatted_symbol,
                start=from_date,
                end=to_date,
                interval=yf_interval,
                progress=False
            )
            
            if data.empty:
                print(f"⚠️  No data found for {symbol}")
                return pd.DataFrame()
            
            # Clean and format data
            data = data.reset_index()
            data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
            
            # Ensure required columns exist
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            elif 'Datetime' in data.columns:
                data['Date'] = pd.to_datetime(data['Datetime'])
                data = data.drop('Datetime', axis=1)
            
            # Validate data
            if self.validate_data(data):
                print(f"✅ Fetched {len(data)} rows for {symbol}")
                return data
            else:
                print(f"⚠️  Invalid data format for {symbol}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_live_price(self, symbol: str) -> float:
        """
        Get latest closing price (simulated live price)
        Note: This is delayed data, not real-time
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Latest closing price
        """
        try:
            formatted_symbol = self._format_nse_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            
            # Try to get current price
            data = ticker.history(period='1d')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            
            # Fallback to info
            info = ticker.info
            return float(info.get('currentPrice', 0) or info.get('regularMarketPrice', 0))
            
        except Exception as e:
            print(f"❌ Error fetching live price for {symbol}: {str(e)}")
            return 0.0
    
    def get_quote(self, symbol: str) -> dict:
        """
        Get detailed quote information
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Dictionary with quote details
        """
        try:
            formatted_symbol = self._format_nse_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            info = ticker.info
            
            # Get latest day data
            hist = ticker.history(period='1d')
            
            quote = {
                'symbol': symbol,
                'last_price': float(hist['Close'].iloc[-1]) if not hist.empty else 0,
                'open': float(hist['Open'].iloc[-1]) if not hist.empty else 0,
                'high': float(hist['High'].iloc[-1]) if not hist.empty else 0,
                'low': float(hist['Low'].iloc[-1]) if not hist.empty else 0,
                'volume': int(hist['Volume'].iloc[-1]) if not hist.empty else 0,
                'prev_close': float(info.get('previousClose', 0)),
                'change': 0,
                'change_percent': 0
            }
            
            # Calculate change
            if quote['prev_close'] > 0:
                quote['change'] = quote['last_price'] - quote['prev_close']
                quote['change_percent'] = (quote['change'] / quote['prev_close']) * 100
            
            return quote
            
        except Exception as e:
            print(f"❌ Error fetching quote for {symbol}: {str(e)}")
            return {'symbol': symbol, 'last_price': 0}
    
    def get_multiple_quotes(self, symbols: list) -> dict:
        """
        Get quotes for multiple symbols
        
        Args:
            symbols: List of stock symbols
        
        Returns:
            Dictionary with symbol as key and quote as value
        """
        quotes = {}
        for symbol in symbols:
            quotes[symbol] = self.get_quote(symbol)
        return quotes
    
    def _format_nse_symbol(self, symbol: str) -> str:
        """
        Format symbol for NSE on yfinance
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Formatted symbol (e.g., RELIANCE.NS)
        """
        symbol = symbol.upper().strip()
        if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
            symbol = f"{symbol}.NS"  # NSE by default
        return symbol
    
    def test_connection(self) -> bool:
        """
        Test if data fetcher is working
        
        Returns:
            True if working, False otherwise
        """
        try:
            # Try to fetch data for a popular stock
            data = self.get_historical_data(
                'RELIANCE',
                (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                datetime.now().strftime('%Y-%m-%d')
            )
            return not data.empty
        except:
            return False


# Quick test when running this file directly
if __name__ == "__main__":
    print("🧪 Testing Free Data Fetcher...\n")
    
    fetcher = FreeFetcher()
    
    # Test 1: Historical data
    print("\n📊 Test 1: Fetching historical data for RELIANCE")
    data = fetcher.get_historical_data(
        'RELIANCE',
        '2024-01-01',
        '2024-12-31'
    )
    if not data.empty:
        print(f"✅ Success! Got {len(data)} rows")
        print(data.head())
    
    # Test 2: Live price
    print("\n💰 Test 2: Fetching live price for TCS")
    price = fetcher.get_live_price('TCS')
    print(f"✅ TCS Price: ₹{price}")
    
    # Test 3: Quote
    print("\n📈 Test 3: Fetching quote for INFY")
    quote = fetcher.get_quote('INFY')
    print(f"✅ INFY Quote: {quote}")
    
    # Test 4: Connection test
    print("\n🔗 Test 4: Testing connection")
    if fetcher.test_connection():
        print("✅ Connection test passed!")
    else:
        print("❌ Connection test failed!")

