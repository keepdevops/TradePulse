#!/usr/bin/env python3
"""
TradePulse Portfolio Panel - Operations
Data processing operations for the portfolio panel
"""

import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class PortfolioOperations:
    """Data processing operations for portfolio panel"""
    
    def create_positions_dataframe(self, data_manager) -> pd.DataFrame:
        """Create positions dataframe from portfolio data"""
        portfolio_data = data_manager.get_portfolio_data()
        positions = portfolio_data['positions']
        data = []
        
        for symbol, pos in positions.items():
            current_value = pos['shares'] * pos['current_price']
            avg_value = pos['shares'] * pos['avg_price']
            pnl = current_value - avg_value
            pnl_pct = (pnl / avg_value) * 100 if avg_value > 0 else 0
            
            data.append({
                'Symbol': symbol,
                'Shares': pos['shares'],
                'Avg Price': f"${pos['avg_price']:.2f}",
                'Current Price': f"${pos['current_price']:.2f}",
                'Current Value': f"${current_value:,.2f}",
                'P&L': f"${pnl:,.2f}",
                'P&L %': f"{pnl_pct:.2f}%"
            })
        
        return pd.DataFrame(data)
    
    def calculate_portfolio_metrics(self, data_manager) -> Dict:
        """Calculate portfolio performance metrics"""
        try:
            portfolio_data = data_manager.get_portfolio_data()
            positions = portfolio_data['positions']
            
            total_value = portfolio_data['total_value']
            total_cost = sum(pos['shares'] * pos['avg_price'] for pos in positions.values())
            total_pnl = total_value - total_cost
            total_pnl_pct = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
            
            return {
                'total_value': total_value,
                'total_cost': total_cost,
                'total_pnl': total_pnl,
                'total_pnl_pct': total_pnl_pct,
                'num_positions': len(positions),
                'yearly_return': portfolio_data['performance']['yearly_return']
            }
        except Exception as e:
            logger.error(f"Failed to calculate portfolio metrics: {e}")
            return {}
    
    def validate_portfolio_data(self, data_manager) -> bool:
        """Validate portfolio data structure"""
        try:
            portfolio_data = data_manager.get_portfolio_data()
            
            required_keys = ['total_value', 'positions', 'performance']
            if not all(key in portfolio_data for key in required_keys):
                return False
            
            if 'positions' not in portfolio_data or not isinstance(portfolio_data['positions'], dict):
                return False
            
            if 'performance' not in portfolio_data or not isinstance(portfolio_data['performance'], dict):
                return False
            
            return True
        except Exception as e:
            logger.error(f"Failed to validate portfolio data: {e}")
            return False
    
    def get_portfolio_summary(self, data_manager) -> Dict:
        """Get portfolio summary statistics"""
        try:
            portfolio_data = data_manager.get_portfolio_data()
            positions = portfolio_data['positions']
            
            if not positions:
                return {'message': 'No positions in portfolio'}
            
            # Calculate summary statistics
            total_shares = sum(pos['shares'] for pos in positions.values())
            total_value = sum(pos['shares'] * pos['current_price'] for pos in positions.values())
            total_cost = sum(pos['shares'] * pos['avg_price'] for pos in positions.values())
            
            # Find best and worst performers
            performances = []
            for symbol, pos in positions.items():
                pnl_pct = ((pos['current_price'] - pos['avg_price']) / pos['avg_price']) * 100
                performances.append((symbol, pnl_pct))
            
            performances.sort(key=lambda x: x[1], reverse=True)
            best_performer = performances[0] if performances else None
            worst_performer = performances[-1] if performances else None
            
            return {
                'total_positions': len(positions),
                'total_shares': total_shares,
                'total_value': total_value,
                'total_cost': total_cost,
                'total_pnl': total_value - total_cost,
                'best_performer': best_performer,
                'worst_performer': worst_performer
            }
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            return {}

