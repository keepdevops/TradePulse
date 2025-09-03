#!/usr/bin/env python3
"""
TradePulse UI Panels - Control Operations
Handles control panel operations and trading state management
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ControlOperations:
    """Handles control panel operations and trading state management"""
    
    def __init__(self):
        self.current_symbol = "AAPL"
        self.current_timeframe = '1h'
        self.trading_active = False
        self.status_indicator = None
        self.callbacks = None
    
    def set_status_indicator(self, status_indicator):
        """Set the status indicator reference"""
        self.status_indicator = status_indicator
    
    def set_callbacks(self, callbacks):
        """Set the callbacks reference"""
        self.callbacks = callbacks
    
    def on_symbol_change(self, event):
        """Handle symbol selection change"""
        try:
            new_symbol = event.new
            old_symbol = event.old
            
            logger.info(f"🔄 Symbol changed: {old_symbol} → {new_symbol}")
            
            # Update current symbol
            self.current_symbol = new_symbol
            
            # Notify callbacks
            if self.callbacks:
                self.callbacks.notify_symbol_change_callbacks(new_symbol, old_symbol)
            
        except Exception as e:
            logger.error(f"Failed to handle symbol change: {e}")
    
    def on_timeframe_change(self, event):
        """Handle timeframe selection change"""
        try:
            new_timeframe = event.new
            old_timeframe = event.old
            
            logger.info(f"🔄 Timeframe changed: {old_timeframe} → {new_timeframe}")
            
            # Update current timeframe
            self.current_timeframe = new_timeframe
            
            # Notify callbacks
            if self.callbacks:
                self.callbacks.notify_timeframe_change_callbacks(new_timeframe, old_timeframe)
            
        except Exception as e:
            logger.error(f"Failed to handle timeframe change: {e}")
    
    def start_trading(self, event):
        """Start trading operations"""
        try:
            if self.trading_active:
                logger.warning("⚠️ Trading is already active")
                return
            
            self.trading_active = True
            if self.status_indicator:
                self.status_indicator.value = True
                self.status_indicator.color = 'success'
            
            logger.info(f"🚀 Trading started for {self.current_symbol} ({self.current_timeframe})")
            
            # Notify callbacks
            if self.callbacks:
                self.callbacks.notify_trading_state_change_callbacks('started', self.current_symbol, self.current_timeframe)
            
        except Exception as e:
            logger.error(f"Failed to start trading: {e}")
    
    def stop_trading(self, event):
        """Stop trading operations"""
        try:
            if not self.trading_active:
                logger.warning("⚠️ Trading is not active")
                return
            
            self.trading_active = False
            if self.status_indicator:
                self.status_indicator.value = False
                self.status_indicator.color = 'danger'
            
            logger.info(f"⏹ Trading stopped for {self.current_symbol}")
            
            # Notify callbacks
            if self.callbacks:
                self.callbacks.notify_trading_state_change_callbacks('stopped', self.current_symbol, self.current_timeframe)
            
        except Exception as e:
            logger.error(f"Failed to stop trading: {e}")
    
    def pause_trading(self, event):
        """Pause trading operations"""
        try:
            if not self.trading_active:
                logger.warning("⚠️ Trading is not active")
                return
            
            if self.status_indicator:
                self.status_indicator.color = 'warning'
            
            logger.info(f"⏸ Trading paused for {self.current_symbol}")
            
            # Notify callbacks
            if self.callbacks:
                self.callbacks.notify_trading_state_change_callbacks('paused', self.current_symbol, self.current_timeframe)
            
        except Exception as e:
            logger.error(f"Failed to pause trading: {e}")
    
    def get_control_statistics(self, current_symbol: str, current_timeframe: str, trading_active: bool, symbols: List[str], timeframes: List[str], callbacks) -> Dict[str, Any]:
        """Get control panel statistics"""
        try:
            return {
                'current_symbol': current_symbol,
                'current_timeframe': current_timeframe,
                'trading_active': trading_active,
                'available_symbols': len(symbols),
                'available_timeframes': len(timeframes),
                'symbol_change_callbacks': len(callbacks.on_symbol_change_callbacks) if callbacks else 0,
                'timeframe_change_callbacks': len(callbacks.on_timeframe_change_callbacks) if callbacks else 0,
                'trading_state_callbacks': len(callbacks.on_trading_state_change_callbacks) if callbacks else 0
            }
        except Exception as e:
            logger.error(f"Failed to get control statistics: {e}")
            return {}
