# 🚀 Automated Trading Application

A comprehensive automated trading bot for Indian stock markets using Kite Connect API (or free data sources for development).

## ✨ Features

- 📊 **Multiple Trading Strategies**
  - Moving Average Crossover
  - RSI (Relative Strength Index)
  - Easy to add custom strategies

- 💰 **Dual Mode Operation**
  - **FREE Mode**: Development & backtesting with free data sources
  - **LIVE Mode**: Real trading with Kite Connect API

- 📈 **Complete Backtesting**
  - Test strategies on historical data
  - Performance metrics and statistics
  - Trade history and reports

- 🎯 **Technical Indicators**
  - SMA, EMA (Moving Averages)
  - RSI, MACD, Bollinger Bands
  - Stochastic, ATR, ADX
  - OBV, VWAP

- 💾 **Database Integration**
  - SQLite database for trade logging
  - Position tracking
  - Signal history
  - Performance analytics

- 📝 **Comprehensive Logging**
  - File and console logging
  - Trade execution logs
  - Error tracking

## 🏗️ Architecture

```
kiteApp/
├── config/              # Configuration files
│   ├── settings.py      # Main settings (FREE/KITE toggle)
│   └── __init__.py
├── data/                # Data fetching modules
│   ├── base_fetcher.py  # Base interface
│   ├── free_fetcher.py  # Free data (yfinance/NSEpy)
│   ├── kite_fetcher.py  # Kite Connect API
│   └── __init__.py
├── strategies/          # Trading strategies
│   ├── base_strategy.py # Base strategy class
│   ├── ma_crossover.py  # MA Crossover strategy
│   ├── rsi_strategy.py  # RSI strategy
│   └── __init__.py
├── indicators/          # Technical indicators
│   ├── technical.py     # All indicators
│   └── __init__.py
├── utils/               # Utility modules
│   ├── database.py      # SQLite database
│   ├── logger.py        # Logging utility
│   └── __init__.py
├── data/                # Data storage
│   ├── historical/      # Historical data cache
│   └── trading.db       # SQLite database
├── logs/                # Log files
├── reports/             # Backtest reports
├── main.py              # Main application
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download this project
cd kiteApp

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Open `config/settings.py` and configure:

```python
# For FREE mode (development)
DATA_SOURCE = "FREE"

# For LIVE trading (when ready)
DATA_SOURCE = "KITE"
KITE_API_KEY = "your_api_key"
KITE_API_SECRET = "your_api_secret"
KITE_ACCESS_TOKEN = "your_access_token"
```

### 3. Run the Application

```bash
python main.py
```

## 📊 Usage Examples

### Backtest a Strategy

```python
from data.free_fetcher import FreeFetcher
from strategies.ma_crossover import MACrossoverStrategy

# Initialize
fetcher = FreeFetcher()
strategy = MACrossoverStrategy(fetcher)

# Run backtest
strategy.backtest('RELIANCE', '2023-01-01', '2024-12-31')
```

### Compare Strategies

```bash
python main.py
# Select option 3: Compare All Strategies
# Enter symbol: RELIANCE
```

### Test Data Connection

```bash
python main.py
# Select option 6: Test Data Connection
```

## 💰 Cost Breakdown

### FREE Mode (Development)
- Cost: **₹0/month**
- Features:
  - ✅ Historical data
  - ✅ Backtesting
  - ✅ Strategy development
  - ✅ All indicators
  - ❌ Live trading
  - ❌ Real-time data

### LIVE Mode (Production)
- Cost: **₹2,000/month** (Kite Connect subscription)
- Features:
  - ✅ Everything in FREE mode
  - ✅ Live trading
  - ✅ Real-time data
  - ✅ Order execution
  - ✅ Portfolio tracking

## 🔄 Switching from FREE to LIVE

Only **3 changes** needed:

1. **Subscribe to Kite Connect** (₹2,000/month)
2. **Update config/settings.py**:
   ```python
   DATA_SOURCE = "KITE"
   KITE_API_KEY = "your_key"
   KITE_API_SECRET = "your_secret"
   ```
3. **Install Kite library**:
   ```bash
   pip install kiteconnect
   ```

That's it! All your strategies work unchanged! 🎉

## 📈 Available Strategies

### 1. Moving Average Crossover
Classic trend-following strategy.
- **Buy**: When short MA crosses above long MA (Golden Cross)
- **Sell**: When short MA crosses below long MA (Death Cross)

### 2. RSI Strategy
Mean reversion strategy.
- **Buy**: When RSI < 30 (Oversold)
- **Sell**: When RSI > 70 (Overbought)

### 3. Custom Strategy
Create your own by extending `BaseStrategy`:

```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def generate_signal(self, data):
        # Your logic here
        return 'BUY' or 'SELL' or 'HOLD'
    
    def should_enter(self, data):
        # Entry condition
        return True/False
    
    def should_exit(self, data, position):
        # Exit condition
        return True/False
