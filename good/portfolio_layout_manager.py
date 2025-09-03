#!/usr/bin/env python3
"""
TradePulse UI Panels - Portfolio Layout Manager
Handles portfolio layout creation and management
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class PortfolioLayoutManager:
    """Handles portfolio layout creation and management"""
    
    def create_portfolio_layout(self, portfolio_controls, portfolio_summary, performance_metrics, positions_table):
        """Create the complete portfolio layout"""
        try:
            # Portfolio controls row
            controls_row = pn.Row(
                pn.pane.Markdown("### 💼 Portfolio Management"),
                pn.Spacer(width=20),
                portfolio_controls,
                align='center',
                sizing_mode='stretch_width'
            )
            
            # Portfolio summary and metrics row
            summary_metrics_row = pn.Row(
                portfolio_summary,
                pn.Spacer(width=30),
                performance_metrics,
                align='start',
                sizing_mode='stretch_width'
            )
            
            # Complete portfolio layout
            complete_layout = pn.Column(
                controls_row,
                summary_metrics_row,
                pn.Divider(),
                positions_table,
                sizing_mode='stretch_width'
            )
            
            return complete_layout
            
        except Exception as e:
            logger.error(f"Failed to create portfolio layout: {e}")
            return pn.pane.Markdown("**Portfolio Layout Error**")
