#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Update Manager
Manages UI updates and data refresh cycles
"""

import time
from datetime import datetime
from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

class UpdateManager:
    """Manages UI updates and data refresh cycles"""
    
    def __init__(self, ui_components: Dict[str, Any], update_interval: int = 5):
        self.ui_components = ui_components
        self.update_interval = update_interval
        self.is_running = False
        self.update_callbacks = {}
        self.component_states = {}
        
        # Setup update system
        self.setup_update_system()
    
    def setup_update_system(self):
        """Setup the update system and callbacks"""
        try:
            logger.info("🔧 Setting up update system")
            
            # Initialize component states
            self.component_states = {
                'trading_active': False,
                'trading_paused': False,
                'last_update': None,
                'update_count': 0
            }
            
            # Setup update callbacks
            self.setup_update_callbacks()
            
            logger.info("✅ Update system setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup update system: {e}")
    
    def setup_update_callbacks(self):
        """Setup update callbacks for components"""
        try:
            from .update_callbacks import UpdateCallbacks
            callbacks = UpdateCallbacks(self)
            callbacks.setup_callbacks()
            
            logger.info("✅ Update callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup update callbacks: {e}")
    
    def start_trading(self, event=None):
        """Start trading operations"""
        try:
            from .trading_manager import TradingManager
            manager = TradingManager(self)
            manager.start_trading()
            
        except Exception as e:
            logger.error(f"Failed to start trading: {e}")
    
    def stop_trading(self, event=None):
        """Stop trading operations"""
        try:
            from .trading_manager import TradingManager
            manager = TradingManager(self)
            manager.stop_trading()
            
        except Exception as e:
            logger.error(f"Failed to stop trading: {e}")
    
    def pause_trading(self, event=None):
        """Pause trading operations"""
        try:
            from .trading_manager import TradingManager
            manager = TradingManager(self)
            manager.pause_trading()
            
        except Exception as e:
            logger.error(f"Failed to pause trading: {e}")
    
    def on_symbol_change(self, event):
        """Handle symbol change events"""
        try:
            from .symbol_manager import SymbolManager
            manager = SymbolManager(self)
            manager.handle_symbol_change(event)
            
        except Exception as e:
            logger.error(f"Failed to handle symbol change: {e}")
    
    def on_timeframe_change(self, event):
        """Handle timeframe change events"""
        try:
            from .timeframe_manager import TimeframeManager
            manager = TimeframeManager(self)
            manager.handle_timeframe_change(event)
            
        except Exception as e:
            logger.error(f"Failed to handle timeframe change: {e}")
    
    def start_updates(self):
        """Start the update system"""
        try:
            if not self.is_running:
                self.is_running = True
                logger.info("🔄 Starting update system")
                
                # Start update loop
                self._update_loop()
            
        except Exception as e:
            logger.error(f"Failed to start updates: {e}")
    
    def stop_updates(self):
        """Stop the update system"""
        try:
            self.is_running = False
            logger.info("🛑 Stopping update system")
            
        except Exception as e:
            logger.error(f"Failed to stop updates: {e}")
    
    def _update_loop(self):
        """Main update loop"""
        try:
            while self.is_running:
                # Update displays
                self._update_data_displays()
                self._update_chart()
                self._update_portfolio()
                
                # Update component states
                self.component_states['last_update'] = datetime.now()
                self.component_states['update_count'] += 1
                
                # Wait for next update
                time.sleep(self.update_interval)
                
        except Exception as e:
            logger.error(f"Update loop failed: {e}")
            self.is_running = False
    
    def _update_data_displays(self):
        """Update data display components"""
        try:
            from .display_updater import DisplayUpdater
            updater = DisplayUpdater(self)
            updater.update_data_displays()
            
        except Exception as e:
            logger.error(f"Failed to update data displays: {e}")
    
    def _update_chart(self):
        """Update chart components"""
        try:
            from .chart_updater import ChartUpdater
            updater = ChartUpdater(self)
            updater.update_chart()
            
        except Exception as e:
            logger.error(f"Failed to update chart: {e}")
    
    def _update_portfolio(self):
        """Update portfolio components"""
        try:
            from .portfolio_updater import PortfolioUpdater
            updater = PortfolioUpdater(self)
            updater.update_portfolio()
            
        except Exception as e:
            logger.error(f"Failed to update portfolio: {e}")
    
    def get_update_status(self) -> Dict[str, Any]:
        """Get update system status"""
        try:
            return {
                'trading_active': self.component_states.get('trading_active', False),
                'trading_paused': self.component_states.get('trading_paused', False),
                'is_running': self.is_running,
                'current_symbol': self.component_states.get('current_symbol', 'Unknown'),
                'current_timeframe': self.component_states.get('current_timeframe', 'Unknown'),
                'update_interval': self.update_interval,
                'last_update': self.component_states.get('last_update'),
                'update_count': self.component_states.get('update_count', 0)
            }
        except Exception as e:
            logger.error(f"Failed to get update status: {e}")
            return {}
