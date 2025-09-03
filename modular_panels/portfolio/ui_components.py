#!/usr/bin/env python3
"""
TradePulse Portfolio - UI Components
Handles UI components initialization for portfolio panel
"""

import panel as pn
import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class PortfolioUIComponents:
    """Handles UI components initialization for portfolio panel"""
    
    def __init__(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager
        self.components = {}
    
    def init_ui_components(self):
        """Initialize UI components"""
        # Portfolio value display
        portfolio_summary = self.portfolio_manager.get_portfolio_summary()
        self.components['portfolio_value'] = pn.indicators.Number(
            name='Portfolio Value',
            value=portfolio_summary['total_value'],
            format='${value:,.0f}',
            font_size='24pt'
        )
        
        # P&L display
        self.components['pnl_display'] = pn.indicators.Number(
            name='Total Return',
            value=portfolio_summary['unrealized_pnl_pct'],
            format='{value:.2f}%',
            font_size='20pt'
        )
        
        # Optimization strategy selector
        self.components['strategy_selector'] = pn.widgets.Select(
            name='Optimization Strategy',
            options=['Markowitz', 'Black-Litterman', 'Risk Parity', 'Equal Weight'],
            value='Markowitz',
            width=200
        )
        
        # Risk tolerance slider
        self.components['risk_tolerance'] = pn.widgets.FloatSlider(
            name='Risk Tolerance',
            start=0.1,
            end=2.0,
            value=1.0,
            step=0.1,
            width=200
        )
        
        # Action buttons
        self.components['optimize_button'] = pn.widgets.Button(
            name='🚀 Optimize Portfolio',
            button_type='primary',
            width=150
        )
        
        self.components['rebalance_button'] = pn.widgets.Button(
            name='⚖️ Rebalance',
            button_type='success',
            width=150
        )
        
        # Positions table
        self.components['positions_table'] = pn.widgets.Tabulator(
            self.portfolio_manager.create_positions_dataframe(),
            height=200,
            name='Current Positions'
        )
        
        # Order entry
        self.components['symbol_input'] = pn.widgets.TextInput(
            name='Symbol',
            placeholder='Enter symbol...',
            width=100
        )
        
        self.components['shares_input'] = pn.widgets.IntInput(
            name='Shares',
            start=1,
            width=100
        )
        
        self.components['price_input'] = pn.widgets.FloatInput(
            name='Price',
            start=0.01,
            width=100
        )
        
        # Buy/Sell buttons
        self.components['buy_button'] = pn.widgets.Button(
            name='🟢 Buy',
            button_type='success',
            width=80
        )
        
        self.components['sell_button'] = pn.widgets.Button(
            name='🔴 Sell',
            button_type='danger',
            width=80
        )
        
        # Portfolio performance
        self.components['performance_display'] = pn.pane.Markdown("""
        ### 📊 Portfolio Performance
        - **Total Positions**: 0
        - **Cash**: $25,000
        - **Invested Value**: $0
        - **Unrealized P&L**: $0 (0.00%)
        """)
    
    def get_components(self) -> Dict:
        """Get all UI components"""
        return self.components
