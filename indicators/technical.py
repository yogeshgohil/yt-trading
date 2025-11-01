"""
Technical Indicators Module
Calculate all popular technical indicators for trading strategies
"""
import pandas as pd
import numpy as np
from typing import Tuple

class TechnicalIndicators:
    """
    Calculate technical indicators for trading strategies
    All methods are static - no need to instantiate
    """
    
    @staticmethod
    def calculate_sma(data: pd.DataFrame, period: int = 20, column: str = 'Close') -> pd.Series:
        """
        Simple Moving Average (SMA)
        
        Args:
            data: DataFrame with price data
            period: Moving average period
            column: Column to calculate SMA on
        
        Returns:
            Series with SMA values
        """
        return data[column].rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int = 20, column: str = 'Close') -> pd.Series:
        """
        Exponential Moving Average (EMA)
        
        Args:
            data: DataFrame with price data
            period: Moving average period
            column: Column to calculate EMA on
        
        Returns:
            Series with EMA values
        """
        return data[column].ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = 'Close') -> pd.Series:
        """
        Relative Strength Index (RSI)
        
        Args:
            data: DataFrame with price data
            period: RSI period (default 14)
            column: Column to calculate RSI on
        
        Returns:
            Series with RSI values (0-100)
        """
        delta = data[column].diff()
        
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, 
                       signal: int = 9, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Moving Average Convergence Divergence (MACD)
        
        Args:
            data: DataFrame with price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            column: Column to calculate MACD on
        
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        ema_fast = data[column].ewm(span=fast, adjust=False).mean()
        ema_slow = data[column].ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, 
                                  std_dev: int = 2, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands
        
        Args:
            data: DataFrame with price data
            period: Moving average period
            std_dev: Number of standard deviations
            column: Column to calculate on
        
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        middle_band = data[column].rolling(window=period).mean()
        std = data[column].rolling(window=period).std()
        
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Average True Range (ATR)
        Measures volatility
        
        Args:
            data: DataFrame with OHLC data
            period: ATR period
        
        Returns:
            Series with ATR values
        """
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def calculate_stochastic(data: pd.DataFrame, period: int = 14, 
                            smooth_k: int = 3, smooth_d: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator
        
        Args:
            data: DataFrame with OHLC data
            period: Lookback period
            smooth_k: K line smoothing
            smooth_d: D line smoothing
        
        Returns:
            Tuple of (%K line, %D line)
        """
        low_min = data['Low'].rolling(window=period).min()
        high_max = data['High'].rolling(window=period).max()
        
        k = 100 * (data['Close'] - low_min) / (high_max - low_min)
        k = k.rolling(window=smooth_k).mean()
        d = k.rolling(window=smooth_d).mean()
        
        return k, d
    
    @staticmethod
    def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Average Directional Index (ADX)
        Measures trend strength
        
        Args:
            data: DataFrame with OHLC data
            period: ADX period
        
        Returns:
            Series with ADX values
        """
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        tr = TechnicalIndicators.calculate_atr(data, period)
        
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return adx
    
    @staticmethod
    def calculate_obv(data: pd.DataFrame) -> pd.Series:
        """
        On-Balance Volume (OBV)
        Volume-based indicator
        
        Args:
            data: DataFrame with Close and Volume
        
        Returns:
            Series with OBV values
        """
        obv = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        return obv
    
    @staticmethod
    def calculate_vwap(data: pd.DataFrame) -> pd.Series:
        """
        Volume Weighted Average Price (VWAP)
        
        Args:
            data: DataFrame with OHLC and Volume
        
        Returns:
            Series with VWAP values
        """
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        vwap = (typical_price * data['Volume']).cumsum() / data['Volume'].cumsum()
        return vwap
    
    @staticmethod
    def add_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
        """
        Add all common indicators to DataFrame
        
        Args:
            data: DataFrame with OHLC data
        
        Returns:
            DataFrame with all indicators added
        """
        df = data.copy()
        
        # Moving Averages
        df['SMA_20'] = TechnicalIndicators.calculate_sma(df, 20)
        df['SMA_50'] = TechnicalIndicators.calculate_sma(df, 50)
        df['SMA_200'] = TechnicalIndicators.calculate_sma(df, 200)
        df['EMA_12'] = TechnicalIndicators.calculate_ema(df, 12)
        df['EMA_26'] = TechnicalIndicators.calculate_ema(df, 26)
        
        # RSI
        df['RSI'] = TechnicalIndicators.calculate_rsi(df, 14)
        
        # MACD
        macd, signal, hist = TechnicalIndicators.calculate_macd(df)
        df['MACD'] = macd
        df['MACD_Signal'] = signal
        df['MACD_Hist'] = hist
        
        # Bollinger Bands
        upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(df)
        df['BB_Upper'] = upper
        df['BB_Middle'] = middle
        df['BB_Lower'] = lower
        
        # ATR
        df['ATR'] = TechnicalIndicators.calculate_atr(df, 14)
        
        # Stochastic
        k, d = TechnicalIndicators.calculate_stochastic(df)
        df['Stoch_K'] = k
        df['Stoch_D'] = d
        
        # OBV
        df['OBV'] = TechnicalIndicators.calculate_obv(df)
        
        # VWAP (if intraday data)
        df['VWAP'] = TechnicalIndicators.calculate_vwap(df)
        
        return df
    
    @staticmethod
    def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate basic buy/sell signals based on indicators
        
        Args:
            data: DataFrame with indicators
        
        Returns:
            DataFrame with signal columns added
        """
        df = data.copy()
        
        # MA Crossover Signal
        df['MA_Signal'] = 0
        df.loc[df['SMA_20'] > df['SMA_50'], 'MA_Signal'] = 1  # Bullish
        df.loc[df['SMA_20'] < df['SMA_50'], 'MA_Signal'] = -1  # Bearish
        
        # RSI Signal
        df['RSI_Signal'] = 0
        df.loc[df['RSI'] < 30, 'RSI_Signal'] = 1  # Oversold - Buy
        df.loc[df['RSI'] > 70, 'RSI_Signal'] = -1  # Overbought - Sell
        
        # MACD Signal
        df['MACD_Signal_Flag'] = 0
        df.loc[df['MACD'] > df['MACD_Signal'], 'MACD_Signal_Flag'] = 1  # Bullish
        df.loc[df['MACD'] < df['MACD_Signal'], 'MACD_Signal_Flag'] = -1  # Bearish
        
        # Bollinger Bands Signal
        df['BB_Signal'] = 0
        df.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 1  # Oversold
        df.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = -1  # Overbought
        
        # Combined Signal (majority vote)
        df['Combined_Signal'] = (
            df['MA_Signal'] + 
            df['RSI_Signal'] + 
            df['MACD_Signal_Flag'] + 
            df['BB_Signal']
        ) / 4
        
        return df


