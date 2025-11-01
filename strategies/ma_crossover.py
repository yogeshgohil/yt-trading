"""
Moving Average Crossover Strategy
Classic and popular trading strategy
"""
import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators.technical import TechnicalIndicators

class MACrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover Strategy
    
    Logic:
    - BUY when short MA crosses above long MA (Golden Cross)
    - SELL when short MA crosses below long MA (Death Cross)
    
    Parameters:
    - short_period: Short MA period (default: 20)
    - long_period: Long MA period (default: 50)
    """
    
    def __init__(self, data_fetcher, short_period: int = 20, long_period: int = 50):
        """
        Initialize MA Crossover Strategy
        
        Args:
            data_fetcher: Data fetcher instance
            short_period: Short moving average period
            long_period: Long moving average period
        """
        super().__init__(data_fetcher, name="MA Crossover Strategy")
        self.short_period = short_period
        self.long_period = long_period
        
        print(f"✅ {self.name} initialized")
        print(f"   Short MA: {short_period}, Long MA: {long_period}")
    
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add indicators to data
        
        Args:
            data: Raw OHLCV data
        
        Returns:
            DataFrame with indicators
        """
        df = data.copy()
        
        # Calculate moving averages
        df['MA_Short'] = TechnicalIndicators.calculate_sma(df, self.short_period)
        df['MA_Long'] = TechnicalIndicators.calculate_sma(df, self.long_period)
        
        # Calculate crossover signals
        df['MA_Diff'] = df['MA_Short'] - df['MA_Long']
        df['MA_Diff_Prev'] = df['MA_Diff'].shift(1)
        
        # Identify crossovers
        df['Golden_Cross'] = (df['MA_Diff'] > 0) & (df['MA_Diff_Prev'] <= 0)
        df['Death_Cross'] = (df['MA_Diff'] < 0) & (df['MA_Diff_Prev'] >= 0)
        
        return df
    
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        Generate trading signal
        
        Args:
            data: DataFrame with indicators
        
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        if len(data) < self.long_period:
            return 'HOLD'
        
        latest = data.iloc[-1]
        
        if latest['Golden_Cross']:
            return 'BUY'
        elif latest['Death_Cross']:
            return 'SELL'
        else:
            return 'HOLD'
    
    def should_enter(self, data: pd.DataFrame) -> bool:
        """
        Check if should enter position
        
        Args:
            data: DataFrame with indicators
        
        Returns:
            True if should enter
        """
        signal = self.generate_signal(data)
        return signal == 'BUY'
    
    def should_exit(self, data: pd.DataFrame, position: dict) -> bool:
        """
        Check if should exit position
        
        Args:
            data: DataFrame with indicators
            position: Current position
        
        Returns:
            True if should exit
        """
        signal = self.generate_signal(data)
        return signal == 'SELL'
    
    def backtest(self, symbol: str, from_date: str, to_date: str):
        """
        Backtest the strategy on historical data
        
        Args:
            symbol: Stock symbol
            from_date: Start date
            to_date: End date
        """
        print(f"\n📊 Backtesting {self.name} on {symbol}")
        print(f"   Period: {from_date} to {to_date}")
        
        # Fetch data
        data = self.data_fetcher.get_historical_data(symbol, from_date, to_date)
        
        if data.empty:
            print("❌ No data available for backtesting")
            return
        
        # Prepare data with indicators
        data = self.prepare_data(data)
        
        # Simulate trading
        in_position = False
        
        for i in range(self.long_period, len(data)):
            current_data = data.iloc[:i+1]
            current_price = current_data['Close'].iloc[-1]
            
            if not in_position:
                # Check for entry
                if self.should_enter(current_data):
                    quantity = self.calculate_position_size(current_price)
                    self.enter_position(symbol, current_price, quantity)
                    in_position = True
            else:
                # Check for exit
                if self.should_exit(current_data, self.positions.get(symbol)):
                    self.exit_position(symbol, current_price)
                    in_position = False
        
        # Close any open positions
        if symbol in self.positions:
            final_price = data['Close'].iloc[-1]
            self.exit_position(symbol, final_price)
        
        # Print results
        self.print_performance()
    
    def run_live(self, symbols: list, check_interval: int = 60):
        """
        Run strategy on live data
        
        Args:
            symbols: List of symbols to trade
            check_interval: Check interval in seconds
        """
        print(f"\n🚀 Running {self.name} live...")
        print(f"   Symbols: {symbols}")
        print(f"   Check interval: {check_interval}s")
        print("\n⚠️  This is for demonstration. Implement proper live trading logic.")


# Test the strategy
if __name__ == "__main__":
    print("🧪 Testing MA Crossover Strategy...\n")
    
    from data.free_fetcher import FreeFetcher
    
    # Initialize
    fetcher = FreeFetcher()
    strategy = MACrossoverStrategy(fetcher, short_period=20, long_period=50)
    
    # Backtest
    strategy.backtest('RELIANCE', '2023-01-01', '2024-12-31')
    
    print("\n✅ Strategy test complete!")

