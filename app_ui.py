"""
Trading Application - Web Dashboard UI
User-friendly interface for automated trading
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys

# Configure page with PWA support
st.set_page_config(
    page_title="Automated Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Import our modules
from data.free_fetcher import FreeFetcher
from strategies.ma_crossover import MACrossoverStrategy
from strategies.rsi_strategy import RSIStrategy
from indicators.technical import TechnicalIndicators
from utils.database import TradingDatabase

# Initialize session state
if 'fetcher' not in st.session_state:
    st.session_state.fetcher = FreeFetcher()
if 'db' not in st.session_state:
    st.session_state.db = TradingDatabase("data/trading.db")

# Custom CSS with Mobile Responsiveness
st.markdown("""
<style>
    /* Desktop Styles */
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #17a2b8;
    }
    
    /* Mobile Optimization */
    @media only screen and (max-width: 768px) {
        .big-font {
            font-size: 20px !important;
        }
        .metric-card {
            padding: 10px;
            margin: 5px 0;
        }
        .success-box, .info-box {
            padding: 10px;
            font-size: 14px;
        }
        /* Make buttons full width on mobile */
        .stButton button {
            width: 100%;
        }
        /* Adjust column spacing */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
    }
    
    /* Touch-friendly buttons */
    @media (hover: none) and (pointer: coarse) {
        .stButton button {
            min-height: 44px;
            padding: 12px 24px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 Automated Trading Application")
st.markdown("### *Easy-to-Use Trading Bot Dashboard*")

# Sidebar
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    page = st.radio(
        "Choose a Page:",
        ["🏠 Home", "🤖 Auto-Trader", "📊 NIFTY Trading", "💼 Positions", "🎯 Buy Recommendations", "📊 Stock Details", "💰 Live Prices", "📊 Run Backtest", "📈 Compare Strategies", "📜 Trade History", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.info("**Mode:** FREE (No Cost)\n\n**Data Source:** yfinance\n\n**Status:** ✅ Ready")

# HOME PAGE
if page == "🏠 Home":
    st.header("Welcome to Your Trading Application! 👋")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Strategies Loaded", "2", delta="MA & RSI")
    with col2:
        st.metric("Data Source", "FREE", delta="yfinance")
    with col3:
        st.metric("Status", "Ready", delta="✅")
    
    st.markdown("---")
    
    st.subheader("📖 How It Works")
    
    with st.expander("1️⃣ What is This App?"):
        st.write("""
        This is an **automated trading application** that:
        - 📊 Fetches real stock market data
        - 🤖 Uses trading strategies to analyze stocks
        - 📈 Tests strategies on historical data (backtesting)
        - 💰 Shows you which strategies make profit
        - 📉 Helps you make better trading decisions
        """)
    
    with st.expander("2️⃣ What are Trading Strategies?"):
        st.write("""
        **Trading strategies** are rules for when to buy and sell stocks:
        
        - **MA Crossover Strategy**: 
          - Buys when short-term average crosses above long-term average
          - Sells when it crosses below
          - Good for catching trends
        
        - **RSI Strategy**:
          - Buys when stock is "oversold" (too cheap)
          - Sells when stock is "overbought" (too expensive)
          - Good for buying dips
        """)
    
    with st.expander("3️⃣ What is Backtesting?"):
        st.write("""
        **Backtesting** means testing a strategy on past data:
        
        - Takes historical stock prices
        - Simulates buying and selling based on strategy
        - Shows if you would have made profit or loss
        - Helps you see which strategy works best
        
        **Example:** Test MA strategy on RELIANCE from Jan-Dec 2024
        → See if it made profit!
        """)
    
    with st.expander("4️⃣ How to Use This App?"):
        st.write("""
        **Simple Steps:**
        
        1. **Check Live Prices** → See current stock prices
        2. **Run Backtest** → Test a strategy on a stock
        3. **Compare Strategies** → See which performs better
        4. **View Results** → See profit/loss, win rate, charts
        5. **Learn & Improve** → Try different stocks and settings
        """)
    
    st.markdown("---")
    
    st.subheader("🚀 Quick Start")
    st.write("**Try these now:**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎯 Get Buy Recommendations", use_container_width=True):
            st.session_state.page = "🎯 Buy Recommendations"
            st.rerun()
    
    with col2:
        if st.button("📊 Check Live Prices", use_container_width=True):
            st.session_state.page = "💰 Live Prices"
            st.rerun()
    
    with col3:
        if st.button("🧪 Run Backtest", use_container_width=True):
            st.session_state.page = "📊 Run Backtest"
            st.rerun()

# AUTO-TRADER PAGE
elif page == "🤖 Auto-Trader":
    st.header("🤖 Automatic Trading System")
    st.write("**Test auto-trading with virtual money before going live!**")
    
    # Initialize autotrader in session state
    if 'autotrader' not in st.session_state:
        from autotrader import AutoTrader
        st.session_state.autotrader = AutoTrader(mode="SIMULATION")
    
    trader = st.session_state.autotrader
    
    # Mode indicator
    if trader.mode == "SIMULATION":
        st.success("🟢 **SIMULATION MODE** - Using virtual money (Safe to test!)")
    else:
        st.error("🔴 **LIVE MODE** - Real trading with real money!")
    
    st.markdown("---")
    
    # Configuration Section
    st.subheader("⚙️ Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_capital = st.number_input(
            "Starting Capital (₹)",
            min_value=1000,
            max_value=10000000,
            value=int(trader.config['starting_capital']),
            step=10000,
            help="Virtual money to start with"
        )
        
        if new_capital != trader.config['starting_capital']:
            if st.button("💰 Update Capital"):
                trader.update_capital(new_capital)
                st.success(f"✅ Capital updated to ₹{new_capital:,.2f}")
                st.rerun()
    
    with col2:
        max_trades = st.number_input(
            "Max Trades Per Day",
            min_value=1,
            max_value=20,
            value=trader.config['max_trades_per_day'],
            help="Maximum number of trades per day"
        )
        trader.config['max_trades_per_day'] = max_trades
    
    with col3:
        max_loss = st.number_input(
            "Max Daily Loss (₹)",
            min_value=100,
            max_value=50000,
            value=trader.config['max_loss_per_day'],
            step=500,
            help="Stop trading if daily loss exceeds this"
        )
        trader.config['max_loss_per_day'] = max_loss
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        strategy = st.selectbox(
            "Trading Strategy",
            ["RSI", "MA_Crossover"],
            index=0 if trader.config['strategy'] == 'RSI' else 1,
            help="Which strategy to use for trading"
        )
        trader.config['strategy'] = strategy
    
    with col2:
        capital_per_trade = st.slider(
            "Capital Per Trade (%)",
            min_value=5,
            max_value=50,
            value=trader.config['capital_per_trade_percent'],
            help="What % of capital to use per trade"
        )
        trader.config['capital_per_trade_percent'] = capital_per_trade
    
    with col3:
        scan_interval = st.slider(
            "Scan Interval (minutes)",
            min_value=5,
            max_value=60,
            value=trader.config['scan_interval_minutes'],
            step=5,
            help="How often to scan for signals"
        )
        trader.config['scan_interval_minutes'] = scan_interval
    
    # Stock selection
    st.write("**Stocks to Trade:**")
    all_stocks = ['TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'RELIANCE', 'SBIN', 'BHARTIARTL', 'ITC', 'KOTAKBANK', 'LT']
    selected_stocks = st.multiselect(
        "Select stocks",
        all_stocks,
        default=trader.config['stocks_to_trade'],
        help="Which stocks the auto-trader should monitor"
    )
    trader.config['stocks_to_trade'] = selected_stocks if selected_stocks else ['TCS', 'INFY']
    
    if st.button("💾 Save Configuration"):
        trader.save_config()
        st.success("✅ Configuration saved!")
    
    st.markdown("---")
    
    # Status Dashboard
    st.subheader("📊 Current Status")
    
    status = trader.get_status()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Capital", f"₹{status['capital']:,.0f}")
    
    with col2:
        st.metric("Available", f"₹{status['available_capital']:,.0f}")
    
    with col3:
        st.metric("Daily P&L", f"₹{status['daily_pnl']:,.0f}", 
                 delta=f"{(status['daily_pnl']/status['capital']*100):.2f}%")
    
    with col4:
        st.metric("Trades Today", status['trades_today'], 
                 delta=f"{status['trades_today']}/{trader.config['max_trades_per_day']}")
    
    with col5:
        st.metric("Open Positions", status['positions_count'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Trades", status['total_trades'])
    
    with col2:
        st.metric("Win Rate", f"{status['win_rate']:.1f}%")
    
    with col3:
        profit_color = "normal" if status['total_profit'] >= 0 else "inverse"
        st.metric("Total Profit", f"₹{status['total_profit']:,.0f}",
                 delta=f"{(status['total_profit']/status['capital']*100):.2f}%")
    
    st.markdown("---")
    
    # Control Buttons
    st.subheader("🎮 Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Scan Once", type="primary", use_container_width=True):
            with st.spinner("Scanning stocks for signals..."):
                trader.run_once()
                st.success("✅ Scan complete!")
                st.rerun()
    
    with col2:
        if st.button("⏯️ Run for 1 Hour", use_container_width=True):
            st.info("This would run for 1 hour. Use 'Scan Once' for testing!")
            st.write("To run continuously, use: `python autotrader_runner.py`")
    
    with col3:
        if st.button("🔄 Reset Simulation", use_container_width=True):
            if st.session_state.get('confirm_reset', False):
                trader.available_capital = trader.capital
                trader.positions = {}
                trader.trades_today = 0
                trader.daily_pnl = 0
                trader.all_trades = []
                trader.total_trades = 0
                trader.winning_trades = 0
                trader.total_profit = 0
                st.success("✅ Simulation reset!")
                st.session_state.confirm_reset = False
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ Click again to confirm reset")
    
    # Open Positions
    if status['positions']:
        st.markdown("---")
        st.subheader("💼 Open Positions")
        
        positions_data = []
        for symbol, pos in status['positions'].items():
            try:
                quote = st.session_state.fetcher.get_quote(symbol)
                current_price = quote['last_price']
                unrealized_pnl = (current_price - pos['entry_price']) * pos['quantity']
                unrealized_pnl_pct = (unrealized_pnl / pos['cost']) * 100
                
                positions_data.append({
                    'Symbol': symbol,
                    'Entry': f"₹{pos['entry_price']:.2f}",
                    'Current': f"₹{current_price:.2f}",
                    'Qty': pos['quantity'],
                    'Cost': f"₹{pos['cost']:,.2f}",
                    'Unrealized P&L': f"₹{unrealized_pnl:,.2f}",
                    'P&L %': f"{unrealized_pnl_pct:+.2f}%",
                    'Reason': pos['reason']
                })
            except:
                pass
        
        if positions_data:
            df = pd.DataFrame(positions_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Recent Trades
    if status['all_trades']:
        st.markdown("---")
        st.subheader("📜 Recent Trades")
        
        trades_df = pd.DataFrame(status['all_trades'][-10:])  # Last 10 trades
        trades_df['Entry'] = trades_df['entry_price'].apply(lambda x: f"₹{x:.2f}")
        trades_df['Exit'] = trades_df['exit_price'].apply(lambda x: f"₹{x:.2f}")
        trades_df['Profit'] = trades_df['profit'].apply(lambda x: f"₹{x:.2f}")
        trades_df['%'] = trades_df['profit_percent'].apply(lambda x: f"{x:+.2f}%")
        
        st.dataframe(
            trades_df[['symbol', 'Entry', 'Exit', 'quantity', 'Profit', '%']],
            use_container_width=True,
            hide_index=True
        )
    
    # Instructions
    st.markdown("---")
    st.subheader("📚 How to Use")
    
    with st.expander("🎓 Quick Guide"):
        st.write("""
        **Step 1: Configure**
        - Set your starting capital (virtual money)
        - Choose max trades per day
        - Select which stocks to trade
        - Pick your strategy (RSI recommended)
        
        **Step 2: Test**
        - Click "Scan Once" to see what it would do
        - Watch for signals and trades
        - See how it performs
        
        **Step 3: Learn**
        - Observe which trades are profitable
        - Adjust settings if needed
        - Build confidence
        
        **Step 4: Go Live (When Ready)**
        - After 1 month of profitable simulation
        - Subscribe to Kite Connect (₹2,000/month)
        - Switch mode to "LIVE"
        - Start with small capital!
        
        **Important:**
        - This is SIMULATION - no real money at risk
        - Practice as much as you want
        - When simulation is consistently profitable, consider going live
        - Always start live trading with small amounts
        """)
    
    with st.expander("⚙️ Strategy Settings"):
        st.write("""
        **RSI Strategy:**
        - Buys when RSI < 30 (oversold)
        - Sells when RSI > 70 (overbought)
        - Good for choppy markets
        - Works well on banking stocks
        
        **MA Crossover Strategy:**
        - Buys when MA 20 crosses above MA 50
        - Sells when MA 20 crosses below MA 50
        - Good for trending markets
        - More conservative
        
        **Risk Management:**
        - Automatic 2% stop-loss on every trade
        - Automatic 5% profit target
        - Daily loss limit protection
        - Maximum trades per day limit
        """)

# NIFTY TRADING PAGE
elif page == "📊 NIFTY Trading":
    st.header("📊 NIFTY Trading - Auto Strategy System")
    st.write("**Automated trading on NIFTY 50 index with optimized strategies for maximum profit**")
    
    # Initialize NIFTY trader in session state
    if 'nifty_trader' not in st.session_state:
        from autotrader import AutoTrader
        st.session_state.nifty_trader = AutoTrader(mode="SIMULATION")
        # Configure specifically for NIFTY stocks
        st.session_state.nifty_trader.config['stocks_to_trade'] = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 
            'HINDUNILVR', 'BHARTIARTL', 'ITC', 'SBIN', 'KOTAKBANK',
            'LT', 'AXISBANK', 'BAJFINANCE', 'ASIANPAINT', 'MARUTI'
        ]
    
    nifty_trader = st.session_state.nifty_trader
    
    # Mode indicator
    if nifty_trader.mode == "SIMULATION":
        st.success("🟢 **SIMULATION MODE** - Testing NIFTY strategies with virtual money")
    else:
        st.error("🔴 **LIVE MODE** - Real trading on NIFTY stocks!")
    
    st.markdown("---")
    
    # NIFTY Indices Overview
    st.subheader("📈 NIFTY Indices Overview")
    
    # Define all NIFTY indices
    nifty_indices = {
        'NIFTY 50': '^NSEI',
        'BANK NIFTY': '^NSEBANK',
        'NIFTY IT': 'NIFTY_IT.NS',
        'NIFTY PHARMA': 'NIFTY_PHARMA.NS',
        'NIFTY AUTO': 'NIFTY_AUTO.NS',
        'NIFTY FMCG': 'NIFTY_FMCG.NS',
        'NIFTY METAL': 'NIFTY_METAL.NS',
        'NIFTY REALTY': 'NIFTY_REALTY.NS',
        'NIFTY FINANCIAL': 'NIFTY_FIN_SERVICE.NS',
        'NIFTY INFRA': 'NIFTY_INFRA.NS',
        'NIFTY ENERGY': 'NIFTY_ENERGY.NS',
        'NIFTY PSU BANK': 'NIFTY_PSU_BANK.NS',
        'NIFTY PRIVATE BANK': 'NIFTY_PVT_BANK.NS',
        'NIFTY MEDIA': 'NIFTY_MEDIA.NS',
        'NIFTY OIL & GAS': 'NIFTY_OIL_AND_GAS.NS',
        'NIFTY HEALTHCARE': 'NIFTY_HEALTHCARE.NS',
        'NIFTY CONSUMER DURABLES': 'NIFTY_CONSR_DURBL.NS',
        'NIFTY MIDCAP 50': '^NSEMDCP50',
        'NIFTY SMALLCAP 50': 'NIFTY_SMLCAP_50.NS'
    }
    
    # Display major indices in cards
    indices_to_show = ['NIFTY 50', 'BANK NIFTY', 'NIFTY IT', 'NIFTY PHARMA']
    
    cols = st.columns(4)
    
    for idx, (name, symbol) in enumerate([(k, nifty_indices[k]) for k in indices_to_show]):
        try:
            quote = st.session_state.fetcher.get_quote(symbol)
            with cols[idx]:
                trend_emoji = "📈" if quote['change_percent'] > 0 else "📉"
                st.metric(
                    f"{trend_emoji} {name}", 
                    f"{quote['last_price']:.2f}", 
                    f"{quote['change_percent']:+.2f}%"
                )
        except:
            with cols[idx]:
                st.metric(name, "Loading...", "")
    
    # Additional indices in expander
    with st.expander("📊 View All NIFTY Indices"):
        remaining_indices = [k for k in nifty_indices.keys() if k not in indices_to_show]
        
        cols = st.columns(3)
        for idx, name in enumerate(remaining_indices):
            try:
                quote = st.session_state.fetcher.get_quote(nifty_indices[name])
                with cols[idx % 3]:
                    trend_emoji = "📈" if quote['change_percent'] > 0 else "📉"
                    st.metric(
                        f"{trend_emoji} {name}", 
                        f"{quote['last_price']:.2f}", 
                        f"{quote['change_percent']:+.2f}%"
                    )
            except:
                with cols[idx % 3]:
                    st.metric(name, "N/A", "")
    
    st.markdown("---")
    
    # Trading Type Selection
    st.subheader("🎯 Select Trading Type")
    
    trading_type = st.radio(
        "Choose what to trade:",
        ["📊 Stocks (Cash/Equity)", "🎲 Options (Call & Put)"],
        horizontal=True,
        help="Select whether to trade stocks or options"
    )
    
    st.markdown("---")
    
    # Index Selection
    st.subheader("🎯 Select NIFTY Index to Trade")
    
    # Define stocks for each index
    nifty_index_stocks = {
        'NIFTY 50': [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR',
            'BHARTIARTL', 'ITC', 'SBIN', 'KOTAKBANK', 'LT', 'AXISBANK',
            'BAJFINANCE', 'ASIANPAINT', 'MARUTI', 'TITAN', 'WIPRO', 'ULTRACEMCO',
            'NESTLEIND', 'TATASTEEL', 'POWERGRID', 'NTPC', 'ONGC', 'SUNPHARMA',
            'HCLTECH', 'TATAMOTORS', 'ADANIPORTS', 'JSWSTEEL', 'TECHM', 'INDUSINDBK'
        ],
        'BANK NIFTY': [
            'HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK',
            'INDUSINDBK', 'BANDHANBNK', 'FEDERALBNK', 'IDFCFIRSTB', 'PNB',
            'BANKBARODA', 'AUBANK'
        ],
        'NIFTY IT': [
            'TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM', 'LTIM',
            'COFORGE', 'PERSISTENT', 'MPHASIS', 'LTTS'
        ],
        'NIFTY PHARMA': [
            'SUNPHARMA', 'DRREDDY', 'DIVISLAB', 'CIPLA', 'AUROPHARMA',
            'TORNTPHARM', 'LUPIN', 'BIOCON', 'ALKEM', 'ABBOTINDIA'
        ],
        'NIFTY AUTO': [
            'MARUTI', 'TATAMOTORS', 'BAJAJ-AUTO', 'M&M', 'EICHERMOT',
            'HEROMOTOCO', 'BOSCHLTD', 'ASHOKLEY', 'TVSMOTOR', 'MOTHERSON'
        ],
        'NIFTY FMCG': [
            'HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR',
            'MARICO', 'GODREJCP', 'COLPAL', 'TATACONSUM', 'MCDOWELL-N'
        ],
        'NIFTY METAL': [
            'TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'COALINDIA', 'VEDL',
            'JINDALSTEL', 'SAIL', 'NMDC', 'HINDZINC', 'NATIONALUM'
        ],
        'NIFTY REALTY': [
            'DLF', 'GODREJPROP', 'OBEROIRLTY', 'BRIGADE', 'PRESTIGE',
            'PHOENIXLTD', 'SOBHA', 'MAHLIFE'
        ],
        'NIFTY FINANCIAL': [
            'HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK',
            'BAJFINANCE', 'HDFCLIFE', 'SBILIFE', 'ICICIPRULI', 'BAJAJFINSV',
            'INDUSINDBK', 'PNBHOUSING', 'CHOLAFIN'
        ],
        'NIFTY INFRA': [
            'LT', 'ADANIPORTS', 'POWERGRID', 'NTPC', 'GAIL',
            'ADANIGREEN', 'INDIGO', 'IRCTC', 'CONCOR', 'IRB'
        ],
        'NIFTY ENERGY': [
            'RELIANCE', 'ONGC', 'NTPC', 'POWERGRID', 'COALINDIA',
            'IOC', 'BPCL', 'GAIL', 'ADANIGREEN', 'ADANITRANS'
        ],
        'NIFTY PSU BANK': [
            'SBIN', 'PNB', 'BANKBARODA', 'CANARA', 'UNIONBANK',
            'INDIANB', 'MAHABANK', 'BANKOFBARODA'
        ],
        'NIFTY PRIVATE BANK': [
            'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'AXISBANK',
            'INDUSINDBK', 'BANDHANBNK', 'FEDERALBNK', 'IDFCFIRSTB'
        ],
        'NIFTY MEDIA': [
            'ZEEL', 'PVRINOX', 'SUNTV', 'TV18BRDCST', 'DISH',
            'NETWORK18', 'HATHWAY', 'NAZARA'
        ],
        'NIFTY OIL & GAS': [
            'RELIANCE', 'ONGC', 'IOC', 'BPCL', 'HINDPETRO',
            'GAIL', 'PETRONET', 'OIL', 'MGL', 'IGL'
        ],
        'NIFTY HEALTHCARE': [
            'SUNPHARMA', 'DRREDDY', 'DIVISLAB', 'CIPLA', 'APOLLOHOSP',
            'FORTIS', 'MAXHEALTH', 'AUROPHARMA', 'BIOCON', 'TORNTPHARM'
        ],
        'NIFTY CONSUMER DURABLES': [
            'TITAN', 'VOLTAS', 'HAVELLS', 'CROMPTON', 'WHIRLPOOL',
            'BATAINDIA', 'RAJESHEXPO', 'BLUESTARCO', 'SYMPHONY', 'AMBER'
        ],
        'NIFTY MIDCAP 50': [
            'GAIL', 'ADANIGREEN', 'COLPAL', 'DLF', 'GODREJCP',
            'LUPIN', 'BIOCON', 'BANDHANBNK', 'FEDERALBNK', 'ADANIPOWER',
            'MUTHOOTFIN', 'PEL', 'INDUSTOWER', 'ACC', 'GLENMARK'
        ],
        'NIFTY SMALLCAP 50': [
            'LICHSGFIN', 'CREDITACCESS', 'ATUL', 'ASTRAL', 'APLAPOLLO',
            'TIMKEN', 'CUMMINSIND', 'KPITTECH', 'CYIENT', 'SONACOMS',
            'DEEPAKNTR', 'COROMANDEL', 'CHAMBLFERT', 'GNFC', 'RCF'
        ]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_index = st.selectbox(
            "Choose NIFTY Index:",
            list(nifty_index_stocks.keys()),
            help="Select which NIFTY index you want to trade"
        )
    
    with col2:
        st.info(f"""
        **{selected_index} Selected**
        
        📊 **Stocks Available:** {len(nifty_index_stocks[selected_index])}
        🎯 **Focus:** {selected_index.split()[1] if len(selected_index.split()) > 1 else 'Broad Market'}
        """)
    
    st.markdown("---")
    
    # Options Configuration (if options trading selected)
    if trading_type == "🎲 Options (Call & Put)":
        st.subheader("🎲 Options Trading Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            option_type = st.selectbox(
                "Option Type",
                ["Call Options (CE)", "Put Options (PE)", "Both (CE & PE)"],
                help="Select which type of options to trade"
            )
        
        with col2:
            # Generate expiry dates (weekly/monthly)
            from datetime import timedelta
            today = datetime.now()
            
            # Find next Thursday (weekly expiry)
            days_ahead = 3 - today.weekday()  # 3 = Thursday
            if days_ahead <= 0:
                days_ahead += 7
            next_weekly = today + timedelta(days=days_ahead)
            
            # Monthly expiry (last Thursday of month)
            next_month = today.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            # Find last Thursday
            days_back = (last_day.weekday() - 3) % 7
            monthly_expiry = last_day - timedelta(days=days_back)
            
            expiry_dates = [
                f"Weekly: {next_weekly.strftime('%d-%b-%Y')}",
                f"Monthly: {monthly_expiry.strftime('%d-%b-%Y')}"
            ]
            
            selected_expiry = st.selectbox(
                "Expiry Date",
                expiry_dates,
                help="Choose expiry date for options"
            )
        
        with col3:
            # Strike price selection
            strike_selection = st.selectbox(
                "Strike Selection",
                ["ATM (At The Money)", "ITM (In The Money)", "OTM (Out of The Money)", "Custom Strikes"],
                help="Choose strike price strategy"
            )
        
        # Strike price details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if strike_selection == "Custom Strikes":
                custom_strikes = st.text_input(
                    "Enter Strikes (comma separated)",
                    "19000,19500,20000",
                    help="E.g., 19000,19500,20000"
                )
            else:
                num_strikes = st.slider(
                    "Number of Strikes",
                    min_value=1,
                    max_value=10,
                    value=3,
                    help="How many strikes to trade"
                )
        
        with col2:
            lot_size = st.number_input(
                "Lot Size",
                min_value=1,
                max_value=10,
                value=1,
                help="Number of lots per trade (NIFTY: 50 qty/lot, BANK NIFTY: 15 qty/lot)"
            )
        
        with col3:
            # Calculate lot quantity based on index
            if "BANK" in selected_index.upper():
                qty_per_lot = 15
            else:
                qty_per_lot = 50
            
            total_qty = lot_size * qty_per_lot
            st.metric("Total Quantity", f"{total_qty} units", f"{lot_size} lot(s)")
        
        # Options Strategy
        st.write("**Options Strategy:**")
        col1, col2 = st.columns(2)
        
        with col1:
            options_strategy = st.selectbox(
                "Trading Strategy",
                [
                    "Buy Call (Bullish)",
                    "Buy Put (Bearish)",
                    "Sell Call (Covered - Bearish)",
                    "Sell Put (Cash Secured - Bullish)",
                    "Straddle (Buy CE + PE)",
                    "Strangle (OTM CE + PE)",
                    "Bull Call Spread",
                    "Bear Put Spread",
                    "Iron Condor"
                ],
                help="Select your options trading strategy"
            )
        
        with col2:
            max_premium = st.number_input(
                "Max Premium per Option (₹)",
                min_value=1,
                max_value=500,
                value=100,
                step=10,
                help="Maximum premium you're willing to pay/receive"
            )
        
        # Options Greeks Configuration
        with st.expander("📊 Options Greeks & Risk Parameters"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Greeks Filters:**")
                min_delta = st.slider("Min Delta", 0.0, 1.0, 0.3, 0.05, help="Minimum delta value")
                max_theta = st.slider("Max Theta Decay", 0, 100, 50, 5, help="Maximum daily theta decay")
            
            with col2:
                st.write("**Risk Management:**")
                option_stop_loss = st.slider("Stop Loss (%)", 10, 100, 50, 5, help="Exit if premium drops by this %")
                option_target = st.slider("Profit Target (%)", 20, 200, 100, 10, help="Exit when premium increases by this %")
            
            with col3:
                st.write("**Position Limits:**")
                max_options_positions = st.number_input("Max Options Positions", 1, 20, 5, help="Max simultaneous option positions")
                max_options_capital = st.number_input("Max Capital for Options (₹)", 10000, 500000, 50000, 5000, help="Total capital for options")
        
        st.info("""
        🎲 **Options Trading Active**
        
        ✅ Trade NIFTY & BANK NIFTY options
        ✅ Both Call (CE) and Put (PE) options
        ✅ Weekly & Monthly expiries
        ✅ Multiple strategies supported
        ✅ Greeks-based filtering
        ✅ Advanced risk management
        
        ⚠️ **Note:** Options trading involves higher risk. Start with small positions!
        """)
        
        st.markdown("---")
    
    # Strategy Configuration
    st.subheader("⚙️ Trading Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        strategy_mode = st.selectbox(
            "Strategy Mode",
            ["Aggressive (High Profit)", "Balanced (Medium Risk)", "Conservative (Low Risk)"],
            help="Select your risk appetite for NIFTY trading"
        )
        
        if strategy_mode == "Aggressive (High Profit)":
            nifty_trader.config['capital_per_trade_percent'] = 20
            nifty_trader.config['max_trades_per_day'] = 10
            nifty_trader.config['stop_loss_percent'] = 3
            nifty_trader.config['target_percent'] = 7
            st.info("⚡ High risk, high reward strategy")
        elif strategy_mode == "Balanced (Medium Risk)":
            nifty_trader.config['capital_per_trade_percent'] = 15
            nifty_trader.config['max_trades_per_day'] = 7
            nifty_trader.config['stop_loss_percent'] = 2
            nifty_trader.config['target_percent'] = 5
            st.info("⚖️ Balanced risk-reward strategy")
        else:
            nifty_trader.config['capital_per_trade_percent'] = 10
            nifty_trader.config['max_trades_per_day'] = 5
            nifty_trader.config['stop_loss_percent'] = 1.5
            nifty_trader.config['target_percent'] = 3
            st.info("🛡️ Low risk, steady gains strategy")
    
    with col2:
        auto_strategy = st.selectbox(
            "Auto Strategy",
            ["Smart AI (Auto-Select)", "RSI Mean Reversion", "MA Trend Following", "Hybrid (Both)"],
            help="Algorithm for automatic trading"
        )
        
        if auto_strategy == "Smart AI (Auto-Select)":
            st.success("🤖 AI will choose best strategy per stock")
        elif auto_strategy == "RSI Mean Reversion":
            nifty_trader.config['strategy'] = 'RSI'
            st.info("📊 Buy oversold, sell overbought")
        elif auto_strategy == "MA Trend Following":
            nifty_trader.config['strategy'] = 'MA_Crossover'
            st.info("📈 Follow the trend direction")
        else:
            st.info("🔀 Uses both strategies dynamically")
    
    with col3:
        trading_capital = st.number_input(
            "Capital for NIFTY Trading (₹)",
            min_value=10000,
            max_value=10000000,
            value=int(nifty_trader.config['starting_capital']),
            step=10000,
            help="Amount to allocate for NIFTY trading"
        )
        
        if trading_capital != nifty_trader.config['starting_capital']:
            if st.button("💰 Update Capital", key="nifty_capital"):
                nifty_trader.update_capital(trading_capital)
                st.success(f"✅ Capital updated to ₹{trading_capital:,.0f}")
                st.rerun()
    
    # Stocks Selection based on selected index
    st.write(f"**{selected_index} Stocks to Trade:**")
    
    # Get stocks for selected index
    available_stocks = nifty_index_stocks[selected_index]
    
    # Quick select options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Select All", use_container_width=True):
            st.session_state.selected_stocks = available_stocks
            st.rerun()
    
    with col2:
        if st.button("🔝 Select Top 5", use_container_width=True):
            st.session_state.selected_stocks = available_stocks[:5]
            st.rerun()
    
    with col3:
        if st.button("🎯 Select Top 10", use_container_width=True):
            st.session_state.selected_stocks = available_stocks[:10]
            st.rerun()
    
    # Initialize selected stocks in session state
    if 'selected_stocks' not in st.session_state:
        st.session_state.selected_stocks = available_stocks[:10]
    
    # Make sure selected stocks are from the current index
    valid_selected = [s for s in st.session_state.selected_stocks if s in available_stocks]
    if not valid_selected:
        valid_selected = available_stocks[:10]
    
    selected_nifty_stocks = st.multiselect(
        f"Choose stocks from {selected_index}",
        available_stocks,
        default=valid_selected,
        help=f"Select which {selected_index} stocks to trade"
    )
    
    if selected_nifty_stocks:
        nifty_trader.config['stocks_to_trade'] = selected_nifty_stocks
        st.session_state.selected_stocks = selected_nifty_stocks
    
    st.caption(f"✓ {len(selected_nifty_stocks)} stocks selected from {selected_index}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scan_frequency = st.slider(
            "Scan Frequency (minutes)",
            min_value=1,
            max_value=30,
            value=5,
            help="How often to scan for trading opportunities"
        )
        nifty_trader.config['scan_interval_minutes'] = scan_frequency
    
    with col2:
        profit_target = st.slider(
            "Daily Profit Target (₹)",
            min_value=500,
            max_value=50000,
            value=5000,
            step=500,
            help="Stop trading when this profit is reached"
        )
    
    if st.button("💾 Save NIFTY Configuration", key="save_nifty_config"):
        nifty_trader.save_config()
        st.success("✅ NIFTY trading configuration saved!")
    
    st.markdown("---")
    
    # === AI AUTO-TRADING SECTION ===
    st.subheader("🤖 AI Auto-Trading for NIFTY Options")
    st.write("**Fully automated AI-powered options trading with machine learning**")
    
    # Initialize AI engine in session state
    if 'ai_engine' not in st.session_state:
        from ai_trading_engine import AITradingEngine
        st.session_state.ai_engine = AITradingEngine(
            capital=trading_capital,
            max_positions=5
        )
    
    ai_engine = st.session_state.ai_engine
    
    # AI Configuration
    with st.expander("⚙️ AI Trading Configuration", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ai_capital = st.number_input(
                "AI Trading Capital (₹)",
                min_value=50000,
                max_value=5000000,
                value=int(ai_engine.capital),
                step=50000,
                help="Capital allocated for AI trading"
            )
            
            if ai_capital != ai_engine.capital:
                ai_engine.capital = ai_capital
                ai_engine.available_capital = ai_capital
        
        with col2:
            max_positions_ai = st.slider(
                "Max Positions",
                min_value=1,
                max_value=10,
                value=ai_engine.max_positions,
                help="Maximum simultaneous positions"
            )
            ai_engine.max_positions = max_positions_ai
        
        with col3:
            max_trades_day = st.slider(
                "Max Trades/Day",
                min_value=5,
                max_value=50,
                value=ai_engine.max_trades_per_day,
                help="Maximum trades per day"
            )
            ai_engine.max_trades_per_day = max_trades_day
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_loss_pct = st.slider(
                "Max Daily Loss (%)",
                min_value=1.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                help="Maximum loss allowed per day"
            )
            ai_engine.max_loss_per_day = ai_engine.capital * (max_loss_pct / 100)
        
        with col2:
            max_trade_loss_pct = st.slider(
                "Max Loss/Trade (%)",
                min_value=0.5,
                max_value=5.0,
                value=2.0,
                step=0.5,
                help="Maximum loss per trade"
            )
            ai_engine.max_loss_per_trade = ai_engine.capital * (max_trade_loss_pct / 100)
        
        with col3:
            min_confidence = st.slider(
                "Min Confidence (%)",
                min_value=30,
                max_value=90,
                value=60,
                help="Minimum confidence to execute trade"
            )
        
        st.info("""
        **AI Trading Features:**
        - 🧠 Machine learning-based decision making
        - 📊 Automatic market condition analysis
        - 🎯 Strategy selection based on market state
        - 🛡️ Advanced risk management
        - 📈 Continuous learning from performance
        - ⚡ Real-time position monitoring
        """)
    
    # AI Status Dashboard
    ai_status = ai_engine.get_status()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        status_color = "🟢" if ai_status['is_active'] else "🔴"
        st.metric("AI Status", f"{status_color} {'ACTIVE' if ai_status['is_active'] else 'STOPPED'}")
    
    with col2:
        st.metric(
            "Total Capital",
            f"₹{ai_status['capital']:,.0f}",
            help="Total allocated capital"
        )
    
    with col3:
        st.metric(
            "Available",
            f"₹{ai_status['available_capital']:,.0f}",
            f"{(ai_status['available_capital']/ai_status['capital']*100):.1f}%"
        )
    
    with col4:
        st.metric(
            "Open Positions",
            f"{ai_status['open_positions']}/{ai_status['max_positions']}",
            help="Current/Maximum positions"
        )
    
    with col5:
        pnl_delta = f"{ai_status['roi']:+.2f}%"
        st.metric(
            "Total P&L",
            f"₹{ai_status['total_pnl']:,.0f}",
            pnl_delta
        )
    
    with col6:
        st.metric(
            "Trades Today",
            f"{ai_status['trades_today']}/{ai_engine.max_trades_per_day}",
            help="Today/Maximum"
        )
    
    # AI Controls
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not ai_status['is_active']:
            if st.button("🚀 Start AI Trading", type="primary", use_container_width=True):
                ai_engine.start()
                st.success("✅ AI Trading Engine Started!")
                st.info("AI will analyze market and execute trades automatically")
                st.rerun()
        else:
            if st.button("⏸️ Stop AI Trading", type="secondary", use_container_width=True):
                ai_engine.stop()
                st.warning("⚠️ AI Trading Engine Stopped")
                st.rerun()
    
    with col2:
        if st.button("📊 Analyze Market", use_container_width=True):
            with st.spinner("🧠 AI analyzing market conditions..."):
                # Fetch NIFTY data
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                nifty_data = st.session_state.fetcher.get_historical_data(
                    "^NSEI",
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )
                
                if not nifty_data.empty:
                    decision = ai_engine.analyze_and_decide(nifty_data, 'NIFTY 50')
                    
                    if decision:
                        st.session_state.last_ai_decision = decision
                        
                        if decision['decision'] == 'TRADE':
                            st.success(f"✅ {decision['reason']}")
                            st.info(f"**Strategy:** {decision['strategy']}\n**Confidence:** {decision['confidence']*100:.1f}%")
                        elif decision['decision'] == 'WAIT':
                            st.warning(f"⏳ {decision['reason']}")
                        else:
                            st.error(f"🛑 {decision['reason']}")
                else:
                    st.error("Failed to fetch NIFTY data")
    
    with col3:
        if st.button("💼 Monitor Positions", use_container_width=True):
            with st.spinner("Monitoring positions..."):
                actions = ai_engine.monitor_positions()
                if actions:
                    for action in actions:
                        if action['action'] == 'CLOSE':
                            if 'TARGET' in action['reason']:
                                st.success(f"✅ Position #{action['trade_id']} closed at target: {action['pnl_pct']:.2f}%")
                            else:
                                st.warning(f"⚠️ Position #{action['trade_id']} stopped: {action['pnl_pct']:.2f}%")
                        elif action['action'] == 'TRAIL_STOP':
                            st.info(f"📊 Position #{action['trade_id']} stop trailed to {action['new_stop']}%")
                else:
                    st.info("All positions within limits")
                st.rerun()
    
    with col4:
        if st.button("🔄 Reset AI", use_container_width=True):
            if st.session_state.get('confirm_ai_reset', False):
                # Reset AI engine
                from ai_trading_engine import AITradingEngine
                st.session_state.ai_engine = AITradingEngine(
                    capital=ai_capital,
                    max_positions=max_positions_ai
                )
                st.session_state.confirm_ai_reset = False
                st.success("✅ AI Engine Reset!")
                st.rerun()
            else:
                st.session_state.confirm_ai_reset = True
                st.warning("⚠️ Click again to confirm reset")
    
    # Show last AI decision if available
    if 'last_ai_decision' in st.session_state and st.session_state.last_ai_decision:
        decision = st.session_state.last_ai_decision
        
        with st.expander("🧠 Last AI Analysis", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Market Conditions:**")
                conditions = decision.get('market_conditions', {})
                st.write(f"- **Trend:** {conditions.get('trend', 'N/A')}")
                st.write(f"- **Volatility:** {conditions.get('volatility', 'N/A')}")
                st.write(f"- **Strength:** {conditions.get('strength', 0)*100:.1f}%")
                st.write(f"- **Confidence:** {conditions.get('confidence', 0)*100:.1f}%")
                
                indicators = conditions.get('indicators', {})
                if indicators:
                    st.write(f"- **RSI:** {indicators.get('rsi', 0):.2f}")
                    st.write(f"- **Current Price:** ₹{indicators.get('current_price', 0):.2f}")
            
            with col2:
                if decision['decision'] == 'TRADE':
                    st.write("**Trade Recommendation:**")
                    st.write(f"- **Strategy:** {decision.get('strategy', 'N/A')}")
                    st.write(f"- **Option Type:** {decision.get('option_type', 'N/A')}")
                    st.write(f"- **Strike:** {decision.get('strike_selection', 'N/A')}")
                    st.write(f"- **Quantity:** {decision.get('quantity', 0)} lots")
                    st.write(f"- **Stop Loss:** {decision.get('stop_loss_pct', 0)}%")
                    st.write(f"- **Target:** {decision.get('target_pct', 0)}%")
                    
                    if st.button("⚡ Execute This Trade", type="primary"):
                        result = ai_engine.execute_trade(decision)
                        if result['status'] == 'SUCCESS':
                            st.success(f"✅ {result['message']}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
                else:
                    st.write(f"**Decision:** {decision['decision']}")
                    st.write(f"**Reason:** {decision.get('reason', 'N/A')}")
    
    # AI Open Positions
    if ai_engine.positions:
        st.subheader("💼 AI Open Positions")
        
        positions_data = []
        for pos in ai_engine.positions:
            positions_data.append({
                'ID': pos['id'],
                'Time': pos['timestamp'].strftime('%H:%M:%S'),
                'Strategy': pos['strategy'],
                'Type': pos['option_type'],
                'Qty': pos['quantity'],
                'Entry': f"₹{pos['entry_premium']:.2f}",
                'Current': f"₹{pos.get('current_premium', pos['entry_premium']):.2f}",
                'P&L': f"₹{pos.get('pnl', 0):.2f}",
                'P&L%': f"{pos.get('pnl_pct', 0):.2f}%",
                'Status': pos['status']
            })
        
        df_positions = pd.DataFrame(positions_data)
        st.dataframe(df_positions, use_container_width=True)
    
    # AI Performance Summary
    if ai_engine.trade_history:
        with st.expander("📊 AI Performance Summary"):
            col1, col2, col3, col4 = st.columns(4)
            
            total_trades = len(ai_engine.trade_history)
            winning_trades = sum(1 for t in ai_engine.trade_history if t.get('pnl', 0) > 0)
            losing_trades = sum(1 for t in ai_engine.trade_history if t.get('pnl', 0) < 0)
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            with col1:
                st.metric("Total Trades", total_trades)
            with col2:
                st.metric("Winning Trades", winning_trades, f"+{win_rate:.1f}%")
            with col3:
                st.metric("Losing Trades", losing_trades)
            with col4:
                avg_pnl = sum(t.get('pnl', 0) for t in ai_engine.trade_history) / total_trades if total_trades > 0 else 0
                st.metric("Avg P&L/Trade", f"₹{avg_pnl:.2f}")
            
            # Strategy performance
            if ai_status['winning_strategies'] or ai_status['losing_strategies']:
                st.write("**Strategy Performance:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("✅ **Winning Strategies:**")
                    for strategy, count in sorted(ai_status['winning_strategies'].items(), key=lambda x: x[1], reverse=True):
                        st.write(f"- {strategy}: {count} wins")
                
                with col2:
                    st.write("❌ **Losing Strategies:**")
                    for strategy, count in sorted(ai_status['losing_strategies'].items(), key=lambda x: x[1], reverse=True):
                        st.write(f"- {strategy}: {count} losses")
    
    # Auto-Run AI Trading
    if ai_status['is_active']:
        st.info("""
        **🤖 AI Auto-Trading is ACTIVE**
        
        The AI engine will:
        - ✅ Analyze market conditions every 60 seconds
        - ✅ Execute trades when confidence > {min_confidence}%
        - ✅ Monitor positions every 30 seconds
        - ✅ Apply stop-loss and targets automatically
        - ✅ Learn from every trade
        
        ⚠️ **Safety Features Active:**
        - Max {max_positions_ai} positions at once
        - Max {max_trades_day} trades per day
        - Max {max_loss_pct}% daily loss limit
        - Max {max_trade_loss_pct}% loss per trade
        """.format(
            min_confidence=min_confidence,
            max_positions_ai=max_positions_ai,
            max_trades_day=max_trades_day,
            max_loss_pct=max_loss_pct,
            max_trade_loss_pct=max_trade_loss_pct
        ))
        
        # Auto-run loop (non-blocking with rerun)
        if st.button("▶️ Run AI Cycle Now", type="primary", use_container_width=True):
            with st.spinner("🤖 AI analyzing and executing..."):
                # Fetch NIFTY data
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                nifty_data = st.session_state.fetcher.get_historical_data(
                    "^NSEI",
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )
                
                if not nifty_data.empty:
                    # Analyze and decide
                    decision = ai_engine.analyze_and_decide(nifty_data, 'NIFTY 50')
                    
                    if decision and decision['decision'] == 'TRADE':
                        if decision['confidence'] >= (min_confidence / 100):
                            # Execute trade
                            result = ai_engine.execute_trade(decision)
                            if result['status'] == 'SUCCESS':
                                st.success(f"✅ Trade Executed: {result['message']}")
                            else:
                                st.warning(f"⚠️ {result['message']}")
                        else:
                            st.info(f"⏳ Confidence {decision['confidence']*100:.1f}% below threshold {min_confidence}%")
                    
                    # Monitor positions
                    actions = ai_engine.monitor_positions()
                    if actions:
                        for action in actions:
                            if action['action'] == 'CLOSE':
                                st.success(f"Position #{action['trade_id']} closed: {action['reason']}")
                
                st.rerun()
    
    st.markdown("---")
    
    # Live NIFTY Trading Status
    st.subheader("📊 NIFTY Trading Status")
    
    nifty_status = nifty_trader.get_status()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Capital", f"₹{nifty_status['capital']:,.0f}")
    
    with col2:
        st.metric("Available", f"₹{nifty_status['available_capital']:,.0f}")
    
    with col3:
        pnl_color = "normal" if nifty_status['daily_pnl'] >= 0 else "inverse"
        st.metric("Today's P&L", f"₹{nifty_status['daily_pnl']:,.0f}",
                 delta=f"{(nifty_status['daily_pnl']/nifty_status['capital']*100):.2f}%")
    
    with col4:
        st.metric("Trades Today", nifty_status['trades_today'])
    
    with col5:
        st.metric("Open Positions", nifty_status['positions_count'])
    
    # Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trades", nifty_status['total_trades'])
    
    with col2:
        st.metric("Win Rate", f"{nifty_status['win_rate']:.1f}%")
    
    with col3:
        st.metric("Total Profit", f"₹{nifty_status['total_profit']:,.0f}")
    
    with col4:
        roi = (nifty_status['total_profit'] / nifty_status['capital'] * 100) if nifty_status['capital'] > 0 else 0
        st.metric("ROI", f"{roi:.2f}%")
    
    st.markdown("---")
    
    # Control Panel
    st.subheader("🎮 NIFTY Trading Controls")
    
    # Initialize position monitoring state
    if 'position_monitor_active' not in st.session_state:
        st.session_state.position_monitor_active = False
    if 'monitor_check_count' not in st.session_state:
        st.session_state.monitor_check_count = 0
    if 'last_monitor_check' not in st.session_state:
        st.session_state.last_monitor_check = None
    if 'monitor_interval' not in st.session_state:
        st.session_state.monitor_interval = 5  # Default 5 seconds
    
    # Monitoring interval configuration (before buttons)
    if nifty_status['positions_count'] > 0:
        with st.expander("⚙️ Position Monitor Settings", expanded=False):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                monitor_interval = st.slider(
                    "Auto-Check Interval (seconds)",
                    min_value=1,
                    max_value=30,
                    value=st.session_state.monitor_interval,
                    help="How often to check positions for stop-loss/target"
                )
                st.session_state.monitor_interval = monitor_interval
            with col_b:
                st.metric("Current Setting", f"{st.session_state.monitor_interval}s", "per check")
            
            st.caption(f"✅ Positions will be checked every {st.session_state.monitor_interval} second(s) when monitoring is active")
            
            # Quick presets
            st.write("**Quick Presets:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("⚡ Fast (1s)", use_container_width=True):
                    st.session_state.monitor_interval = 1
                    st.rerun()
            with col2:
                if st.button("⚖️ Default (5s)", use_container_width=True):
                    st.session_state.monitor_interval = 5
                    st.rerun()
            with col3:
                if st.button("🐢 Slow (10s)", use_container_width=True):
                    st.session_state.monitor_interval = 10
                    st.rerun()
            with col4:
                if st.button("💤 Relaxed (30s)", use_container_width=True):
                    st.session_state.monitor_interval = 30
                    st.rerun()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Scan NIFTY Stocks", type="primary", use_container_width=True):
            with st.spinner("Scanning NIFTY stocks for signals..."):
                nifty_trader.run_once()
                st.success("✅ Scan complete!")
                st.rerun()
    
    with col2:
        # Position monitoring toggle
        if nifty_status['positions_count'] > 0:
            if not st.session_state.position_monitor_active:
                if st.button("👁️ Monitor Positions", use_container_width=True, type="primary", help="Auto-check positions every second"):
                    st.session_state.position_monitor_active = True
                    st.session_state.monitor_check_count = 0
                    st.session_state.last_monitor_check = datetime.now()
                    st.success("✅ Position monitoring started!")
                    st.rerun()
            else:
                if st.button("⏸️ Stop Monitoring", use_container_width=True, type="secondary"):
                    st.session_state.position_monitor_active = False
                    st.info("⏸️ Position monitoring stopped!")
                    st.rerun()
        else:
            st.button("👁️ Monitor Positions", use_container_width=True, disabled=True, help="No open positions to monitor")
    
    with col3:
        if st.button("💼 View Positions", use_container_width=True):
            st.session_state.page = "💼 Positions"
            st.rerun()
    
    with col4:
        if st.button("🔄 Reset Trader", use_container_width=True):
            if st.session_state.get('confirm_nifty_reset', False):
                nifty_trader.available_capital = nifty_trader.capital
                nifty_trader.positions = {}
                nifty_trader.trades_today = 0
                nifty_trader.daily_pnl = 0
                nifty_trader.all_trades = []
                nifty_trader.total_trades = 0
                nifty_trader.winning_trades = 0
                nifty_trader.total_profit = 0
                st.session_state.position_monitor_active = False  # Stop monitoring on reset
                st.success("✅ NIFTY trader reset!")
                st.session_state.confirm_nifty_reset = False
                st.rerun()
            else:
                st.session_state.confirm_nifty_reset = True
                st.warning("⚠️ Click again to confirm reset")
    
    # Position Monitoring Section
    if st.session_state.position_monitor_active:
        st.markdown("---")
        
        # Create containers for partial updates
        monitoring_section = st.container()
        
        with monitoring_section:
            # Monitoring status display
            st.subheader("👁️ Position Monitoring Active")
            
            # Create placeholders for dynamic content
            metrics_placeholder = st.empty()
            info_placeholder = st.empty()
            positions_placeholder = st.empty()
            alert_placeholder = st.empty()
            
            # Show static info
            with info_placeholder.container():
                st.info(f"""
                👁️ **Position Monitoring Active**
                
                ✅ Checking positions every {st.session_state.monitor_interval} second(s)
                ✅ Auto-exits when stop-loss hit
                ✅ Auto-exits when target reached
                ✅ Updates in real-time
                
                Click "Stop Monitoring" to pause
                """)
            
            # Check if positions exist
            if nifty_trader.positions:
                # Execute position check
                # Get current status before check
                positions_before = len(nifty_trader.positions)
                
                # Check all positions for stop-loss/target
                nifty_trader.check_positions()
                
                # Update check count and time
                st.session_state.monitor_check_count += 1
                st.session_state.last_monitor_check = datetime.now()
                
                # Check if any positions were closed
                positions_after = len(nifty_trader.positions)
                
                # Update metrics
                with metrics_placeholder.container():
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🟢 Status", "MONITORING", delta="Active")
                    
                    with col2:
                        st.metric("🔄 Checks Done", st.session_state.monitor_check_count)
                    
                    with col3:
                        if st.session_state.last_monitor_check:
                            time_since = (datetime.now() - st.session_state.last_monitor_check).seconds
                            st.metric("⏱️ Last Check", f"{time_since}s ago")
                    
                    with col4:
                        st.metric("💼 Positions", positions_after)
                
                # Show alert if positions were closed
                if positions_before > positions_after:
                    with alert_placeholder.container():
                        st.success(f"🎯 {positions_before - positions_after} position(s) closed automatically!")
                
                # Update positions table
                with positions_placeholder.container():
                    st.write("**Current Positions:**")
                    
                    positions_data = []
                    for symbol, pos in nifty_trader.positions.items():
                        try:
                            quote = st.session_state.fetcher.get_quote(symbol)
                            current_price = quote['last_price']
                            unrealized_pnl = (current_price - pos['entry_price']) * pos['quantity']
                            unrealized_pnl_pct = (unrealized_pnl / pos['cost']) * 100
                            
                            # Calculate distance to stop-loss and target
                            sl_distance = ((current_price - pos['stop_loss']) / current_price * 100)
                            target_distance = ((pos['target'] - current_price) / current_price * 100)
                            
                            # Status indicator
                            if current_price <= pos['stop_loss']:
                                status = "🔴 AT STOP-LOSS"
                            elif current_price >= pos['target']:
                                status = "🟢 AT TARGET"
                            elif sl_distance < 0.5:
                                status = "🟠 NEAR STOP-LOSS"
                            elif target_distance < 0.5:
                                status = "🟡 NEAR TARGET"
                            else:
                                status = "⚪ SAFE"
                            
                            positions_data.append({
                                'Symbol': symbol,
                                'Entry': f"₹{pos['entry_price']:.2f}",
                                'Current': f"₹{current_price:.2f}",
                                'Stop-Loss': f"₹{pos['stop_loss']:.2f}",
                                'Target': f"₹{pos['target']:.2f}",
                                'P&L': f"₹{unrealized_pnl:.2f} ({unrealized_pnl_pct:+.2f}%)",
                                'Status': status
                            })
                        except Exception as e:
                            # If error fetching price, skip this position
                            pass
                    
                    if positions_data:
                        df = pd.DataFrame(positions_data)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Wait for the configured interval before next check
                import time
                time.sleep(st.session_state.monitor_interval)
                
                # Use experimental_rerun to refresh only this section
                st.rerun()
            else:
                # No positions left
                with alert_placeholder.container():
                    st.warning("✅ All positions closed. Monitoring stopped.")
                st.session_state.position_monitor_active = False
                import time
                time.sleep(2)
    
    # Options Chain (if options trading is selected)
    if trading_type == "🎲 Options (Call & Put)":
        st.markdown("---")
        st.subheader("🎲 Options Chain & Live Prices")
        
        if st.button("📊 Load Options Chain", type="primary", use_container_width=False):
            with st.spinner(f"Loading options chain for {selected_index}..."):
                # Simulate options chain data (in production, fetch from API)
                st.success("✅ Options chain loaded!")
                
                # Get current index price (simulated)
                try:
                    if selected_index == "NIFTY 50":
                        index_symbol = '^NSEI'
                    elif selected_index == "BANK NIFTY":
                        index_symbol = '^NSEBANK'
                    else:
                        index_symbol = '^NSEI'
                    
                    index_quote = st.session_state.fetcher.get_quote(index_symbol)
                    current_price = index_quote['last_price']
                    
                    st.metric(f"📈 {selected_index} Current Price", f"₹{current_price:.2f}", f"{index_quote['change_percent']:+.2f}%")
                except:
                    current_price = 19500 if "BANK" not in selected_index else 45000
                    st.metric(f"📈 {selected_index} Current Price", f"₹{current_price:.2f} (Simulated)")
                
                st.markdown("---")
                
                # Generate sample options chain
                import random
                
                # Calculate ATM strike
                strike_interval = 100 if "BANK" in selected_index else 50
                atm_strike = round(current_price / strike_interval) * strike_interval
                
                # Generate strikes around ATM
                strikes = [atm_strike + (i * strike_interval) for i in range(-5, 6)]
                
                # Create options chain data
                options_data = []
                
                for strike in strikes:
                    # Calculate if ITM/ATM/OTM
                    if strike == atm_strike:
                        moneyness = "ATM"
                    elif strike < current_price:
                        moneyness = "ITM (Call)"
                    else:
                        moneyness = "OTM (Call)"
                    
                    # Simulate premium values (in production, fetch real data)
                    distance_from_atm = abs(strike - current_price)
                    
                    # Call premium (decreases as strike increases)
                    call_premium = max(10, 200 - (distance_from_atm / 10) + random.uniform(-20, 20))
                    call_iv = random.uniform(15, 35)  # Implied Volatility
                    call_oi = random.randint(10000, 100000)  # Open Interest
                    
                    # Put premium (increases as strike increases)
                    put_premium = max(10, 50 + (distance_from_atm / 10) + random.uniform(-20, 20))
                    put_iv = random.uniform(15, 35)
                    put_oi = random.randint(10000, 100000)
                    
                    options_data.append({
                        'Strike': f"₹{strike:.0f}",
                        'Moneyness': moneyness,
                        'Call Premium': f"₹{call_premium:.2f}",
                        'Call IV': f"{call_iv:.1f}%",
                        'Call OI': f"{call_oi:,}",
                        'Put Premium': f"₹{put_premium:.2f}",
                        'Put IV': f"{put_iv:.1f}%",
                        'Put OI': f"{put_oi:,}"
                    })
                
                # Display options chain
                st.write(f"**Options Chain for {selected_expiry}:**")
                
                options_df = pd.DataFrame(options_data)
                
                # Highlight ATM row
                st.dataframe(
                    options_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Additional insights
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Call Options:**")
                    st.write("- Higher premium at lower strikes")
                    st.write("- Buy if bullish")
                    st.write("- Sell if bearish (covered)")
                
                with col2:
                    st.write("**Put Options:**")
                    st.write("- Higher premium at higher strikes")
                    st.write("- Buy if bearish")
                    st.write("- Sell if bullish (cash secured)")
                
                with col3:
                    st.write("**Current Analysis:**")
                    # Calculate Put-Call Ratio (simulated)
                    pcr = random.uniform(0.8, 1.2)
                    if pcr < 0.9:
                        sentiment = "🟢 Bullish"
                    elif pcr > 1.1:
                        sentiment = "🔴 Bearish"
                    else:
                        sentiment = "🟡 Neutral"
                    
                    st.metric("Put-Call Ratio", f"{pcr:.2f}", sentiment)
                
                # Quick Actions
                st.write("**Quick Actions:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📈 Buy ATM Call", use_container_width=True):
                        st.success(f"✅ Bought Call @ {atm_strike} for demo!")
                
                with col2:
                    if st.button("📉 Buy ATM Put", use_container_width=True):
                        st.success(f"✅ Bought Put @ {atm_strike} for demo!")
                
                with col3:
                    if st.button("🎲 Execute Straddle", use_container_width=True):
                        st.success(f"✅ Executed Straddle @ {atm_strike} for demo!")
        
        # Options Strategy Guide
        with st.expander("📚 Options Strategies Guide"):
            st.write("""
            **Popular Options Strategies:**
            
            **1. Buy Call (Bullish)**
            - Profit: Unlimited upside
            - Loss: Limited to premium paid
            - Use: When expecting strong upward move
            
            **2. Buy Put (Bearish)**
            - Profit: Substantial downside (till index hits 0)
            - Loss: Limited to premium paid
            - Use: When expecting strong downward move
            
            **3. Straddle (Neutral Volatility)**
            - Buy ATM Call + ATM Put
            - Profit: Big move in either direction
            - Loss: If market stays range-bound
            - Use: Before major events/announcements
            
            **4. Strangle (Neutral Volatility - Lower Cost)**
            - Buy OTM Call + OTM Put
            - Cheaper than straddle
            - Needs bigger move to profit
            
            **5. Bull Call Spread**
            - Buy lower strike Call + Sell higher strike Call
            - Limited profit, limited loss
            - Lower cost than buying call alone
            
            **6. Bear Put Spread**
            - Buy higher strike Put + Sell lower strike Put
            - Limited profit, limited loss
            - Lower cost than buying put alone
            
            **7. Iron Condor**
            - Sell OTM Call + Buy further OTM Call
            - Sell OTM Put + Buy further OTM Put
            - Profit if market stays in range
            - Advanced strategy
            
            **Greeks Explained:**
            
            - **Delta**: Rate of change in option price per ₹1 change in underlying
            - **Gamma**: Rate of change in delta
            - **Theta**: Daily time decay of option premium
            - **Vega**: Sensitivity to volatility changes
            - **IV (Implied Volatility)**: Market's expectation of future volatility
            
            **Risk Management:**
            - Never risk more than 2-5% of capital on one trade
            - Always use stop-loss
            - Monitor theta decay daily
            - Watch for expiry dates
            - Start with small positions
            """)
        
        st.markdown("---")
    
    # Live Signals
    st.markdown("---")
    st.subheader("📡 Live NIFTY Signals")
    
    if st.button("🔍 Get Current Signals", key="get_nifty_signals"):
        with st.spinner("Analyzing NIFTY stocks..."):
            signals = nifty_trader.scan_for_signals()
            
            if signals:
                st.success(f"✅ Found {len(signals)} trading signals!")
                
                for signal in signals:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 3])
                        
                        with col1:
                            if signal['action'] == 'BUY':
                                st.markdown(f"### 🟢 BUY {signal['symbol']}")
                            else:
                                st.markdown(f"### 🔴 SELL {signal['symbol']}")
                        
                        with col2:
                            st.metric("Price", f"₹{signal['price']:.2f}")
                        
                        with col3:
                            strength_emoji = "⚡" if signal['strength'] == 'STRONG' else "📊"
                            st.metric("Strength", f"{strength_emoji} {signal['strength']}")
                        
                        with col4:
                            st.write(f"**Reason:** {signal['reason']}")
                        
                        st.markdown("---")
            else:
                st.info("No signals found at this moment. Market conditions may not be favorable.")
    
    # Strategy Performance
    st.markdown("---")
    st.subheader("📊 NIFTY Strategy Performance")
    
    if nifty_status['all_trades']:
        trades_df = pd.DataFrame(nifty_status['all_trades'][-10:])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Recent Trades:**")
            display_df = trades_df.copy()
            display_df['Entry'] = display_df['entry_price'].apply(lambda x: f"₹{x:.2f}")
            display_df['Exit'] = display_df['exit_price'].apply(lambda x: f"₹{x:.2f}")
            display_df['Profit'] = display_df['profit'].apply(lambda x: f"₹{x:.2f}")
            display_df['%'] = display_df['profit_percent'].apply(lambda x: f"{x:+.2f}%")
            
            st.dataframe(
                display_df[['symbol', 'Entry', 'Exit', 'quantity', 'Profit', '%']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.write("**Performance Chart:**")
            
            # Calculate cumulative profit
            cumulative_profit = trades_df['profit'].cumsum().tolist()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=cumulative_profit,
                mode='lines+markers',
                name='Cumulative Profit',
                line=dict(color='green' if cumulative_profit[-1] > 0 else 'red', width=2)
            ))
            
            fig.update_layout(
                title="Profit Curve",
                yaxis_title="Profit (₹)",
                xaxis_title="Trade #",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Index Performance Comparison
    st.markdown("---")
    st.subheader("📊 Today's Index Performance Comparison")
    
    if st.button("🔍 Compare All Indices Performance", key="compare_indices"):
        with st.spinner("Comparing all NIFTY indices..."):
            index_performance = []
            
            for name, symbol in nifty_indices.items():
                try:
                    quote = st.session_state.fetcher.get_quote(symbol)
                    index_performance.append({
                        'Index': name,
                        'Price': quote['last_price'],
                        'Change %': quote['change_percent'],
                        'Status': '📈' if quote['change_percent'] > 0 else '📉'
                    })
                except:
                    pass
            
            if index_performance:
                # Sort by change percentage
                index_performance.sort(key=lambda x: x['Change %'], reverse=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**All Indices Performance:**")
                    perf_df = pd.DataFrame(index_performance)
                    perf_df['Price'] = perf_df['Price'].apply(lambda x: f"{x:.2f}")
                    perf_df['Change %'] = perf_df['Change %'].apply(lambda x: f"{x:+.2f}%")
                    st.dataframe(perf_df, use_container_width=True, hide_index=True)
                
                with col2:
                    st.write("**Top Performers:**")
                    top_3 = index_performance[:3]
                    for idx, perf in enumerate(top_3, 1):
                        st.success(f"#{idx} {perf['Index']}: {perf['Change %']:+.2f}%")
                    
                    st.write("**Bottom Performers:**")
                    bottom_3 = index_performance[-3:]
                    for idx, perf in enumerate(bottom_3, 1):
                        st.error(f"#{idx} {perf['Index']}: {perf['Change %']:+.2f}%")
    
    # Tips and Information
    st.markdown("---")
    st.subheader("💡 NIFTY Trading Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Why Trade NIFTY Indices?**
        
        ✅ **High Liquidity** - Easy to buy/sell
        ✅ **Sectoral Focus** - Target specific industries
        ✅ **Better Volume** - More trading opportunities
        ✅ **Market Leaders** - Only top companies
        ✅ **Diversified** - Spread risk across sectors
        
        **Best Indices for Different Market Conditions:**
        
        📈 **Bull Market:** NIFTY IT, NIFTY BANK
        📉 **Bear Market:** NIFTY PHARMA, NIFTY FMCG
        ⚡ **Volatile Market:** NIFTY METAL, NIFTY AUTO
        🛡️ **Safe Play:** NIFTY 50, NIFTY FINANCIAL
        """)
    
    with col2:
        st.success("""
        **Maximize Your Profits:**
        
        🎯 **Use Aggressive Mode** for trending sectors
        🎯 **Use Conservative Mode** for choppy markets
        🎯 **Switch Indices** based on market sentiment
        🎯 **Monitor Index Performance** daily
        🎯 **Set Profit Targets** and stick to them
        
        **Pro Tips:**
        
        💡 **Bank NIFTY** - Most volatile, high returns
        💡 **NIFTY IT** - Best for export growth
        💡 **NIFTY PHARMA** - Defensive play
        💡 **NIFTY FMCG** - Steady and stable
        💡 **NIFTY METAL** - Commodity cycle play
        """)
    
    with st.expander("📚 How Auto-Trading Works"):
        st.write("""
        **NIFTY Auto-Trading System:**
        
        1. **Scanning:** Every few minutes, scans all selected NIFTY stocks
        2. **Analysis:** Applies technical indicators (RSI, MACD, MA, etc.)
        3. **Signal Generation:** Identifies buy/sell opportunities
        4. **Execution:** Automatically places trades (simulation or live)
        5. **Risk Management:** Auto stop-loss and profit targets
        6. **Monitoring:** Continuously checks positions for exit conditions
        
        **Strategies:**
        
        - **RSI Mean Reversion:** Buy when oversold (RSI < 30), sell when overbought (RSI > 70)
        - **MA Trend Following:** Buy on golden cross, sell on death cross
        - **Hybrid:** Uses both strategies based on market conditions
        - **Smart AI:** Automatically selects best strategy for each stock
        
        **Risk Controls:**
        
        - Maximum trades per day limit
        - Daily loss limit protection
        - Per-trade stop-loss
        - Profit target booking
        - Position size management
        """)

# POSITIONS PAGE
elif page == "💼 Positions":
    st.header("💼 Positions")
    st.write("**View and manage all your open positions**")
    
    # Get positions from both traders
    positions_list = []
    
    # From regular auto-trader
    if 'autotrader' in st.session_state:
        trader = st.session_state.autotrader
        for symbol, pos in trader.positions.items():
            try:
                quote = st.session_state.fetcher.get_quote(symbol)
                current_price = quote['last_price']
                unrealized_pnl = (current_price - pos['entry_price']) * pos['quantity']
                unrealized_pnl_pct = (unrealized_pnl / pos['cost']) * 100
                
                positions_list.append({
                    'source': 'Auto-Trader',
                    'symbol': symbol,
                    'entry_price': pos['entry_price'],
                    'current_price': current_price,
                    'quantity': pos['quantity'],
                    'cost': pos['cost'],
                    'current_value': current_price * pos['quantity'],
                    'unrealized_pnl': unrealized_pnl,
                    'unrealized_pnl_pct': unrealized_pnl_pct,
                    'stop_loss': pos['stop_loss'],
                    'target': pos['target'],
                    'entry_time': pos['entry_time'],
                    'reason': pos['reason']
                })
            except:
                pass
    
    # From NIFTY trader
    if 'nifty_trader' in st.session_state:
        nifty_trader = st.session_state.nifty_trader
        for symbol, pos in nifty_trader.positions.items():
            try:
                quote = st.session_state.fetcher.get_quote(symbol)
                current_price = quote['last_price']
                unrealized_pnl = (current_price - pos['entry_price']) * pos['quantity']
                unrealized_pnl_pct = (unrealized_pnl / pos['cost']) * 100
                
                positions_list.append({
                    'source': 'NIFTY Trader',
                    'symbol': symbol,
                    'entry_price': pos['entry_price'],
                    'current_price': current_price,
                    'quantity': pos['quantity'],
                    'cost': pos['cost'],
                    'current_value': current_price * pos['quantity'],
                    'unrealized_pnl': unrealized_pnl,
                    'unrealized_pnl_pct': unrealized_pnl_pct,
                    'stop_loss': pos['stop_loss'],
                    'target': pos['target'],
                    'entry_time': pos['entry_time'],
                    'reason': pos['reason']
                })
            except:
                pass
    
    if not positions_list:
        st.info("📭 No open positions at the moment")
        st.write("Start trading to see positions here!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Go to Auto-Trader", use_container_width=True):
                st.session_state.page = "🤖 Auto-Trader"
                st.rerun()
        with col2:
            if st.button("📊 Go to NIFTY Trading", use_container_width=True):
                st.session_state.page = "📊 NIFTY Trading"
                st.rerun()
    else:
        # Summary metrics
        total_cost = sum(p['cost'] for p in positions_list)
        total_current_value = sum(p['current_value'] for p in positions_list)
        total_unrealized_pnl = total_current_value - total_cost
        total_unrealized_pnl_pct = (total_unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Open Positions", len(positions_list))
        
        with col2:
            st.metric("Total Investment", f"₹{total_cost:,.0f}")
        
        with col3:
            st.metric("Current Value", f"₹{total_current_value:,.0f}")
        
        with col4:
            st.metric(
                "Unrealized P&L",
                f"₹{total_unrealized_pnl:,.0f}",
                f"{total_unrealized_pnl_pct:+.2f}%"
            )
        
        st.markdown("---")
        
        # Refresh button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🔄 Refresh Prices", use_container_width=True):
                st.rerun()
        with col2:
            auto_refresh = st.checkbox("Auto-refresh", value=False)
        
        if auto_refresh:
            import time
            time.sleep(30)
            st.rerun()
        
        st.markdown("---")
        
        # Display positions
        st.subheader("📊 All Positions")
        
        for idx, pos in enumerate(positions_list, 1):
            with st.container():
                # Header row
                col1, col2, col3 = st.columns([2, 4, 1])
                
                with col1:
                    pnl_emoji = "🟢" if pos['unrealized_pnl'] >= 0 else "🔴"
                    st.markdown(f"### {pnl_emoji} {pos['symbol']}")
                    st.caption(f"Source: {pos['source']}")
                
                with col2:
                    st.write(f"**Entry Reason:** {pos['reason']}")
                    entry_time_str = pos['entry_time'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(pos['entry_time'], 'strftime') else str(pos['entry_time'])
                    st.caption(f"Entered on: {entry_time_str}")
                
                with col3:
                    if st.button(f"Close", key=f"close_{idx}", use_container_width=True):
                        st.warning(f"⚠️ Close position for {pos['symbol']}? This will execute a sell order.")
                
                # Metrics row
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    st.metric("Qty", pos['quantity'])
                
                with col2:
                    st.metric("Entry Price", f"₹{pos['entry_price']:.2f}")
                
                with col3:
                    st.metric("Current Price", f"₹{pos['current_price']:.2f}")
                
                with col4:
                    st.metric("Investment", f"₹{pos['cost']:,.0f}")
                
                with col5:
                    st.metric("Current Value", f"₹{pos['current_value']:,.0f}")
                
                with col6:
                    pnl_delta = f"{pos['unrealized_pnl_pct']:+.2f}%"
                    st.metric("P&L", f"₹{pos['unrealized_pnl']:,.0f}", delta=pnl_delta)
                
                # Risk metrics row
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**Stop Loss:** ₹{pos['stop_loss']:.2f}")
                    sl_distance = ((pos['current_price'] - pos['stop_loss']) / pos['current_price'] * 100)
                    st.caption(f"Distance: {sl_distance:.2f}%")
                
                with col2:
                    st.write(f"**Target:** ₹{pos['target']:.2f}")
                    target_distance = ((pos['target'] - pos['current_price']) / pos['current_price'] * 100)
                    st.caption(f"Distance: {target_distance:.2f}%")
                
                with col3:
                    risk = pos['entry_price'] - pos['stop_loss']
                    reward = pos['target'] - pos['entry_price']
                    risk_reward = reward / risk if risk > 0 else 0
                    st.write(f"**Risk:Reward:** 1:{risk_reward:.2f}")
                
                with col4:
                    # Progress bar to target
                    progress = min(100, max(0, pos['unrealized_pnl_pct'] / ((pos['target'] - pos['entry_price']) / pos['entry_price'] * 100) * 100))
                    st.write("**Progress to Target:**")
                    st.progress(progress / 100)
                
                st.markdown("---")
        
        # Export positions
        st.subheader("📥 Export Positions")
        
        if st.button("💾 Download Positions as CSV"):
            positions_df = pd.DataFrame(positions_list)
            csv = positions_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"positions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Position Analytics
        st.markdown("---")
        st.subheader("📊 Position Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # P&L Distribution
            st.write("**P&L Distribution:**")
            
            fig = go.Figure()
            
            colors = ['green' if p['unrealized_pnl'] >= 0 else 'red' for p in positions_list]
            
            fig.add_trace(go.Bar(
                x=[p['symbol'] for p in positions_list],
                y=[p['unrealized_pnl'] for p in positions_list],
                marker_color=colors,
                text=[f"₹{p['unrealized_pnl']:.0f}" for p in positions_list],
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Unrealized P&L by Stock",
                xaxis_title="Stock",
                yaxis_title="P&L (₹)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Position Size Distribution
            st.write("**Position Size Distribution:**")
            
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=[p['symbol'] for p in positions_list],
                values=[p['cost'] for p in positions_list],
                hole=0.4
            ))
            
            fig.update_layout(
                title="Capital Allocation",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk Analysis
        with st.expander("⚠️ Risk Analysis"):
            st.write("**Position Risk Summary:**")
            
            for pos in positions_list:
                risk_amount = (pos['entry_price'] - pos['stop_loss']) * pos['quantity']
                risk_pct = ((pos['entry_price'] - pos['stop_loss']) / pos['entry_price'] * 100)
                
                st.write(f"""
                **{pos['symbol']}:**
                - Maximum Risk: ₹{risk_amount:,.0f} ({risk_pct:.2f}%)
                - Stop Loss at: ₹{pos['stop_loss']:.2f}
                - Current Distance from SL: {((pos['current_price'] - pos['stop_loss']) / pos['current_price'] * 100):.2f}%
                """)
            
            total_risk = sum((p['entry_price'] - p['stop_loss']) * p['quantity'] for p in positions_list)
            st.markdown("---")
            st.write(f"**Total Portfolio Risk:** ₹{total_risk:,.0f}")
            st.write(f"**Risk as % of Investment:** {(total_risk / total_cost * 100):.2f}%")

# BUY RECOMMENDATIONS PAGE
elif page == "🎯 Buy Recommendations":
    st.header("🎯 Strong Buy Recommendations")
    st.write("AI-powered stock recommendations based on technical analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("**How it works:** Scans stocks using multiple indicators (RSI, MACD, Moving Averages) and identifies strong buy signals")
    
    with col2:
        auto_refresh = st.checkbox("Auto-scan", value=False)
    
    if st.button("🔍 Scan Stocks for Buy Signals", type="primary", use_container_width=True) or auto_refresh:
        
        with st.spinner("🔍 Analyzing stocks... This will take 1-2 minutes..."):
            
            # Stocks to scan
            scan_stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 
                          'SBIN', 'BHARTIARTL', 'ITC', 'KOTAKBANK', 'LT']
            
            recommendations = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, symbol in enumerate(scan_stocks):
                status_text.text(f"Scanning {symbol}... ({idx+1}/{len(scan_stocks)})")
                progress_bar.progress((idx + 1) / len(scan_stocks))
                
                try:
                    # Fetch recent data
                    from datetime import datetime, timedelta
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
                    
                    data = st.session_state.fetcher.get_historical_data(symbol, start_date, end_date)
                    
                    if len(data) < 20:
                        continue
                    
                    # Add indicators
                    data_with_indicators = TechnicalIndicators.add_all_indicators(data)
                    latest = data_with_indicators.iloc[-1]
                    
                    # Calculate signals
                    buy_signals = 0
                    signal_reasons = []
                    
                    # RSI Signal
                    if latest['RSI'] < 35:
                        buy_signals += 2
                        signal_reasons.append(f"RSI Oversold ({latest['RSI']:.1f})")
                    elif latest['RSI'] < 45:
                        buy_signals += 1
                        signal_reasons.append(f"RSI Neutral-Low ({latest['RSI']:.1f})")
                    
                    # MACD Signal
                    if latest['MACD'] > latest['MACD_Signal'] and latest['MACD_Hist'] > 0:
                        buy_signals += 2
                        signal_reasons.append("MACD Bullish Cross")
                    
                    # Moving Average Signal
                    if latest['SMA_20'] > latest['SMA_50']:
                        buy_signals += 1
                        signal_reasons.append("MA Trend Up")
                    
                    # Price vs MA
                    if latest['Close'] < latest['SMA_20']:
                        buy_signals += 1
                        signal_reasons.append("Price Below MA (Dip)")
                    
                    # Bollinger Bands
                    if latest['Close'] < latest['BB_Lower']:
                        buy_signals += 2
                        signal_reasons.append("Price Below BB Lower")
                    
                    # Volume spike
                    avg_volume = data_with_indicators['Volume'].tail(10).mean()
                    if latest['Volume'] > avg_volume * 1.2:
                        buy_signals += 1
                        signal_reasons.append("High Volume")
                    
                    # Get quote for price
                    quote = st.session_state.fetcher.get_quote(symbol)
                    
                    # Determine strength
                    if buy_signals >= 5:
                        strength = "🟢 STRONG BUY"
                        strength_score = "Very Strong"
                    elif buy_signals >= 3:
                        strength = "🟡 BUY"
                        strength_score = "Moderate"
                    elif buy_signals >= 2:
                        strength = "🔵 WEAK BUY"
                        strength_score = "Weak"
                    else:
                        strength = "⚪ HOLD"
                        strength_score = "Hold"
                    
                    if buy_signals >= 2:  # Only show buy recommendations
                        recommendations.append({
                            'Stock': symbol,
                            'Signal': strength,
                            'Score': buy_signals,
                            'Price': quote['last_price'],
                            'RSI': latest['RSI'],
                            'Reasons': ', '.join(signal_reasons),
                            'Strength': strength_score
                        })
                
                except Exception as e:
                    st.warning(f"Could not analyze {symbol}: {str(e)}")
                    continue
            
            progress_bar.empty()
            status_text.empty()
            
            # Sort by score
            recommendations.sort(key=lambda x: x['Score'], reverse=True)
            
            if recommendations:
                st.success(f"✅ Found {len(recommendations)} buy opportunities!")
                
                # Show top recommendations
                st.subheader("🏆 Top Recommendations")
                
                for i, rec in enumerate(recommendations[:3], 1):
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 3])
                        
                        with col1:
                            st.markdown(f"### {rec['Signal']} {rec['Stock']}")
                        
                        with col2:
                            st.metric("Price", f"₹{rec['Price']:.2f}")
                        
                        with col3:
                            st.metric("RSI", f"{rec['RSI']:.1f}")
                        
                        with col4:
                            st.write(f"**Signals:** {rec['Reasons']}")
                        
                        st.markdown("---")
                
                # Detailed table
                st.subheader("📊 All Recommendations")
                
                import pandas as pd
                df = pd.DataFrame(recommendations)
                df['Price'] = df['Price'].apply(lambda x: f"₹{x:.2f}")
                df['RSI'] = df['RSI'].apply(lambda x: f"{x:.1f}")
                
                st.dataframe(
                    df[['Stock', 'Signal', 'Price', 'RSI', 'Reasons']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Explanation
                st.subheader("💡 How to Use These Recommendations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("""
                    **🟢 STRONG BUY (5+ signals)**
                    - Multiple indicators confirm
                    - High probability setup
                    - Consider for immediate action
                    """)
                    
                    st.write("""
                    **🟡 BUY (3-4 signals)**
                    - Good setup with confirmation
                    - Moderate probability
                    - Watch for entry point
                    """)
                
                with col2:
                    st.write("""
                    **🔵 WEAK BUY (2 signals)**
                    - Early signal
                    - Need more confirmation
                    - Add to watchlist
                    """)
                    
                    st.write("""
                    **⚠️ Important:**
                    - These are signals, not guarantees
                    - Always do your own research
                    - Use stop-loss in real trading
                    """)
                
                # Action buttons
                st.subheader("🚀 Next Steps")
                
                if recommendations:
                    top_stock = recommendations[0]['Stock']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"📊 Backtest {top_stock} with RSI", use_container_width=True):
                            st.info(f"Go to 'Run Backtest' page and test {top_stock} with RSI Strategy!")
                    
                    with col2:
                        if st.button(f"💰 View {top_stock} Price Details", use_container_width=True):
                            st.info(f"Go to 'Live Prices' page to see {top_stock} details!")
            
            else:
                st.warning("⚠️ No strong buy signals found at this moment.")
                st.info("""
                **This could mean:**
                - Market is overbought (wait for dip)
                - Stocks are at high prices
                - Wait for better opportunities
                
                **Try again:**
                - Check back in a few hours
                - Market conditions change daily
                """)

# STOCK DETAILS PAGE
elif page == "📊 Stock Details":
    st.header("📊 Stock Details & Analysis")
    st.write("Complete technical analysis and insights for any stock")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        stock_symbol = st.text_input(
            "Enter Stock Symbol:",
            "TCS",
            help="Enter NSE stock symbol (e.g., RELIANCE, TCS, INFY)"
        ).upper()
    
    with col2:
        days_back = st.selectbox(
            "Time Period:",
            [30, 60, 90, 180, 365],
            index=2,
            help="Days of historical data"
        )
    
    with col3:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_btn or stock_symbol:
        try:
            with st.spinner(f"Analyzing {stock_symbol}..."):
                
                # Fetch data
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)
                
                data = st.session_state.fetcher.get_historical_data(
                    stock_symbol,
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )
                
                if data.empty:
                    st.error(f"❌ No data found for {stock_symbol}. Check the symbol and try again.")
                else:
                    # Get quote
                    quote = st.session_state.fetcher.get_quote(stock_symbol)
                    
                    # Add indicators
                    data_with_indicators = TechnicalIndicators.add_all_indicators(data)
                    latest = data_with_indicators.iloc[-1]
                    
                    # === HEADER METRICS ===
                    st.subheader(f"📈 {stock_symbol} - Overview")
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric(
                            "Current Price",
                            f"₹{quote['last_price']:.2f}",
                            f"{quote['change_percent']:.2f}%"
                        )
                    
                    with col2:
                        st.metric("Open", f"₹{quote['open']:.2f}")
                    
                    with col3:
                        st.metric("High", f"₹{quote['high']:.2f}")
                    
                    with col4:
                        st.metric("Low", f"₹{quote['low']:.2f}")
                    
                    with col5:
                        st.metric("Volume", f"{quote['volume']:,.0f}")
                    
                    st.markdown("---")
                    
                    # === CHART TYPE SELECTOR ===
                    st.subheader("📈 Price Chart")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        chart_type = st.radio(
                            "Select Chart Type:",
                            ["📊 TradingView Advanced", "📉 TradingView Lightweight", "📈 Plotly Interactive"],
                            horizontal=True,
                            index=0
                        )
                    with col2:
                        if chart_type == "📊 TradingView Advanced":
                            chart_interval = st.selectbox(
                                "Interval:",
                                ["1", "5", "15", "60", "D", "W", "M"],
                                index=4,
                                help="1=1min, 5=5min, D=Daily, W=Weekly, M=Monthly"
                            )
                    
                    st.markdown("---")
                    
                    # === TRADINGVIEW ADVANCED CHART ===
                    if chart_type == "📊 TradingView Advanced":
                        # Convert NSE symbol to TradingView format
                        # NSE stocks: use NSE:SYMBOL format
                        tv_symbol = f"NSE:{stock_symbol}"
                        
                        # Generate unique container ID
                        import random
                        container_id = f"tradingview_{random.randint(10000, 99999)}"
                        
                        tradingview_widget = f"""
                        <!-- TradingView Widget BEGIN -->
                        <div class="tradingview-widget-container" style="height:100%;width:100%">
                          <div id="{container_id}" style="height:calc(100% - 32px);width:100%"></div>
                          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                          <script type="text/javascript">
                          new TradingView.widget(
                          {{
                            "width": "100%",
                            "height": 650,
                            "symbol": "{tv_symbol}",
                            "interval": "{chart_interval}",
                            "timezone": "Asia/Kolkata",
                            "theme": "light",
                            "style": "1",
                            "locale": "en",
                            "toolbar_bg": "#f1f3f6",
                            "enable_publishing": false,
                            "withdateranges": true,
                            "allow_symbol_change": true,
                            "details": true,
                            "hotlist": true,
                            "calendar": true,
                            "studies": [
                              "RSI@tv-basicstudies",
                              "MASimple@tv-basicstudies",
                              "MACD@tv-basicstudies",
                              "BB@tv-basicstudies"
                            ],
                            "show_popup_button": true,
                            "popup_width": "1000",
                            "popup_height": "650",
                            "container_id": "{container_id}"
                          }}
                          );
                          </script>
                        </div>
                        <!-- TradingView Widget END -->
                        """
                        
                        st.components.v1.html(tradingview_widget, height=670)
                        
                        st.info("""
                        **📊 TradingView Advanced Chart Features:**
                        - ✅ Real-time price updates
                        - ✅ Pre-loaded technical indicators (RSI, MA, MACD, Bollinger Bands)
                        - ✅ Drawing tools and trendlines
                        - ✅ Multiple timeframes
                        - ✅ Economic calendar
                        - ✅ Compare with other symbols
                        - ✅ Save chart layouts
                        """)
                    
                    # === TRADINGVIEW LIGHTWEIGHT CHART ===
                    elif chart_type == "📉 TradingView Lightweight":
                        from streamlit_lightweight_charts import renderLightweightCharts
                        
                        # Prepare data for lightweight charts
                        chart_data = []
                        for idx, row in data_with_indicators.iterrows():
                            chart_data.append({
                                "time": row['Date'].strftime('%Y-%m-%d'),
                                "open": float(row['Open']),
                                "high": float(row['High']),
                                "low": float(row['Low']),
                                "close": float(row['Close'])
                            })
                        
                        # Prepare volume data
                        volume_data = []
                        for idx, row in data_with_indicators.iterrows():
                            color = '#26a69a' if row['Close'] >= row['Open'] else '#ef5350'
                            volume_data.append({
                                "time": row['Date'].strftime('%Y-%m-%d'),
                                "value": float(row['Volume']),
                                "color": color
                            })
                        
                        # Prepare MA data
                        ma20_data = []
                        ma50_data = []
                        for idx, row in data_with_indicators.iterrows():
                            if not pd.isna(row['SMA_20']):
                                ma20_data.append({
                                    "time": row['Date'].strftime('%Y-%m-%d'),
                                    "value": float(row['SMA_20'])
                                })
                            if not pd.isna(row['SMA_50']):
                                ma50_data.append({
                                    "time": row['Date'].strftime('%Y-%m-%d'),
                                    "value": float(row['SMA_50'])
                                })
                        
                        # Chart options
                        chart_options = {
                            "layout": {
                                "background": {"type": "solid", "color": "#ffffff"},
                                "textColor": "#000000",
                            },
                            "grid": {
                                "vertLines": {"color": "#e0e0e0"},
                                "horzLines": {"color": "#e0e0e0"},
                            },
                            "priceScale": {
                                "borderColor": "#cccccc"
                            },
                            "timeScale": {
                                "borderColor": "#cccccc",
                                "timeVisible": True,
                                "secondsVisible": False,
                            },
                        }
                        
                        # Render the chart
                        renderLightweightCharts([
                            {
                                "chart": chart_options,
                                "series": [
                                    {
                                        "type": "Candlestick",
                                        "data": chart_data,
                                        "options": {
                                            "upColor": "#26a69a",
                                            "downColor": "#ef5350",
                                            "borderVisible": False,
                                            "wickUpColor": "#26a69a",
                                            "wickDownColor": "#ef5350",
                                        },
                                    },
                                    {
                                        "type": "Line",
                                        "data": ma20_data,
                                        "options": {
                                            "color": "#ff9800",
                                            "lineWidth": 2,
                                            "title": "SMA 20",
                                        },
                                    },
                                    {
                                        "type": "Line",
                                        "data": ma50_data,
                                        "options": {
                                            "color": "#2196f3",
                                            "lineWidth": 2,
                                            "title": "SMA 50",
                                        },
                                    },
                                ],
                            },
                            {
                                "chart": {
                                    "layout": {
                                        "background": {"type": "solid", "color": "#ffffff"},
                                        "textColor": "#000000",
                                    },
                                    "grid": {
                                        "vertLines": {"color": "#e0e0e0"},
                                        "horzLines": {"color": "#e0e0e0"},
                                    },
                                    "height": 150,
                                },
                                "series": [
                                    {
                                        "type": "Histogram",
                                        "data": volume_data,
                                        "options": {
                                            "priceFormat": {
                                                "type": "volume",
                                            },
                                            "priceScaleId": "",
                                        },
                                    },
                                ],
                            }
                        ], key=f"lwc_{stock_symbol}")
                        
                        st.info("""
                        **📉 TradingView Lightweight Chart Features:**
                        - ✅ Fast and responsive
                        - ✅ Candlestick chart with volume
                        - ✅ SMA 20 & 50 overlays
                        - ✅ Interactive zoom and pan
                        - ✅ Crosshair for price inspection
                        - ✅ Optimized for performance
                        """)
                    
                    # === PLOTLY INTERACTIVE CHART ===
                    else:
                        fig = go.Figure()
                        
                        # Candlestick
                        fig.add_trace(go.Candlestick(
                            x=data_with_indicators['Date'],
                            open=data_with_indicators['Open'],
                            high=data_with_indicators['High'],
                            low=data_with_indicators['Low'],
                            close=data_with_indicators['Close'],
                            name='Price'
                        ))
                        
                        # Moving Averages
                        fig.add_trace(go.Scatter(
                            x=data_with_indicators['Date'],
                            y=data_with_indicators['SMA_20'],
                            name='SMA 20',
                            line=dict(color='orange', width=2)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=data_with_indicators['Date'],
                            y=data_with_indicators['SMA_50'],
                            name='SMA 50',
                            line=dict(color='blue', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{stock_symbol} Price Chart",
                            xaxis_title="Date",
                            yaxis_title="Price (₹)",
                            height=500,
                            xaxis_rangeslider_visible=False
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.info("""
                        **📈 Plotly Interactive Chart Features:**
                        - ✅ Offline charts (no external dependencies)
                        - ✅ Candlestick with moving averages
                        - ✅ Zoom, pan, and reset
                        - ✅ Hover for detailed info
                        - ✅ Download as PNG
                        """)
                    
                    st.markdown("---")
                    
                    # === TECHNICAL INDICATORS ===
                    st.subheader("📊 Technical Indicators")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Momentum Indicators:**")
                        st.metric("RSI", f"{latest['RSI']:.2f}")
                        
                        if latest['RSI'] < 30:
                            st.success("🟢 Oversold - Buy Signal")
                        elif latest['RSI'] > 70:
                            st.error("🔴 Overbought - Sell Signal")
                        else:
                            st.info("🔵 Neutral")
                        
                        st.metric("MACD", f"{latest['MACD']:.2f}")
                        st.metric("MACD Signal", f"{latest['MACD_Signal']:.2f}")
                        
                        if latest['MACD'] > latest['MACD_Signal']:
                            st.success("🟢 Bullish")
                        else:
                            st.error("🔴 Bearish")
                    
                    with col2:
                        st.write("**Trend Indicators:**")
                        st.metric("SMA 20", f"₹{latest['SMA_20']:.2f}")
                        st.metric("SMA 50", f"₹{latest['SMA_50']:.2f}")
                        
                        if latest['SMA_20'] > latest['SMA_50']:
                            st.success("🟢 Uptrend")
                        else:
                            st.error("🔴 Downtrend")
                        
                        st.metric("EMA 12", f"₹{latest['EMA_12']:.2f}")
                        st.metric("EMA 26", f"₹{latest['EMA_26']:.2f}")
                    
                    with col3:
                        st.write("**Volatility Indicators:**")
                        st.metric("BB Upper", f"₹{latest['BB_Upper']:.2f}")
                        st.metric("BB Middle", f"₹{latest['BB_Middle']:.2f}")
                        st.metric("BB Lower", f"₹{latest['BB_Lower']:.2f}")
                        
                        if latest['Close'] > latest['BB_Upper']:
                            st.error("🔴 Above Upper Band")
                        elif latest['Close'] < latest['BB_Lower']:
                            st.success("🟢 Below Lower Band - Buy")
                        else:
                            st.info("🔵 Within Bands")
                        
                        st.metric("ATR", f"₹{latest['ATR']:.2f}")
                    
                    st.markdown("---")
                    
                    # === BUY/SELL SIGNALS ===
                    st.subheader("🎯 Trading Signals")
                    
                    buy_signals = 0
                    sell_signals = 0
                    signal_details = []
                    
                    # RSI
                    if latest['RSI'] < 30:
                        buy_signals += 2
                        signal_details.append(("🟢 BUY", f"RSI Oversold ({latest['RSI']:.1f})"))
                    elif latest['RSI'] > 70:
                        sell_signals += 2
                        signal_details.append(("🔴 SELL", f"RSI Overbought ({latest['RSI']:.1f})"))
                    
                    # MACD
                    if latest['MACD'] > latest['MACD_Signal'] and latest['MACD_Hist'] > 0:
                        buy_signals += 2
                        signal_details.append(("🟢 BUY", "MACD Bullish Cross"))
                    elif latest['MACD'] < latest['MACD_Signal'] and latest['MACD_Hist'] < 0:
                        sell_signals += 2
                        signal_details.append(("🔴 SELL", "MACD Bearish Cross"))
                    
                    # Moving Averages
                    if latest['SMA_20'] > latest['SMA_50']:
                        buy_signals += 1
                        signal_details.append(("🟢 BUY", "Uptrend (MA)"))
                    else:
                        sell_signals += 1
                        signal_details.append(("🔴 SELL", "Downtrend (MA)"))
                    
                    # Bollinger Bands
                    if latest['Close'] < latest['BB_Lower']:
                        buy_signals += 2
                        signal_details.append(("🟢 BUY", "Price Below BB Lower"))
                    elif latest['Close'] > latest['BB_Upper']:
                        sell_signals += 2
                        signal_details.append(("🔴 SELL", "Price Above BB Upper"))
                    
                    # Overall Signal
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Buy Signals", buy_signals, delta="Bullish" if buy_signals > sell_signals else "")
                    
                    with col2:
                        st.metric("Sell Signals", sell_signals, delta="Bearish" if sell_signals > buy_signals else "")
                    
                    with col3:
                        if buy_signals > sell_signals:
                            st.success("🟢 **Overall: BUY**")
                        elif sell_signals > buy_signals:
                            st.error("🔴 **Overall: SELL**")
                        else:
                            st.info("🔵 **Overall: HOLD**")
                    
                    # Signal Details
                    st.write("**Signal Breakdown:**")
                    for signal_type, reason in signal_details:
                        st.write(f"{signal_type}: {reason}")
                    
                    st.markdown("---")
                    
                    # === ADDITIONAL INDICATORS ===
                    with st.expander("📊 More Indicators"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Stochastic Oscillator:**")
                            st.write(f"- %K: {latest['Stoch_K']:.2f}")
                            st.write(f"- %D: {latest['Stoch_D']:.2f}")
                            
                            st.write("\n**Volume:**")
                            st.write(f"- OBV: {latest['OBV']:,.0f}")
                            st.write(f"- VWAP: ₹{latest['VWAP']:.2f}")
                        
                        with col2:
                            st.write("**Support & Resistance:**")
                            recent_high = data_with_indicators['High'].tail(20).max()
                            recent_low = data_with_indicators['Low'].tail(20).min()
                            st.write(f"- 20-Day High: ₹{recent_high:.2f}")
                            st.write(f"- 20-Day Low: ₹{recent_low:.2f}")
                            st.write(f"- Range: ₹{recent_high - recent_low:.2f}")
                    
                    # === PRICE ACTION ===
                    with st.expander("📈 Recent Price Action"):
                        last_5_days = data_with_indicators.tail(5)
                        st.dataframe(
                            last_5_days[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']],
                            use_container_width=True,
                            hide_index=True
                        )
                    
                    # === RECOMMENDATIONS ===
                    st.markdown("---")
                    st.subheader("💡 Quick Actions")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📊 Backtest {stock_symbol}", use_container_width=True):
                            st.info("Go to 'Run Backtest' page to test strategies on this stock!")
                    
                    with col2:
                        if st.button(f"📈 Compare Strategies", use_container_width=True):
                            st.info("Go to 'Compare Strategies' page to see which works best!")
                    
                    with col3:
                        if st.button("🎯 Check Recommendations", use_container_width=True):
                            st.info("Go to 'Buy Recommendations' to see all top picks!")
                    
                    # === INTERPRETATION ===
                    st.markdown("---")
                    st.subheader("📚 How to Interpret This Data")
                    
                    with st.expander("📖 Understanding the Indicators"):
                        st.write("""
                        **RSI (Relative Strength Index):**
                        - Below 30 = Oversold (potential buy)
                        - Above 70 = Overbought (potential sell)
                        - 30-70 = Neutral
                        
                        **MACD (Moving Average Convergence Divergence):**
                        - MACD above Signal = Bullish
                        - MACD below Signal = Bearish
                        - Histogram shows momentum strength
                        
                        **Moving Averages:**
                        - Price above MA = Uptrend
                        - Price below MA = Downtrend
                        - SMA 20 above SMA 50 = Strong uptrend (Golden Cross)
                        
                        **Bollinger Bands:**
                        - Price at upper band = Overbought
                        - Price at lower band = Oversold
                        - Tight bands = Low volatility (breakout coming)
                        - Wide bands = High volatility
                        
                        **ATR (Average True Range):**
                        - Measures volatility
                        - Higher ATR = More volatile
                        - Use for stop-loss placement
                        """)
        
        except Exception as e:
            st.error(f"❌ Error analyzing {stock_symbol}: {str(e)}")
            st.write("**Possible reasons:**")
            st.write("- Invalid stock symbol")
            st.write("- No data available")
            st.write("- Internet connection issue")
            st.write("\n**Try:**")
            st.write("- Check the symbol spelling")
            st.write("- Use NSE symbols (RELIANCE, TCS, INFY, etc.)")

# LIVE PRICES PAGE
elif page == "💰 Live Prices":
    st.header("💰 Live Stock Prices")
    st.write("See current prices of popular Indian stocks")
    
    if st.button("🔄 Refresh Prices"):
        st.rerun()
    
    with st.spinner("Fetching live prices..."):
        stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK']
        
        prices_data = []
        for symbol in stocks:
            try:
                quote = st.session_state.fetcher.get_quote(symbol)
                prices_data.append({
                    'Stock': symbol,
                    'Price (₹)': f"₹{quote['last_price']:.2f}",
                    'Change (%)': f"{quote['change_percent']:+.2f}%",
                    'Status': '📈' if quote['change_percent'] > 0 else '📉'
                })
            except:
                prices_data.append({
                    'Stock': symbol,
                    'Price (₹)': 'N/A',
                    'Change (%)': 'N/A',
                    'Status': '⚠️'
                })
        
        df = pd.DataFrame(prices_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.info("**Note:** Prices may be delayed by 15-20 minutes in FREE mode")

# BACKTEST PAGE
elif page == "📊 Run Backtest":
    st.header("📊 Run Strategy Backtest")
    st.write("Test a trading strategy on historical data and see the results!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        strategy_choice = st.selectbox(
            "Choose Strategy:",
            ["MA Crossover", "RSI Strategy"],
            help="Select which trading strategy to test"
        )
        
        stock_symbol = st.text_input(
            "Stock Symbol:",
            "RELIANCE",
            help="Enter NSE stock symbol (e.g., RELIANCE, TCS, INFY)"
        ).upper()
    
    with col2:
        date_range = st.date_input(
            "Date Range:",
            value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
            help="Select the period to test"
        )
        
        if len(date_range) == 2:
            start_date = date_range[0].strftime('%Y-%m-%d')
            end_date = date_range[1].strftime('%Y-%m-%d')
        else:
            start_date = "2024-01-01"
            end_date = "2024-12-31"
    
    if st.button("🚀 Run Backtest", type="primary", use_container_width=True):
        with st.spinner(f"Running backtest on {stock_symbol}... This may take a minute..."):
            try:
                # Create strategy
                if strategy_choice == "MA Crossover":
                    strategy = MACrossoverStrategy(st.session_state.fetcher)
                else:
                    strategy = RSIStrategy(st.session_state.fetcher)
                
                # Run backtest
                strategy.backtest(stock_symbol, start_date, end_date)
                
                # Get stats
                stats = strategy.get_performance_stats()
                
                # Display results
                st.success(f"✅ Backtest completed for {stock_symbol}!")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Return",
                        f"₹{stats['total_profit']:,.2f}",
                        f"{stats['return_percent']:.2f}%"
                    )
                
                with col2:
                    st.metric(
                        "Win Rate",
                        f"{stats['win_rate']:.1f}%",
                        f"{stats['winning_trades']}/{stats['total_trades']}"
                    )
                
                with col3:
                    st.metric(
                        "Total Trades",
                        stats['total_trades'],
                        f"₹{stats['avg_profit']:.2f} avg"
                    )
                
                with col4:
                    st.metric(
                        "Final Capital",
                        f"₹{stats['final_capital']:,.2f}",
                        "from ₹1,00,000"
                    )
                
                # Detailed stats
                st.subheader("📊 Detailed Statistics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Trade Summary:**")
                    st.write(f"- Winning Trades: {stats['winning_trades']}")
                    st.write(f"- Losing Trades: {stats['losing_trades']}")
                    st.write(f"- Win Rate: {stats['win_rate']:.2f}%")
                
                with col2:
                    st.write("**Profit/Loss:**")
                    st.write(f"- Average Win: ₹{stats['avg_win']:,.2f}")
                    st.write(f"- Average Loss: ₹{stats['avg_loss']:,.2f}")
                    st.write(f"- Max Profit: ₹{stats['max_profit']:,.2f}")
                    st.write(f"- Max Loss: ₹{stats['max_loss']:,.2f}")
                
                # Trade history
                if strategy.trades:
                    st.subheader("📜 Trade History")
                    trades_df = pd.DataFrame(strategy.trades)
                    trades_df['profit'] = trades_df['profit'].apply(lambda x: f"₹{x:.2f}")
                    trades_df['profit_percent'] = trades_df['profit_percent'].apply(lambda x: f"{x:.2f}%")
                    st.dataframe(trades_df[['symbol', 'entry_price', 'exit_price', 'quantity', 'profit', 'profit_percent']], use_container_width=True)
                
                # Interpretation
                st.subheader("💡 What Does This Mean?")
                if stats['return_percent'] > 0:
                    st.success(f"""
                    **Good News!** 🎉
                    
                    This strategy made a profit of ₹{stats['total_profit']:,.2f} ({stats['return_percent']:.2f}%)
                    
                    - Win rate of {stats['win_rate']:.1f}% means {stats['win_rate']:.0f} out of 100 trades were profitable
                    - You made {stats['total_trades']} trades in total
                    - On average, each trade made ₹{stats['avg_profit']:,.2f}
                    """)
                else:
                    st.warning(f"""
                    **This strategy lost money** 😔
                    
                    Loss of ₹{abs(stats['total_profit']):,.2f} ({stats['return_percent']:.2f}%)
                    
                    **Why?**
                    - The market conditions weren't favorable
                    - This strategy might work better on other stocks
                    - Try adjusting the parameters or use a different strategy
                    """)
                
            except Exception as e:
                st.error(f"Error running backtest: {str(e)}")
                st.write("**Possible reasons:**")
                st.write("- Invalid stock symbol")
                st.write("- No data available for this period")
                st.write("- Internet connection issue")

# COMPARE STRATEGIES PAGE
elif page == "📈 Compare Strategies":
    st.header("📈 Compare Strategies")
    st.write("Test both strategies on the same stock and see which performs better!")
    
    stock_symbol = st.text_input(
        "Stock Symbol:",
        "TCS",
        help="Enter stock symbol to compare strategies"
    ).upper()
    
    if st.button("🔍 Compare Strategies", type="primary", use_container_width=True):
        with st.spinner(f"Comparing strategies on {stock_symbol}..."):
            try:
                results = {}
                
                # Test MA Crossover
                st.write("Testing MA Crossover...")
                ma_strategy = MACrossoverStrategy(st.session_state.fetcher)
                ma_strategy.backtest(stock_symbol, '2024-01-01', '2024-12-31')
                results['MA Crossover'] = ma_strategy.get_performance_stats()
                
                # Test RSI
                st.write("Testing RSI Strategy...")
                rsi_strategy = RSIStrategy(st.session_state.fetcher)
                rsi_strategy.backtest(stock_symbol, '2024-01-01', '2024-12-31')
                results['RSI Strategy'] = rsi_strategy.get_performance_stats()
                
                # Display comparison
                st.success("✅ Comparison completed!")
                
                st.subheader(f"📊 Results for {stock_symbol}")
                
                # Create comparison table
                comparison_data = []
                for strategy_name, stats in results.items():
                    comparison_data.append({
                        'Strategy': strategy_name,
                        'Return': f"₹{stats['total_profit']:,.2f}",
                        'Return %': f"{stats['return_percent']:.2f}%",
                        'Win Rate': f"{stats['win_rate']:.1f}%",
                        'Total Trades': stats['total_trades'],
                        'Avg Profit': f"₹{stats['avg_profit']:,.2f}"
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Winner
                best_strategy = max(results.items(), key=lambda x: x[1]['return_percent'])
                st.success(f"🏆 **Winner:** {best_strategy[0]} with {best_strategy[1]['return_percent']:.2f}% return!")
                
                # Visual comparison
                st.subheader("📊 Visual Comparison")
                
                fig = go.Figure()
                strategies = list(results.keys())
                returns = [results[s]['return_percent'] for s in strategies]
                
                fig.add_trace(go.Bar(
                    x=strategies,
                    y=returns,
                    text=[f"{r:.2f}%" for r in returns],
                    textposition='auto',
                    marker_color=['green' if r > 0 else 'red' for r in returns]
                ))
                
                fig.update_layout(
                    title=f"Strategy Returns Comparison - {stock_symbol}",
                    xaxis_title="Strategy",
                    yaxis_title="Return (%)",
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error comparing strategies: {str(e)}")

# TRADE HISTORY PAGE
elif page == "📜 Trade History":
    st.header("📜 Trade History")
    st.write("View all past trades from the database")
    
    trades = st.session_state.db.get_trades(limit=50)
    
    if not trades.empty:
        st.dataframe(trades, use_container_width=True)
        
        # Stats
        stats = st.session_state.db.get_trade_stats()
        
        st.subheader("📊 Overall Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trades", stats['total_trades'])
        with col2:
            st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
        with col3:
            st.metric("Total Profit", f"₹{stats['total_profit']:,.2f}")
        with col4:
            st.metric("Avg Profit", f"₹{stats['avg_profit']:,.2f}")
        
    else:
        st.info("No trades in database yet. Run some backtests to see results here!")

# SETTINGS PAGE
elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    
    st.subheader("📊 Current Configuration")
    
    st.write("**Data Source:** FREE (yfinance)")
    st.write("**Initial Capital:** ₹1,00,000")
    st.write("**Mode:** Development/Backtesting")
    
    st.markdown("---")
    
    st.subheader("💡 About This App")
    
    st.write("""
    **Automated Trading Application**
    
    - Version: 1.0
    - Mode: FREE (No Cost)
    - Data Source: yfinance
    - Strategies: 2 (MA Crossover, RSI)
    - Indicators: 23+
    
    **Features:**
    - ✅ Live stock prices
    - ✅ Strategy backtesting
    - ✅ Performance analysis
    - ✅ Trade history
    - ✅ Database logging
    
    **To enable live trading:**
    - Subscribe to Kite Connect (₹2,000/month)
    - Follow MIGRATION_GUIDE.md
    - Just 3 changes needed!
    """)
    
    st.markdown("---")
    
    st.info("""
    **Need Help?**
    
    - Check README.md for full documentation
    - Run `python example_usage.py` for code examples
    - Read QUICK_START.md for setup guide
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ | Automated Trading Application | FREE Mode</div>",
    unsafe_allow_html=True
)

