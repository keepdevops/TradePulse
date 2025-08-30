"""
Portfolio Optimizer
Handles portfolio optimization requests and implements various optimization strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from scipy.optimize import minimize
from scipy.stats import norm
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin


class PortfolioOptimizer(LoggerMixin):
    """
    Portfolio optimization engine that implements various optimization strategies.
    
    Supports:
    - Markowitz Mean-Variance Optimization
    - Risk Parity Optimization
    - Maximum Sharpe Ratio Optimization
    - Black-Litterman Optimization
    - Hierarchical Risk Parity (HRP)
    """
    
    def __init__(self):
        """Initialize the portfolio optimizer."""
        super().__init__()
        self.log_info("Portfolio Optimizer initialized")
    
    def optimize_portfolio(
        self,
        returns: pd.DataFrame,
        optimization_type: str = "markowitz",
        risk_tolerance: str = "moderate",
        constraints: Optional[Dict[str, Any]] = None,
        target_return: Optional[float] = None,
        target_volatility: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Optimize portfolio based on specified strategy.
        
        Args:
            returns: Asset returns DataFrame (assets as columns, dates as rows)
            optimization_type: Type of optimization ('markowitz', 'risk_parity', 'sharpe', 'black_litterman', 'hrp')
            risk_tolerance: Risk tolerance level ('low', 'moderate', 'high')
            constraints: Additional optimization constraints
            target_return: Target portfolio return (for constrained optimization)
            target_volatility: Target portfolio volatility (for constrained optimization)
        
        Returns:
            Dictionary containing optimization results
        """
        try:
            self.log_info(f"Starting {optimization_type} portfolio optimization")
            
            # Calculate basic statistics
            mean_returns = returns.mean()
            cov_matrix = returns.cov()
            
            # Get risk parameters based on risk tolerance
            risk_params = self._get_risk_parameters(risk_tolerance)
            
            # Apply optimization strategy
            if optimization_type == "markowitz":
                weights = self._markowitz_optimization(
                    mean_returns, cov_matrix, risk_params, constraints, target_return, target_volatility
                )
            elif optimization_type == "risk_parity":
                weights = self._risk_parity_optimization(cov_matrix, risk_params)
            elif optimization_type == "sharpe":
                weights = self._sharpe_optimization(mean_returns, cov_matrix, risk_params)
            elif optimization_type == "black_litterman":
                weights = self._black_litterman_optimization(mean_returns, cov_matrix, risk_params)
            elif optimization_type == "hrp":
                weights = self._hierarchical_risk_parity(cov_matrix, risk_params)
            else:
                raise ValueError(f"Unknown optimization type: {optimization_type}")
            
            # Calculate portfolio metrics
            portfolio_metrics = self._calculate_portfolio_metrics(weights, mean_returns, cov_matrix)
            
            # Prepare results
            results = {
                'optimization_type': optimization_type,
                'risk_tolerance': risk_tolerance,
                'optimal_weights': weights.to_dict(),
                'portfolio_metrics': portfolio_metrics,
                'constraints_applied': constraints or {},
                'optimization_timestamp': pd.Timestamp.now().isoformat()
            }
            
            self.log_info(f"Portfolio optimization completed successfully")
            return results
            
        except Exception as e:
            self.log_error(f"Error in portfolio optimization: {e}")
            raise
    
    def _markowitz_optimization(
        self,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        risk_params: Dict[str, float],
        constraints: Optional[Dict[str, Any]],
        target_return: Optional[float],
        target_volatility: Optional[float]
    ) -> pd.Series:
        """Markowitz mean-variance optimization."""
        n_assets = len(mean_returns)
        
        # Objective function: minimize portfolio variance
        def objective(weights):
            portfolio_var = np.dot(weights.T, np.dot(cov_matrix.values, weights))
            return portfolio_var
        
        # Constraints
        constraints_list = []
        
        # Weight sum constraint
        constraints_list.append({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Target return constraint (if specified)
        if target_return is not None:
            constraints_list.append({
                'type': 'eq', 
                'fun': lambda x: np.dot(x, mean_returns.values) - target_return
            })
        
        # Target volatility constraint (if specified)
        if target_volatility is not None:
            constraints_list.append({
                'type': 'ineq', 
                'fun': lambda x: target_volatility - np.sqrt(np.dot(x.T, np.dot(cov_matrix.values, x)))
            })
        
        # Add custom constraints
        if constraints:
            if 'min_weight' in constraints:
                min_weight = constraints['min_weight']
                constraints_list.append({'type': 'ineq', 'fun': lambda x: x - min_weight})
            
            if 'max_weight' in constraints:
                max_weight = constraints['max_weight']
                constraints_list.append({'type': 'ineq', 'fun': lambda x: max_weight - x})
        
        # Bounds: weights between 0 and 1 (long-only portfolio)
        bounds = [(0, 1) for _ in range(n_assets)]
        
        # Initial guess: equal weights
        initial_weights = np.full(n_assets, 1.0 / n_assets)
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_list,
            options={'maxiter': 1000}
        )
        
        if not result.success:
            self.log_warning(f"Markowitz optimization warning: {result.message}")
        
        return pd.Series(result.x, index=mean_returns.index)
    
    def _risk_parity_optimization(
        self,
        cov_matrix: pd.DataFrame,
        risk_params: Dict[str, float]
    ) -> pd.Series:
        """Risk parity optimization."""
        n_assets = len(cov_matrix)
        
        # Objective function: minimize the difference in risk contributions
        def objective(weights):
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights)))
            risk_contributions = weights * (np.dot(cov_matrix.values, weights)) / portfolio_risk
            
            # Calculate variance of risk contributions
            risk_contrib_var = np.var(risk_contributions)
            return risk_contrib_var
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weight sum constraint
        ]
        
        # Bounds
        bounds = [(0, 1) for _ in range(n_assets)]
        
        # Initial guess
        initial_weights = np.full(n_assets, 1.0 / n_assets)
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if not result.success:
            self.log_warning(f"Risk parity optimization warning: {result.message}")
        
        return pd.Series(result.x, index=cov_matrix.index)
    
    def _sharpe_optimization(
        self,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        risk_params: Dict[str, float]
    ) -> pd.Series:
        """Maximum Sharpe ratio optimization."""
        n_assets = len(mean_returns)
        
        # Risk-free rate (can be made configurable)
        risk_free_rate = 0.02  # 2% annual
        
        # Objective function: maximize Sharpe ratio (minimize negative Sharpe)
        def objective(weights):
            portfolio_return = np.dot(weights, mean_returns.values)
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights)))
            
            if portfolio_vol == 0:
                return 0
            
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_vol
            return -sharpe_ratio  # Minimize negative Sharpe
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weight sum constraint
        ]
        
        # Bounds
        bounds = [(0, 1) for _ in range(n_assets)]
        
        # Initial guess
        initial_weights = np.full(n_assets, 1.0 / n_assets)
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if not result.success:
            self.log_warning(f"Sharpe optimization warning: {result.message}")
        
        return pd.Series(result.x, index=mean_returns.index)
    
    def _black_litterman_optimization(
        self,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        risk_params: Dict[str, float]
    ) -> pd.Series:
        """Black-Litterman optimization (simplified version)."""
        # For now, return equal weights as placeholder
        # Full Black-Litterman implementation would require views and confidence levels
        n_assets = len(mean_returns)
        weights = np.full(n_assets, 1.0 / n_assets)
        
        self.log_info("Black-Litterman optimization: returning equal weights (full implementation pending)")
        return pd.Series(weights, index=mean_returns.index)
    
    def _hierarchical_risk_parity(
        self,
        cov_matrix: pd.DataFrame,
        risk_params: Dict[str, float]
    ) -> pd.Series:
        """Hierarchical Risk Parity optimization (simplified version)."""
        # For now, return equal weights as placeholder
        # Full HRP implementation would require hierarchical clustering
        n_assets = len(cov_matrix)
        weights = np.full(n_assets, 1.0 / n_assets)
        
        self.log_info("HRP optimization: returning equal weights (full implementation pending)")
        return pd.Series(weights, index=cov_matrix.index)
    
    def _calculate_portfolio_metrics(
        self,
        weights: pd.Series,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame
    ) -> Dict[str, float]:
        """Calculate portfolio performance metrics."""
        try:
            # Portfolio return
            portfolio_return = np.dot(weights, mean_returns.values)
            
            # Portfolio volatility
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights)))
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_vol if portfolio_vol > 0 else 0
            
            # Maximum drawdown approximation (simplified)
            # In practice, this would require historical simulation
            max_drawdown_approx = portfolio_vol * 2.0  # Rough approximation
            
            # Diversification ratio
            asset_vols = np.sqrt(np.diag(cov_matrix.values))
            weighted_vol = np.dot(weights, asset_vols)
            diversification_ratio = weighted_vol / portfolio_vol if portfolio_vol > 0 else 1
            
            return {
                'expected_return': float(portfolio_return),
                'volatility': float(portfolio_vol),
                'sharpe_ratio': float(sharpe_ratio),
                'max_drawdown_approx': float(max_drawdown_approx),
                'diversification_ratio': float(diversification_ratio),
                'concentration_index': float(np.sum(weights ** 2))  # Herfindahl index
            }
            
        except Exception as e:
            self.log_error(f"Error calculating portfolio metrics: {e}")
            return {}
    
    def _get_risk_parameters(self, risk_tolerance: str) -> Dict[str, float]:
        """Get risk parameters based on risk tolerance level."""
        risk_params = {
            'low': {
                'max_volatility': 0.10,
                'max_drawdown': 0.05,
                'min_diversification': 0.8
            },
            'moderate': {
                'max_volatility': 0.15,
                'max_drawdown': 0.10,
                'min_diversification': 0.7
            },
            'high': {
                'max_volatility': 0.25,
                'max_drawdown': 0.20,
                'min_diversification': 0.6
            }
        }
        
        return risk_params.get(risk_tolerance, risk_params['moderate'])
    
    def rebalance_portfolio(
        self,
        current_weights: pd.Series,
        target_weights: pd.Series,
        transaction_costs: float = 0.001,
        rebalancing_threshold: float = 0.05
    ) -> Dict[str, Any]:
        """
        Calculate rebalancing trades.
        
        Args:
            current_weights: Current portfolio weights
            target_weights: Target portfolio weights
            transaction_costs: Transaction cost as percentage
            rebalancing_threshold: Minimum weight change to trigger rebalancing
        
        Returns:
            Dictionary containing rebalancing information
        """
        try:
            # Calculate weight differences
            weight_diff = target_weights - current_weights
            
            # Filter trades above threshold
            significant_trades = weight_diff[abs(weight_diff) > rebalancing_threshold]
            
            # Calculate transaction costs
            total_transaction_cost = abs(significant_trades).sum() * transaction_costs
            
            # Prepare rebalancing plan
            rebalancing_plan = {
                'trades': significant_trades.to_dict(),
                'total_transaction_cost': total_transaction_cost,
                'rebalancing_threshold': rebalancing_threshold,
                'trades_count': len(significant_trades)
            }
            
            self.log_info(f"Rebalancing plan created: {len(significant_trades)} trades, cost: {total_transaction_cost:.4f}")
            return rebalancing_plan
            
        except Exception as e:
            self.log_error(f"Error calculating rebalancing: {e}")
            return {}
