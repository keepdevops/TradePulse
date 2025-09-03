#!/usr/bin/env python3
"""
TradePulse UI Panels - Portfolio UI Components
Handles portfolio UI component creation
"""

import panel as pn
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PortfolioUIComponents:
    """Handles portfolio UI component creation"""
    
    def create_portfolio_summary(self):
        """Create portfolio summary display"""
        try:
            summary_section = pn.Column(
                pn.pane.Markdown("**💼 Portfolio Summary**"),
                pn.pane.Markdown("**Total Value:** $0.00"),
                pn.pane.Markdown("**Total P&L:** $0.00 (0.00%)"),
                pn.pane.Markdown("**Positions:** 0"),
                sizing_mode='stretch_width'
            )
            
            return summary_section
            
        except Exception as e:
            logger.error(f"Failed to create portfolio summary: {e}")
            return pn.pane.Markdown("**Portfolio Summary Error**")
    
    def create_positions_table(self):
        """Create positions table display"""
        try:
            # Create empty DataFrame for positions
            empty_df = pd.DataFrame({
                'Symbol': [],
                'Shares': [],
                'Avg Price': [],
                'Current Price': [],
                'Market Value': [],
                'P&L': [],
                'P&L %': []
            })
            
            positions_table = pn.widgets.Tabulator(
                empty_df,
                height=200,
                name='Portfolio Positions',
                sizing_mode='stretch_width'
            )
            
            return positions_table
            
        except Exception as e:
            logger.error(f"Failed to create positions table: {e}")
            return pn.pane.Markdown("**Positions Table Error**")
    
    def create_performance_metrics(self):
        """Create performance metrics display"""
        try:
            metrics_section = pn.Column(
                pn.pane.Markdown("**📈 Performance Metrics**"),
                pn.pane.Markdown("**Daily P&L:** $0.00"),
                pn.pane.Markdown("**Weekly P&L:** $0.00"),
                pn.pane.Markdown("**Monthly P&L:** $0.00"),
                pn.pane.Markdown("**YTD P&L:** $0.00"),
                pn.pane.Markdown("**Sharpe Ratio:** 0.00"),
                pn.pane.Markdown("**Max Drawdown:** 0.00%"),
                sizing_mode='stretch_width'
            )
            
            return metrics_section
            
        except Exception as e:
            logger.error(f"Failed to create performance metrics: {e}")
            return pn.pane.Markdown("**Performance Metrics Error**")
    
    def create_portfolio_controls(self, operations):
        """Create portfolio control buttons"""
        try:
            refresh_button = pn.widgets.Button(
                name='🔄 Refresh',
                button_type='primary',
                width=100
            )
            refresh_button.on_click(operations.refresh_portfolio)
            
            export_button = pn.widgets.Button(
                name='📤 Export',
                button_type='success',
                width=100
            )
            export_button.on_click(operations.export_portfolio)
            
            add_position_button = pn.widgets.Button(
                name='➕ Add Position',
                button_type='light',
                width=120
            )
            add_position_button.on_click(operations.add_position)
            
            controls_row = pn.Row(
                refresh_button,
                export_button,
                add_position_button,
                align='center'
            )
            
            return controls_row
            
        except Exception as e:
            logger.error(f"Failed to create portfolio controls: {e}")
            return pn.pane.Markdown("**Portfolio Controls Error**")
