#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Operations Manager
Handles demo operations and management
"""

import threading
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DemoOperationsManager:
    """Handles demo operations and management"""
    
    def __init__(self, data_generator, ui_components, chart_manager):
        self.data_generator = data_generator
        self.ui_components = ui_components
        self.chart_manager = chart_manager
        
        # Demo state
        self.is_running = False
        self.demo_interval = 2  # seconds
        self.demo_thread = None
    
    def start_demo(self):
        """Start the demo system"""
        try:
            if not self.is_running:
                self.is_running = True
                logger.info("🚀 Starting demo system")
                
                # Start demo thread
                self.demo_thread = threading.Thread(target=self._demo_loop, daemon=True)
                self.demo_thread.start()
                
                logger.info("✅ Demo system started")
            else:
                logger.info("⚠️ Demo system already running")
                
        except Exception as e:
            logger.error(f"Failed to start demo: {e}")
    
    def stop_demo(self):
        """Stop the demo system"""
        try:
            if self.is_running:
                self.is_running = False
                logger.info("⏸ Stopping demo system")
                
                # Wait for demo thread to finish
                if self.demo_thread and self.demo_thread.is_alive():
                    self.demo_thread.join(timeout=1.0)
                
                logger.info("✅ Demo system stopped")
            else:
                logger.info("⚠️ Demo system not running")
                
        except Exception as e:
            logger.error(f"Failed to stop demo: {e}")
    
    def _demo_loop(self):
        """Main demo loop"""
        try:
            logger.info("🔄 Demo loop started")
            
            while self.is_running:
                try:
                    # Update demo data
                    self._update_demo_data()
                    
                    # Update UI displays
                    self._update_ui_displays()
                    
                    # Update charts
                    self._update_charts()
                    
                    # Wait for next update
                    time.sleep(self.demo_interval)
                    
                except Exception as e:
                    logger.error(f"Demo loop iteration failed: {e}")
                    time.sleep(self.demo_interval)
            
            logger.info("🛑 Demo loop stopped")
            
        except Exception as e:
            logger.error(f"Demo loop failed: {e}")
            self.is_running = False
    
    def _update_demo_data(self):
        """Update demo data"""
        try:
            # Update portfolio values
            self.data_generator.update_portfolio_value()
            
            # Add some random trading activity
            if np.random.random() < 0.1:  # 10% chance per update
                self._generate_random_trade()
            
        except Exception as e:
            logger.error(f"Failed to update demo data: {e}")
    
    def _generate_random_trade(self):
        """Generate a random trade for demo purposes"""
        try:
            # Select random symbol
            symbol = np.random.choice(self.data_generator.symbols)
            
            # Select random action
            action = np.random.choice(['BUY', 'SELL'])
            
            # Generate random quantity and price
            quantity = np.random.randint(50, 500)
            current_price = self.data_generator.get_current_price(symbol)
            price = current_price * (0.95 + np.random.random() * 0.1) if current_price else 100.0
            
            # Create trade data
            trade_data = {
                'symbol': symbol,
                'action': action,
                'quantity': quantity,
                'price': price
            }
            
            # Execute trade
            self.data_generator.add_trade(trade_data)
            
            logger.debug(f"🎲 Random trade generated: {action} {quantity} {symbol} @ {price:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to generate random trade: {e}")
    
    def _update_ui_displays(self):
        """Update UI displays"""
        try:
            # Update all UI displays
            self.ui_components._update_all_displays()
            
        except Exception as e:
            logger.error(f"Failed to update UI displays: {e}")
    
    def _update_charts(self):
        """Update charts"""
        try:
            # Update all charts
            self.chart_manager.update_charts()
            
        except Exception as e:
            logger.error(f"Failed to update charts: {e}")
    
    def reset_demo(self):
        """Reset the demo system"""
        try:
            logger.info("🔄 Resetting demo system")
            
            # Stop demo if running
            if self.is_running:
                self.stop_demo()
            
            # Reset data generator
            self.data_generator.reset_demo_data()
            
            # Refresh UI components
            self.ui_components.refresh_components()
            
            # Refresh charts
            self.chart_manager.refresh_charts()
            
            logger.info("✅ Demo system reset completed")
            
        except Exception as e:
            logger.error(f"Failed to reset demo: {e}")
    
    def pause_demo(self):
        """Pause the demo system"""
        try:
            if self.is_running:
                logger.info("⏸ Pausing demo system")
                self.stop_demo()
            else:
                logger.info("⚠️ Demo system not running")
                
        except Exception as e:
            logger.error(f"Failed to pause demo: {e}")
    
    def resume_demo(self):
        """Resume the demo system"""
        try:
            if not self.is_running:
                logger.info("▶ Resuming demo system")
                self.start_demo()
            else:
                logger.info("⚠️ Demo system already running")
                
        except Exception as e:
            logger.error(f"Failed to resume demo: {e}")
    
    def set_demo_interval(self, interval: float):
        """Set the demo update interval"""
        try:
            if interval > 0:
                self.demo_interval = interval
                logger.info(f"⏱️ Demo interval set to {interval} seconds")
            else:
                logger.warning("⚠️ Invalid demo interval, must be positive")
                
        except Exception as e:
            logger.error(f"Failed to set demo interval: {e}")
    
    def get_demo_status(self) -> Dict[str, Any]:
        """Get demo system status"""
        try:
            return {
                'is_running': self.is_running,
                'demo_interval': self.demo_interval,
                'demo_thread_alive': self.demo_thread.is_alive() if self.demo_thread else False,
                'last_update': datetime.now()
            }
        except Exception as e:
            logger.error(f"Failed to get demo status: {e}")
            return {}
    
    def cleanup_demo_system(self):
        """Cleanup the demo system"""
        try:
            logger.info("🧹 Cleaning up demo system")
            
            # Stop demo if running
            if self.is_running:
                self.stop_demo()
            
            logger.info("✅ Demo system cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup demo system: {e}")
