#!/usr/bin/env python3
"""
TradePulse Portfolio - Optimization History
Handles optimization history tracking and statistics
"""

import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class OptimizationHistory:
    """Handles optimization history tracking and statistics"""
    
    def __init__(self):
        self.optimization_history = []
    
    def record_optimization(self, strategy: str, portfolio_data: Dict, 
                           result: Dict, risk_tolerance: float):
        """Record optimization operation"""
        try:
            optimization_record = {
                'timestamp': pd.Timestamp.now(),
                'strategy': strategy,
                'risk_tolerance': risk_tolerance,
                'positions_count': len(portfolio_data.get('positions', {})),
                'result': result
            }
            
            self.optimization_history.append(optimization_record)
            
        except Exception as e:
            logger.error(f"Failed to record optimization: {e}")
    
    def get_optimization_history(self) -> List[Dict]:
        """Get optimization history"""
        return self.optimization_history.copy()
    
    def get_optimization_statistics(self) -> Dict:
        """Get optimization statistics"""
        try:
            total_optimizations = len(self.optimization_history)
            
            if total_optimizations == 0:
                return {'total_optimizations': 0}
            
            # Count by strategy
            strategy_counts = {}
            for opt in self.optimization_history:
                strategy = opt['strategy']
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            
            return {
                'total_optimizations': total_optimizations,
                'strategy_distribution': strategy_counts,
                'last_optimization': self.optimization_history[-1]['timestamp'] if self.optimization_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get optimization statistics: {e}")
            return {}
