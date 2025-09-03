#!/usr/bin/env python3
"""
TradePulse UI Panels - Control Callbacks
Handles control panel callback operations and event handling
"""

import logging
from typing import Callable

logger = logging.getLogger(__name__)

class ControlCallbacks:
    """Handles control panel callback operations and event handling"""
    
    def __init__(self):
        self.on_symbol_change_callbacks = []
        self.on_timeframe_change_callbacks = []
        self.on_trading_state_change_callbacks = []
    
    def setup_control_callbacks(self, symbol_selector, timeframe_selector, operations):
        """Setup control component callbacks"""
        try:
            # Symbol change callback
            symbol_selector.param.watch(operations.on_symbol_change, 'value')
            
            # Timeframe change callback
            timeframe_selector.param.watch(operations.on_timeframe_change, 'value')
            
            logger.info("✅ Control panel callbacks setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup control callbacks: {e}")
    
    def add_symbol_change_callback(self, callback: Callable):
        """Add callback for symbol change events"""
        if callback not in self.on_symbol_change_callbacks:
            self.on_symbol_change_callbacks.append(callback)
            logger.info(f"✅ Added symbol change callback")
    
    def add_timeframe_change_callback(self, callback: Callable):
        """Add callback for timeframe change events"""
        if callback not in self.on_timeframe_change_callbacks:
            self.on_timeframe_change_callbacks.append(callback)
            logger.info(f"✅ Added timeframe change callback")
    
    def add_trading_state_change_callback(self, callback: Callable):
        """Add callback for trading state change events"""
        if callback not in self.on_trading_state_change_callbacks:
            self.on_trading_state_change_callbacks.append(callback)
            logger.info(f"✅ Added trading state change callback")
    
    def notify_symbol_change_callbacks(self, new_symbol: str, old_symbol: str):
        """Notify all symbol change callbacks"""
        try:
            for callback in self.on_symbol_change_callbacks:
                try:
                    callback(new_symbol, old_symbol)
                except Exception as e:
                    logger.error(f"Symbol change callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify symbol change callbacks: {e}")
    
    def notify_timeframe_change_callbacks(self, new_timeframe: str, old_timeframe: str):
        """Notify all timeframe change callbacks"""
        try:
            for callback in self.on_timeframe_change_callbacks:
                try:
                    callback(new_timeframe, old_timeframe)
                except Exception as e:
                    logger.error(f"Timeframe change callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify timeframe change callbacks: {e}")
    
    def notify_trading_state_change_callbacks(self, state: str, current_symbol: str, current_timeframe: str):
        """Notify all trading state change callbacks"""
        try:
            for callback in self.on_trading_state_change_callbacks:
                try:
                    callback(state, current_symbol, current_timeframe)
                except Exception as e:
                    logger.error(f"Trading state change callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify trading state change callbacks: {e}")
