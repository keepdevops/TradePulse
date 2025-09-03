#!/usr/bin/env python3
"""
TradePulse UI Control Component
Component for trading controls
"""

import panel as pn
from typing import Callable
from .base_component import BaseComponent
from .data_manager import DataManager

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
