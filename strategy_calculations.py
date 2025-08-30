"""
Strategy Calculations
Contains the calculation logic for different trading strategy indicators and signals.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from .signal_generators import SignalGenerators
from .risk_manager import RiskManager


class StrategyCalculations(LoggerMixin):
    """
    Calculation class for different trading strategy components.
    
    This class contains all the calculation logic that was moved
    from the StrategyImplementations to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the strategy calculations."""
        super().__init__()
        self.signal_generators = SignalGenerators()
        self.risk_manager = RiskManager()
        self.log_info("Strategy Calculations initialized")
    
    def calculate_trend_indicators(self, market_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate trend following indicators."""
        try:
            # Simple moving averages
            sma_20 = market_data['close'].rolling(window=20).mean()
            sma_50 = market_data['close'].rolling(window=50).mean()
            
            # Trend strength
            trend_strength = (sma_20 - sma_50) / sma_50
            
            # Price momentum
            momentum = market_data['close'].pct_change(periods=10)
            
            # Volatility
            volatility = market_data['close'].rolling(window=20).std()
            
            return {
                'sma_20': sma_20,
                'sma_50': sma_50,
                'trend_strength': trend_strength,
                'momentum': momentum,
                'volatility': volatility
            }
            
        except Exception as e:
            self.log_error(f"Error calculating trend indicators: {e}")
            return {}
    
    def calculate_reversion_indicators(self, market_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate mean reversion indicators."""
        try:
            # Bollinger Bands
            sma_20 = market_data['close'].rolling(window=20).mean()
            std_20 = market_data['close'].rolling(window=20).std()
            
            upper_band = sma_20 + (2 * std_20)
            lower_band = sma_20 - (2 * std_20)
            
            # RSI
            delta = market_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Mean reversion signal
            reversion_signal = (market_data['close'] - sma_20) / std_20
            
            return {
                'upper_band': upper_band,
                'lower_band': lower_band,
                'rsi': rsi,
                'reversion_signal': reversion_signal,
                'sma_20': sma_20
            }
            
        except Exception as e:
            self.log_error(f"Error calculating reversion indicators: {e}")
            return {}
    
    def calculate_momentum_indicators(self, market_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate momentum indicators."""
        try:
            # Price momentum
            momentum_5 = market_data['close'].pct_change(periods=5)
            momentum_10 = market_data['close'].pct_change(periods=10)
            momentum_20 = market_data['close'].pct_change(periods=20)
            
            # Volume momentum
            volume_momentum = market_data['volume'].pct_change(periods=5)
            
            # MACD
            ema_12 = market_data['close'].ewm(span=12).mean()
            ema_26 = market_data['close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            
            return {
                'momentum_5': momentum_5,
                'momentum_10': momentum_10,
                'momentum_20': momentum_20,
                'volume_momentum': volume_momentum,
                'macd': macd,
                'macd_signal': signal
            }
            
        except Exception as e:
            self.log_error(f"Error calculating momentum indicators: {e}")
            return {}
    
    def calculate_risk_metrics(self, market_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate risk metrics for risk parity."""
        try:
            # Returns
            returns = market_data['close'].pct_change()
            
            # Volatility
            volatility = returns.rolling(window=20).std()
            
            # VaR (Value at Risk)
            var_95 = returns.rolling(window=20).quantile(0.05)
            
            # Expected shortfall
            es_95 = returns.rolling(window=20).apply(
                lambda x: x[x <= x.quantile(0.05)].mean()
            )
            
            return {
                'returns': returns,
                'volatility': volatility,
                'var_95': var_95,
                'es_95': es_95
            }
            
        except Exception as e:
            self.log_error(f"Error calculating risk metrics: {e}")
            return {}
    
    def generate_entry_signals(self, indicators: Dict[str, np.ndarray], strategy_type: str) -> np.ndarray:
        """Generate entry signals based on indicators and strategy type."""
        return self.signal_generators.generate_entry_signals(indicators, strategy_type)
    
    def generate_exit_signals(self, indicators: Dict[str, np.ndarray], strategy_type: str) -> np.ndarray:
        """Generate exit signals based on indicators and strategy type."""
        return self.signal_generators.generate_exit_signals(indicators, strategy_type)
    
    def calculate_position_sizing(self, risk_tolerance: str, indicators: Dict[str, np.ndarray]) -> np.ndarray:
        """Calculate position sizing based on risk tolerance and indicators."""
        return self.risk_manager.calculate_position_sizing(risk_tolerance, indicators)
    
    def calculate_risk_parity_weights(self, risk_metrics: Dict[str, np.ndarray]) -> np.ndarray:
        """Calculate risk parity weights."""
        return self.risk_manager.calculate_risk_parity_weights(risk_metrics)
    
    def generate_rebalancing_signals(self, risk_metrics: Dict[str, np.ndarray], optimal_weights: np.ndarray) -> np.ndarray:
        """Generate rebalancing signals for risk parity strategy."""
        return self.risk_manager.generate_rebalancing_signals(risk_metrics, optimal_weights)
    
    def get_risk_parameters(self, risk_tolerance: str) -> Dict[str, float]:
        """Get risk parameters based on risk tolerance."""
        return self.risk_manager.get_risk_parameters(risk_tolerance)
