"""
Signal Generators
Contains methods for generating trading signals based on indicators.
"""

import numpy as np
from typing import Dict
from utils.logger import LoggerMixin


class SignalGenerators(LoggerMixin):
    """
    Class for generating trading signals based on indicators.
    
    This class contains the signal generation methods that were extracted
    from StrategyCalculations to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the signal generators."""
        super().__init__()
        self.log_info("Signal Generators initialized")
    
    def generate_entry_signals(self, indicators: Dict[str, np.ndarray], strategy_type: str) -> np.ndarray:
        """Generate entry signals based on indicators and strategy type."""
        try:
            if strategy_type == 'trend_following':
                # Buy when trend is strong and positive
                trend_strength = indicators.get('trend_strength', np.zeros(100))
                momentum = indicators.get('momentum', np.zeros(100))
                
                entry_signals = np.where(
                    (trend_strength > 0.02) & (momentum > 0),
                    1,  # Buy signal
                    0   # No signal
                )
                
            elif strategy_type == 'mean_reversion':
                # Buy when price is below lower band and RSI is oversold
                reversion_signal = indicators.get('reversion_signal', np.zeros(100))
                rsi = indicators.get('rsi', np.zeros(100))
                
                entry_signals = np.where(
                    (reversion_signal < -1.5) & (rsi < 30),
                    1,  # Buy signal
                    0   # No signal
                )
                
            elif strategy_type == 'momentum':
                # Buy when momentum is strong and increasing
                momentum_5 = indicators.get('momentum_5', np.zeros(100))
                momentum_10 = indicators.get('momentum_10', np.zeros(100))
                
                entry_signals = np.where(
                    (momentum_5 > 0.01) & (momentum_5 > momentum_10),
                    1,  # Buy signal
                    0   # No signal
                )
                
            else:
                entry_signals = np.zeros(100)
            
            return entry_signals
            
        except Exception as e:
            self.log_error(f"Error generating entry signals: {e}")
            return np.zeros(100)
    
    def generate_exit_signals(self, indicators: Dict[str, np.ndarray], strategy_type: str) -> np.ndarray:
        """Generate exit signals based on indicators and strategy type."""
        try:
            if strategy_type == 'trend_following':
                # Sell when trend weakens or reverses
                trend_strength = indicators.get('trend_strength', np.zeros(100))
                momentum = indicators.get('momentum', np.zeros(100))
                
                exit_signals = np.where(
                    (trend_strength < -0.01) | (momentum < -0.01),
                    1,  # Sell signal
                    0   # No signal
                )
                
            elif strategy_type == 'mean_reversion':
                # Sell when price is above upper band and RSI is overbought
                reversion_signal = indicators.get('reversion_signal', np.zeros(100))
                rsi = indicators.get('rsi', np.zeros(100))
                
                exit_signals = np.where(
                    (reversion_signal > 1.5) & (rsi > 70),
                    1,  # Sell signal
                    0   # No signal
                )
                
            elif strategy_type == 'momentum':
                # Sell when momentum weakens
                momentum_5 = indicators.get('momentum_5', np.zeros(100))
                momentum_10 = indicators.get('momentum_10', np.zeros(100))
                
                exit_signals = np.where(
                    (momentum_5 < -0.01) | (momentum_5 < momentum_10),
                    1,  # Sell signal
                    0   # No signal
                )
                
            else:
                exit_signals = np.zeros(100)
            
            return exit_signals
            
        except Exception as e:
            self.log_error(f"Error generating exit signals: {e}")
            return np.zeros(100)
