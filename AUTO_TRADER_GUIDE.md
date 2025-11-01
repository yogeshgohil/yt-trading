# 🤖 Auto-Trader Guide

## What is Auto-Trading?

**Automatic Trading** means the app:
- Scans stocks automatically
- Detects buy/sell signals
- Places orders automatically
- Manages positions
- Exits when targets/stop-loss hit

**You don't need to watch the market!**

---

## Two Modes

### 🟢 SIMULATION Mode (FREE)
- Uses virtual money
- No risk
- Perfect for learning
- See what it would do
- **Start here!**

### 🔴 LIVE Mode (₹2,000/month)
- Real money
- Real trades
- Requires Kite Connect
- Only use after successful simulation

---

## How to Use

### Step 1: Open Auto-Trader

1. Open Web UI: `http://localhost:8501`
2. Click "🤖 Auto-Trader" in sidebar
3. You'll see the configuration page

### Step 2: Configure Settings

**Capital Settings:**
- Starting Capital: ₹10,000 to ₹1,00,000 (your choice)
- Click "Update Capital" to change anytime

**Trading Rules:**
- Max Trades Per Day: 3-5 (recommended)
- Max Daily Loss: ₹1,000-2,000
- Capital Per Trade: 10% (don't risk too much)

**Strategy:**
- RSI (recommended for beginners)
- MA Crossover (for trending markets)

**Stocks:**
- Select which stocks to trade
- Recommended: TCS, INFY, HDFCBANK, ICICIBANK
- Start with 3-5 stocks

### Step 3: Test It

Click **"Scan Once"** to:
- Scan all selected stocks
- Find buy/sell signals
- Execute simulated trades
- See results instantly!

### Step 4: Monitor Performance

Watch the dashboard:
- Total Capital
- Available Capital
- Daily P&L (Profit/Loss)
- Win Rate
- Open Positions
- Recent Trades

---

## Example Day

```
Morning 9:15 AM:
You: Click "Scan Once"
App: Scans 5 stocks
App: Finds "ICICIBANK - RSI 28 - Oversold - BUY"
App: Buys 8 shares @ ₹1,200 = ₹9,600

Afternoon 2:00 PM:
You: Click "Scan Once" again
App: Checks ICICIBANK
App: RSI now 72 - Overbought - SELL
App: Sells 8 shares @ ₹1,240 = ₹9,920
App: Profit: ₹320 (3.33%)

Result: ₹320 profit in one day!
```

---

## Settings Explained

### Starting Capital
- Virtual money to trade with
- Can change anytime
- Start with ₹50,000-1,00,000

### Max Trades Per Day
- Limits overtrading
- 3-5 is good for beginners
- Prevents emotional decisions

### Max Daily Loss
- Stops trading if you lose this much
- Protection from bad days
- ₹1,000-2,000 recommended

### Capital Per Trade
- How much to use per trade
- 10% = ₹10,000 capital → ₹1,000 per trade
- Don't go above 20%!

### Strategy
**RSI:**
- Buys oversold stocks (RSI < 30)
- Sells overbought stocks (RSI > 70)
- Good in choppy markets

**MA Crossover:**
- Buys on golden cross
- Sells on death cross
- Good in trending markets

---

## Safety Features

### Automatic Stop-Loss
- 2% stop-loss on every trade
- Prevents big losses
- Exits automatically if price drops

### Automatic Target
- 5% profit target
- Takes profit automatically
- Locks in gains

### Daily Limits
- Max trades per day
- Max loss per day
- Can't overtrade

### Position Monitoring
- Checks positions constantly
- Exits when signals change
- You stay protected

---

## What You'll See

### Dashboard Shows:
- 📊 Total Capital
- 💰 Available Capital
- 📈 Daily P&L
- 📉 Trades Today
- 💼 Open Positions
- 📜 Recent Trades
- 🎯 Win Rate
- 💵 Total Profit

### When It Trades:
```
📊 SIMULATED BUY ORDER
Symbol: TCS
Price: ₹3,000
Quantity: 3
Cost: ₹9,000
Reason: RSI Oversold (28.5)
```

### When It Sells:
```
📊 SIMULATED SELL ORDER
Symbol: TCS
Entry: ₹3,000
Exit: ₹3,150
Quantity: 3
Revenue: ₹9,450
Profit: ₹450 (+5.00%)
Reason: RSI Overbought (71.2)
```

---

## Monthly Testing Plan

### Week 1: Learn
- Set capital to ₹50,000
- Click "Scan Once" 2-3 times daily
- Watch what it does
- Learn the patterns

### Week 2-3: Test
- Increase scans to 4-5 times daily
- Try different stocks
- Adjust settings
- Track performance

### Week 4: Evaluate
- Check win rate
- Is it profitable?
- Consistent results?
- Ready for more?

### Month 2-3: Continue
- Keep testing
- Build confidence
- Save real money
- Prepare for live

### Month 4+: Go Live
- If consistently profitable
- Subscribe to Kite (₹2,000/month)
- Start with ₹10,000 real money
- Scale gradually

---

## Tips for Success

### Do:
✅ Start with simulation
✅ Test for 1-3 months
✅ Keep notes of what works
✅ Adjust settings based on results
✅ Be patient
✅ Learn from losses

### Don't:
❌ Rush to live trading
❌ Use all capital per trade
❌ Ignore daily loss limits
❌ Overtrade
❌ Get emotional
❌ Skip the learning phase

---

## Common Questions

**Q: How often should I scan?**
A: During simulation, scan 3-5 times daily to learn patterns.

**Q: What if it makes losses?**
A: Normal! Adjust settings, try different stocks, keep learning.

**Q: When to go live?**
A: After 1-3 months of profitable simulation.

**Q: How much capital to start live?**
A: ₹10,000-25,000 maximum initially.

**Q: Can I change settings anytime?**
A: Yes! Adjust capital, stocks, limits anytime.

**Q: What if internet disconnects?**
A: In simulation, no problem. In live, positions stay (check manually).

---

## Realistic Expectations

### Simulation (First Month):
- Win Rate: 40-60%
- Monthly Return: -2% to +5%
- Learning experience
- Building confidence

### After 3 Months Practice:
- Win Rate: 50-70%
- Monthly Return: +2% to +5%
- Understanding market
- Ready to consider live

### Live Trading (If successful):
- Win Rate: 50-65%
- Monthly Return: +1% to +3%
- Real money stress
- Smaller returns normal

---

## Going Live (When Ready)

### Requirements:
1. ✅ 3 months profitable simulation
2. ✅ Understand the strategy
3. ✅ Saved ₹10,000-25,000
4. ✅ Subscribed to Kite Connect
5. ✅ Comfortable with risk

### Steps:
1. Subscribe to Kite Connect (₹2,000/month)
2. Get API credentials
3. Update config to "LIVE" mode
4. Start with ₹10,000
5. Monitor closely
6. Scale gradually

---

## Emergency Stop

**Need to stop immediately?**

**In Web UI:**
- Close the browser
- Positions stay (check dashboard)

**In Runner Script:**
- Press `Ctrl+C`
- Auto-trader stops
- Check open positions

**Reset Simulation:**
- Click "Reset Simulation"
- Confirm by clicking again
- Everything resets
- Start fresh!

---

## Support

**Having issues?**
1. Check configuration
2. Verify internet connection
3. Look at logs folder
4. Try "Reset Simulation"
5. Restart web UI

**Want to learn more?**
- Check backtesting results
- Compare with manual analysis
- Read strategy documentation
- Practice daily!

---

## Success Story Path

```
Month 1: Learn
- Capital: ₹50,000 (virtual)
- Scans: 3-5 per day
- Result: -1% (learning)

Month 2: Improve
- Capital: ₹50,000 (virtual)
- Scans: 4-6 per day
- Result: +2% (getting better)

Month 3: Confidence
- Capital: ₹1,00,000 (virtual)
- Scans: 5-8 per day
- Result: +4% (profitable!)

Month 4: Go Live
- Capital: ₹15,000 (REAL!)
- Trades: Automatic
- Result: +1.5% (Success!)

Year 1: Growth
- Capital: ₹50,000 (REAL)
- Return: +25% yearly
- Profit: ₹12,500!
```

---

## Final Words

**Remember:**
- Start with SIMULATION
- Learn before risking money
- Be patient and consistent
- Adjust and improve
- Success takes time!

**You can do this!** 🚀

Start small, practice often, grow gradually! 💪

---

*Good luck with your auto-trading journey!* 🎉

