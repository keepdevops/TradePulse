#!/usr/bin/env python3
"""
TradePulse Panel UI - Data Update Logic
Data update and synchronization logic
"""

import threading
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DataUpdater:
    """Handles data updates and synchronization"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
        self.update_interval = 5  # seconds
        self.is_running = False
    
    def update_price_data(self):
        """Update price data for all symbols"""
        for symbol in self.data_manager.symbols:
            if symbol in self.data_manager.price_data:
                df = self.data_manager.price_data[symbol]
                last_price = df.iloc[-1]['Close']
                new_price = last_price + np.random.normal(0, 1)
                
                # Update the last row
                df.iloc[-1, df.columns.get_loc('Close')] = new_price
                df.iloc[-1, df.columns.get_loc('High')] = max(df.iloc[-1]['High'], new_price)
                df.iloc[-1, df.columns.get_loc('Low')] = min(df.iloc[-1]['Low'], new_price)
                
                # Update portfolio positions
                if symbol in self.data_manager.portfolio_data['positions']:
                    self.data_manager.portfolio_data['positions'][symbol]['current_price'] = new_price
    
    def update_ml_predictions(self):
        """Update ML predictions"""
        for symbol in self.data_manager.symbols:
            if symbol in self.data_manager.ml_predictions:
                for model in self.data_manager.ml_predictions[symbol]:
                    self.data_manager.ml_predictions[symbol][model] = np.random.normal(0, 1, len(self.data_manager.ml_predictions[symbol][model]))
    
    def update_displays(self):
        """Update all displays"""
        current_symbol = self.components['control'].get_current_symbol()
        
        # Update current symbol display
        if current_symbol in self.data_manager.price_data:
            self.components['data_display'].update_price_display(current_symbol)
            self.components['chart'].update_charts(current_symbol)
        
        # Update portfolio display
        self.components['portfolio'].update_portfolio_display()
    
    def run_integrated_updates(self):
        """Run integrated updates with all TradePulse features"""
        while self.is_running:
            try:
                self.update_price_data()
                self.update_displays()
                self.update_ml_predictions()
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in integrated updates: {e}")
                time.sleep(self.update_interval)
    
    def start_updates(self):
        """Start periodic updates"""
        def update_loop():
            while True:
                try:
                    self.update_displays()
                    time.sleep(self.update_interval)
                except Exception as e:
                    logger.error(f"❌ Error in update loop: {e}")
                    time.sleep(self.update_interval)
        
        threading.Thread(target=update_loop, daemon=True).start()
    
    def start_trading_updates(self):
        """Start trading updates"""
        self.is_running = True
        threading.Thread(target=self.run_integrated_updates, daemon=True).start()
    
    def stop_trading_updates(self):
        """Stop trading updates"""
        self.is_running = False
