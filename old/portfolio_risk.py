#!/usr/bin/env python3
"""
TradePulse Portfolio - Portfolio Risk Manager
Handles portfolio risk calculations and management
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PortfolioRiskManager:
    """Handles portfolio risk calculations and management"""
    
    def __init__(self):
        self.risk_metrics = {}
        self.risk_history = []
    
    def calculate_portfolio_risk(self, positions: Dict, price_data: Optional[Dict] = None) -> Dict:
        """
        Calculate comprehensive portfolio risk metrics
        
        Args:
            positions: Portfolio positions
            price_data: Historical price data for risk calculations
            
        Returns:
            Dict: Risk metrics
        """
        try:
            if not positions:
                return self._create_empty_risk_metrics()
            
            logger.info(f"📊 Calculating risk metrics for {len(positions)} positions")
            
            # Calculate basic risk metrics
            risk_metrics = self._calculate_basic_risk_metrics(positions)
            
            # Calculate advanced risk metrics if price data available
            if price_data:
                risk_metrics.update(self._calculate_advanced_risk_metrics(positions, price_data))
            
            # Store risk metrics
            self.risk_metrics = risk_metrics
            
            # Record risk calculation
            self._record_risk_calculation(positions, risk_metrics)
            
            logger.info("✅ Portfolio risk metrics calculated successfully")
            return risk_metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate portfolio risk: {e}")
            return self._create_empty_risk_metrics()
    
    def _calculate_basic_risk_metrics(self, positions: Dict) -> Dict:
        """Calculate basic risk metrics"""
        try:
            total_value = sum(pos['current_value'] for pos in positions.values())
            total_cost = sum(pos['shares'] * pos['avg_price'] for pos in positions.values())
            
            # Position concentration metrics
            position_weights = {}
            for symbol, pos in positions.items():
                position_weights[symbol] = pos['current_value'] / total_value if total_value > 0 else 0
            
            # Calculate concentration risk (Herfindahl index)
            concentration_index = sum(weight ** 2 for weight in position_weights.values())
            
            # Calculate sector risk (simplified)
            sector_exposure = self._calculate_sector_exposure(positions)
            
            return {
                'total_value': total_value,
                'total_cost': total_cost,
                'unrealized_pnl': total_value - total_cost,
                'unrealized_pnl_pct': ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0,
                'position_count': len(positions),
                'concentration_index': concentration_index,
                'position_weights': position_weights,
                'sector_exposure': sector_exposure,
                'largest_position': max(position_weights.values()) if position_weights else 0,
                'smallest_position': min(position_weights.values()) if position_weights else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate basic risk metrics: {e}")
            return {}
    
    def _calculate_advanced_risk_metrics(self, positions: Dict, price_data: Dict) -> Dict:
        """Calculate advanced risk metrics using price data"""
        try:
            # Calculate volatility for each position
            position_volatilities = {}
            for symbol, pos in positions.items():
                if symbol in price_data:
                    # Calculate daily returns and volatility
                    returns = self._calculate_returns(price_data[symbol])
                    volatility = np.std(returns) * np.sqrt(252)  # Annualized
                    position_volatilities[symbol] = volatility
            
            # Portfolio volatility (simplified)
            if position_volatilities:
                avg_volatility = np.mean(list(position_volatilities.values()))
                portfolio_volatility = avg_volatility * 0.8  # Simplified correlation assumption
            else:
                portfolio_volatility = 0.0
            
            # Value at Risk (VaR) calculation
            var_95 = self._calculate_var(positions, price_data, confidence=0.95)
            var_99 = self._calculate_var(positions, price_data, confidence=0.99)
            
            # Maximum drawdown
            max_drawdown = self._calculate_max_drawdown(positions, price_data)
            
            return {
                'portfolio_volatility': portfolio_volatility,
                'position_volatilities': position_volatilities,
                'var_95': var_95,
                'var_99': var_99,
                'max_drawdown': max_drawdown,
                'risk_adjusted_return': self._calculate_risk_adjusted_return(positions, portfolio_volatility)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate advanced risk metrics: {e}")
            return {}
    
    def _calculate_returns(self, price_data: pd.DataFrame) -> np.ndarray:
        """Calculate daily returns from price data"""
        try:
            if 'Close' in price_data.columns:
                close_prices = price_data['Close']
                returns = close_prices.pct_change().dropna()
                return returns.values
            else:
                # Generate sample returns if no price data
                return np.random.normal(0, 0.02, 100)
        except Exception as e:
            logger.error(f"Failed to calculate returns: {e}")
            return np.array([])
    
    def _calculate_var(self, positions: Dict, price_data: Dict, confidence: float = 0.95) -> float:
        """Calculate Value at Risk"""
        try:
            total_value = sum(pos['current_value'] for pos in positions.values())
            
            # Simplified VaR calculation
            # In practice, this would use historical simulation or Monte Carlo
            if confidence == 0.95:
                var_multiplier = 1.645
            elif confidence == 0.99:
                var_multiplier = 2.326
            else:
                var_multiplier = 1.96
            
            # Assume 20% annual volatility for portfolio
            daily_volatility = 0.20 / np.sqrt(252)
            var = total_value * var_multiplier * daily_volatility
            
            return var
            
        except Exception as e:
            logger.error(f"Failed to calculate VaR: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, positions: Dict, price_data: Dict) -> float:
        """Calculate maximum drawdown"""
        try:
            # Simplified max drawdown calculation
            # In practice, this would use actual price data
            total_value = sum(pos['current_value'] for pos in positions.values())
            
            # Assume 15% maximum drawdown for demonstration
            max_drawdown = total_value * 0.15
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Failed to calculate max drawdown: {e}")
            return 0.0
    
    def _calculate_risk_adjusted_return(self, positions: Dict, volatility: float) -> float:
        """Calculate risk-adjusted return (Sharpe ratio)"""
        try:
            total_value = sum(pos['current_value'] for pos in positions.values())
            total_cost = sum(pos['shares'] * pos['avg_price'] for pos in positions.values())
            
            if total_cost > 0 and volatility > 0:
                return_pct = (total_value - total_cost) / total_cost
                risk_adjusted_return = return_pct / volatility
                return risk_adjusted_return
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Failed to calculate risk-adjusted return: {e}")
            return 0.0
    
    def _calculate_sector_exposure(self, positions: Dict) -> Dict:
        """Calculate sector exposure (simplified)"""
        try:
            # Simplified sector mapping
            sector_mapping = {
                'AAPL': 'Technology',
                'GOOGL': 'Technology',
                'MSFT': 'Technology',
                'TSLA': 'Automotive',
                'AMZN': 'Consumer',
                'NVDA': 'Technology',
                'META': 'Technology',
                'NFLX': 'Media'
            }
            
            sector_exposure = {}
            total_value = sum(pos['current_value'] for pos in positions.values())
            
            for symbol, pos in positions.items():
                sector = sector_mapping.get(symbol, 'Other')
                sector_value = sector_exposure.get(sector, 0)
                sector_exposure[sector] = sector_value + pos['current_value']
            
            # Convert to percentages
            if total_value > 0:
                sector_exposure = {sector: (value / total_value) * 100 
                                 for sector, value in sector_exposure.items()}
            
            return sector_exposure
            
        except Exception as e:
            logger.error(f"Failed to calculate sector exposure: {e}")
            return {}
    
    def _create_empty_risk_metrics(self) -> Dict:
        """Create empty risk metrics"""
        return {
            'total_value': 0.0,
            'total_cost': 0.0,
            'unrealized_pnl': 0.0,
            'unrealized_pnl_pct': 0.0,
            'position_count': 0,
            'concentration_index': 0.0,
            'portfolio_volatility': 0.0,
            'var_95': 0.0,
            'var_99': 0.0,
            'max_drawdown': 0.0,
            'risk_adjusted_return': 0.0
        }
    
    def _record_risk_calculation(self, positions: Dict, risk_metrics: Dict):
        """Record risk calculation in history"""
        try:
            risk_record = {
                'timestamp': pd.Timestamp.now(),
                'positions_count': len(positions),
                'total_value': risk_metrics.get('total_value', 0),
                'portfolio_volatility': risk_metrics.get('portfolio_volatility', 0),
                'var_95': risk_metrics.get('var_95', 0),
                'concentration_index': risk_metrics.get('concentration_index', 0)
            }
            
            self.risk_history.append(risk_record)
            
        except Exception as e:
            logger.error(f"Failed to record risk calculation: {e}")
    
    def get_risk_history(self) -> List[Dict]:
        """Get risk calculation history"""
        return self.risk_history.copy()
    
    def get_risk_statistics(self) -> Dict:
        """Get risk statistics"""
        try:
            if not self.risk_history:
                return {'total_calculations': 0}
            
            total_calculations = len(self.risk_history)
            avg_volatility = np.mean([r['portfolio_volatility'] for r in self.risk_history])
            avg_var = np.mean([r['var_95'] for r in self.risk_history])
            
            return {
                'total_calculations': total_calculations,
                'average_volatility': avg_volatility,
                'average_var_95': avg_var,
                'last_calculation': self.risk_history[-1]['timestamp'] if self.risk_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get risk statistics: {e}")
            return {}
    
    def clear_risk_history(self) -> int:
        """Clear risk history and return count"""
        try:
            count = len(self.risk_history)
            self.risk_history.clear()
            logger.info(f"🗑️ Cleared {count} risk calculations from history")
            return count
        except Exception as e:
            logger.error(f"Failed to clear risk history: {e}")
            return 0
