#!/usr/bin/env python3
"""
TradePulse Portfolio - Portfolio Manager
Manages portfolio data, positions, and operations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PortfolioManager:
    """Manages portfolio data, positions, and operations"""
    
    def __init__(self):
        self.positions = {}
        self.transactions = []
        self.portfolio_data = {
            'total_value': 100000.0,
            'cash': 25000.0,
            'performance': {
                'daily_return': 0.0,
                'weekly_return': 0.0,
                'monthly_return': 0.0,
                'yearly_return': 0.0,
                'total_return': 0.0
            }
        }
        self.position_counter = 0
    
    def add_position(self, symbol: str, shares: int, price: float, 
                    transaction_type: str = 'buy') -> str:
        """Add a new position or update existing one"""
        try:
            self.position_counter += 1
            position_id = f"position_{self.position_counter}"
            
            if symbol in self.positions:
                # Update existing position
                existing = self.positions[symbol]
                if transaction_type == 'buy':
                    total_shares = existing['shares'] + shares
                    avg_price = ((existing['shares'] * existing['avg_price']) + (shares * price)) / total_shares
                else:  # sell
                    total_shares = existing['shares'] - shares
                    avg_price = existing['avg_price']
                
                if total_shares <= 0:
                    # Remove position if no shares left
                    del self.positions[symbol]
                    logger.info(f"✅ Position {symbol} removed (no shares remaining)")
                else:
                    # Update position
                    self.positions[symbol].update({
                        'shares': total_shares,
                        'avg_price': avg_price,
                        'current_value': total_shares * price,
                        'last_updated': pd.Timestamp.now()
                    })
                    logger.info(f"✅ Position {symbol} updated: {total_shares} shares at ${avg_price:.2f}")
            else:
                # Create new position
                self.positions[symbol] = {
                    'id': position_id,
                    'symbol': symbol,
                    'shares': shares,
                    'avg_price': price,
                    'current_price': price,
                    'current_value': shares * price,
                    'created': pd.Timestamp.now(),
                    'last_updated': pd.Timestamp.now()
                }
                logger.info(f"✅ New position created: {symbol} - {shares} shares at ${price:.2f}")
            
            # Record transaction
            self._record_transaction(symbol, shares, price, transaction_type)
            
            # Update portfolio value
            self._update_portfolio_value()
            
            return position_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add position: {e}")
            raise
    
    def remove_position(self, symbol: str, shares: int) -> bool:
        """Remove shares from a position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"Position {symbol} not found")
                return False
            
            position = self.positions[symbol]
            if shares >= position['shares']:
                # Remove entire position
                del self.positions[symbol]
                logger.info(f"✅ Position {symbol} completely removed")
            else:
                # Reduce shares
                position['shares'] -= shares
                position['current_value'] = position['shares'] * position['current_price']
                position['last_updated'] = pd.Timestamp.now()
                logger.info(f"✅ Position {symbol} reduced by {shares} shares")
            
            # Record transaction
            self._record_transaction(symbol, shares, position['current_price'], 'sell')
            
            # Update portfolio value
            self._update_portfolio_value()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to remove position: {e}")
            return False
    
    def update_position_price(self, symbol: str, new_price: float) -> bool:
        """Update the current price of a position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"Position {symbol} not found")
                return False
            
            position = self.positions[symbol]
            old_value = position['current_value']
            
            position['current_price'] = new_price
            position['current_value'] = position['shares'] * new_price
            position['last_updated'] = pd.Timestamp.now()
            
            # Calculate P&L
            pnl = position['current_value'] - (position['shares'] * position['avg_price'])
            position['unrealized_pnl'] = pnl
            position['unrealized_pnl_pct'] = (pnl / (position['shares'] * position['avg_price'])) * 100
            
            logger.info(f"✅ Position {symbol} price updated: ${new_price:.2f} (P&L: ${pnl:.2f})")
            
            # Update portfolio value
            self._update_portfolio_value()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update position price: {e}")
            return False
    
    def get_position(self, symbol: str) -> Optional[Dict]:
        """Get position by symbol"""
        return self.positions.get(symbol)
    
    def get_all_positions(self) -> List[Dict]:
        """Get all positions"""
        return list(self.positions.values())
    
    def get_portfolio_summary(self) -> Dict:
        """Get comprehensive portfolio summary"""
        try:
            if not self.positions:
                return {
                    'total_positions': 0,
                    'total_value': self.portfolio_data['cash'],
                    'cash': self.portfolio_data['cash'],
                    'invested_value': 0.0,
                    'unrealized_pnl': 0.0,
                    'unrealized_pnl_pct': 0.0
                }
            
            total_value = sum(pos['current_value'] for pos in self.positions.values())
            total_cost = sum(pos['shares'] * pos['avg_price'] for pos in self.positions.values())
            unrealized_pnl = total_value - total_cost
            unrealized_pnl_pct = (unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
            
            return {
                'total_positions': len(self.positions),
                'total_value': total_value + self.portfolio_data['cash'],
                'cash': self.portfolio_data['cash'],
                'invested_value': total_value,
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_pct': unrealized_pnl_pct,
                'positions': self.positions
            }
            
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            return {}
    
    def create_positions_dataframe(self) -> pd.DataFrame:
        """Create DataFrame representation of positions"""
        try:
            if not self.positions:
                return pd.DataFrame()
            
            positions_data = []
            for symbol, position in self.positions.items():
                positions_data.append({
                    'Symbol': symbol,
                    'Shares': position['shares'],
                    'Avg Price': f"${position['avg_price']:.2f}",
                    'Current Price': f"${position['current_price']:.2f}",
                    'Current Value': f"${position['current_value']:,.2f}",
                    'Unrealized P&L': f"${position.get('unrealized_pnl', 0):,.2f}",
                    'P&L %': f"{position.get('unrealized_pnl_pct', 0):.2f}%"
                })
            
            return pd.DataFrame(positions_data)
            
        except Exception as e:
            logger.error(f"Failed to create positions DataFrame: {e}")
            return pd.DataFrame()
    
    def _record_transaction(self, symbol: str, shares: int, price: float, 
                           transaction_type: str):
        """Record a transaction"""
        try:
            transaction = {
                'id': f"tx_{len(self.transactions) + 1}",
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'type': transaction_type,
                'timestamp': pd.Timestamp.now(),
                'total_value': shares * price
            }
            
            self.transactions.append(transaction)
            
        except Exception as e:
            logger.error(f"Failed to record transaction: {e}")
    
    def _update_portfolio_value(self):
        """Update total portfolio value"""
        try:
            positions_value = sum(pos['current_value'] for pos in self.positions.values())
            self.portfolio_data['total_value'] = positions_value + self.portfolio_data['cash']
            
            # Update performance metrics (simplified)
            if self.transactions:
                total_invested = sum(tx['total_value'] for tx in self.transactions if tx['type'] == 'buy')
                if total_invested > 0:
                    self.portfolio_data['performance']['total_return'] = (
                        (self.portfolio_data['total_value'] - total_invested) / total_invested
                    ) * 100
            
        except Exception as e:
            logger.error(f"Failed to update portfolio value: {e}")
    
    def get_transaction_history(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get transaction history, optionally filtered by symbol"""
        if symbol:
            return [tx for tx in self.transactions if tx['symbol'] == symbol]
        return self.transactions.copy()
    
    def clear_portfolio(self) -> int:
        """Clear all positions and return count of cleared positions"""
        try:
            count = len(self.positions)
            self.positions.clear()
            self.transactions.clear()
            self.portfolio_data['total_value'] = self.portfolio_data['cash']
            logger.info(f"🗑️ Cleared {count} positions from portfolio")
            return count
        except Exception as e:
            logger.error(f"Failed to clear portfolio: {e}")
            return 0
