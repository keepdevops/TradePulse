#!/usr/bin/env python3
"""
Message Handler for AI Module
Processes incoming messages and sends appropriate responses.
"""

import json
import time
import pandas as pd
from typing import Dict, Any, Optional
from utils.logger import setup_logger
from utils.message_bus_client import MessageBusClient
from .portfolio_optimizer import PortfolioOptimizer
from .strategy_generator import AIStrategyGenerator
from .risk_manager import RiskManager

logger = setup_logger(__name__)


class AIModuleMessageHandler:
    """Handles incoming messages for the AI Module."""
    
    def __init__(self, message_bus: MessageBusClient, strategy_generator: AIStrategyGenerator, 
                 risk_manager: RiskManager, portfolio_optimizer: PortfolioOptimizer):
        """Initialize the message handler."""
        self.message_bus = message_bus
        self.strategy_generator = strategy_generator
        self.risk_manager = risk_manager
        self.portfolio_optimizer = portfolio_optimizer
        self.logger = setup_logger(__name__)
        
        self.logger.info("AI Module Message Handler initialized")
    
    def get_message_handlers(self) -> Dict[str, callable]:
        """Get mapping of topics to handler functions."""
        return {
            "strategy_request": self.handle_strategy_request,
            "risk_assessment_request": self.handle_risk_assessment_request,
            "portfolio_optimization_request": self.handle_portfolio_optimization_request,
            "market_data_update": self.handle_market_data_update,
            "ml_predictions": self.handle_ml_predictions
        }
    
    def handle_strategy_request(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle strategy generation requests."""
        try:
            self.logger.info(f"Processing strategy request: {data}")
            
            # Extract request details
            request_id = data.get('id', 'unknown')
            strategy_type = data.get('strategy_type')
            market_conditions = data.get('market_conditions', 'neutral')
            risk_tolerance = data.get('risk_tolerance', 'moderate')
            timeframe = data.get('timeframe', '1d')
            
            # Generate mock market data for demonstration
            # In real implementation, this would come from the data module
            market_data = self._generate_mock_market_data()
            
            # Generate strategy
            strategy = self.strategy_generator.generate_strategy(
                market_data=market_data,
                strategy_type=strategy_type,
                risk_tolerance=risk_tolerance
            )
            
            # Prepare response
            response = {
                "id": request_id,
                "type": "strategy_response",
                "status": "success",
                "strategy": strategy,
                "timestamp": time.time(),
                "message": f"Strategy generated successfully for {strategy_type or 'auto-selected'} strategy"
            }
            
            # Send response
            self.message_bus.publish("strategy_response", json.dumps(response))
            self.logger.info(f"Sent strategy response for request {request_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling strategy request: {e}")
            # Send error response
            error_response = {
                "id": data.get('id', 'unknown'),
                "type": "strategy_response",
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
            self.message_bus.publish("strategy_response", json.dumps(error_response))
    
    def handle_risk_assessment_request(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle risk assessment requests."""
        try:
            self.logger.info(f"Processing risk assessment request: {data}")
            
            # Extract request details
            request_id = data.get('id', 'unknown')
            portfolio_data = data.get('portfolio_data', {})
            risk_tolerance = data.get('risk_tolerance', 'moderate')
            
            # Generate mock portfolio data for demonstration
            if not portfolio_data:
                portfolio_data = self._generate_mock_portfolio_data()
            
            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(portfolio_data, risk_tolerance)
            
            # Prepare response
            response = {
                "id": request_id,
                "type": "risk_assessment_response",
                "status": "success",
                "risk_metrics": risk_metrics,
                "risk_tolerance": risk_tolerance,
                "timestamp": time.time(),
                "message": "Risk assessment completed successfully"
            }
            
            # Send response
            self.message_bus.publish("risk_assessment_response", json.dumps(response))
            self.logger.info(f"Sent risk assessment response for request {request_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling risk assessment request: {e}")
            # Send error response
            error_response = {
                "id": data.get('id', 'unknown'),
                "type": "risk_assessment_response",
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
            self.message_bus.publish("risk_assessment_response", json.dumps(error_response))
    
    def handle_portfolio_optimization_request(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle portfolio optimization requests."""
        try:
            self.logger.info(f"Processing portfolio optimization request: {data}")
            
            # Extract request details
            request_id = data.get('id', 'unknown')
            optimization_type = data.get('optimization_type', 'markowitz')
            risk_tolerance = data.get('risk_tolerance', 'moderate')
            constraints = data.get('constraints', {})
            target_return = data.get('target_return')
            target_volatility = data.get('target_volatility')
            
            # Generate mock returns data for demonstration
            # In real implementation, this would come from the data module
            returns_data = self._generate_mock_returns_data()
            
            # Perform portfolio optimization
            optimization_result = self.portfolio_optimizer.optimize_portfolio(
                returns=returns_data,
                optimization_type=optimization_type,
                risk_tolerance=risk_tolerance,
                constraints=constraints,
                target_return=target_return,
                target_volatility=target_volatility
            )
            
            # Prepare response
            response = {
                "id": request_id,
                "type": "portfolio_optimization_response",
                "status": "success",
                "optimization_result": optimization_result,
                "timestamp": time.time(),
                "message": f"Portfolio optimization completed successfully using {optimization_type} method"
            }
            
            # Send response
            self.message_bus.publish("portfolio_optimization_response", json.dumps(response))
            self.logger.info(f"Sent portfolio optimization response for request {request_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling portfolio optimization request: {e}")
            # Send error response
            error_response = {
                "id": data.get('id', 'unknown'),
                "type": "portfolio_optimization_response",
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
            self.message_bus.publish("portfolio_optimization_response", json.dumps(error_response))
    
    def handle_market_data_update(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle market data updates."""
        try:
            self.logger.info(f"Received market data update: {data}")
            
            # Store market data for use in strategy generation
            # In real implementation, this would update a data store
            self.logger.info("Market data update processed")
            
        except Exception as e:
            self.logger.error(f"Error handling market data update: {e}")
    
    def handle_ml_predictions(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle ML predictions updates."""
        try:
            self.logger.info(f"Received ML predictions update: {data}")
            
            # Store ML predictions for use in strategy generation
            # In real implementation, this would update a predictions store
            self.logger.info("ML predictions update processed")
            
        except Exception as e:
            self.logger.error(f"Error handling ML predictions update: {e}")
    
    def _generate_mock_market_data(self) -> pd.DataFrame:
        """Generate mock market data for demonstration purposes."""
        import numpy as np
        
        # Generate 100 days of mock data for 5 assets
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        assets = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
        
        # Generate random price data
        np.random.seed(42)  # For reproducible results
        base_prices = [150, 2800, 300, 200, 3300]
        
        data = {}
        for i, asset in enumerate(assets):
            # Generate price series with some trend and volatility
            returns = np.random.normal(0.001, 0.02, 100)  # Daily returns
            prices = [base_prices[i]]
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            data[asset] = prices
        
        return pd.DataFrame(data, index=dates)
    
    def _generate_mock_portfolio_data(self) -> Dict[str, Any]:
        """Generate mock portfolio data for demonstration purposes."""
        return {
            'positions': {
                'AAPL': {'weight': 0.3, 'value': 30000},
                'GOOGL': {'weight': 0.25, 'value': 25000},
                'MSFT': {'weight': 0.25, 'value': 25000},
                'TSLA': {'weight': 0.1, 'value': 10000},
                'AMZN': {'weight': 0.1, 'value': 10000}
            },
            'total_value': 100000,
            'cash': 5000
        }
    
    def _generate_mock_returns_data(self) -> pd.DataFrame:
        """Generate mock returns data for demonstration purposes."""
        import numpy as np
        
        # Generate 252 days of mock returns (trading days in a year)
        dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
        assets = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META', 'NFLX']
        
        # Generate correlated returns
        np.random.seed(42)  # For reproducible results
        
        # Create correlation matrix (assets are somewhat correlated)
        n_assets = len(assets)
        correlation_matrix = np.eye(n_assets) * 0.3 + np.ones((n_assets, n_assets)) * 0.7
        
        # Generate correlated random returns
        returns = np.random.multivariate_normal(
            mean=np.full(n_assets, 0.001),  # 0.1% daily return
            cov=correlation_matrix * 0.02**2,  # 2% daily volatility
            size=252
        )
        
        return pd.DataFrame(returns, index=dates, columns=assets)
    
    def _calculate_risk_metrics(self, portfolio_data: Dict[str, Any], risk_tolerance: str) -> Dict[str, Any]:
        """Calculate risk metrics for the portfolio."""
        try:
            positions = portfolio_data.get('positions', {})
            total_value = portfolio_data.get('total_value', 100000)
            
            # Calculate basic risk metrics
            position_count = len(positions)
            max_position_weight = max([pos['weight'] for pos in positions.values()]) if positions else 0
            concentration_risk = sum([pos['weight']**2 for pos in positions.values()]) if positions else 0
            
            # Calculate portfolio-level metrics
            portfolio_metrics = {
                'position_count': position_count,
                'max_position_weight': max_position_weight,
                'concentration_risk': concentration_risk,
                'diversification_score': 1.0 / (1.0 + concentration_risk),
                'risk_tolerance': risk_tolerance,
                'total_value': total_value
            }
            
            # Add risk tolerance specific metrics
            if risk_tolerance == 'low':
                portfolio_metrics['risk_score'] = 'Low'
                portfolio_metrics['max_drawdown_limit'] = 0.05
            elif risk_tolerance == 'moderate':
                portfolio_metrics['risk_score'] = 'Medium'
                portfolio_metrics['max_drawdown_limit'] = 0.10
            else:  # high
                portfolio_metrics['risk_score'] = 'High'
                portfolio_metrics['max_drawdown_limit'] = 0.20
            
            return portfolio_metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {e}")
            return {}
