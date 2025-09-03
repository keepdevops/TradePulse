#!/usr/bin/env python3
"""
TradePulse Panel UI - Portfolio Components
Portfolio management and ML model components
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Callable
import logging

from .base import BaseComponent, DataManager

logger = logging.getLogger(__name__)

class PortfolioComponent(BaseComponent):
    """Component for portfolio management"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("PortfolioComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create portfolio components"""
        self.components['portfolio_value'] = pn.pane.Markdown("**Portfolio Value:** $100,000.00")
        self.components['portfolio_pnl'] = pn.pane.Markdown("**P&L:** +$0.00 (+0.00%)")
        
        self.components['optimization_strategy'] = pn.widgets.Select(
            name='Optimization Strategy',
            options=['Markowitz', 'Risk Parity', 'Sharpe Ratio', 'Black-Litterman', 'HRP'],
            value='Markowitz',
            width=150
        )
        
        self.components['risk_tolerance'] = pn.widgets.Select(
            name='Risk Tolerance',
            options=['Conservative', 'Moderate', 'Aggressive'],
            value='Moderate',
            width=120
        )
        
        self.components['optimize_button'] = pn.widgets.Button(
            name='Optimize Portfolio',
            button_type='primary',
            width=140
        )
        
        self.components['positions_table'] = pn.widgets.Tabulator(
            self.create_positions_dataframe(),
            height=200
        )
        
        # Order entry
        self.components['order_symbol'] = pn.widgets.TextInput(
            name='Symbol',
            value='AAPL',
            width=100
        )
        
        self.components['order_quantity'] = pn.widgets.IntInput(
            name='Quantity',
            value=100,
            width=100
        )
        
        self.components['order_type'] = pn.widgets.Select(
            name='Order Type',
            options=['Market', 'Limit', 'Stop'],
            value='Market',
            width=100
        )
        
        self.components['order_price'] = pn.widgets.FloatInput(
            name='Price',
            value=0.0,
            width=100
        )
        
        self.components['place_order_button'] = pn.widgets.Button(
            name='Place Order',
            button_type='primary',
            width=120
        )
    
    def get_layout(self):
        """Get the portfolio layout"""
        return pn.Column(
            pn.pane.Markdown("### 💼 Portfolio Management"),
            pn.Row(self.components['portfolio_value'], self.components['portfolio_pnl']),
            pn.pane.Markdown("#### Portfolio Optimization"),
            pn.Row(self.components['optimization_strategy'], self.components['risk_tolerance'], self.components['optimize_button']),
            pn.pane.Markdown("#### Current Positions"),
            self.components['positions_table'],
            pn.pane.Markdown("#### Place Order"),
            pn.Row(
                self.components['order_symbol'],
                self.components['order_quantity'],
                self.components['order_type'],
                self.components['order_price'],
                self.components['place_order_button']
            )
        )
    
    def create_positions_dataframe(self):
        """Create positions dataframe"""
        positions = self.data_manager.get_portfolio_data()['positions']
        data = []
        
        for symbol, pos in positions.items():
            pnl = (pos['current_price'] - pos['avg_price']) * pos['shares']
            pnl_pct = (pos['current_price'] / pos['avg_price'] - 1) * 100
            data.append({
                'Symbol': symbol,
                'Shares': pos['shares'],
                'Avg Price': f"${pos['avg_price']:.2f}",
                'Current Price': f"${pos['current_price']:.2f}",
                'P&L': f"${pnl:.2f}",
                'P&L %': f"{pnl_pct:+.2f}%"
            })
        
        return pd.DataFrame(data)
    
    def update_portfolio_display(self):
        """Update portfolio display"""
        portfolio = self.data_manager.get_portfolio_data()
        total_value = portfolio['total_value']
        performance = portfolio['performance']
        
        self.components['portfolio_value'].object = f"**Portfolio Value:** ${total_value:,.2f}"
        self.components['portfolio_pnl'].object = f"**P&L:** +${performance['daily_pnl']:,.2f} (+{performance['total_return']*100:.2f}%)"
        self.components['positions_table'].value = self.create_positions_dataframe()
    
    def set_optimize_callback(self, callback: Callable):
        """Set callback for optimize button"""
        self.components['optimize_button'].on_click(callback)
    
    def set_place_order_callback(self, callback: Callable):
        """Set callback for place order button"""
        self.components['place_order_button'].on_click(callback)

class MLComponent(BaseComponent):
    """Component for ML model controls"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("MLComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create ML components"""
        self.components['ml_model_selector'] = pn.widgets.Select(
            name='ML Model',
            options=['ADM', 'CIPO', 'BICIPO', 'Ensemble'],
            value='Ensemble',
            width=120
        )
        
        self.components['predict_button'] = pn.widgets.Button(
            name='Generate Prediction',
            button_type='warning',
            width=140
        )
    
    def get_layout(self):
        """Get the ML layout"""
        return pn.Column(
            pn.pane.Markdown("### 🤖 ML Model Controls"),
            pn.Row(self.components['ml_model_selector'], self.components['predict_button'])
        )
    
    def set_predict_callback(self, callback: Callable):
        """Set callback for predict button"""
        self.components['predict_button'].on_click(callback)
    
    def get_selected_model(self) -> str:
        """Get selected ML model"""
        return self.components['ml_model_selector'].value
