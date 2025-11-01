"""
Database module for storing trades, positions, and logs
Uses SQLite - no external database needed
"""
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class TradingDatabase:
    """
    SQLite database for trading application
    Stores trades, positions, signals, and logs
    """
    
    def __init__(self, db_path: str = "data/trading.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.create_tables()
        
        print(f"✅ Database initialized: {db_path}")
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        
        # Trades table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy TEXT NOT NULL,
                entry_date TEXT NOT NULL,
                exit_date TEXT,
                entry_price REAL NOT NULL,
                exit_price REAL,
                quantity INTEGER NOT NULL,
                profit REAL,
                profit_percent REAL,
                status TEXT DEFAULT 'OPEN',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Signals table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                price REAL NOT NULL,
                indicators TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Positions table (current open positions)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                strategy TEXT NOT NULL,
                entry_price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                current_price REAL,
                unrealized_pnl REAL,
                entry_date TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Strategy performance table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy TEXT NOT NULL,
                date TEXT NOT NULL,
                total_trades INTEGER DEFAULT 0,
                winning_trades INTEGER DEFAULT 0,
                total_profit REAL DEFAULT 0,
                win_rate REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Logs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                module TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    # ========================================
    # TRADES
    # ========================================
    
    def insert_trade(self, trade: Dict) -> int:
        """
        Insert a new trade
        
        Args:
            trade: Trade dictionary
        
        Returns:
            Trade ID
        """
        self.cursor.execute("""
            INSERT INTO trades (
                symbol, strategy, entry_date, exit_date, 
                entry_price, exit_price, quantity, profit, profit_percent, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade.get('symbol'),
            trade.get('strategy', 'Unknown'),
            trade.get('entry_date'),
            trade.get('exit_date'),
            trade.get('entry_price'),
            trade.get('exit_price'),
            trade.get('quantity'),
            trade.get('profit'),
            trade.get('profit_percent'),
            trade.get('status', 'CLOSED')
        ))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_trades(self, symbol: str = None, strategy: str = None, 
                   limit: int = 100) -> pd.DataFrame:
        """
        Get trades from database
        
        Args:
            symbol: Filter by symbol
            strategy: Filter by strategy
            limit: Max number of trades
        
        Returns:
            DataFrame with trades
        """
        query = "SELECT * FROM trades WHERE 1=1"
        params = []
        
        if symbol:
            query += " AND symbol = ?"
            params.append(symbol)
        
        if strategy:
            query += " AND strategy = ?"
            params.append(strategy)
        
        query += f" ORDER BY id DESC LIMIT {limit}"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    def get_trade_stats(self, strategy: str = None) -> Dict:
        """
        Get trade statistics
        
        Args:
            strategy: Filter by strategy
        
        Returns:
            Dictionary with stats
        """
        query = """
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) as winning_trades,
                SUM(profit) as total_profit,
                AVG(profit) as avg_profit,
                MAX(profit) as max_profit,
                MIN(profit) as min_loss
            FROM trades 
            WHERE status = 'CLOSED'
        """
        
        if strategy:
            query += " AND strategy = ?"
            self.cursor.execute(query, (strategy,))
        else:
            self.cursor.execute(query)
        
        result = self.cursor.fetchone()
        
        return {
            'total_trades': result[0] or 0,
            'winning_trades': result[1] or 0,
            'total_profit': result[2] or 0,
            'avg_profit': result[3] or 0,
            'max_profit': result[4] or 0,
            'min_loss': result[5] or 0,
            'win_rate': (result[1] / result[0] * 100) if result[0] else 0
        }
    
    # ========================================
    # SIGNALS
    # ========================================
    
    def insert_signal(self, signal: Dict) -> int:
        """
        Insert a trading signal
        
        Args:
            signal: Signal dictionary
        
        Returns:
            Signal ID
        """
        self.cursor.execute("""
            INSERT INTO signals (symbol, strategy, signal_type, price, indicators)
            VALUES (?, ?, ?, ?, ?)
        """, (
            signal.get('symbol'),
            signal.get('strategy'),
            signal.get('signal_type'),
            signal.get('price'),
            signal.get('indicators', '')
        ))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_signals(self, symbol: str = None, limit: int = 100) -> pd.DataFrame:
        """Get recent signals"""
        query = "SELECT * FROM signals WHERE 1=1"
        params = []
        
        if symbol:
            query += " AND symbol = ?"
            params.append(symbol)
        
        query += f" ORDER BY id DESC LIMIT {limit}"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ========================================
    # POSITIONS
    # ========================================
    
    def insert_position(self, position: Dict) -> int:
        """Insert a new position"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO positions (
                symbol, strategy, entry_price, quantity, 
                current_price, unrealized_pnl, entry_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            position.get('symbol'),
            position.get('strategy'),
            position.get('entry_price'),
            position.get('quantity'),
            position.get('current_price'),
            position.get('unrealized_pnl'),
            position.get('entry_date')
        ))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_position(self, symbol: str, current_price: float, unrealized_pnl: float):
        """Update position with current price and P&L"""
        self.cursor.execute("""
            UPDATE positions 
            SET current_price = ?, unrealized_pnl = ?, updated_at = CURRENT_TIMESTAMP
            WHERE symbol = ?
        """, (current_price, unrealized_pnl, symbol))
        
        self.conn.commit()
    
    def delete_position(self, symbol: str):
        """Delete a position (when closed)"""
        self.cursor.execute("DELETE FROM positions WHERE symbol = ?", (symbol,))
        self.conn.commit()
    
    def get_positions(self) -> pd.DataFrame:
        """Get all open positions"""
        return pd.read_sql_query("SELECT * FROM positions", self.conn)
    
    # ========================================
    # LOGS
    # ========================================
    
    def log(self, level: str, message: str, module: str = None):
        """
        Add a log entry
        
        Args:
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            message: Log message
            module: Module name
        """
        self.cursor.execute("""
            INSERT INTO logs (level, message, module)
            VALUES (?, ?, ?)
        """, (level, message, module))
        
        self.conn.commit()
    
    def get_logs(self, level: str = None, limit: int = 100) -> pd.DataFrame:
        """Get recent logs"""
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        if level:
            query += " AND level = ?"
            params.append(level)
        
        query += f" ORDER BY id DESC LIMIT {limit}"
        
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ========================================
    # UTILITY
    # ========================================
    
    def clear_table(self, table_name: str):
        """Clear all data from a table"""
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()
        print(f"✅ Cleared table: {table_name}")
    
    def get_table_count(self, table_name: str) -> int:
        """Get row count of a table"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("✅ Database connection closed")
    
    def __del__(self):
        """Destructor - close connection"""
        try:
            self.conn.close()
        except:
            pass


# Test the database
if __name__ == "__main__":
    print("🧪 Testing Trading Database...\n")
    
    # Initialize
    db = TradingDatabase("data/test_trading.db")
    
    # Test 1: Insert trade
    print("📝 Test 1: Inserting trade...")
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
    print(f"✅ Trade inserted with ID: {trade_id}")
    
    # Test 2: Get trades
    print("\n📊 Test 2: Fetching trades...")
    trades = db.get_trades()
    print(trades)
    
    # Test 3: Insert signal
    print("\n📡 Test 3: Inserting signal...")
    signal = {
        'symbol': 'TCS',
        'strategy': 'RSI Strategy',
        'signal_type': 'BUY',
        'price': 3500
    }
    signal_id = db.insert_signal(signal)
    print(f"✅ Signal inserted with ID: {signal_id}")
    
    # Test 4: Get stats
    print("\n📈 Test 4: Trade statistics...")
    stats = db.get_trade_stats()
    print(stats)
    
    # Test 5: Logging
    print("\n📝 Test 5: Logging...")
    db.log('INFO', 'Database test successful', 'database.py')
    logs = db.get_logs()
    print(logs)
    
    print("\n✅ All database tests passed!")
    
    # Cleanup
    db.close()

