"""
Main Trading Application
Automated Trading Bot using Kite API (or Free data sources)

Usage:
    python main.py
"""
import sys
from datetime import datetime, timedelta

from config.settings import Settings
from data.free_fetcher import FreeFetcher
from data.kite_fetcher import KiteFetcher
from strategies.ma_crossover import MACrossoverStrategy
from strategies.rsi_strategy import RSIStrategy
from utils.database import TradingDatabase
from utils.logger import get_logger

class TradingApp:
    """
    Main Trading Application
    """
    
    def __init__(self):
        """Initialize the trading application"""
        print("\n" + "="*60)
        print("🚀 AUTOMATED TRADING APPLICATION")
        print("="*60)
        
        # Initialize logger
        self.logger = get_logger("TradingApp")
        self.logger.info("Initializing Trading Application...")
        
        # Initialize database
        self.db = TradingDatabase(str(Settings.DATABASE_PATH))
        
        # Initialize data fetcher based on configuration
        self.data_fetcher = self._initialize_data_fetcher()
        
        # Initialize strategies
        self.strategies = self._initialize_strategies()
        
        self.logger.info("✅ Trading Application initialized successfully!")
        print("="*60 + "\n")
    
    def _initialize_data_fetcher(self):
        """
        Initialize data fetcher based on settings
        
        Returns:
            Data fetcher instance (Free or Kite)
        """
        data_source = Settings.get_data_source()
        
        if data_source == "FREE":
            self.logger.info("📊 Using FREE data source (yfinance/NSEpy)")
            print("💡 Mode: FREE (Development/Backtesting)")
            print("   Data may be delayed by 15-20 minutes")
            return FreeFetcher()
        
        elif data_source == "KITE":
            self.logger.info("🔴 Using KITE CONNECT API (Live Trading)")
            print("💰 Mode: LIVE TRADING with Kite Connect")
            
            if not Settings.is_kite_configured():
                self.logger.error("Kite Connect not configured properly!")
                print("❌ Error: Kite API credentials not found!")
                print("   Please configure in config/settings.py")
                sys.exit(1)
            
            return KiteFetcher(
                Settings.KITE_API_KEY,
                Settings.KITE_ACCESS_TOKEN
            )
        
        else:
            self.logger.error(f"Unknown data source: {data_source}")
            sys.exit(1)
    
    def _initialize_strategies(self):
        """
        Initialize trading strategies
        
        Returns:
            Dictionary of strategies
        """
        self.logger.info("📈 Initializing trading strategies...")
        
        strategies = {
            'ma_crossover': MACrossoverStrategy(
                self.data_fetcher,
                short_period=Settings.MA_SHORT_PERIOD,
                long_period=Settings.MA_LONG_PERIOD
            ),
            'rsi': RSIStrategy(
                self.data_fetcher,
                rsi_period=Settings.RSI_PERIOD,
                oversold=Settings.RSI_OVERSOLD,
                overbought=Settings.RSI_OVERBOUGHT
            )
        }
        
        print(f"\n📊 Loaded {len(strategies)} strategies:")
        for name in strategies.keys():
            print(f"   ✓ {name}")
        
        return strategies
    
    def run_backtest(self, strategy_name: str, symbol: str, 
                    from_date: str = None, to_date: str = None):
        """
        Run backtest for a strategy
        
        Args:
            strategy_name: Name of strategy to backtest
            symbol: Stock symbol
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
        """
        if strategy_name not in self.strategies:
            print(f"❌ Strategy '{strategy_name}' not found!")
            return
        
        # Default dates
        if not from_date:
            from_date = Settings.BACKTEST_START_DATE
        if not to_date:
            to_date = Settings.BACKTEST_END_DATE
        
        strategy = self.strategies[strategy_name]
        
        self.logger.info(f"🔬 Starting backtest: {strategy_name} on {symbol}")
        print(f"\n🔬 Running Backtest")
        print(f"Strategy: {strategy_name}")
        print(f"Symbol: {symbol}")
        print(f"Period: {from_date} to {to_date}\n")
        
        # Run backtest
        strategy.backtest(symbol, from_date, to_date)
        
        # Save trades to database
        for trade in strategy.trades:
            trade['strategy'] = strategy_name
            self.db.insert_trade(trade)
        
        # Save to CSV
        if strategy.trades:
            filename = f"reports/{strategy_name}_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            strategy.save_trades_to_csv(filename)
        
        self.logger.info("✅ Backtest completed!")
    
    def run_backtest_all_symbols(self, strategy_name: str):
        """
        Run backtest for all symbols in watchlist
        
        Args:
            strategy_name: Name of strategy
        """
        print(f"\n📊 Running backtest on all watchlist symbols...")
        print(f"Strategy: {strategy_name}")
        print(f"Symbols: {Settings.WATCHLIST}\n")
        
        for symbol in Settings.WATCHLIST:
            print(f"\n{'='*60}")
            print(f"Testing {symbol}...")
            print('='*60)
            
            try:
                self.run_backtest(strategy_name, symbol)
            except Exception as e:
                self.logger.error(f"Error backtesting {symbol}: {str(e)}")
                print(f"❌ Error: {str(e)}")
            
            print("")
        
        print("\n✅ All backtests completed!")
    
    def compare_strategies(self, symbol: str):
        """
        Compare all strategies on a single symbol
        
        Args:
            symbol: Stock symbol
        """
        print(f"\n📊 Comparing strategies on {symbol}\n")
        
        results = {}
        
        for strategy_name, strategy in self.strategies.items():
            print(f"\n{'='*60}")
            print(f"Testing: {strategy_name}")
            print('='*60)
            
            try:
                self.run_backtest(strategy_name, symbol)
                stats = strategy.get_performance_stats()
                results[strategy_name] = stats
            except Exception as e:
                self.logger.error(f"Error with {strategy_name}: {str(e)}")
                print(f"❌ Error: {str(e)}")
        
        # Print comparison
        print("\n" + "="*60)
        print("📊 STRATEGY COMPARISON")
        print("="*60)
        print(f"Symbol: {symbol}\n")
        
        for strategy_name, stats in results.items():
            print(f"{strategy_name}:")
            print(f"  Return: {stats['return_percent']:.2f}%")
            print(f"  Win Rate: {stats['win_rate']:.2f}%")
            print(f"  Total Trades: {stats['total_trades']}")
            print(f"  Total Profit: ₹{stats['total_profit']:,.2f}\n")
        
        # Find best strategy
        if results:
            best_strategy = max(results.items(), key=lambda x: x[1]['return_percent'])
            print(f"🏆 Best Strategy: {best_strategy[0]} ({best_strategy[1]['return_percent']:.2f}% return)")
        
        print("="*60 + "\n")
    
    def show_menu(self):
        """Display interactive menu"""
        print("\n" + "="*60)
        print("📋 TRADING APPLICATION MENU")
        print("="*60)
        print("1. Run Backtest (Single Stock)")
        print("2. Run Backtest (All Watchlist)")
        print("3. Compare All Strategies")
        print("4. View Trade History")
        print("5. View Database Stats")
        print("6. Test Data Connection")
        print("7. Exit")
        print("="*60)
    
    def test_data_connection(self):
        """Test data fetcher connection"""
        print("\n🔗 Testing data connection...\n")
        
        try:
            # Test with a popular stock
            test_symbol = "RELIANCE"
            print(f"Fetching data for {test_symbol}...")
            
            # Get quote
            quote = self.data_fetcher.get_quote(test_symbol)
            print(f"\n✅ Quote received:")
            print(f"   Symbol: {quote['symbol']}")
            print(f"   Price: ₹{quote['last_price']}")
            print(f"   Change: {quote['change_percent']:.2f}%")
            
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            data = self.data_fetcher.get_historical_data(
                test_symbol,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if not data.empty:
                print(f"\n✅ Historical data received:")
                print(f"   Rows: {len(data)}")
                print(f"   Date range: {data['Date'].iloc[0]} to {data['Date'].iloc[-1]}")
            
            print("\n✅ Connection test successful!")
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            print(f"\n❌ Connection test failed: {str(e)}")
    
    def view_trade_history(self):
        """View trade history from database"""
        print("\n📊 Trade History\n")
        
        trades = self.db.get_trades(limit=20)
        
        if trades.empty:
            print("No trades found in database.")
            return
        
        print(trades[['symbol', 'strategy', 'entry_price', 'exit_price', 
                     'profit', 'profit_percent', 'status']].to_string())
        
        # Show stats
        print("\n" + "="*60)
        stats = self.db.get_trade_stats()
        print("📈 Overall Statistics:")
        print(f"  Total Trades: {stats['total_trades']}")
        print(f"  Win Rate: {stats['win_rate']:.2f}%")
        print(f"  Total Profit: ₹{stats['total_profit']:,.2f}")
        print(f"  Avg Profit: ₹{stats['avg_profit']:,.2f}")
        print("="*60)
    
    def view_database_stats(self):
        """View database statistics"""
        print("\n📊 Database Statistics\n")
        
        print(f"Trades:    {self.db.get_table_count('trades')}")
        print(f"Signals:   {self.db.get_table_count('signals')}")
        print(f"Positions: {self.db.get_table_count('positions')}")
        print(f"Logs:      {self.db.get_table_count('logs')}")
    
    def run_interactive(self):
        """Run interactive mode"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    # Single backtest
                    print("\nAvailable strategies:")
                    for i, name in enumerate(self.strategies.keys(), 1):
                        print(f"  {i}. {name}")
                    
                    strategy = input("\nEnter strategy name: ").strip()
                    symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip().upper()
                    
                    self.run_backtest(strategy, symbol)
                
                elif choice == '2':
                    # All watchlist
                    print("\nAvailable strategies:")
                    for i, name in enumerate(self.strategies.keys(), 1):
                        print(f"  {i}. {name}")
                    
                    strategy = input("\nEnter strategy name: ").strip()
                    self.run_backtest_all_symbols(strategy)
                
                elif choice == '3':
                    # Compare strategies
                    symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip().upper()
                    self.compare_strategies(symbol)
                
                elif choice == '4':
                    # View trades
                    self.view_trade_history()
                
                elif choice == '5':
                    # Database stats
                    self.view_database_stats()
                
                elif choice == '6':
                    # Test connection
                    self.test_data_connection()
                
                elif choice == '7':
                    # Exit
                    print("\n👋 Thank you for using the Trading Application!")
                    print("="*60 + "\n")
                    break
                
                else:
                    print("❌ Invalid choice. Please try again.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")
                print(f"\n❌ Error: {str(e)}")
    
    def run(self):
        """Main run method"""
        self.run_interactive()


def main():
    """Main entry point"""
    try:
        app = TradingApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

