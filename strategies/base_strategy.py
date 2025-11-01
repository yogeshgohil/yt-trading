"""
Base Strategy Class
All trading strategies inherit from this
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies
    """
    
    def __init__(self, data_fetcher, name: str = "Base Strategy"):
        """
        Initialize strategy
        
        Args:
            data_fetcher: Data fetcher instance (Free or Kite)
            name: Strategy name
        """
        self.data_fetcher = data_fetcher
        self.name = name
        self.positions = {}  # Current positions
        self.trades = []  # Trade history
        self.capital = 100000  # Starting capital
        self.current_capital = self.capital
        
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        Generate trading signal (BUY, SELL, HOLD)
        
        Args:
            data: DataFrame with price data and indicators
        
        Returns:
            Signal string: 'BUY', 'SELL', or 'HOLD'
        """
        pass
    
    @abstractmethod
    def should_enter(self, data: pd.DataFrame) -> bool:
        """
        Check if should enter a position
        
        Args:
            data: DataFrame with price data
        
        Returns:
            True if should enter, False otherwise
        """
        pass
    
    @abstractmethod
    def should_exit(self, data: pd.DataFrame, position: dict) -> bool:
        """
        Check if should exit a position
        
        Args:
            data: DataFrame with price data
            position: Current position details
        
        Returns:
            True if should exit, False otherwise
        """
        pass
    
    def calculate_position_size(self, price: float, risk_percent: float = 0.1) -> int:
        """
        Calculate position size based on available capital
        
        Args:
            price: Current price
            risk_percent: Percentage of capital to risk
        
        Returns:
            Number of shares to buy
        """
        risk_amount = self.current_capital * risk_percent
        shares = int(risk_amount / price)
        return max(1, shares)  # At least 1 share
    
    def enter_position(self, symbol: str, price: float, quantity: int, 
                      signal_type: str = "BUY") -> Dict:
        """
        Enter a new position
        
        Args:
            symbol: Stock symbol
            price: Entry price
            quantity: Number of shares
            signal_type: Type of signal
        
        Returns:
            Position dictionary
        """
        cost = price * quantity
        
        if cost > self.current_capital:
            print(f"⚠️  Insufficient capital for {symbol}")
            return None
        
        position = {
            'symbol': symbol,
            'entry_price': price,
            'quantity': quantity,
            'entry_date': datetime.now(),
            'cost': cost,
            'signal': signal_type
        }
        
        self.positions[symbol] = position
        self.current_capital -= cost
        
        print(f"✅ Entered {signal_type} position: {symbol} @ ₹{price} x {quantity}")
        return position
    
    def exit_position(self, symbol: str, price: float) -> Dict:
        """
        Exit an existing position
        
        Args:
            symbol: Stock symbol
            price: Exit price
        
        Returns:
            Trade result dictionary
        """
        if symbol not in self.positions:
            print(f"⚠️  No position found for {symbol}")
            return None
        
        position = self.positions[symbol]
        revenue = price * position['quantity']
        profit = revenue - position['cost']
        profit_percent = (profit / position['cost']) * 100
        
        trade = {
            'symbol': symbol,
            'entry_price': position['entry_price'],
            'exit_price': price,
            'quantity': position['quantity'],
            'entry_date': position['entry_date'],
            'exit_date': datetime.now(),
            'profit': profit,
            'profit_percent': profit_percent,
            'signal': position['signal']
        }
        
        self.trades.append(trade)
        self.current_capital += revenue
        del self.positions[symbol]
        
        print(f"✅ Exited position: {symbol} @ ₹{price} | P&L: ₹{profit:.2f} ({profit_percent:.2f}%)")
        return trade
    
    def get_performance_stats(self) -> Dict:
        """
        Calculate strategy performance statistics
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_profit': 0,
                'avg_profit': 0,
                'max_profit': 0,
                'max_loss': 0
            }
        
        profits = [trade['profit'] for trade in self.trades]
        winning_trades = [p for p in profits if p > 0]
        
        stats = {
            'total_trades': len(self.trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(profits) - len(winning_trades),
            'win_rate': (len(winning_trades) / len(self.trades)) * 100,
            'total_profit': sum(profits),
            'avg_profit': sum(profits) / len(profits),
            'avg_win': sum(winning_trades) / len(winning_trades) if winning_trades else 0,
            'avg_loss': sum([p for p in profits if p < 0]) / len([p for p in profits if p < 0]) if any(p < 0 for p in profits) else 0,
            'max_profit': max(profits),
            'max_loss': min(profits),
            'final_capital': self.current_capital,
            'return_percent': ((self.current_capital - self.capital) / self.capital) * 100
        }
        
        return stats
    
    def print_performance(self):
        """Print strategy performance summary"""
        stats = self.get_performance_stats()
        
        print("\n" + "="*60)
        print(f"📊 {self.name} - Performance Summary")
        print("="*60)
        print(f"Initial Capital:     ₹{self.capital:,.2f}")
        print(f"Final Capital:       ₹{stats['final_capital']:,.2f}")
        print(f"Total Return:        ₹{stats['total_profit']:,.2f} ({stats['return_percent']:.2f}%)")
        print(f"\nTotal Trades:        {stats['total_trades']}")
        print(f"Winning Trades:      {stats['winning_trades']}")
        print(f"Losing Trades:       {stats['losing_trades']}")
        print(f"Win Rate:            {stats['win_rate']:.2f}%")
        print(f"\nAverage Profit:      ₹{stats['avg_profit']:,.2f}")
        print(f"Average Win:         ₹{stats['avg_win']:,.2f}")
        print(f"Average Loss:        ₹{stats['avg_loss']:,.2f}")
        print(f"Max Profit:          ₹{stats['max_profit']:,.2f}")
        print(f"Max Loss:            ₹{stats['max_loss']:,.2f}")
        print("="*60 + "\n")
    
    def save_trades_to_csv(self, filename: str):
        """
        Save trade history to CSV
        
        Args:
            filename: Output filename
        """
        if not self.trades:
            print("⚠️  No trades to save")
            return
        
        df = pd.DataFrame(self.trades)
        df.to_csv(filename, index=False)
        print(f"✅ Trades saved to {filename}")

