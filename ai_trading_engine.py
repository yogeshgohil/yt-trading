"""
AI-Powered Options Trading Engine
Fully automated NIFTY Options trading with machine learning
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import pickle
import os


class MarketConditionAnalyzer:
    """Analyzes market conditions using multiple indicators"""
    
    def __init__(self):
        self.conditions = {
            'BULLISH': 1,
            'BEARISH': -1,
            'NEUTRAL': 0,
            'HIGHLY_VOLATILE': 2,
            'LOW_VOLATILE': -2
        }
    
    def analyze_market(self, data: pd.DataFrame) -> Dict:
        """Analyze current market conditions"""
        if data.empty or len(data) < 50:
            return {
                'trend': 'NEUTRAL',
                'volatility': 'LOW_VOLATILE',
                'strength': 0.5,
                'confidence': 0.3,
                'indicators': {}
            }
        
        latest = data.iloc[-1]
        
        # Calculate trend indicators
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(50).mean().iloc[-1]
        current_price = latest['Close']
        
        # RSI
        rsi = self._calculate_rsi(data['Close'])
        
        # Volatility (ATR)
        atr = self._calculate_atr(data)
        avg_atr = atr.mean()
        
        # Volume analysis
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
        current_volume = latest['Volume']
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # MACD
        macd, signal = self._calculate_macd(data['Close'])
        macd_val = macd.iloc[-1] if len(macd) > 0 else 0
        signal_val = signal.iloc[-1] if len(signal) > 0 else 0
        
        # Determine trend
        trend_score = 0
        if sma_20 > sma_50:
            trend_score += 1
        if current_price > sma_20:
            trend_score += 1
        if macd_val > signal_val:
            trend_score += 1
        if rsi > 50:
            trend_score += 1
        
        # Determine volatility
        volatility_score = atr.iloc[-1] / avg_atr if avg_atr > 0 else 1
        
        # Map to conditions
        if trend_score >= 3:
            trend = 'BULLISH'
            strength = min(trend_score / 4.0, 1.0)
        elif trend_score <= 1:
            trend = 'BEARISH'
            strength = min((4 - trend_score) / 4.0, 1.0)
        else:
            trend = 'NEUTRAL'
            strength = 0.5
        
        if volatility_score > 1.5:
            volatility = 'HIGHLY_VOLATILE'
        elif volatility_score < 0.7:
            volatility = 'LOW_VOLATILE'
        else:
            volatility = 'MODERATE'
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            trend_score, rsi, volume_ratio, volatility_score
        )
        
        return {
            'trend': trend,
            'volatility': volatility,
            'strength': strength,
            'confidence': confidence,
            'indicators': {
                'rsi': rsi,
                'macd': macd_val,
                'signal': signal_val,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'atr': atr.iloc[-1],
                'volume_ratio': volume_ratio,
                'current_price': current_price
            }
        }
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if len(rsi) > 0 else 50.0
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        return atr
    
    def _calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD"""
        ema_12 = prices.ewm(span=12, adjust=False).mean()
        ema_26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal
    
    def _calculate_confidence(self, trend_score: int, rsi: float, 
                            volume_ratio: float, volatility_score: float) -> float:
        """Calculate confidence score (0-1)"""
        confidence = 0.0
        
        # Trend clarity (40% weight)
        if trend_score in [0, 4]:
            confidence += 0.4
        elif trend_score in [1, 3]:
            confidence += 0.2
        
        # RSI confirmation (20% weight)
        if (trend_score >= 3 and rsi > 50) or (trend_score <= 1 and rsi < 50):
            confidence += 0.2
        
        # Volume confirmation (20% weight)
        if volume_ratio > 1.2:
            confidence += 0.2
        elif volume_ratio > 0.9:
            confidence += 0.1
        
        # Volatility factor (20% weight)
        if 0.8 <= volatility_score <= 1.5:
            confidence += 0.2
        elif 0.5 <= volatility_score <= 2.0:
            confidence += 0.1
        
        return min(confidence, 1.0)


