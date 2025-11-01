"""
Auto-Trader Runner
Run the auto-trader continuously during market hours
"""
from autotrader import AutoTrader
import sys

def main():
    print("\n" + "="*60)
    print("🤖 AUTO-TRADER RUNNER")
    print("="*60)
    
    # Initialize auto-trader
    trader = AutoTrader(mode="SIMULATION")
    
    print("\nCurrent Configuration:")
    print(f"  Capital: ₹{trader.config['starting_capital']:,.2f}")
    print(f"  Strategy: {trader.config['strategy']}")
    print(f"  Stocks: {', '.join(trader.config['stocks_to_trade'])}")
    print(f"  Max trades/day: {trader.config['max_trades_per_day']}")
    print(f"  Scan interval: {trader.config['scan_interval_minutes']} minutes")
    
    print("\n" + "="*60)
    choice = input("\nHow long to run? (Enter minutes or 'forever'): ")
    print("="*60)
    
    try:
        if choice.lower() == 'forever':
            print("\n🚀 Starting auto-trader (running indefinitely)...")
            print("Press Ctrl+C to stop\n")
            trader.start()
        else:
            minutes = int(choice)
            print(f"\n🚀 Starting auto-trader for {minutes} minutes...")
            print("Press Ctrl+C to stop early\n")
            trader.start(duration_minutes=minutes)
    
    except ValueError:
        print("❌ Invalid input. Please enter a number or 'forever'")
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user")
    
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    trader.print_status()
    
    if trader.all_trades:
        print("\n📜 Trade Log:")
        for trade in trader.all_trades:
            print(f"  {trade['symbol']}: ₹{trade['profit']:,.2f} ({trade['profit_percent']:+.2f}%)")
    
    print("\n✅ Auto-trader finished!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

