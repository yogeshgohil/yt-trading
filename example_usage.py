"""
Example Usage of the Trading Application
Run this to see how different components work
"""

def example_1_basic_backtest():
    """Example 1: Basic Backtest"""
    print("\n" + "="*60)
    print("Example 1: Basic Backtest with MA Crossover")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    from strategies.ma_crossover import MACrossoverStrategy
    
    # Initialize
    fetcher = FreeFetcher()
    strategy = MACrossoverStrategy(fetcher, short_period=20, long_period=50)
    
    # Run backtest
    strategy.backtest('RELIANCE', '2023-01-01', '2024-12-31')


def example_2_rsi_strategy():
    """Example 2: RSI Strategy"""
    print("\n" + "="*60)
    print("Example 2: RSI Strategy Backtest")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    from strategies.rsi_strategy import RSIStrategy
    
    # Initialize
    fetcher = FreeFetcher()
    strategy = RSIStrategy(fetcher, rsi_period=14, oversold=30, overbought=70)
    
    # Run backtest
    strategy.backtest('TCS', '2023-01-01', '2024-12-31')


def example_3_compare_strategies():
    """Example 3: Compare Multiple Strategies"""
    print("\n" + "="*60)
    print("Example 3: Compare Strategies on Same Stock")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    from strategies.ma_crossover import MACrossoverStrategy
    from strategies.rsi_strategy import RSIStrategy
    
    fetcher = FreeFetcher()
    symbol = 'INFY'
    
    # Test MA Crossover
    print("\n--- Testing MA Crossover ---")
    ma_strategy = MACrossoverStrategy(fetcher)
    ma_strategy.backtest(symbol, '2023-01-01', '2024-12-31')
    ma_stats = ma_strategy.get_performance_stats()
    
    # Test RSI
    print("\n--- Testing RSI Strategy ---")
    rsi_strategy = RSIStrategy(fetcher)
    rsi_strategy.backtest(symbol, '2023-01-01', '2024-12-31')
    rsi_stats = rsi_strategy.get_performance_stats()
    
    # Compare
    print("\n" + "="*60)
    print("📊 COMPARISON RESULTS")
    print("="*60)
    print(f"MA Crossover:  {ma_stats['return_percent']:.2f}% return, {ma_stats['win_rate']:.2f}% win rate")
    print(f"RSI Strategy:  {rsi_stats['return_percent']:.2f}% return, {rsi_stats['win_rate']:.2f}% win rate")
    
    if ma_stats['return_percent'] > rsi_stats['return_percent']:
        print(f"\n🏆 Winner: MA Crossover")
    else:
        print(f"\n🏆 Winner: RSI Strategy")


def example_4_technical_indicators():
    """Example 4: Using Technical Indicators"""
    print("\n" + "="*60)
    print("Example 4: Calculate Technical Indicators")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    from indicators.technical import TechnicalIndicators
    
    # Fetch data
    fetcher = FreeFetcher()
    data = fetcher.get_historical_data('RELIANCE', '2024-01-01', '2024-12-31')
    
    print(f"\n📊 Data fetched: {len(data)} rows")
    
    # Add all indicators
    data_with_indicators = TechnicalIndicators.add_all_indicators(data)
    
    print(f"\n✅ Indicators added!")
    print(f"Total columns: {len(data_with_indicators.columns)}")
    
    # Show latest values
    print("\n📈 Latest Indicator Values:")
    latest = data_with_indicators.iloc[-1]
    print(f"Close Price: ₹{latest['Close']:.2f}")
    print(f"SMA 20: ₹{latest['SMA_20']:.2f}")
    print(f"SMA 50: ₹{latest['SMA_50']:.2f}")
    print(f"RSI: {latest['RSI']:.2f}")
    print(f"MACD: {latest['MACD']:.2f}")


