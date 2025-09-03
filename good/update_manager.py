#!/usr/bin/env python3
"""
TradePulse Panel UI - Update Manager
Handles update operations and data flow
"""

import threading
import time
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class UpdateManager:
    """Handles update operations and data flow"""
    
    def __init__(self, control_panel, data_displays, chart_manager, header, data_manager):
        self.control_panel = control_panel
        self.data_displays = data_displays
        self.chart_manager = chart_manager
        self.header = header
        self.data_manager = data_manager
        
        self.update_interval = 5  # seconds
        self.data_update_thread = None
        self.stop_updates = False
    
    def start_data_updates(self):
        """Start the data update thread"""
        try:
            if self.data_update_thread is None or not self.data_update_thread.is_alive():
                self.stop_updates = False
                self.data_update_thread = threading.Thread(target=self._data_update_loop, daemon=True)
                self.data_update_thread.start()
                logger.info("✅ Data update thread started")
            
        except Exception as e:
            logger.error(f"Failed to start data updates: {e}")
    
    def stop_data_updates(self):
        """Stop the data update thread"""
        try:
            self.stop_updates = True
            if self.data_update_thread and self.data_update_thread.is_alive():
                self.data_update_thread.join(timeout=1)
                logger.info("✅ Data update thread stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop data updates: {e}")
    
    def _data_update_loop(self):
        """Main data update loop"""
        try:
            while not self.stop_updates:
                try:
                    # Update data for current symbol
                    current_symbol = self.control_panel.get_current_symbol()
                    if current_symbol:
                        self._update_data_for_symbol(current_symbol)
                        self._update_charts_for_symbol(current_symbol)
                    
                    # Update system status
                    self._update_system_status()
                    
                    # Wait for next update
                    time.sleep(self.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in data update loop: {e}")
                    time.sleep(self.update_interval)
                    
        except Exception as e:
            logger.error(f"Data update loop failed: {e}")
    
    def _update_data_for_symbol(self, symbol: str):
        """Update data displays for a specific symbol"""
        try:
            # Generate simulated data
            simulated_data = self.data_manager.generate_simulated_data(symbol)
            
            # Update data displays
            self.data_displays.update_price_data(
                simulated_data['price'],
                simulated_data['change'],
                simulated_data['change_percent']
            )
            
            self.data_displays.update_volume_data(simulated_data['volume'])
            
            self.data_displays.update_market_data(
                simulated_data['market_cap'],
                simulated_data['high_24h'],
                simulated_data['low_24h']
            )
            
            self.data_displays.update_summary_statistics(
                simulated_data['avg_volume'],
                simulated_data['high_52w'],
                simulated_data['low_52w'],
                simulated_data['pe_ratio']
            )
            
            logger.info(f"✅ Data updated for {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to update data for symbol: {e}")
    
    def _update_charts_for_symbol(self, symbol: str):
        """Update charts for a specific symbol"""
        try:
            # Generate simulated chart data
            chart_data = self.data_manager.generate_simulated_chart_data(symbol)
            
            # Update chart manager
            self.chart_manager.update_chart(chart_data, symbol)
            
            logger.info(f"✅ Charts updated for {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to update charts for symbol: {e}")
    
    def _update_system_status(self):
        """Update system status indicators"""
        try:
            # Generate system metrics
            system_metrics = self.data_manager.generate_system_metrics()
            
            # Update header system status
            self.header.update_system_status(
                system_metrics['cpu_usage'],
                system_metrics['memory_usage'],
                system_metrics['network_usage']
            )
            
        except Exception as e:
            logger.error(f"Failed to update system status: {e}")
    
    def set_update_interval(self, interval: float):
        """Set the update interval"""
        if interval > 0:
            self.update_interval = interval
            logger.info(f"⏱️ Update interval set to {interval} seconds")
    
    def get_update_status(self) -> Dict[str, Any]:
        """Get update status information"""
        return {
            'data_update_thread_active': self.data_update_thread.is_alive() if self.data_update_thread else False,
            'update_interval': self.update_interval,
            'stop_updates': self.stop_updates
        }
