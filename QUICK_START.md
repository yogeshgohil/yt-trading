# 🚀 Quick Start Guide

## Step-by-Step Setup (5 Minutes)

### 1️⃣ Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- ✅ Make sure to check "Add Python to PATH" during installation

### 2️⃣ Install Dependencies

Open terminal/command prompt in the project folder:

```bash
# Install required packages
pip install -r requirements.txt
```

**Note**: This might take 2-3 minutes.

### 3️⃣ Run the Application

```bash
python main.py
```

You'll see:
```
============================================================
🚀 AUTOMATED TRADING APPLICATION
============================================================
💡 Mode: FREE (Development/Backtesting)
```

### 4️⃣ First Backtest

When the menu appears:
1. Press `1` for "Run Backtest (Single Stock)"
2. Enter strategy: `ma_crossover`
3. Enter symbol: `RELIANCE`
4. Wait for results!

## 📊 What You'll See

```
📊 MA Crossover Strategy - Performance Summary
============================================================
Initial Capital:     ₹1,00,000.00
Final Capital:       ₹1,05,234.00
Total Return:        ₹5,234.00 (5.23%)

Total Trades:        8
Winning Trades:      5
Losing Trades:       3
Win Rate:            62.50%
============================================================
```

## 🎯 What to Try Next

### Option 1: Try Different Strategy
```
Strategy: rsi
Symbol: TCS
```

### Option 2: Compare All Strategies
```
Menu option: 3
Symbol: INFY
```

### Option 3: Test All Watchlist Stocks
```
Menu option: 2
Strategy: ma_crossover
```

## ⚙️ Quick Configuration

Edit `config/settings.py` to customize:

```python
# Change initial capital
INITIAL_CAPITAL = 100000  # ₹1,00,000

# Change watchlist
WATCHLIST = [
    "RELIANCE",
    "TCS",
    "INFY"
]

# Change strategy parameters
MA_SHORT_PERIOD = 20  # Short moving average
MA_LONG_PERIOD = 50   # Long moving average
```

## 🆘 Common Issues

### Issue: "pip not found"
**Solution**: Reinstall Python and check "Add to PATH"

### Issue: "No module named 'pandas'"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: "No data found"
**Solution**: Check internet connection. Data comes from free sources online.

### Issue: Taking too long
**Solution**: Normal! First time downloads data. Subsequent runs are faster.

## 📈 Understanding Results

### Metrics Explained:

- **Total Return**: Profit/Loss percentage
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of buy/sell cycles
- **Average Profit**: Average profit per trade

### What's Good?

✅ Win Rate > 50%
✅ Positive Total Return
✅ Consistent profits
✅ Manageable drawdown

## 🎓 Learning Path

1. **Day 1-2**: Run backtests, understand basics
2. **Day 3-4**: Try different strategies
3. **Day 5-6**: Modify parameters
4. **Week 2**: Create custom strategy
5. **Week 3**: Optimize and fine-tune
6. **Week 4**: Ready for paper trading
7. **Month 2**: Consider live trading (with Kite subscription)

## 🔄 Moving to Live Trading

When ready (after thorough testing):

1. Subscribe to Kite Connect (₹2,000/month)
2. Get API credentials from [developers.kite.trade](https://developers.kite.trade/)
3. Update `config/settings.py`:
   ```python
   DATA_SOURCE = "KITE"
   KITE_API_KEY = "your_api_key"
   KITE_API_SECRET = "your_secret"
   ```
4. Install Kite library:
   ```bash
   pip install kiteconnect
   ```

## 💡 Pro Tips

1. **Start Small**: Test with default settings first
2. **Be Patient**: Good strategies take time to develop
3. **Keep Records**: Check `reports/` folder for CSV files
4. **Compare**: Test same stock with different strategies
5. **Learn**: Read Zerodha Varsity for trading basics

## 🎉 You're Ready!

Now you know how to:
- ✅ Run backtests
- ✅ Analyze results
- ✅ Compare strategies
- ✅ Customize settings

**Next Steps**: 
- Try different stocks
- Experiment with parameters
- Learn about technical indicators
- Build your trading knowledge

---

Happy Trading! 📈

Need help? Check `README.md` for detailed documentation.

