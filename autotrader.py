"""
Auto-Trading Simulation Module
Test automatic trading with virtual money before going live!
"""
import time
from datetime import datetime, timedelta
import pandas as pd
from threading import Thread
import json
from pathlib import Path

from data.free_fetcher import FreeFetcher
from strategies.rsi_strategy import RSIStrategy
from strategies.ma_crossover import MACrossoverStrategy
from indicators.technical import TechnicalIndicators
from utils.database import TradingDatabase
from utils.logger import get_logger

class AutoTrader:
    """
    Automatic Trading System (Simulation & Live)
    
    Simulation Mode: Tests with virtual money (FREE)
    Live Mode: Real trading with Kite API (requires subscription)
    """
    
    def __init__(self, mode="SIMULATION"):
        """
        Initialize Auto-Trader
        
        Args:
            mode: "SIMULATION" or "LIVE"
        """
        self.mode = mode
        self.logger = get_logger("AutoTrader")
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize components
        self.fetcher = FreeFetcher()
        self.db = TradingDatabase("data/trading.db")
        
        # Trading state
        self.is_running = False
        self.positions = {}  # Current open positions
        self.capital = self.config['starting_capital']
        self.available_capital = self.capital
        self.trades_today = 0
        self.daily_pnl = 0
        self.all_trades = []
        
        # Statistics
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit = 0
        
        self.logger.info(f"AutoTrader initialized in {mode} mode")
        print(f"\n{'='*60}")
        print(f"🤖 AUTO-TRADER INITIALIZED")
        print(f"{'='*60}")
        print(f"Mode: {mode}")
        print(f"Starting Capital: ₹{self.capital:,.2f}")
        print(f"Strategy: {self.config['strategy']}")
        print(f"{'='*60}\n")
    
    def load_config(self):
        """Load trading configuration"""
        config_file = Path("autotrader_config.json")
        
        default_config = {
            'mode': 'SIMULATION',
            'starting_capital': 100000,
            'max_trades_per_day': 5,
            'max_loss_per_day': 2000,
            'capital_per_trade_percent': 10,
            'strategy': 'RSI',
            'stocks_to_trade': ['TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'RELIANCE'],
            'stop_loss_percent': 2,
            'target_percent': 5,
            'scan_interval_minutes': 30,
            'require_confirmation': False,
            'rsi_oversold': 30,
            'rsi_overbought': 70
        }
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                saved_config = json.load(f)
                default_config.update(saved_config)
        else:
            self.save_config(default_config)
        
        return default_config
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        with open("autotrader_config.json", 'w') as f:
            json.dump(config, f, indent=4)
        
        print("✅ Configuration saved!")
    
    def update_capital(self, new_capital):
        """Update starting capital"""
        self.config['starting_capital'] = new_capital
        self.capital = new_capital
        self.available_capital = new_capital
        self.save_config()
        print(f"✅ Capital updated to ₹{new_capital:,.2f}")
    
    def scan_for_signals(self):
        """Scan stocks for buy/sell signals"""
        print(f"\n🔍 Scanning stocks at {datetime.now().strftime('%H:%M:%S')}...")
        
        signals = []
        
        for symbol in self.config['stocks_to_trade']:
            try:
                # Fetch recent data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                data = self.fetcher.get_historical_data(
                    symbol,
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )
                
                if len(data) < 20:
                    continue
                
                # Add indicators
                data_with_indicators = TechnicalIndicators.add_all_indicators(data)
                latest = data_with_indicators.iloc[-1]
                
                # Get current price
                quote = self.fetcher.get_quote(symbol)
                current_price = quote['last_price']
                
                # Check for signals based on strategy
                if self.config['strategy'] == 'RSI':
                    signal = self._check_rsi_signal(latest, symbol, current_price)
                else:
                    signal = self._check_ma_signal(latest, symbol, current_price)
                
                if signal:
                    signals.append(signal)
            
            except Exception as e:
                self.logger.error(f"Error scanning {symbol}: {str(e)}")
                continue
        
        return signals
    
    def _check_rsi_signal(self, latest, symbol, price):
        """Check RSI-based signals"""
        rsi = latest['RSI']
        
        # Buy signal
        if rsi < self.config['rsi_oversold'] and symbol not in self.positions:
            return {
                'symbol': symbol,
                'action': 'BUY',
                'price': price,
                'reason': f"RSI Oversold ({rsi:.1f})",
                'rsi': rsi,
                'strength': 'STRONG' if rsi < 25 else 'MODERATE'
            }
        
        # Sell signal
        elif rsi > self.config['rsi_overbought'] and symbol in self.positions:
            return {
                'symbol': symbol,
                'action': 'SELL',
                'price': price,
                'reason': f"RSI Overbought ({rsi:.1f})",
                'rsi': rsi,
                'strength': 'STRONG' if rsi > 75 else 'MODERATE'
            }
        
        return None
    
    def _check_ma_signal(self, latest, symbol, price):
        """Check Moving Average signals"""
        # Golden cross / Death cross
        if latest['SMA_20'] > latest['SMA_50'] and symbol not in self.positions:
            return {
                'symbol': symbol,
                'action': 'BUY',
                'price': price,
                'reason': "Golden Cross (MA 20 > MA 50)",
                'strength': 'MODERATE'
            }
        elif latest['SMA_20'] < latest['SMA_50'] and symbol in self.positions:
            return {
                'symbol': symbol,
                'action': 'SELL',
                'price': price,
                'reason': "Death Cross (MA 20 < MA 50)",
                'strength': 'MODERATE'
            }
        
        return None
    
    def execute_signal(self, signal):
        """Execute a trading signal"""
        if signal['action'] == 'BUY':
            return self.buy(signal)
        else:
            return self.sell(signal)
    
    def buy(self, signal):
        """Execute buy order"""
        symbol = signal['symbol']
        price = signal['price']
        
        # Check limits
        if self.trades_today >= self.config['max_trades_per_day']:
            print(f"⚠️  Max trades per day reached ({self.config['max_trades_per_day']})")
            return False
        
        if abs(self.daily_pnl) >= self.config['max_loss_per_day']:
            print(f"⚠️  Daily loss limit reached (₹{self.config['max_loss_per_day']})")
            return False
        
        # Calculate position size
        trade_amount = self.available_capital * (self.config['capital_per_trade_percent'] / 100)
        quantity = int(trade_amount / price)
        
        if quantity < 1:
            print(f"⚠️  Insufficient capital for {symbol}")
            return False
        
        cost = quantity * price
        
        # Execute (simulation or live)
        if self.mode == "SIMULATION":
            print(f"\n{'='*60}")
            print(f"📊 SIMULATED BUY ORDER")
            print(f"{'='*60}")
            print(f"Symbol: {symbol}")
            print(f"Price: ₹{price:.2f}")
            print(f"Quantity: {quantity}")
            print(f"Cost: ₹{cost:,.2f}")
            print(f"Reason: {signal['reason']}")
            print(f"{'='*60}\n")
        else:
            # TODO: Place real order via Kite API
            print(f"🔴 LIVE BUY ORDER: {symbol} x {quantity} @ ₹{price:.2f}")
        
        # Update position
        self.positions[symbol] = {
            'symbol': symbol,
            'entry_price': price,
            'quantity': quantity,
            'cost': cost,
            'entry_time': datetime.now(),
            'stop_loss': price * (1 - self.config['stop_loss_percent'] / 100),
            'target': price * (1 + self.config['target_percent'] / 100),
            'reason': signal['reason']
        }
        
        self.available_capital -= cost
        self.trades_today += 1
        
        # Log trade
        self.log_trade('BUY', symbol, price, quantity, cost)
        
        return True
    
    def sell(self, signal):
        """Execute sell order"""
        symbol = signal['symbol']
        
        if symbol not in self.positions:
            return False
        
        position = self.positions[symbol]
        price = signal['price']
        quantity = position['quantity']
        revenue = quantity * price
        
        profit = revenue - position['cost']
        profit_percent = (profit / position['cost']) * 100
        
        # Execute (simulation or live)
        if self.mode == "SIMULATION":
            print(f"\n{'='*60}")
            print(f"📊 SIMULATED SELL ORDER")
            print(f"{'='*60}")
            print(f"Symbol: {symbol}")
            print(f"Entry: ₹{position['entry_price']:.2f}")
            print(f"Exit: ₹{price:.2f}")
            print(f"Quantity: {quantity}")
            print(f"Revenue: ₹{revenue:,.2f}")
            print(f"Profit: ₹{profit:,.2f} ({profit_percent:+.2f}%)")
            print(f"Reason: {signal['reason']}")
            print(f"{'='*60}\n")
        else:
            # TODO: Place real order via Kite API
            print(f"🔴 LIVE SELL ORDER: {symbol} x {quantity} @ ₹{price:.2f}")
        
        # Update capital
        self.available_capital += revenue
        self.daily_pnl += profit
        self.total_profit += profit
        self.total_trades += 1
        
        if profit > 0:
            self.winning_trades += 1
        
        # Remove position
        del self.positions[symbol]
        
        # Log trade
        self.log_trade('SELL', symbol, price, quantity, revenue, profit, profit_percent)
        
        # Save trade
        trade = {
            'symbol': symbol,
            'entry_price': position['entry_price'],
            'exit_price': price,
            'quantity': quantity,
            'profit': profit,
            'profit_percent': profit_percent,
            'entry_time': position['entry_time'],
            'exit_time': datetime.now()
        }
        self.all_trades.append(trade)
        
        return True
    
    def check_positions(self):
        """Check open positions for stop-loss or target"""
        for symbol in list(self.positions.keys()):
            position = self.positions[symbol]
            
            try:
                quote = self.fetcher.get_quote(symbol)
                current_price = quote['last_price']
                
                # Check stop-loss
                if current_price <= position['stop_loss']:
                    print(f"🛑 Stop-loss hit for {symbol}!")
                    signal = {
                        'symbol': symbol,
                        'action': 'SELL',
                        'price': current_price,
                        'reason': 'Stop-loss hit'
                    }
                    self.sell(signal)
                
                # Check target
                elif current_price >= position['target']:
                    print(f"🎯 Target hit for {symbol}!")
                    signal = {
                        'symbol': symbol,
                        'action': 'SELL',
                        'price': current_price,
                        'reason': 'Target achieved'
                    }
                    self.sell(signal)
            
            except Exception as e:
                self.logger.error(f"Error checking position {symbol}: {str(e)}")
    
    def log_trade(self, action, symbol, price, quantity, amount, profit=None, profit_percent=None):
        """Log trade to console and file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if action == 'BUY':
            msg = f"[{timestamp}] BUY {symbol}: {quantity} @ ₹{price:.2f} = ₹{amount:,.2f}"
        else:
            msg = f"[{timestamp}] SELL {symbol}: {quantity} @ ₹{price:.2f} | P&L: ₹{profit:,.2f} ({profit_percent:+.2f}%)"
        
        print(msg)
        self.logger.info(msg)
    
    def get_status(self):
        """Get current trading status"""
        status = {
            'mode': self.mode,
            'is_running': self.is_running,
            'capital': self.capital,
            'available_capital': self.available_capital,
            'positions_count': len(self.positions),
            'trades_today': self.trades_today,
            'daily_pnl': self.daily_pnl,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'win_rate': (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0,
            'total_profit': self.total_profit,
            'positions': self.positions,
            'all_trades': self.all_trades
        }
        return status
    
    def print_status(self):
        """Print current status"""
        status = self.get_status()
        
        print(f"\n{'='*60}")
        print(f"📊 AUTO-TRADER STATUS")
        print(f"{'='*60}")
        print(f"Mode: {status['mode']}")
        print(f"Status: {'🟢 Running' if status['is_running'] else '🔴 Stopped'}")
        print(f"\n💰 Capital:")
        print(f"  Starting: ₹{status['capital']:,.2f}")
        print(f"  Available: ₹{status['available_capital']:,.2f}")
        print(f"  In Positions: ₹{status['capital'] - status['available_capital']:,.2f}")
        print(f"\n📊 Trading:")
        print(f"  Trades Today: {status['trades_today']}")
        print(f"  Open Positions: {status['positions_count']}")
        print(f"  Daily P&L: ₹{status['daily_pnl']:,.2f}")
        print(f"\n📈 Performance:")
        print(f"  Total Trades: {status['total_trades']}")
        print(f"  Win Rate: {status['win_rate']:.1f}%")
        print(f"  Total Profit: ₹{status['total_profit']:,.2f}")
        print(f"{'='*60}\n")
    
    def run_once(self):
        """Run one cycle of auto-trading"""
        print(f"\n🔄 Running auto-trader cycle...")
        
        # Scan for signals
        signals = self.scan_for_signals()
        
        if signals:
            print(f"\n✅ Found {len(signals)} signals!")
            for signal in signals:
                print(f"  {signal['strength']} {signal['action']}: {signal['symbol']} - {signal['reason']}")
                
                if not self.config['require_confirmation']:
                    self.execute_signal(signal)
                else:
                    print(f"  ⚠️  Confirmation required (set in config)")
        else:
            print("  No signals found.")
        
        # Check existing positions
        if self.positions:
            print(f"\n🔍 Checking {len(self.positions)} open positions...")
            self.check_positions()
        
        # Print status
        self.print_status()
    
    def start(self, duration_minutes=None):
        """Start auto-trading"""
        self.is_running = True
        print(f"\n🚀 Starting auto-trader...")
        
        if duration_minutes:
            print(f"Will run for {duration_minutes} minutes")
        else:
            print("Running indefinitely (press Ctrl+C to stop)")
        
        start_time = datetime.now()
        
        try:
            while self.is_running:
                self.run_once()
                
                # Check if duration reached
                if duration_minutes:
                    elapsed = (datetime.now() - start_time).total_seconds() / 60
                    if elapsed >= duration_minutes:
                        print(f"\n⏰ Duration of {duration_minutes} minutes reached")
                        break
                
                # Wait for next cycle
                print(f"\n💤 Sleeping for {self.config['scan_interval_minutes']} minutes...")
                time.sleep(self.config['scan_interval_minutes'] * 60)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Auto-trader stopped by user")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop auto-trading"""
        self.is_running = False
        print(f"\n🛑 Auto-trader stopped")
        self.print_status()
        
        # Close all positions
        if self.positions:
            print(f"\n⚠️  You have {len(self.positions)} open positions")
            print("Consider closing them manually or let them run")


# Quick test
if __name__ == "__main__":
    print("🤖 Auto-Trader Test Mode\n")
    
    trader = AutoTrader(mode="SIMULATION")
    
    print("\nConfiguration:")
    print(f"  Capital: ₹{trader.config['starting_capital']:,.2f}")
    print(f"  Strategy: {trader.config['strategy']}")
    print(f"  Stocks: {', '.join(trader.config['stocks_to_trade'])}")
    print(f"  Max trades/day: {trader.config['max_trades_per_day']}")
    
    print("\n" + "="*60)
    print("Ready to start!")
    print("="*60)

