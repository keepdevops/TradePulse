#!/usr/bin/env python3
"""
TradePulse Panel UI - Event Handler Coordinator
Main event handler that coordinates all event types
"""

import logging
from typing import Dict, Any

from .event_handlers import TradingEventHandler, PortfolioEventHandler, MLEventHandler, AlertEventHandler
from .data_updater import DataUpdater

logger = logging.getLogger(__name__)

class EventHandler:
    """Main event handler that coordinates all event types"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
        
        # Initialize specialized event handlers
        self.trading_handler = TradingEventHandler(data_manager, components)
        self.portfolio_handler = PortfolioEventHandler(data_manager, components)
        self.ml_handler = MLEventHandler(data_manager, components)
        self.alert_handler = AlertEventHandler(data_manager, components)
        
        # Initialize data updater
        self.data_updater = DataUpdater(data_manager, components)
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        self.trading_handler.on_symbol_change(event)
    
    def start_trading(self, event):
        """Start trading session"""
        self.trading_handler.start_trading(event)
        self.data_updater.start_trading_updates()
    
    def stop_trading(self, event):
        """Stop trading session"""
        self.trading_handler.stop_trading(event)
        self.data_updater.stop_trading_updates()
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using selected strategy"""
        self.portfolio_handler.optimize_portfolio(event)
    
    def generate_prediction(self, event):
        """Generate ML prediction"""
        self.ml_handler.generate_prediction(event)
    
    def place_order(self, event):
        """Place trading order"""
        self.portfolio_handler.place_order(event)
    
    def add_alert(self, event):
        """Add price alert"""
        self.alert_handler.add_alert(event)
    
    def start_updates(self):
        """Start periodic updates"""
        self.data_updater.start_updates()
