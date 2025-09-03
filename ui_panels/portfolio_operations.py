#!/usr/bin/env python3
"""
TradePulse UI Panels - Portfolio Operations
Handles portfolio operations and data management
"""

import pandas as pd
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PortfolioOperations:
    """Handles portfolio operations and data management"""
    
    def update_portfolio_summary(self, portfolio_summary, total_value: float, total_pnl: float, total_pnl_percent: float, positions_count: int):
        """Update portfolio summary display"""
        try:
            if hasattr(portfolio_summary, 'objects') and len(portfolio_summary.objects) > 1:
                # Update total value
                total_value_display = portfolio_summary.objects[1]
                total_value_display.object = f"**Total Value:** ${total_value:,.2f}"
                
                # Update total P&L
                pnl_color = "green" if total_pnl >= 0 else "red"
                pnl_symbol = "+" if total_pnl >= 0 else ""
                total_pnl_display = portfolio_summary.objects[2]
                total_pnl_display.object = f"**Total P&L:** {pnl_symbol}${total_pnl:,.2f} ({pnl_symbol}{total_pnl_percent:.2f}%)"
                total_pnl_display.style = {'color': pnl_color}
                
                # Update positions count
                positions_count_display = portfolio_summary.objects[3]
                positions_count_display.object = f"**Positions:** {positions_count}"
                
        except Exception as e:
            logger.error(f"Failed to update portfolio summary: {e}")
    
    def update_positions_table(self, positions_table, positions: List):
        """Update positions table display"""
        try:
            if not positions:
                # Clear table if no positions
                positions_table.value = pd.DataFrame()
                return
            
            # Create DataFrame from positions
            positions_df = pd.DataFrame(positions)
            
            # Ensure required columns exist
            required_columns = ['symbol', 'shares', 'avg_price', 'current_price', 'market_value', 'pnl', 'pnl_percent']
            for col in required_columns:
                if col not in positions_df.columns:
                    positions_df[col] = 0
            
            # Format the data
            positions_df['avg_price'] = positions_df['avg_price'].apply(lambda x: f"${x:.2f}")
            positions_df['current_price'] = positions_df['current_price'].apply(lambda x: f"${x:.2f}")
            positions_df['market_value'] = positions_df['market_value'].apply(lambda x: f"${x:,.2f}")
            positions_df['pnl'] = positions_df['pnl'].apply(lambda x: f"${x:,.2f}")
            positions_df['pnl_percent'] = positions_df['pnl_percent'].apply(lambda x: f"{x:.2f}%")
            
            # Update table
            positions_table.value = positions_df
            
        except Exception as e:
            logger.error(f"Failed to update positions table: {e}")
    
    def update_performance_metrics(self, performance_metrics, portfolio_data: Dict):
        """Update performance metrics display"""
        try:
            # Get performance data from portfolio
            daily_pnl = portfolio_data.get('daily_pnl', 0.0)
            weekly_pnl = portfolio_data.get('weekly_pnl', 0.0)
            monthly_pnl = portfolio_data.get('monthly_pnl', 0.0)
            ytd_pnl = portfolio_data.get('ytd_pnl', 0.0)
            sharpe_ratio = portfolio_data.get('sharpe_ratio', 0.0)
            max_drawdown = portfolio_data.get('max_drawdown', 0.0)
            
            if hasattr(performance_metrics, 'objects') and len(performance_metrics.objects) > 1:
                # Update daily P&L
                daily_pnl_display = performance_metrics.objects[1]
                daily_pnl_display.object = f"**Daily P&L:** ${daily_pnl:,.2f}"
                
                # Update weekly P&L
                weekly_pnl_display = performance_metrics.objects[2]
                weekly_pnl_display.object = f"**Weekly P&L:** ${weekly_pnl:,.2f}"
                
                # Update monthly P&L
                monthly_pnl_display = performance_metrics.objects[3]
                monthly_pnl_display.object = f"**Monthly P&L:** ${monthly_pnl:,.2f}"
                
                # Update YTD P&L
                ytd_pnl_display = performance_metrics.objects[4]
                ytd_pnl_display.object = f"**YTD P&L:** ${ytd_pnl:,.2f}"
                
                # Update Sharpe ratio
                sharpe_display = performance_metrics.objects[5]
                sharpe_display.object = f"**Sharpe Ratio:** {sharpe_ratio:.2f}"
                
                # Update max drawdown
                max_dd_display = performance_metrics.objects[6]
                max_dd_display.object = f"**Max Drawdown:** {max_drawdown:.2f}%"
                
        except Exception as e:
            logger.error(f"Failed to update performance metrics: {e}")
    
    def refresh_portfolio(self, event):
        """Refresh portfolio data"""
        try:
            logger.info("🔄 Refreshing portfolio...")
            # This would typically trigger a data refresh
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Failed to refresh portfolio: {e}")
    
    def export_portfolio(self, event):
        """Export portfolio data"""
        try:
            # Create export filename
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f"portfolio_{timestamp}.csv"
            
            logger.info(f"📤 Portfolio export requested: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to export portfolio: {e}")
    
    def add_position(self, event):
        """Add new position to portfolio"""
        try:
            logger.info("➕ Adding new position...")
            # This would typically open a dialog for adding positions
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Failed to add position: {e}")
    
    def get_portfolio_statistics(self, total_value: float, total_pnl: float, total_pnl_percent: float, positions: List, portfolio_data: Dict) -> Dict[str, Any]:
        """Get portfolio statistics"""
        try:
            return {
                'total_value': total_value,
                'total_pnl': total_pnl,
                'total_pnl_percent': total_pnl_percent,
                'positions_count': len(positions),
                'has_data': len(portfolio_data) > 0,
                'last_update': pd.Timestamp.now()
            }
        except Exception as e:
            logger.error(f"Failed to get portfolio statistics: {e}")
            return {}
