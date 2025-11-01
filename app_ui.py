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
        ["🏠 Home", "🤖 Auto-Trader", "🎯 Buy Recommendations", "📊 Stock Details", "💰 Live Prices", "📊 Run Backtest", "📈 Compare Strategies", "📜 Trade History", "⚙️ Settings"]
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
                    
                    # === PRICE CHART ===
                    st.subheader("📈 Price Chart with Moving Averages")
                    
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