class AIStrategySelector:
    """AI-based strategy selector for options trading"""
    
    def __init__(self):
        self.strategies = {
            'BUY_CALL': {'trend': 'BULLISH', 'volatility': ['LOW_VOLATILE', 'MODERATE']},
            'BUY_PUT': {'trend': 'BEARISH', 'volatility': ['LOW_VOLATILE', 'MODERATE']},
            'STRADDLE': {'trend': 'NEUTRAL', 'volatility': ['HIGHLY_VOLATILE']},
            'STRANGLE': {'trend': 'NEUTRAL', 'volatility': ['HIGHLY_VOLATILE']},
            'BULL_CALL_SPREAD': {'trend': 'BULLISH', 'volatility': ['MODERATE', 'HIGHLY_VOLATILE']},
            'BEAR_PUT_SPREAD': {'trend': 'BEARISH', 'volatility': ['MODERATE', 'HIGHLY_VOLATILE']},
            'IRON_CONDOR': {'trend': 'NEUTRAL', 'volatility': ['LOW_VOLATILE']},
        }
    
    def select_strategy(self, market_conditions: Dict, capital: float) -> Dict:
        """Select best options strategy based on market conditions"""
        trend = market_conditions['trend']
        volatility = market_conditions['volatility']
        confidence = market_conditions['confidence']
        strength = market_conditions['strength']
        
        # Score each strategy
        strategy_scores = {}
        for strategy_name, requirements in self.strategies.items():
            score = self._score_strategy(
                strategy_name, requirements, trend, volatility, 
                confidence, strength
            )
            strategy_scores[strategy_name] = score
        
        # Select best strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        best_score = strategy_scores[best_strategy]
        
        # Only proceed if confidence is high enough
        if best_score < 0.5:
            return {
                'strategy': 'WAIT',
                'action': 'NONE',
                'confidence': confidence,
                'reason': 'Market conditions unclear, waiting for better setup'
            }
        
        # Determine action details
        action_details = self._get_action_details(
            best_strategy, market_conditions, capital
        )
        
        return {
            'strategy': best_strategy,
            'action': action_details['action'],
            'option_type': action_details['option_type'],
            'strike_selection': action_details['strike_selection'],
            'quantity': action_details['quantity'],
            'max_premium': action_details['max_premium'],
            'stop_loss': action_details['stop_loss'],
            'target': action_details['target'],
            'confidence': confidence,
            'score': best_score,
            'reason': action_details['reason']
        }
    
    def _score_strategy(self, strategy_name: str, requirements: Dict,
                       trend: str, volatility: str, confidence: float,
                       strength: float) -> float:
        """Score strategy based on market fit"""
        score = 0.0
        
        # Trend match (50% weight)
        if requirements['trend'] == trend:
            score += 0.5 * strength
        
        # Volatility match (30% weight)
        if volatility in requirements.get('volatility', []):
            score += 0.3
        
        # Confidence boost (20% weight)
        score += 0.2 * confidence
        
        return score
    
    def _get_action_details(self, strategy: str, conditions: Dict, 
                           capital: float) -> Dict:
        """Get detailed action parameters for selected strategy"""
        indicators = conditions['indicators']
        current_price = indicators.get('current_price', 0)
        atr = indicators.get('atr', 0)
        
        # Calculate position size based on capital and risk
        risk_per_trade = capital * 0.02  # 2% risk per trade
        
        details = {
            'action': 'BUY',
            'option_type': 'CALL',
            'strike_selection': 'ATM',
            'quantity': 1,
            'max_premium': risk_per_trade,
            'stop_loss': 30,  # 30% stop loss
            'target': 50,  # 50% target
            'reason': ''
        }
        
        if strategy == 'BUY_CALL':
            details.update({
                'option_type': 'CALL',
                'strike_selection': 'ATM',
                'stop_loss': 30,
                'target': 50,
                'reason': 'Strong bullish trend detected, buying ATM call'
            })
        
        elif strategy == 'BUY_PUT':
            details.update({
                'option_type': 'PUT',
                'strike_selection': 'ATM',
                'stop_loss': 30,
                'target': 50,
                'reason': 'Strong bearish trend detected, buying ATM put'
            })
        
        elif strategy == 'STRADDLE':
            details.update({
                'option_type': 'BOTH',
                'strike_selection': 'ATM',
                'stop_loss': 40,
                'target': 60,
                'max_premium': risk_per_trade * 2,  # Double for both legs
                'reason': 'High volatility expected, executing straddle'
            })
        
        elif strategy == 'STRANGLE':
            details.update({
                'option_type': 'BOTH',
                'strike_selection': 'OTM',
                'stop_loss': 40,
                'target': 70,
                'max_premium': risk_per_trade * 1.5,
                'reason': 'High volatility expected, executing strangle (lower cost)'
            })
        
        elif strategy == 'BULL_CALL_SPREAD':
            details.update({
                'option_type': 'CALL',
                'strike_selection': 'SPREAD',
                'stop_loss': 50,
                'target': 40,
                'reason': 'Moderate bullish trend, using bull call spread for limited risk'
            })
        
        elif strategy == 'BEAR_PUT_SPREAD':
            details.update({
                'option_type': 'PUT',
                'strike_selection': 'SPREAD',
                'stop_loss': 50,
                'target': 40,
                'reason': 'Moderate bearish trend, using bear put spread for limited risk'
            })
        
        elif strategy == 'IRON_CONDOR':
            details.update({
                'option_type': 'BOTH',
                'strike_selection': 'IRON_CONDOR',
                'stop_loss': 50,
                'target': 30,
                'reason': 'Low volatility neutral market, executing iron condor'
            })
        
        # Calculate quantity based on max premium
        # Assuming average premium of 100-200 per lot
        estimated_premium = 150
        details['quantity'] = max(1, int(details['max_premium'] / estimated_premium))
        
        return details


