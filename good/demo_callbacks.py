#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Callbacks
Handles demo callback functionality
"""

from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

class DemoCallbacks:
    """Handles demo callback functionality"""
    
    def __init__(self, demo_controller, ui_components, chart_manager, data_generator):
        self.demo_controller = demo_controller
        self.ui_components = ui_components
        self.chart_manager = chart_manager
        self.data_generator = data_generator
        self.demo_callbacks = {}
        
        # Setup demo callbacks
        self._setup_demo_callbacks()
    
    def _setup_demo_callbacks(self):
        """Setup demo-specific callbacks"""
        try:
            # Demo start callback
            self.demo_callbacks['demo_start'] = self._on_demo_start
            
            # Demo stop callback
            self.demo_callbacks['demo_stop'] = self._on_demo_stop
            
            # Demo reset callback
            self.demo_callbacks['demo_reset'] = self._on_demo_reset
            
            # Symbol change callback
            self.demo_callbacks['symbol_change'] = self._on_symbol_change
            
            # Trade executed callback
            self.demo_callbacks['trade_executed'] = self._on_trade_executed
            
            # Data export callback
            self.demo_callbacks['data_export'] = self._on_data_export
            
        except Exception as e:
            logger.error(f"Failed to setup demo callbacks: {e}")
    
    def _on_demo_start(self):
        """Handle demo start event"""
        try:
            logger.info("🚀 Demo start event received")
            
            # Start demo loop
            self.demo_controller.start_demo()
            
        except Exception as e:
            logger.error(f"Failed to handle demo start: {e}")
    
    def _on_demo_stop(self):
        """Handle demo stop event"""
        try:
            logger.info("⏸ Demo stop event received")
            
            # Stop demo loop
            self.demo_controller.stop_demo()
            
        except Exception as e:
            logger.error(f"Failed to handle demo stop: {e}")
    
    def _on_demo_reset(self):
        """Handle demo reset event"""
        try:
            logger.info("🔄 Demo reset event received")
            
            # Reset demo data
            self.demo_controller.reset_demo()
            
        except Exception as e:
            logger.error(f"Failed to handle demo reset: {e}")
    
    def _on_symbol_change(self, new_symbol: str):
        """Handle symbol change event"""
        try:
            logger.info(f"🔄 Symbol change event received: {new_symbol}")
            
            # Update charts for new symbol
            self.chart_manager.update_charts(new_symbol)
            
            # Update UI displays
            self.ui_components._update_price_displays(new_symbol)
            
        except Exception as e:
            logger.error(f"Failed to handle symbol change: {e}")
    
    def _on_trade_executed(self, trade_data: Dict[str, Any]):
        """Handle trade execution event"""
        try:
            logger.info(f"📈 Trade execution event received: {trade_data}")
            
            # Update portfolio displays
            self.ui_components._update_portfolio_displays()
            
            # Update trading displays
            self.ui_components._update_trading_displays()
            
            # Update charts
            self.chart_manager.update_charts()
            
        except Exception as e:
            logger.error(f"Failed to handle trade execution: {e}")
    
    def _on_data_export(self, export_data: Dict[str, Any]):
        """Handle data export event"""
        try:
            logger.info(f"📤 Data export event received: {len(export_data)} sections")
            
            # Log export details
            logger.info(f"📊 Export completed: {len(export_data)} data sections exported")
            
        except Exception as e:
            logger.error(f"Failed to handle data export: {e}")
    
    def setup_ui_callbacks(self):
        """Setup UI component callbacks"""
        try:
            # Register callbacks with UI components
            for event_name, callback in self.demo_callbacks.items():
                self.ui_components.add_callback(event_name, callback)
            
            logger.info("✅ UI callbacks registered")
            
        except Exception as e:
            logger.error(f"Failed to setup UI callbacks: {e}")
    
    def add_demo_callback(self, event_name: str, callback: Callable):
        """Add a custom demo callback"""
        try:
            if event_name not in self.demo_callbacks:
                self.demo_callbacks[event_name] = []
            
            if callback not in self.demo_callbacks[event_name]:
                self.demo_callbacks[event_name].append(callback)
                
                # Register with UI components if it's a new event
                self.ui_components.add_callback(event_name, callback)
                
                logger.info(f"✅ Added custom demo callback for {event_name}")
            
        except Exception as e:
            logger.error(f"Failed to add demo callback: {e}")
    
    def remove_demo_callback(self, event_name: str, callback: Callable):
        """Remove a demo callback"""
        try:
            if event_name in self.demo_callbacks:
                if callback in self.demo_callbacks[event_name]:
                    self.demo_callbacks[event_name].remove(callback)
                    logger.info(f"✅ Removed demo callback for {event_name}")
                
                # Remove from UI components if no more callbacks for this event
                if not self.demo_callbacks[event_name]:
                    del self.demo_callbacks[event_name]
            
        except Exception as e:
            logger.error(f"Failed to remove demo callback: {e}")
    
    def get_callbacks_count(self) -> int:
        """Get the number of registered callbacks"""
        return len(self.demo_callbacks)
    
    def clear_callbacks(self):
        """Clear all callbacks"""
        try:
            self.demo_callbacks.clear()
            logger.info("✅ All demo callbacks cleared")
        except Exception as e:
            logger.error(f"Failed to clear callbacks: {e}")
