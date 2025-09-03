#!/usr/bin/env python3
"""
TradePulse Portfolio - Layout Manager
Handles layout creation for portfolio panel
"""

import panel as pn
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class PortfolioLayoutManager:
    """Handles layout creation for portfolio panel"""
    
    def __init__(self, components: Dict, dataset_selector):
        self.components = components
        self.dataset_selector = dataset_selector
    
    def create_panel_layout(self):
        """Create the portfolio panel layout"""
        # Portfolio overview
        portfolio_overview = pn.Column(
            pn.pane.Markdown("### 💼 Portfolio Overview"),
            pn.Row(
                self.components['portfolio_value'],
                self.components['pnl_display'],
                align='center'
            ),
            self.components['performance_display'],
            sizing_mode='stretch_width'
        )
        
        # Portfolio optimization
        portfolio_optimization = pn.Column(
            pn.pane.Markdown("### 🚀 Portfolio Optimization"),
            pn.Row(
                self.components['strategy_selector'],
                self.components['risk_tolerance'],
                align='center'
            ),
            pn.Row(
                self.components['optimize_button'],
                self.components['rebalance_button'],
                align='center'
            ),
            sizing_mode='stretch_width'
        )
        
        # Trading interface
        trading_interface = pn.Column(
            pn.pane.Markdown("### 📈 Trading Interface"),
            pn.Row(
                self.components['symbol_input'],
                self.components['shares_input'],
                self.components['price_input'],
                align='center'
            ),
            pn.Row(
                self.components['buy_button'],
                self.components['sell_button'],
                align='center'
            ),
            sizing_mode='stretch_width'
        )
        
        # Positions management
        positions_management = pn.Column(
            pn.pane.Markdown("### 📊 Positions Management"),
            self.components['positions_table'],
            sizing_mode='stretch_width'
        )
        
        # Dataset selector
        dataset_section = self.dataset_selector.get_component()
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('💼 Overview', portfolio_overview),
            ('🚀 Optimization', portfolio_optimization),
            ('📈 Trading', trading_interface),
            ('📊 Positions', positions_management),
            ('📁 Data Sources', dataset_section),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 💼 Enhanced Portfolio Management"),
            pn.pane.Markdown("Manage your portfolio with advanced optimization and trading tools"),
            tabs,
            sizing_mode='stretch_width'
        )