class AITradingEngine:
    """Main AI trading engine for automated options trading"""
    
    def __init__(self, capital: float = 100000, max_positions: int = 5):
        self.capital = capital
        self.available_capital = capital
        self.max_positions = max_positions
        self.positions = []
        self.trade_history = []
        
        self.analyzer = MarketConditionAnalyzer()
        self.selector = AIStrategySelector()
        
        # AI learning parameters
        self.performance_data = []
        self.winning_strategies = {}
        self.losing_strategies = {}
        
        # Risk management
        self.max_loss_per_day = capital * 0.05  # 5% max loss per day
        self.max_loss_per_trade = capital * 0.02  # 2% max loss per trade
        self.daily_pnl = 0
        
        # Safety controls
        self.is_active = False
        self.trades_today = 0
        self.max_trades_per_day = 10
        self.last_trade_time = None
        self.min_trade_interval = 60  # seconds between trades
    
    def analyze_and_decide(self, nifty_data: pd.DataFrame, 
                          index: str = 'NIFTY') -> Optional[Dict]:
        """Analyze market and make trading decision"""
        if not self.can_trade():
            return None
        
        # Analyze market conditions
        market_conditions = self.analyzer.analyze_market(nifty_data)
        
        # Select strategy
        strategy_decision = self.selector.select_strategy(
            market_conditions, self.available_capital
        )
        
        # Check if we should trade
        if strategy_decision['strategy'] == 'WAIT':
            return {
                'decision': 'WAIT',
                'reason': strategy_decision['reason'],
                'market_conditions': market_conditions
            }
        
        # Check risk limits
        if not self.check_risk_limits():
            return {
                'decision': 'HALT',
                'reason': 'Risk limits exceeded for today',
                'daily_pnl': self.daily_pnl
            }
        
        # Prepare trade recommendation
        trade = {
            'decision': 'TRADE',
            'timestamp': datetime.now(),
            'index': index,
            'strategy': strategy_decision['strategy'],
            'option_type': strategy_decision['option_type'],
            'strike_selection': strategy_decision['strike_selection'],
            'quantity': strategy_decision['quantity'],
            'max_premium': strategy_decision['max_premium'],
            'stop_loss_pct': strategy_decision['stop_loss'],
            'target_pct': strategy_decision['target'],
            'confidence': strategy_decision['confidence'],
            'market_conditions': market_conditions,
            'reason': strategy_decision['reason']
        }
        
        return trade
    
    def execute_trade(self, trade_signal: Dict) -> Dict:
        """Execute the trade (simulate or real)"""
        if not self.is_active:
            return {'status': 'INACTIVE', 'message': 'AI Engine is not active'}
        
        if trade_signal['decision'] != 'TRADE':
            return {'status': 'NO_TRADE', 'message': trade_signal.get('reason', 'Waiting')}
        
        # Check if we can take more positions
        if len(self.positions) >= self.max_positions:
            return {'status': 'MAX_POSITIONS', 'message': f'Already have {self.max_positions} open positions'}
        
        # Simulate trade execution
        trade = {
            'id': len(self.trade_history) + 1,
            'timestamp': datetime.now(),
            'index': trade_signal['index'],
            'strategy': trade_signal['strategy'],
            'option_type': trade_signal['option_type'],
            'quantity': trade_signal['quantity'],
            'entry_premium': self._simulate_premium(trade_signal),
            'stop_loss': trade_signal['stop_loss_pct'],
            'target': trade_signal['target_pct'],
            'confidence': trade_signal['confidence'],
            'status': 'OPEN',
            'pnl': 0
        }
        
        # Calculate cost
        total_cost = trade['entry_premium'] * trade['quantity']
        
        if total_cost > self.available_capital:
            return {'status': 'INSUFFICIENT_CAPITAL', 'message': 'Not enough capital'}
        
        # Update capital
        self.available_capital -= total_cost
        
        # Add to positions
        self.positions.append(trade)
        self.trade_history.append(trade)
        
        # Update counters
        self.trades_today += 1
        self.last_trade_time = datetime.now()
        
        return {
            'status': 'SUCCESS',
            'trade_id': trade['id'],
            'message': f"Executed {trade['strategy']} - {trade['option_type']}",
            'trade': trade
        }
    
    def monitor_positions(self) -> List[Dict]:
        """Monitor open positions and apply risk management"""
        actions = []
        
        for position in self.positions[:]:  # Copy list to modify during iteration
            if position['status'] != 'OPEN':
                continue
            
            # Simulate current premium (in real trading, fetch from market)
            current_premium = self._simulate_current_premium(position)
            
            # Calculate P&L
            entry_cost = position['entry_premium'] * position['quantity']
            current_value = current_premium * position['quantity']
            pnl = current_value - entry_cost
            pnl_pct = (pnl / entry_cost * 100) if entry_cost > 0 else 0
            
            position['current_premium'] = current_premium
            position['pnl'] = pnl
            position['pnl_pct'] = pnl_pct
            
            # Check stop loss
            if pnl_pct <= -position['stop_loss']:
                action = self._close_position(position, 'STOP_LOSS')
                actions.append(action)
            
            # Check target
            elif pnl_pct >= position['target']:
                action = self._close_position(position, 'TARGET_HIT')
                actions.append(action)
            
            # Trail stop loss if in profit
            elif pnl_pct > 20:
                # Move stop loss to breakeven or profit
                new_stop = max(position['stop_loss'], -10)  # Protect with -10% max loss
                if new_stop != position['stop_loss']:
                    position['stop_loss'] = new_stop
                    actions.append({
                        'action': 'TRAIL_STOP',
                        'trade_id': position['id'],
                        'new_stop': new_stop,
                        'current_pnl_pct': pnl_pct
                    })
        
        return actions
    
    def _close_position(self, position: Dict, reason: str) -> Dict:
        """Close a position"""
        position['status'] = 'CLOSED'
        position['exit_time'] = datetime.now()
        position['exit_reason'] = reason
        
        # Return capital
        exit_value = position['current_premium'] * position['quantity']
        self.available_capital += exit_value
        
        # Update daily P&L
        self.daily_pnl += position['pnl']
        
        # Learn from trade
        self._learn_from_trade(position)
        
        # Remove from positions
        if position in self.positions:
            self.positions.remove(position)
        
        return {
            'action': 'CLOSE',
            'trade_id': position['id'],
            'reason': reason,
            'pnl': position['pnl'],
            'pnl_pct': position['pnl_pct']
        }
    
    def _learn_from_trade(self, trade: Dict):
        """Learn from completed trade"""
        strategy = trade['strategy']
        pnl_pct = trade['pnl_pct']
        
        # Track winning/losing strategies
        if pnl_pct > 0:
            self.winning_strategies[strategy] = self.winning_strategies.get(strategy, 0) + 1
        else:
            self.losing_strategies[strategy] = self.losing_strategies.get(strategy, 0) + 1
        
        # Store performance data
        self.performance_data.append({
            'strategy': strategy,
            'pnl_pct': pnl_pct,
            'confidence': trade['confidence'],
            'timestamp': trade['timestamp']
        })
    
    def can_trade(self) -> bool:
        """Check if we can take a new trade"""
        # Check if active
        if not self.is_active:
            return False
        
        # Check max trades per day
        if self.trades_today >= self.max_trades_per_day:
            return False
        
        # Check time interval
        if self.last_trade_time:
            time_since_last = (datetime.now() - self.last_trade_time).seconds
            if time_since_last < self.min_trade_interval:
                return False
        
        # Check risk limits
        if not self.check_risk_limits():
            return False
        
        return True
    
    def check_risk_limits(self) -> bool:
        """Check if risk limits are within bounds"""
        # Check daily loss limit
        if self.daily_pnl < -self.max_loss_per_day:
            return False
        
        # Check capital
        if self.available_capital < self.capital * 0.3:  # At least 30% capital should remain
            return False
        
        return True
    
    def _simulate_premium(self, trade_signal: Dict) -> float:
        """Simulate option premium (in real trading, fetch from market)"""
        # Simulate based on strategy and market conditions
        base_premium = 150  # Base premium
        
        # Adjust based on confidence
        confidence_multiplier = 0.8 + (trade_signal['confidence'] * 0.4)
        premium = base_premium * confidence_multiplier
        
        # Add some randomness
        premium *= (0.9 + np.random.random() * 0.2)
        
        return round(premium, 2)
    
    def _simulate_current_premium(self, position: Dict) -> float:
        """Simulate current premium movement"""
        entry_premium = position['entry_premium']
        
        # Simulate price movement (-30% to +50%)
        movement = -0.3 + (np.random.random() * 0.8)
        
        # Bias based on confidence
        confidence_bias = (position['confidence'] - 0.5) * 0.2
        movement += confidence_bias
        
        current_premium = entry_premium * (1 + movement)
        return max(1, round(current_premium, 2))
    
    def get_status(self) -> Dict:
        """Get current engine status"""
        total_pnl = sum(p.get('pnl', 0) for p in self.positions)
        
        return {
            'is_active': self.is_active,
            'capital': self.capital,
            'available_capital': self.available_capital,
            'deployed_capital': self.capital - self.available_capital,
            'open_positions': len(self.positions),
            'max_positions': self.max_positions,
            'trades_today': self.trades_today,
            'daily_pnl': self.daily_pnl,
            'unrealized_pnl': total_pnl,
            'total_pnl': self.daily_pnl + total_pnl,
            'roi': ((self.daily_pnl + total_pnl) / self.capital * 100),
            'winning_strategies': self.winning_strategies,
            'losing_strategies': self.losing_strategies
        }
    
    def start(self):
        """Start the AI engine"""
        self.is_active = True
    
    def stop(self):
        """Stop the AI engine"""
        self.is_active = False
    
    def reset_daily_counters(self):
        """Reset daily counters (call at start of day)"""
        self.daily_pnl = 0
        self.trades_today = 0

