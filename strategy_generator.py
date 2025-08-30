"""
AI Strategy Generator
Generates AI-driven trading strategies to maximize profits and minimize losses.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from .strategy_implementations import StrategyImplementations
from .strategy_analyzer import StrategyAnalyzer


class AIStrategyGenerator(LoggerMixin):
    """
    AI-driven trading strategy generator.
    
    Generates strategies including:
    - Trend following
    - Mean reversion
    - Momentum
    - Risk parity
    - Multi-factor strategies
    """
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """
        Initialize the AI strategy generator.
        
        Args:
            config: Configuration loader instance
            message_bus: Message Bus client for communication
        """
        super().__init__()
        self.config = config
        self.message_bus = message_bus
        
        # Strategy configuration
        self.enabled_strategies = config.get('ai_module.strategies', [
            'trend_following', 'mean_reversion', 'momentum', 'risk_parity'
        ])
        
        # Risk management settings
        self.risk_config = config.get('ai_module.risk_management', {})
        self.max_correlation = self.risk_config.get('max_correlation', 0.7)
        self.volatility_target = self.risk_config.get('volatility_target', 0.15)
        
        # Strategy cache
        self.strategy_cache: Dict[str, Dict[str, Any]] = {}
        
        # Strategy implementations and analyzer
        self.strategy_impl = StrategyImplementations()
        self.strategy_analyzer = StrategyAnalyzer()
        
        self.log_info("AI Strategy Generator initialized")
    
    def generate_strategy(
        self, 
        market_data: pd.DataFrame,
        ml_predictions: Optional[Dict[str, np.ndarray]] = None,
        strategy_type: Optional[str] = None,
        risk_tolerance: str = 'moderate'
    ) -> Dict[str, Any]:
        """
        Generate a trading strategy based on market data and ML predictions.
        
        Args:
            market_data: Market data DataFrame
            ml_predictions: ML model predictions (optional)
            strategy_type: Specific strategy type to generate
            risk_tolerance: Risk tolerance level ('low', 'moderate', 'high')
        
        Returns:
            Dictionary containing strategy details
        """
        try:
            if strategy_type is None:
                # Auto-select best strategy
                strategy_type = self.strategy_analyzer.select_optimal_strategy(
                    market_data, ml_predictions, self.enabled_strategies
                )
            
            if strategy_type not in self.enabled_strategies:
                raise ValueError(f"Strategy type '{strategy_type}' not enabled")
            
            # Generate the selected strategy using implementations
            strategy = self.strategy_impl.generate_strategy(
                strategy_type, market_data, ml_predictions, risk_tolerance
            )
            
            # Add strategy metadata
            strategy['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'strategy_type': strategy_type,
                'risk_tolerance': risk_tolerance,
                'market_conditions': self.strategy_analyzer.assess_market_conditions(market_data),
                'confidence_score': self.strategy_analyzer.calculate_confidence_score(strategy, market_data, ml_predictions)
            }
            
            # Cache the strategy
            cache_key = f"{strategy_type}_{risk_tolerance}_{datetime.now().strftime('%Y%m%d')}"
            self.strategy_cache[cache_key] = strategy
            
            # Publish strategy generated message
            self.message_bus.publish("strategy_generated", {
                'strategy_type': strategy_type,
                'risk_tolerance': risk_tolerance,
                'confidence_score': strategy['metadata']['confidence_score'],
                'timestamp': datetime.now().isoformat()
            })
            
            self.log_info(f"Generated {strategy_type} strategy with confidence {strategy['metadata']['confidence_score']:.3f}")
            return strategy
            
        except Exception as e:
            self.log_error(f"Error generating strategy: {e}")
            raise
    
    def get_strategy_summary(self, strategy: Dict[str, Any]) -> str:
        """Get a human-readable summary of the generated strategy."""
        try:
            metadata = strategy.get('metadata', {})
            
            summary = f"""
AI-Generated Trading Strategy Summary
====================================

Strategy Type: {metadata.get('strategy_type', 'Unknown')}
Risk Tolerance: {metadata.get('risk_tolerance', 'Unknown')}
Confidence Score: {metadata.get('confidence_score', 0):.3f}
Generated At: {metadata.get('generated_at', 'Unknown')}

Market Conditions:
- Regime: {metadata.get('market_conditions', {}).get('regime', 'Unknown')}
- Volatility: {metadata.get('market_conditions', {}).get('volatility', 0):.3f}
- Trend: {metadata.get('market_conditions', {}).get('trend', 0):.3f}

Strategy Components:
- Entry Signals: {len(strategy.get('entry_signals', [])) if 'entry_signals' in strategy else 'N/A'}
- Exit Signals: {len(strategy.get('exit_signals', [])) if 'exit_signals' in strategy else 'N/A'}
- Position Sizing: {len(strategy.get('position_sizing', [])) if 'position_sizing' in strategy else 'N/A'}

Risk Parameters:
"""
            
            risk_params = strategy.get('risk_parameters', {})
            for param, value in risk_params.items():
                summary += f"- {param.replace('_', ' ').title()}: {value:.3f}\n"
            
            return summary
            
        except Exception as e:
            self.log_error(f"Error generating strategy summary: {e}")
            return "Error generating strategy summary"
    
    def clear_cache(self) -> None:
        """Clear the strategy cache."""
        self.strategy_cache.clear()
        self.log_info("Strategy cache cleared")