def example_5_database_usage():
    """Example 5: Using Database"""
    print("\n" + "="*60)
    print("Example 5: Database Operations")
    print("="*60)
    
    from utils.database import TradingDatabase
    from datetime import datetime
    
    # Initialize database
    db = TradingDatabase("data/example_trading.db")
    
    # Insert a sample trade
    trade = {
        'symbol': 'RELIANCE',
        'strategy': 'MA Crossover',
        'entry_date': '2024-01-01',
        'exit_date': '2024-01-10',
        'entry_price': 2500,
        'exit_price': 2600,
        'quantity': 10,
        'profit': 1000,
        'profit_percent': 4.0,
        'status': 'CLOSED'
    }
    
    trade_id = db.insert_trade(trade)
    print(f"\n✅ Trade inserted with ID: {trade_id}")
    
    # Get trades
    trades = db.get_trades(limit=5)
    print(f"\n📊 Recent Trades:")
    print(trades[['symbol', 'entry_price', 'exit_price', 'profit']].to_string())
    
    # Get statistics
    stats = db.get_trade_stats()
    print(f"\n📈 Statistics:")
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Win Rate: {stats['win_rate']:.2f}%")
    print(f"Total Profit: ₹{stats['total_profit']:,.2f}")
    
    db.close()


def example_6_get_live_data():
    """Example 6: Get Live/Latest Data"""
    print("\n" + "="*60)
    print("Example 6: Fetch Live Stock Data")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    
    fetcher = FreeFetcher()
    
    symbols = ['RELIANCE', 'TCS', 'INFY']
    
    print("\n💰 Current Prices:\n")
    for symbol in symbols:
        quote = fetcher.get_quote(symbol)
        print(f"{symbol:12} ₹{quote['last_price']:8.2f}  "
              f"Change: {quote['change_percent']:+6.2f}%")


def example_7_custom_parameters():
    """Example 7: Custom Strategy Parameters"""
    print("\n" + "="*60)
    print("Example 7: Test Different Parameters")
    print("="*60)
    
    from data.free_fetcher import FreeFetcher
    from strategies.ma_crossover import MACrossoverStrategy
    
    fetcher = FreeFetcher()
    symbol = 'HDFCBANK'
    
    # Test different MA periods
    configs = [
        (10, 30, "Fast"),
        (20, 50, "Standard"),
        (50, 200, "Slow")
    ]
    
    results = []
    
    for short, long, name in configs:
        print(f"\n--- Testing {name} Config ({short}/{long}) ---")
        strategy = MACrossoverStrategy(fetcher, short_period=short, long_period=long)
        strategy.backtest(symbol, '2023-01-01', '2024-12-31')
        stats = strategy.get_performance_stats()
        results.append((name, stats))
    
    # Compare results
    print("\n" + "="*60)
    print("📊 PARAMETER COMPARISON")
    print("="*60)
    for name, stats in results:
        print(f"{name:12} Return: {stats['return_percent']:6.2f}%  "
              f"Win Rate: {stats['win_rate']:5.2f}%  "
              f"Trades: {stats['total_trades']}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🧪 TRADING APPLICATION EXAMPLES")
    print("="*60)
    print("\nSelect an example to run:")
    print("1. Basic Backtest (MA Crossover)")
    print("2. RSI Strategy")
    print("3. Compare Strategies")
    print("4. Technical Indicators")
    print("5. Database Usage")
    print("6. Get Live Data")
    print("7. Custom Parameters")
    print("8. Run All Examples")
    print("="*60)
    
    choice = input("\nEnter choice (1-8): ").strip()
    
    examples = {
        '1': example_1_basic_backtest,
        '2': example_2_rsi_strategy,
        '3': example_3_compare_strategies,
        '4': example_4_technical_indicators,
        '5': example_5_database_usage,
        '6': example_6_get_live_data,
        '7': example_7_custom_parameters,
    }
    
    if choice in examples:
        examples[choice]()
    elif choice == '8':
        for func in examples.values():
            func()
            input("\nPress Enter to continue...")
    else:
        print("❌ Invalid choice!")
    
    print("\n✅ Example completed!\n")


if __name__ == "__main__":
    main()

