# 🔄 Migration Guide: FREE → LIVE Trading

Complete guide to switch from FREE mode to LIVE trading with Kite Connect.

## 📋 Prerequisites Checklist

Before migrating to live trading:

- [ ] Tested strategies thoroughly with FREE data
- [ ] Strategies are profitable in backtests
- [ ] Understanding of trading risks
- [ ] Comfortable with capital at risk
- [ ] Zerodha trading account ready
- [ ] Budget for ₹2,000/month API subscription

## 💰 Step 1: Subscribe to Kite Connect

1. Visit [https://kite.trade/](https://kite.trade/)
2. Click "Get Started" or "Subscribe"
3. Pay ₹2,000/month subscription fee
4. You'll receive confirmation email

## 🔑 Step 2: Get API Credentials

1. Visit [https://developers.kite.trade/](https://developers.kite.trade/)
2. Login with your Zerodha credentials
3. Click "Create New App"
4. Fill in details:
   - App Name: "My Trading Bot"
   - App Type: "Connect"
   - Redirect URL: `http://127.0.0.1:5000/` (or your callback URL)
5. Submit and note down:
   - **API Key**
   - **API Secret**

## 🔧 Step 3: Update Configuration

Edit `config/settings.py`:

```python
# Change this line
DATA_SOURCE = "KITE"  # Changed from "FREE"

# Add your credentials
KITE_API_KEY = "abcdefghijklmnop"      # Your API key
KITE_API_SECRET = "qrstuvwxyz123456"   # Your API secret
```

## 📦 Step 4: Install Kite Connect Library

```bash
pip install kiteconnect
```

## 🔓 Step 5: Implement Authentication

The Kite Connect API requires OAuth authentication. Here's how:

### Option A: Manual Token (Quick Start)

1. Run this Python script once:

```python
from kiteconnect import KiteConnect

api_key = "your_api_key"
kite = KiteConnect(api_key=api_key)

# Get login URL
print(kite.login_url())
```

2. Open the URL in browser
3. Login with Zerodha credentials
4. You'll be redirected to a URL like:
   ```
   http://127.0.0.1:5000/?request_token=XXXXXX&action=login&status=success
   ```
5. Copy the `request_token` from URL
6. Generate access token:

```python
api_secret = "your_api_secret"
request_token = "copied_request_token"

data = kite.generate_session(request_token, api_secret=api_secret)
access_token = data["access_token"]
print(f"Access Token: {access_token}")
```

7. Add access token to `config/settings.py`:

```python
KITE_ACCESS_TOKEN = "your_access_token"
```

### Option B: Automated Authentication (Recommended for Production)

Create `auth.py`:

```python
from kiteconnect import KiteConnect
from config.settings import Settings

def get_access_token():
    kite = KiteConnect(api_key=Settings.KITE_API_KEY)
    
    # Step 1: Generate login URL
    print(f"Please visit: {kite.login_url()}")
    
    # Step 2: After login, paste the request token
    request_token = input("Enter request token: ")
    
    # Step 3: Generate session
    data = kite.generate_session(
        request_token,
        api_secret=Settings.KITE_API_SECRET
    )
    
    print(f"\nAccess Token: {data['access_token']}")
    print("Add this to config/settings.py")
    
    return data['access_token']

if __name__ == "__main__":
    get_access_token()
```

Run: `python auth.py`

## 🔧 Step 6: Enable Kite Fetcher

Edit `data/kite_fetcher.py`:

1. **Uncomment the import** at the top:
```python
from kiteconnect import KiteConnect, KiteTicker
```

2. **Uncomment all method implementations** (marked with comments)

## ✅ Step 7: Test Connection

Run the test:

```bash
python main.py
# Select option 6: Test Data Connection
```

You should see:
```
✅ Kite Connect initialized
🔴 Live trading is now possible!
```

## 🎯 Step 8: Start Small

### Paper Trading First

Before using real money:

1. Test with very small quantities (1 share)
2. Monitor carefully
3. Check order execution
4. Verify prices and timing

### First Live Trade Checklist

- [ ] Tested data connection
- [ ] Verified quotes are real-time
- [ ] Checked order placement (small quantity)
- [ ] Confirmed order execution
- [ ] Verified position tracking
- [ ] Tested exit order

## 📝 Code Changes Summary

### Files That Need Changes:

1. **config/settings.py** (3 lines)
   ```python
   DATA_SOURCE = "KITE"
   KITE_API_KEY = "your_key"
   KITE_API_SECRET = "your_secret"
   KITE_ACCESS_TOKEN = "your_token"
   ```

2. **data/kite_fetcher.py** (uncomment code)
   - Uncomment import
   - Uncomment all methods

3. **Install library** (1 command)
   ```bash
   pip install kiteconnect
   ```

### Files That DON'T Need Changes:

- ✅ All strategies (`strategies/`)
- ✅ All indicators (`indicators/`)
- ✅ Database (`utils/database.py`)
- ✅ Logger (`utils/logger.py`)
- ✅ Main app (`main.py`)

**Total changes: ~15 lines of code!** 🎉

## 🔐 Security Best Practices

### Protect Your Credentials

1. **Never commit credentials to Git**
   ```bash
   # Already in .gitignore
   config/secrets.py
   .env
   ```

2. **Use environment variables** (optional but recommended)
   ```python
   import os
   KITE_API_KEY = os.getenv('KITE_API_KEY')
   ```

3. **Rotate access tokens regularly**
   - Access tokens expire daily
   - Regenerate using request token

## 🚨 Common Issues

### Issue 1: Token Expired
**Error**: `TokenException: The API key is invalid`
**Solution**: Regenerate access token using auth script

### Issue 2: Rate Limit Exceeded
**Error**: `TooManyRequests: Request limit exceeded`
**Solution**: Add delays between API calls, respect rate limits

### Issue 3: Invalid Symbol
**Error**: `InputException: Invalid trading symbol`
**Solution**: Use proper format (e.g., "RELIANCE" not "RELIANCE.NS")

### Issue 4: Insufficient Funds
**Error**: `Insufficient funds`
**Solution**: Check available margin before placing orders

## 🎯 Testing Procedure

### Step-by-Step Testing:

1. **Test Data Fetching**
   ```python
   quote = kite_fetcher.get_quote('RELIANCE')
   print(quote)
   ```

2. **Test Historical Data**
   ```python
   data = kite_fetcher.get_historical_data('RELIANCE', '2024-01-01', '2024-12-31')
   print(data.head())
   ```

3. **Test Order Placement** (SMALL QUANTITY!)
   ```python
   # Start with just 1 share!
   response = kite_fetcher.place_order(
       symbol='RELIANCE',
       transaction_type='BUY',
       quantity=1,
       order_type='MARKET'
   )
   print(response)
   ```

4. **Test Position Tracking**
   ```python
   positions = kite_fetcher.get_positions()
   print(positions)
   ```

## 📊 Monitoring Live Trading

### What to Monitor:

- Order execution status
- Position profit/loss
- Available margin
- Order rejections
- Error logs

### Set Up Alerts:

1. **Log monitoring** - Check `logs/` folder regularly
2. **Database tracking** - Monitor trades table
3. **Position limits** - Set maximum position size
4. **Loss limits** - Implement daily loss limit

## 💡 Pro Tips

1. **Start Very Small**
   - Use 1% of capital initially
   - Gradually increase as confidence grows

2. **Monitor First Week Closely**
   - Check every trade
   - Review logs daily
   - Verify P&L calculations

3. **Have a Kill Switch**
   - Know how to stop the bot quickly
   - Keep manual control ready

4. **Backup Plans**
   - What if internet fails?
   - What if API is down?
   - How to exit positions manually?

## 🔄 Rollback Plan

If something goes wrong, rollback to FREE mode:

```python
# config/settings.py
DATA_SOURCE = "FREE"  # Change back
```

Close all open positions manually via Kite web/app.

## ✅ Final Checklist

Before going fully live:

- [ ] API credentials configured
- [ ] Access token working
- [ ] Data fetching tested
- [ ] Small test orders executed successfully
- [ ] Position tracking verified
- [ ] Logs monitoring set up
- [ ] Risk limits configured
- [ ] Emergency stop procedure known
- [ ] Comfortable with capital at risk

## 🎉 You're Ready!

Once everything is tested and verified:

1. Start with small capital
2. Run during market hours
3. Monitor closely
4. Scale gradually
5. Keep learning and improving

---

⚠️ **Final Warning**: Live trading involves real money and real risk. Never trade with money you can't afford to lose. Always use stop-loss and risk management.

**Good luck with your trading! 📈💰**

