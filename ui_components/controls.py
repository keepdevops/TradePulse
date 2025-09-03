#!/usr/bin/env python3
"""
TradePulse Panel UI - Control Components
Trading control and data display components
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Callable
import logging

from .base import BaseComponent, DataManager

logger = logging.getLogger(__name__)

class ControlComponent(BaseComponent):
    """Component for trading controls"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("ControlComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create control components"""
        self.components['symbol_selector'] = pn.widgets.Select(
            name='Symbol',
            options=self.data_manager.symbols,
            value='AAPL',
            width=150
        )
        
        self.components['timeframe_selector'] = pn.widgets.Select(
            name='Timeframe',
            options=['1m', '5m', '15m', '1h', '1d'],
            value='1h',
            width=100
        )
        
        self.components['start_button'] = pn.widgets.Button(
            name='▶ Start Trading',
            button_type='success',
            width=120
        )
        
        self.components['stop_button'] = pn.widgets.Button(
            name='⏹ Stop Trading',
            button_type='danger',
            width=120
        )
        
        self.components['status_indicator'] = pn.indicators.LoadingSpinner(
            value=False,
            color='success',
            size=20
        )
    
    def get_layout(self):
        """Get the control layout"""
        return pn.Row(
            self.components['symbol_selector'],
            self.components['timeframe_selector'],
            self.components['start_button'],
            self.components['stop_button'],
            self.components['status_indicator'],
            align='center'
        )
    
    def set_symbol_change_callback(self, callback: Callable):
        """Set callback for symbol change"""
        self.components['symbol_selector'].param.watch(callback, 'value')
    
    def set_start_callback(self, callback: Callable):
        """Set callback for start button"""
        self.components['start_button'].on_click(callback)
    
    def set_stop_callback(self, callback: Callable):
        """Set callback for stop button"""
        self.components['stop_button'].on_click(callback)
    
    def get_current_symbol(self) -> str:
        """Get current selected symbol"""
        return self.components['symbol_selector'].value
    
    def set_trading_status(self, is_running: bool):
        """Set trading status"""
        self.components['status_indicator'].value = is_running
        self.components['start_button'].disabled = is_running
        self.components['stop_button'].disabled = not is_running

class DataDisplayComponent(BaseComponent):
    """Component for displaying data"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("DataDisplayComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create data display components"""
        self.components['price_display'] = pn.pane.Markdown("**Current Price:** $0.00")
        self.components['change_display'] = pn.pane.Markdown("**Change:** +0.00%")
        self.components['volume_display'] = pn.pane.Markdown("**Volume:** 0")
        self.components['market_cap_display'] = pn.pane.Markdown("**Market Cap:** $0.00B")
    
    def get_layout(self):
        """Get the data display layout"""
        return pn.Row(
            self.components['price_display'],
            self.components['change_display'],
            self.components['volume_display'],
            self.components['market_cap_display'],
            align='center'
        )
    
    def update_price_display(self, symbol: str):
        """Update price display for a symbol"""
        df = self.data_manager.get_price_data(symbol)
        if df.empty:
            return
        
        latest = df.iloc[-1]
        
        current_price = latest['Close']
        prev_price = df.iloc[-2]['Close'] if len(df) > 1 else current_price
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
        volume = latest['Volume']
        market_cap = current_price * np.random.randint(1000000000, 10000000000)
        
        self.components['price_display'].object = f"**Current Price:** ${current_price:.2f}"
        self.components['change_display'].object = f"**Change:** {change:+.2f} ({change_pct:+.2f}%)"
        self.components['volume_display'].object = f"**Volume:** {volume:,}"
        self.components['market_cap_display'].object = f"**Market Cap:** ${market_cap/1e9:.2f}B"
