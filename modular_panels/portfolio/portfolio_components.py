#!/usr/bin/env python3
"""
TradePulse Portfolio Panel - Components
UI components for the portfolio panel
"""

import panel as pn
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PortfolioComponents:
    """UI components for portfolio panel"""
    
    def __init__(self):
        self.portfolio_value = None
        self.pnl_display = None
        self.strategy_selector = None
        self.risk_tolerance = None
        self.optimize_button = None
        self.rebalance_button = None
        self.refresh_data_button = None
        self.positions_table = None
        self.symbol_input = None
        self.shares_input = None
        self.price_input = None
        self.order_button = None
    
    def create_basic_components(self, data_manager):
        """Create basic UI components"""
        # Portfolio value display
        portfolio_data = data_manager.get_portfolio_data()
        self.portfolio_value = pn.indicators.Number(
            name='Portfolio Value',
            value=portfolio_data['total_value'],
            format='${value:,.0f}',
            font_size='24pt'
        )
        
        # P&L display
        total_return = portfolio_data['performance']['yearly_return']
        self.pnl_display = pn.indicators.Number(
            name='Total Return',
            value=total_return * 100,
            format='{value:.2f}%',
            font_size='20pt'
        )
        
        # Optimization strategy selector
        self.strategy_selector = pn.widgets.Select(
            name='Optimization Strategy',
            options=['Markowitz', 'Risk Parity', 'Maximum Sharpe', 'Black-Litterman', 'HRP'],
            value='Markowitz',
            width=200
        )
        
        # Risk tolerance slider
        self.risk_tolerance = pn.widgets.FloatSlider(
            name='Risk Tolerance',
            start=0.1,
            end=2.0,
            value=1.0,
            step=0.1,
            width=200
        )
        
        # Action buttons
        self.optimize_button = pn.widgets.Button(
            name='📈 Optimize Portfolio',
            button_type='primary',
            width=150
        )
        
        self.rebalance_button = pn.widgets.Button(
            name='⚖️ Rebalance',
            button_type='success',
            width=150
        )
        
        self.refresh_data_button = pn.widgets.Button(
            name='🔄 Refresh Data',
            button_type='light',
            width=150
        )
        
        # Positions table
        self.positions_table = pn.widgets.Tabulator(
            self._create_positions_dataframe(data_manager),
            height=200,
            name='Current Positions'
        )
        
        # Order entry
        self.symbol_input = pn.widgets.TextInput(
            name='Symbol',
            placeholder='Enter symbol...',
            width=100
        )
        
        self.shares_input = pn.widgets.IntInput(
            name='Shares',
            start=1,
            width=100
        )
        
        self.price_input = pn.widgets.FloatInput(
            name='Price',
            start=0.01,
            width=100
        )
        
        self.order_button = pn.widgets.Button(
            name='📈 Place Order',
            button_type='primary',
            width=120
        )
    
    def _create_positions_dataframe(self, data_manager) -> pd.DataFrame:
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

