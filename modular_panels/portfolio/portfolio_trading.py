#!/usr/bin/env python3
"""
TradePulse Portfolio Panel - Trading
Trading operations for the portfolio panel
"""

import pandas as pd
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class PortfolioTrading:
    """Trading operations for portfolio panel"""
    
    def place_order(self, symbol: str, shares: int, price: float, data_manager) -> bool:
        """Place a new order"""
        try:
            if not symbol or not shares or not price:
                logger.warning("Invalid order parameters")
                return False
            
            if shares <= 0 or price <= 0:
                logger.warning("Invalid shares or price")
                return False
            
            order_value = shares * price
            
            # Add to orders (in a real system, this would go to a broker)
            order = {
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'value': order_value,
                'timestamp': pd.Timestamp.now()
            }
            
            data_manager.orders.append(order)
            
            logger.info(f"📈 Order placed: {shares} shares of {symbol} at ${price:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return False
    
    def validate_order(self, symbol: str, shares: int, price: float) -> Dict:
        """Validate order parameters"""
        validation_result = {
            'valid': True,
            'errors': []
        }
        
        if not symbol or not symbol.strip():
            validation_result['valid'] = False
            validation_result['errors'].append("Symbol is required")
        
        if not shares or shares <= 0:
            validation_result['valid'] = False
            validation_result['errors'].append("Shares must be positive")
        
        if not price or price <= 0:
            validation_result['valid'] = False
            validation_result['errors'].append("Price must be positive")
        
        return validation_result
    
    def calculate_order_metrics(self, symbol: str, shares: int, price: float) -> Dict:
        """Calculate order metrics"""
        try:
            order_value = shares * price
            
            return {
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'order_value': order_value,
                'commission': self._calculate_commission(order_value),
                'total_cost': order_value + self._calculate_commission(order_value)
            }
        except Exception as e:
            logger.error(f"Failed to calculate order metrics: {e}")
            return {}
    
    def _calculate_commission(self, order_value: float) -> float:
        """Calculate commission for order"""
        # Simple commission calculation (can be enhanced)
        if order_value < 1000:
            return 5.0  # Flat $5 for small orders
        elif order_value < 10000:
            return order_value * 0.005  # 0.5% for medium orders
        else:
            return order_value * 0.003  # 0.3% for large orders
    
    def get_order_history(self, data_manager) -> pd.DataFrame:
        """Get order history"""
        try:
            if not data_manager.orders:
                return pd.DataFrame()
            
            orders_data = []
            for order in data_manager.orders:
                orders_data.append({
                    'Symbol': order['symbol'],
                    'Shares': order['shares'],
                    'Price': f"${order['price']:.2f}",
                    'Value': f"${order['value']:,.2f}",
                    'Timestamp': order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return pd.DataFrame(orders_data)
        except Exception as e:
            logger.error(f"Failed to get order history: {e}")
            return pd.DataFrame()
    
    def cancel_order(self, order_index: int, data_manager) -> bool:
        """Cancel an order"""
        try:
            if 0 <= order_index < len(data_manager.orders):
                cancelled_order = data_manager.orders.pop(order_index)
                logger.info(f"📉 Order cancelled: {cancelled_order['symbol']}")
                return True
            else:
                logger.warning(f"Invalid order index: {order_index}")
                return False
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return False