# Test the indicators
if __name__ == "__main__":
    print("🧪 Testing Technical Indicators...\n")
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100)
    sample_data = pd.DataFrame({
        'Date': dates,
        'Open': np.random.randn(100).cumsum() + 100,
        'High': np.random.randn(100).cumsum() + 105,
        'Low': np.random.randn(100).cumsum() + 95,
        'Close': np.random.randn(100).cumsum() + 100,
        'Volume': np.random.randint(1000, 10000, 100)
    })
    
    print("📊 Sample Data:")
    print(sample_data.head())
    
    # Test SMA
    print("\n📈 Testing SMA...")
    sma = TechnicalIndicators.calculate_sma(sample_data, 20)
    print(f"✅ SMA calculated: {sma.tail(3).values}")
    
    # Test RSI
    print("\n📈 Testing RSI...")
    rsi = TechnicalIndicators.calculate_rsi(sample_data, 14)
    print(f"✅ RSI calculated: {rsi.tail(3).values}")
    
    # Test MACD
    print("\n📈 Testing MACD...")
    macd, signal, hist = TechnicalIndicators.calculate_macd(sample_data)
    print(f"✅ MACD calculated: {macd.tail(3).values}")
    
    # Test all indicators
    print("\n📈 Adding all indicators...")
    data_with_indicators = TechnicalIndicators.add_all_indicators(sample_data)
    print(f"✅ Total columns: {len(data_with_indicators.columns)}")
    print(f"✅ Indicators added: {list(data_with_indicators.columns)}")
    
    # Test signals
    print("\n📈 Generating signals...")
    data_with_signals = TechnicalIndicators.generate_signals(data_with_indicators)
    print(f"✅ Signals generated!")
    print(data_with_signals[['Close', 'MA_Signal', 'RSI_Signal', 'Combined_Signal']].tail())
    
    print("\n✅ All tests passed!")

