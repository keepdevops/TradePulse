#!/usr/bin/env python3
"""
TradePulse Portfolio - Portfolio Optimizer
Handles portfolio optimization strategies and calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .optimization_strategies import OptimizationStrategies
from .optimization_history import OptimizationHistory

logger = logging.getLogger(__name__)

class PortfolioOptimizer:
    """Handles portfolio optimization strategies and calculations"""
    
    def __init__(self):
        self.supported_strategies = [
            'Markowitz', 'Risk Parity', 'Maximum Sharpe', 'Black-Litterman', 'HRP'
        ]
        
        # Initialize components
        self.strategies = OptimizationStrategies()
        self.history = OptimizationHistory()
    
    def optimize_portfolio(self, strategy: str, portfolio_data: Dict, 
                         risk_tolerance: float = 1.0) -> Dict:
        """
        Optimize portfolio using the specified strategy
        
        Args:
            strategy: Optimization strategy to use
            portfolio_data: Current portfolio data
            risk_tolerance: Risk tolerance parameter (0.1 to 2.0)
            
        Returns:
            Dict: Optimization results
        """
        try:
            if strategy not in self.supported_strategies:
                raise ValueError(f"Unsupported optimization strategy: {strategy}")
            
            logger.info(f"🚀 Optimizing portfolio using {strategy} strategy")
            
            # Get current positions for optimization
            positions = portfolio_data.get('positions', {})
            
            if not positions:
                logger.warning("No positions to optimize")
                return self.strategies.create_empty_optimization_result(strategy)
            
            # Run optimization based on strategy
            result = self.strategies.run_optimization(strategy, positions, risk_tolerance)
            
            # Record optimization
            self.history.record_optimization(strategy, portfolio_data, result, risk_tolerance)
            
            logger.info(f"✅ Portfolio optimization completed using {strategy}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
            raise
    
    def get_optimization_history(self) -> List[Dict]:
        """Get optimization history"""
        return self.history.get_optimization_history()
    
    def get_optimization_statistics(self) -> Dict:
        """Get optimization statistics"""
        return self.history.get_optimization_statistics()
