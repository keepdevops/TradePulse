#!/usr/bin/env python3
"""
TradePulse UI Panels - Control Panel
Handles trading controls, symbol selection, and system settings
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .control_ui_components import ControlUIComponents
from .control_callbacks import ControlCallbacks
from .control_operations import ControlOperations

logger = logging.getLogger(__name__)

class ControlPanel:
    """Handles trading controls, symbol selection, and system settings"""
    
    def __init__(self):
        self.current_symbol = "AAPL"
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.timeframes = ['1m', '5m', '15m', '1h', '1d']
        self.current_timeframe = '1h'
        self.trading_active = False
        
        # Initialize components
        self.ui_components = ControlUIComponents()
        self.callbacks = ControlCallbacks()
        self.operations = ControlOperations()
        
        # Create control components
        self.symbol_selector = self.ui_components.create_symbol_selector(self.symbols, self.current_symbol)
        self.timeframe_selector = self.ui_components.create_timeframe_selector(self.timeframes, self.current_timeframe)
        self.trading_controls = self.ui_components.create_trading_controls(self.operations)
        self.status_indicator = self.ui_components.create_status_indicator()
        
        # Setup callbacks and connect components
        self.operations.set_status_indicator(self.status_indicator)
        self.operations.set_callbacks(self.callbacks)
        self.callbacks.setup_control_callbacks(self.symbol_selector, self.timeframe_selector, self.operations)
    
    def add_symbol_change_callback(self, callback: Callable):
        """Add callback for symbol change events"""
        self.callbacks.add_symbol_change_callback(callback)
    
    def add_timeframe_change_callback(self, callback: Callable):
        """Add callback for timeframe change events"""
        self.callbacks.add_timeframe_change_callback(callback)
    
    def add_trading_state_change_callback(self, callback: Callable):
        """Add callback for trading state change events"""
        self.callbacks.add_trading_state_change_callback(callback)
    
    def get_control_layout(self):
        """Get the complete control panel layout"""
        return self.ui_components.create_control_layout(self.symbol_selector, self.timeframe_selector, self.trading_controls, self.status_indicator)
    
    def get_current_symbol(self) -> str:
        """Get current selected symbol"""
        return self.current_symbol
    
    def get_current_timeframe(self) -> str:
        """Get current selected timeframe"""
        return self.current_timeframe
    
    def is_trading_active(self) -> bool:
        """Check if trading is currently active"""
        return self.trading_active
    
    def get_control_statistics(self) -> Dict[str, Any]:
        """Get control panel statistics"""
        return self.operations.get_control_statistics(self.current_symbol, self.current_timeframe, self.trading_active, self.symbols, self.timeframes, self.callbacks)
    
    def update_symbols_list(self, new_symbols: List[str]):
        """Update available symbols list"""
        try:
            self.symbols = new_symbols.copy()
            self.symbol_selector.options = new_symbols
            
            # Ensure current symbol is still valid
            if self.current_symbol not in new_symbols and new_symbols:
                self.current_symbol = new_symbols[0]
                self.symbol_selector.value = self.current_symbol
            
            logger.info(f"✅ Symbols list updated: {len(new_symbols)} symbols available")
            
        except Exception as e:
            logger.error(f"Failed to update symbols list: {e}")
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'symbol_selector': self.symbol_selector,
            'timeframe_selector': self.timeframe_selector,
            'trading_controls': self.trading_controls,
            'status_indicator': self.status_indicator
        }
