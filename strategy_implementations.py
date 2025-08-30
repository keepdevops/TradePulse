"""
Strategy Implementations
Contains the implementation logic for different trading strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from .strategy_calculations import StrategyCalculations


class StrategyImplementations(LoggerMixin):
    """
    Implementation class for different trading strategies.
    
    This class contains all the strategy-specific logic that was moved
    from the main AIStrategyGenerator to keep files under 400 lines.
    """
    
    def __init__(self):
        """Initialize the strategy implementations."""
        super().__init__()
        self.calculations = StrategyCalculations()
        self.log_info("Strategy Implementations initialized")
    
    def generate_strategy(
        self,
        strategy_type: str,
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]],
        risk_tolerance: str
    ) -> Dict[str, Any]:
        """
        Generate a trading strategy based on type.
        
        Args:
            strategy_type: Type of strategy to generate
            market_data: Market data DataFrame
            ml_predictions: ML model predictions (optional)
            risk_tolerance: Risk tolerance level
        
        Returns:
            Strategy dictionary
        """
        if strategy_type == 'trend_following':
            return self._generate_trend_following_strategy(market_data, ml_predictions, risk_tolerance)
        elif strategy_type == 'mean_reversion':
            return self._generate_mean_reversion_strategy(market_data, ml_predictions, risk_tolerance)
        elif strategy_type == 'momentum':
            return self._generate_momentum_strategy(market_data, ml_predictions, risk_tolerance)
        elif strategy_type == 'risk_parity':
            return self._generate_risk_parity_strategy(market_data, ml_predictions, risk_tolerance)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
    
    def _generate_trend_following_strategy(
        self, 
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]],
        risk_tolerance: str
    ) -> Dict[str, Any]:
        """Generate trend following strategy."""
        try:
            # Calculate trend indicators
            trend_indicators = self.calculations.calculate_trend_indicators(market_data)
            
            # Generate entry/exit signals
            entry_signals = self.calculations.generate_entry_signals(trend_indicators, 'trend_following')
            exit_signals = self.calculations.generate_exit_signals(trend_indicators, 'trend_following')
            
            # Calculate position sizing
            position_sizing = self.calculations.calculate_position_sizing(risk_tolerance, trend_indicators)
            
            strategy = {
                'type': 'trend_following',
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'position_sizing': position_sizing,
                'indicators': trend_indicators,
                'risk_parameters': self.calculations.get_risk_parameters(risk_tolerance)
            }
            
            return strategy
            
        except Exception as e:
            self.log_error(f"Error generating trend following strategy: {e}")
            raise
    
    def _generate_mean_reversion_strategy(
        self, 
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]],
        risk_tolerance: str
    ) -> Dict[str, Any]:
        """Generate mean reversion strategy."""
        try:
            # Calculate mean reversion indicators
            reversion_indicators = self.calculations.calculate_reversion_indicators(market_data)
            
            # Generate entry/exit signals
            entry_signals = self.calculations.generate_entry_signals(reversion_indicators, 'mean_reversion')
            exit_signals = self.calculations.generate_exit_signals(reversion_indicators, 'mean_reversion')
            
            # Calculate position sizing
            position_sizing = self.calculations.calculate_position_sizing(risk_tolerance, reversion_indicators)
            
            strategy = {
                'type': 'mean_reversion',
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'position_sizing': position_sizing,
                'indicators': reversion_indicators,
                'risk_parameters': self.calculations.get_risk_parameters(risk_tolerance)
            }
            
            return strategy
            
        except Exception as e:
            self.log_error(f"Error generating mean reversion strategy: {e}")
            raise
    
    def _generate_momentum_strategy(
        self, 
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]],
        risk_tolerance: str
    ) -> Dict[str, Any]:
        """Generate momentum strategy."""
        try:
            # Calculate momentum indicators
            momentum_indicators = self.calculations.calculate_momentum_indicators(market_data)
            
            # Generate entry/exit signals
            entry_signals = self.calculations.generate_entry_signals(momentum_indicators, 'momentum')
            exit_signals = self.calculations.generate_exit_signals(momentum_indicators, 'momentum')
            
            # Calculate position sizing
            position_sizing = self.calculations.calculate_position_sizing(risk_tolerance, momentum_indicators)
            
            strategy = {
                'type': 'momentum',
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'position_sizing': position_sizing,
                'indicators': momentum_indicators,
                'risk_parameters': self.calculations.get_risk_parameters(risk_tolerance)
            }
            
            return strategy
            
        except Exception as e:
            self.log_error(f"Error generating momentum strategy: {e}")
            raise
    
    def _generate_risk_parity_strategy(
        self, 
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]],
        risk_tolerance: str
    ) -> Dict[str, Any]:
        """Generate risk parity strategy."""
        try:
            # Calculate risk metrics
            risk_metrics = self.calculations.calculate_risk_metrics(market_data)
            
            # Calculate optimal weights
            optimal_weights = self.calculations.calculate_risk_parity_weights(risk_metrics)
            
            # Generate rebalancing signals
            rebalancing_signals = self.calculations.generate_rebalancing_signals(risk_metrics, optimal_weights)
            
            strategy = {
                'type': 'risk_parity',
                'optimal_weights': optimal_weights,
                'rebalancing_signals': rebalancing_signals,
                'risk_metrics': risk_metrics,
                'risk_parameters': self.calculations.get_risk_parameters(risk_tolerance)
            }
            
            return strategy
            
        except Exception as e:
            self.log_error(f"Error generating risk parity strategy: {e}")
            raise
