#!/usr/bin/env python3
"""
TradePulse Portfolio Panel - Layout Manager
Layout management for the portfolio panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class PortfolioLayout:
    """Layout management for portfolio panel"""
    
    @staticmethod
    def create_overview_section(components):
        """Create portfolio overview section"""
        return pn.Column(
            pn.pane.Markdown("### 💼 Portfolio Overview"),
            pn.Row(
                components.portfolio_value,
                components.pnl_display,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_optimization_section(components):
        """Create portfolio optimization section"""
        return pn.Column(
            pn.pane.Markdown("### 📈 Portfolio Optimization"),
            pn.Row(
                components.strategy_selector,
                components.risk_tolerance,
                align='center'
            ),
            pn.Row(
                components.optimize_button,
                components.rebalance_button,
                components.refresh_data_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_trading_section(components):
        """Create trading section"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Current Positions"),
            components.positions_table,
            pn.pane.Markdown("### 📈 Place Order"),
            pn.Row(
                components.symbol_input,
                components.shares_input,
                components.price_input,
                components.order_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_main_layout(components, dataset_selector):
        """Create main portfolio layout"""
        # Create sections
        overview_section = PortfolioLayout.create_overview_section(components)
        optimization_section = PortfolioLayout.create_optimization_section(components)
        trading_section = PortfolioLayout.create_trading_section(components)
        dataset_section = dataset_selector.get_component()
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('💼 Overview', overview_section),
            ('📈 Optimization', optimization_section),
            ('📊 Trading', trading_section),
            ('📁 Data Sources', dataset_section),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 💼 Enhanced Portfolio Management"),
            pn.pane.Markdown("Manage your portfolio with uploaded data and advanced optimization"),
            tabs,
            sizing_mode='stretch_width'
        )

