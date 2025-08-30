"""
Strategy Analyzer
Contains methods for analyzing market conditions and calculating strategy scores.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from utils.logger import LoggerMixin


class StrategyAnalyzer(LoggerMixin):
    """
    Class for analyzing market conditions and calculating strategy scores.
    
    This class contains the analysis methods that were extracted
    from AIStrategyGenerator to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the strategy analyzer."""
        super().__init__()
        self.log_info("Strategy Analyzer initialized")
    
    def select_optimal_strategy(
        self, 
        market_data: pd.DataFrame, 
        ml_predictions: Optional[Dict[str, np.ndarray]],
        enabled_strategies: List[str]
    ) -> str:
        """Select the optimal strategy based on market conditions and ML predictions."""
        try:
            # Assess market conditions
            market_conditions = self.assess_market_conditions(market_data)
            
            # Calculate strategy scores
            strategy_scores = {}
            
            for strategy in enabled_strategies:
                score = self.calculate_strategy_score(strategy, market_conditions, ml_predictions)
                strategy_scores[strategy] = score
            
            # Select strategy with highest score
            best_strategy = max(strategy_scores.keys(), key=lambda x: strategy_scores[x])
            
            self.log_info(f"Selected optimal strategy: {best_strategy} (score: {strategy_scores[best_strategy]:.3f})")
            return best_strategy
            
        except Exception as e:
            self.log_error(f"Error selecting optimal strategy: {e}")
            # Fallback to trend following
            return 'trend_following'
    
    def assess_market_conditions(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess current market conditions."""
        try:
            # Calculate basic market metrics
            returns = market_data['close'].pct_change()
            volatility = returns.rolling(window=20).std().iloc[-1]
            trend = (market_data['close'].iloc[-1] / market_data['close'].iloc[-20] - 1)
            
            # Determine market regime
            if trend > 0.05 and volatility < 0.2:
                regime = 'bull_trending'
            elif trend < -0.05 and volatility < 0.2:
                regime = 'bear_trending'
            elif volatility > 0.3:
                regime = 'volatile'
            else:
                regime = 'sideways'
            
            return {
                'regime': regime,
                'volatility': volatility,
                'trend': trend,
                'current_price': market_data['close'].iloc[-1],
                'volume_trend': market_data['volume'].pct_change(periods=5).iloc[-1]
            }
            
        except Exception as e:
            self.log_error(f"Error assessing market conditions: {e}")
            return {'regime': 'unknown', 'volatility': 0.0, 'trend': 0.0}
    
    def calculate_confidence_score(
        self, 
        strategy: Dict[str, Any], 
        market_data: pd.DataFrame, 
        ml_predictions: Optional[Dict[str, np.ndarray]]
    ) -> float:
        """Calculate confidence score for the generated strategy."""
        try:
            confidence = 0.5  # Base confidence
            
            # Market condition confidence
            market_conditions = strategy['metadata']['market_conditions']
            if market_conditions['regime'] in ['bull_trending', 'bear_trending']:
                confidence += 0.2
            elif market_conditions['regime'] == 'volatile':
                confidence -= 0.1
            
            # ML prediction confidence (if available)
            if ml_predictions and 'confidence' in ml_predictions:
                ml_confidence = np.mean(ml_predictions['confidence'])
                confidence += 0.3 * ml_confidence
            
            # Strategy-specific confidence
            if strategy['type'] == 'trend_following' and market_conditions['trend'] > 0.02:
                confidence += 0.1
            elif strategy['type'] == 'mean_reversion' and abs(market_conditions['trend']) < 0.01:
                confidence += 0.1
            
            # Clamp confidence to [0, 1]
            confidence = np.clip(confidence, 0.0, 1.0)
            
            return confidence
            
        except Exception as e:
            self.log_error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def calculate_strategy_score(
        self, 
        strategy_type: str, 
        market_conditions: Dict[str, Any], 
        ml_predictions: Optional[Dict[str, np.ndarray]]
    ) -> float:
        """Calculate score for a specific strategy type."""
        try:
            score = 0.0
            
            # Market regime compatibility
            regime_scores = {
                'trend_following': {'bull_trending': 0.8, 'bear_trending': 0.8, 'volatile': 0.3, 'sideways': 0.4},
                'mean_reversion': {'bull_trending': 0.3, 'bear_trending': 0.3, 'volatile': 0.6, 'sideways': 0.8},
                'momentum': {'bull_trending': 0.9, 'bear_trending': 0.1, 'volatile': 0.5, 'sideways': 0.6},
                'risk_parity': {'bull_trending': 0.7, 'bear_trending': 0.7, 'volatile': 0.8, 'sideways': 0.7}
            }
            
            regime = market_conditions.get('regime', 'unknown')
            if regime in regime_scores.get(strategy_type, {}):
                score += regime_scores[strategy_type][regime]
            
            # ML prediction alignment
            if ml_predictions and 'predictions' in ml_predictions:
                predictions = ml_predictions['predictions']
                if len(predictions) > 0:
                    # Simple alignment score based on prediction direction
                    prediction_trend = np.mean(np.diff(predictions[-10:])) if len(predictions) >= 10 else 0
                    market_trend = market_conditions.get('trend', 0)
                    
                    if (prediction_trend > 0 and market_trend > 0) or (prediction_trend < 0 and market_trend < 0):
                        score += 0.2
            
            return score
            
        except Exception as e:
            self.log_error(f"Error calculating strategy score: {e}")
            return 0.0
    
    def get_risk_parameters(self, risk_tolerance: str) -> Dict[str, float]:
        """Get risk parameters based on risk tolerance."""
        risk_params = {
            'low': {
                'max_position_size': 0.02,
                'stop_loss': 0.01,
                'take_profit': 0.03,
                'max_drawdown': 0.05
            },
            'moderate': {
                'max_position_size': 0.05,
                'stop_loss': 0.02,
                'take_profit': 0.06,
                'max_drawdown': 0.10
            },
            'high': {
                'max_position_size': 0.10,
                'stop_loss': 0.03,
                'take_profit': 0.09,
                'max_drawdown': 0.15
            }
        }
        
        return risk_params.get(risk_tolerance, risk_params['moderate'])