```

## 🎯 Watchlist

Default watchlist (configurable in `settings.py`):
- RELIANCE
- TCS
- INFY
- HDFCBANK
- ICICIBANK
- SBIN
- BHARTIARTL
- ITC
- KOTAKBANK
- LT

## 📝 Database Schema

### Trades Table
- symbol, strategy, entry_date, exit_date
- entry_price, exit_price, quantity
- profit, profit_percent, status

### Signals Table
- symbol, strategy, signal_type
- price, indicators, timestamp

### Positions Table
- symbol, strategy, entry_price
- quantity, current_price, unrealized_pnl

## 🔧 Technical Indicators

All indicators available:
- **Trend**: SMA, EMA, MACD, ADX
- **Momentum**: RSI, Stochastic
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, VWAP

## 📊 Performance Metrics

Automatic calculation of:
- Total trades
- Win rate
- Total profit/loss
- Average profit/loss
- Maximum profit/loss
- Return percentage

## ⚠️ Important Notes

### Risk Warning
- Trading involves substantial risk
- Past performance doesn't guarantee future results
- Always use stop-loss
- Start with paper trading
- Test thoroughly before live trading

### Best Practices
1. **Always backtest** strategies before live trading
2. **Start small** with live capital
3. **Use stop-loss** for risk management
4. **Monitor regularly** your trades
5. **Keep logs** of all activities

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'yfinance'`
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: No data fetched for a symbol
**Solution**: Check symbol format (use NSE symbols like 'RELIANCE', 'TCS')

**Issue**: TA-Lib installation fails
**Solution**: 
- Windows: `pip install TA-Lib-binary`
- Linux: `sudo apt-get install ta-lib`

## 📚 Resources

### Learning
- [Zerodha Varsity](https://zerodha.com/varsity/) - Free trading education
- [Kite Connect Docs](https://kite.trade/docs/connect/v3/) - API documentation
- [TradingView](https://www.tradingview.com/) - Chart analysis

### Community
- [TradingQnA](https://tradingqna.com/) - Zerodha community
- [Reddit r/algotrading](https://www.reddit.com/r/algotrading/)
- [Reddit r/IndiaInvestments](https://www.reddit.com/r/IndiaInvestments/)

## 🛣️ Roadmap

- [ ] Web dashboard for monitoring
- [ ] More strategies (Breakout, Options)
- [ ] Machine learning strategies
- [ ] Telegram/Email alerts
- [ ] Portfolio optimization
- [ ] Risk management tools
- [ ] Multi-timeframe analysis

## 📄 License

This project is for educational purposes only.

## 🤝 Contributing

Feel free to:
- Add new strategies
- Improve existing code
- Fix bugs
- Add documentation

## 📧 Support

For issues and questions:
1. Check the documentation
2. Review common issues above
3. Test with sample data first

## ⭐ Features Summary

| Feature | FREE Mode | LIVE Mode |
|---------|-----------|-----------|
| Backtesting | ✅ | ✅ |
| Historical Data | ✅ | ✅ |
| Technical Indicators | ✅ | ✅ |
| Strategy Development | ✅ | ✅ |
| Real-time Data | ❌ | ✅ |
| Live Trading | ❌ | ✅ |
| Order Execution | ❌ | ✅ |
| Cost | Free | ₹2,000/month |

## 🎉 Get Started Now!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py

# 3. Select option 6 to test data connection
# 4. Select option 1 to run your first backtest
# 5. Analyze results and refine your strategy
```

**Happy Trading! 📈💰**

---

⚠️ **Disclaimer**: This software is for educational purposes only. Trading involves risk. Always do your own research and never trade with money you can't afford to lose.

