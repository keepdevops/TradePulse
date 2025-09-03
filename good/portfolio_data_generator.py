#!/usr/bin/env python3
"""
TradePulse Demo Panels - Portfolio Data Generator
Handles generation of demo portfolio data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class PortfolioDataGenerator:
    """Handles generation of demo portfolio data"""
    
    def __init__(self, price_data_generator):
        self.price_data_generator = price_data_generator
        self.portfolio_data = {}
        self.init_portfolio_data()
    
    def init_portfolio_data(self):
        """Initialize demo portfolio data"""
        try:
            logger.info("🔧 Initializing demo portfolio data")
            
            # Generate sample portfolio positions
            self.portfolio_data = {
                'total_value': 100000.0,
                'cash': 25000.0,
                'positions': {},
                'performance_metrics': {
                    'total_return': 0.0,
                    'daily_return': 0.0,
                    'sharpe_ratio': 0.0,
                    'max_drawdown': 0.0
                }
            }
            
            # Generate positions for each symbol
            for symbol in self.price_data_generator.symbols[:5]:  # First 5 symbols
                quantity = np.random.randint(100, 1000)
                avg_price = self.price_data_generator.price_data[symbol]['Close'].iloc[-1] * (0.8 + np.random.random() * 0.4)
                current_price = self.price_data_generator.price_data[symbol]['Close'].iloc[-1]
                
                self.portfolio_data['positions'][symbol] = {
                    'quantity': quantity,
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'market_value': quantity * current_price,
                    'unrealized_pnl': quantity * (current_price - avg_price),
                    'unrealized_pnl_pct': ((current_price - avg_price) / avg_price) * 100
                }
            
            # Calculate total portfolio value
            total_market_value = sum(pos['market_value'] for pos in self.portfolio_data['positions'].values())
            self.portfolio_data['total_value'] = self.portfolio_data['cash'] + total_market_value
            
            logger.info("✅ Demo portfolio data initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize demo portfolio data: {e}")
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary data"""
        try:
            return self.portfolio_data.copy()
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            return {}
    
    def update_portfolio_value(self):
        """Update portfolio values based on current prices"""
        try:
            total_market_value = 0
            
            for symbol, position in self.portfolio_data['positions'].items():
                current_price = self.price_data_generator.get_current_price(symbol)
                if current_price:
                    position['current_price'] = current_price
                    position['market_value'] = position['quantity'] * current_price
                    position['unrealized_pnl'] = position['quantity'] * (current_price - position['avg_price'])
                    position['unrealized_pnl_pct'] = ((current_price - position['avg_price']) / position['avg_price']) * 100
                    
                    total_market_value += position['market_value']
            
            # Update total portfolio value
            self.portfolio_data['total_value'] = self.portfolio_data['cash'] + total_market_value
            
            # Calculate performance metrics
            self._calculate_performance_metrics()
            
            logger.debug("✅ Portfolio values updated")
            
        except Exception as e:
            logger.error(f"Failed to update portfolio values: {e}")
    
    def _calculate_performance_metrics(self):
        """Calculate portfolio performance metrics"""
        try:
            initial_value = 100000.0
            current_value = self.portfolio_data['total_value']
            total_return = ((current_value - initial_value) / initial_value) * 100
            daily_return = np.random.normal(0, 2)
            sharpe_ratio = np.random.normal(0, 1)
            max_drawdown = abs(np.random.normal(0, 5))
            
            self.portfolio_data['performance_metrics'] = {
                'total_return': total_return,
                'daily_return': daily_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate performance metrics: {e}")
    
    def update_portfolio_from_trade(self, trade: Dict[str, Any]):
        """Update portfolio based on a trade"""
        try:
            symbol = trade['symbol']
            action = trade['action']
            quantity = trade['quantity']
            price = trade['price']
            
            if symbol not in self.portfolio_data['positions']:
                self.portfolio_data['positions'][symbol] = {
                    'quantity': 0,
                    'avg_price': 0.0,
                    'current_price': price,
                    'market_value': 0.0,
                    'unrealized_pnl': 0.0,
                    'unrealized_pnl_pct': 0.0
                }
            
            position = self.portfolio_data['positions'][symbol]
            
            if action == 'BUY':
                total_cost = (position['quantity'] * position['avg_price']) + (quantity * price)
                total_quantity = position['quantity'] + quantity
                position['avg_price'] = total_cost / total_quantity if total_quantity > 0 else price
                position['quantity'] = total_quantity
                self.portfolio_data['cash'] -= (quantity * price)
            elif action == 'SELL':
                position['quantity'] -= quantity
                if position['quantity'] <= 0:
                    del self.portfolio_data['positions'][symbol]
                self.portfolio_data['cash'] += (quantity * price)
            self.update_portfolio_value()
            
        except Exception as e:
            logger.error(f"Failed to update portfolio from trade: {e}")
    
    def reset_portfolio_data(self):
        """Reset portfolio data to initial state"""
        try:
            logger.info("🔄 Resetting portfolio data")
            self.init_portfolio_data()
            logger.info("✅ Portfolio data reset completed")
        except Exception as e:
            logger.error(f"Failed to reset portfolio data: {e}")
    
    def export_portfolio_data(self) -> Dict[str, Any]:
        """Export portfolio data for external use"""
        try:
            export_data = {
                'portfolio_data': self.portfolio_data.copy(),
                'export_timestamp': datetime.now().isoformat()
            }
            logger.info("📤 Portfolio data exported")
            return export_data
        except Exception as e:
            logger.error(f"Failed to export portfolio data: {e}")
            return {}
    
    def import_portfolio_data(self, portfolio_data: Dict[str, Any]):
        """Import portfolio data from external source"""
        try:
            if 'portfolio_data' in portfolio_data:
                self.portfolio_data = portfolio_data['portfolio_data']
            logger.info("📥 Portfolio data imported")
        except Exception as e:
            logger.error(f"Failed to import portfolio data: {e}")
