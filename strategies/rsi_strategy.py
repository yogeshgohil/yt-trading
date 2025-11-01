"""
RSI (Relative Strength Index) Strategy
Mean reversion strategy based on RSI indicator
"""
import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators.technical import TechnicalIndicators

class RSIStrategy(BaseStrategy):
    """
    RSI Trading Strategy
    
    Logic:
    - BUY when RSI < oversold level (default: 30)
    - SELL when RSI > overbought level (default: 70)
    
    This is a mean reversion strategy
    """
    
    def __init__(self, data_fetcher, rsi_period: int = 14, 
                 oversold: int = 30, overbought: int = 70):
        """
        Initialize RSI Strategy
        
        Args:
            data_fetcher: Data fetcher instance
            rsi_period: RSI calculation period
            oversold: Oversold threshold (buy signal)
            overbought: Overbought threshold (sell signal)
        """
        super().__init__(data_fetcher, name="RSI Strategy")
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
        print(f"✅ {self.name} initialized")
        print(f"   RSI Period: {rsi_period}")
        print(f"   Oversold: {oversold}, Overbought: {overbought}")
    
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add RSI indicator to data
        
        Args:
            data: Raw OHLCV data
        
        Returns:
            DataFrame with RSI
        """
        df = data.copy()
        
        # Calculate RSI
        df['RSI'] = TechnicalIndicators.calculate_rsi(df, self.rsi_period)
        
        # Previous RSI for crossover detection
        df['RSI_Prev'] = df['RSI'].shift(1)
        
        # Signal flags
        df['Oversold'] = df['RSI'] < self.oversold
        df['Overbought'] = df['RSI'] > self.overbought
        
        # Crossover signals
        df['Oversold_Cross'] = (df['RSI'] < self.oversold) & (df['RSI_Prev'] >= self.oversold)
        df['Overbought_Cross'] = (df['RSI'] > self.overbought) & (df['RSI_Prev'] <= self.overbought)
        
        return df
    
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        Generate trading signal based on RSI
        
        Args:
            data: DataFrame with RSI
        
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        if len(data) < self.rsi_period + 1:
            return 'HOLD'
        
        latest = data.iloc[-1]
        
        # Strong buy signal when crossing into oversold
        if latest['Oversold_Cross']:
            return 'BUY'
        
        # Strong sell signal when crossing into overbought
        elif latest['Overbought_Cross']:
            return 'SELL'
        
        # Weaker signals for being in zones
        elif latest['Oversold']:
            return 'BUY'
        
        elif latest['Overbought']:
            return 'SELL'
        
        else:
            return 'HOLD'
    
    def should_enter(self, data: pd.DataFrame) -> bool:
        """
        Check if should enter position (buy signal)
        
        Args:
            data: DataFrame with RSI
        
        Returns:
            True if should enter
        """
        signal = self.generate_signal(data)
        return signal == 'BUY'
    
    def should_exit(self, data: pd.DataFrame, position: dict) -> bool:
        """
        Check if should exit position
        
        Args:
            data: DataFrame with RSI
            position: Current position
        
        Returns:
            True if should exit
        """
        if len(data) < self.rsi_period + 1:
            return False
        
        latest = data.iloc[-1]
        
        # Exit when reaching overbought (take profit)
        if latest['RSI'] > self.overbought:
            return True
        
        # Exit when RSI moves back to neutral zone
        if 45 < latest['RSI'] < 55:
            # Check if we have profit
            current_price = latest['Close']
            if current_price > position['entry_price'] * 1.02:  # 2% profit
                return True
        
        return False
    
    def backtest(self, symbol: str, from_date: str, to_date: str):
        """
        Backtest the strategy
        
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
        
        # Prepare data with RSI
        data = self.prepare_data(data)
        
        # Simulate trading
        in_position = False
        
        for i in range(self.rsi_period + 1, len(data)):
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
        print(f"   RSI Period: {self.rsi_period}")
        print(f"   Oversold: {self.oversold}, Overbought: {self.overbought}")
        print("\n⚠️  This is for demonstration. Implement proper live trading logic.")


# Test the strategy
if __name__ == "__main__":
    print("🧪 Testing RSI Strategy...\n")
    
    from data.free_fetcher import FreeFetcher
    
    # Initialize
    fetcher = FreeFetcher()
    strategy = RSIStrategy(fetcher, rsi_period=14, oversold=30, overbought=70)
    
    # Backtest
    strategy.backtest('TCS', '2023-01-01', '2024-12-31')
    
    print("\n✅ Strategy test complete!")

