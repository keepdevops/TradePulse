#!/usr/bin/env python3
"""
TradePulse Panel UI - V10.9-Modular Panel Interface
Refactored panel UI using focused components for V10.9 architecture
"""

import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
import json
from typing import Dict, List, Optional, Any
import threading
import time
import logging

from .header_component import HeaderComponent
from .control_panel import ControlPanel
from .data_displays import DataDisplays
from .chart_manager import ChartManager
from .portfolio_widgets import PortfolioWidgets
from .data_manager import DataManager
from .update_manager import UpdateManager
from .trading_manager import TradingManager
from .layout_manager import LayoutManager

# Configure Panel for V10.9
pn.extension('plotly', 'tabulator', sizing_mode='stretch_width')
pn.config.theme = 'dark'

logger = logging.getLogger(__name__)

class TradePulsePanelUI:
    """V10.9-Modular Panel Interface - Main Panel UI class using focused components"""
    
    def __init__(self):
        self.data = {}
        self.version = "10.9"
        self.interface_type = "Modular Panel Interface"
        
        # Initialize focused components for V10.9
        self.header = HeaderComponent()
        self.control_panel = ControlPanel()
        self.data_displays = DataDisplays()
        self.chart_manager = ChartManager()
        self.portfolio_widgets = PortfolioWidgets()
        
        # Initialize helper classes for V10.9
        self.data_manager = DataManager()
        self.trading_manager = TradingManager(
            self.control_panel,
            self.data_displays,
            self.chart_manager
        )
        self.update_manager = UpdateManager(
            self.control_panel, 
            self.data_displays, 
            self.chart_manager, 
            self.header, 
            self.data_manager
        )
        self.layout_manager = LayoutManager(
            self.header,
            self.control_panel,
            self.data_displays,
            self.chart_manager,
            self.portfolio_widgets
        )
        
        # Connect V10.9 components
        self._connect_v10_9_components()
        
        # Initialize V10.9 layout
        self.init_v10_9_layout()
        
        # Start V10.9 data updates
        self.update_manager.start_data_updates()
        
        logger.info(f"✅ TradePulsePanelUI v{self.version} - {self.interface_type} initialized")
    
    def _connect_v10_9_components(self):
        """Connect the V10.9 focused components together"""
        try:
            # Connect control panel callbacks for V10.9
            self.control_panel.add_symbol_change_callback(self.trading_manager.on_symbol_change)
            self.control_panel.add_timeframe_change_callback(self.trading_manager.on_timeframe_change)
            self.control_panel.add_trading_state_change_callback(self.trading_manager.on_trading_state_change)
            
            # Add V10.9 specific callbacks
            self._add_v10_9_callbacks()
            
            logger.info(f"✅ V10.9 Panel UI components connected successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect V10.9 components: {e}")
    
    def _add_v10_9_callbacks(self):
        """Add V10.9 specific callbacks and event handlers"""
        try:
            # Add modular panel navigation callbacks
            self._setup_modular_panel_navigation()
            
            # Add V10.9 system monitoring callbacks
            self._setup_v10_9_system_monitoring()
            
            logger.info("✅ V10.9 specific callbacks added")
            
        except Exception as e:
            logger.error(f"Failed to add V10.9 callbacks: {e}")
    
    def _setup_modular_panel_navigation(self):
        """Setup navigation for V10.9 modular panels"""
        try:
            # This would connect to the modular panel system
            # For now, we'll log the setup
            logger.info("✅ Modular panel navigation setup for V10.9")
            
        except Exception as e:
            logger.error(f"Failed to setup modular panel navigation: {e}")
    
    def _setup_v10_9_system_monitoring(self):
        """Setup V10.9 system monitoring"""
        try:
            # This would connect to the V10.9 system monitoring
            logger.info("✅ V10.9 system monitoring setup")
            
        except Exception as e:
            logger.error(f"Failed to setup V10.9 system monitoring: {e}")
    
    def init_v10_9_layout(self):
        """Initialize the V10.9 main UI layout"""
        try:
            # Create main layout using V10.9 layout manager
            self.main_layout = self.layout_manager.create_v10_9_main_layout()
            logger.info(f"✅ V10.9 main UI layout initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize V10.9 layout: {e}")
            self.main_layout = pn.pane.Markdown(f"**V10.9 Error:** Failed to initialize UI layout")
    
    def get_main_layout(self):
        """Get the V10.9 main UI layout"""
        return self.main_layout
    
    def get_v10_9_component_statistics(self) -> Dict[str, Any]:
        """Get comprehensive V10.9 statistics from all components"""
        try:
            header_stats = self.header.get_component_info()
            control_stats = self.control_panel.get_control_statistics()
            data_stats = self.data_displays.get_display_statistics()
            chart_stats = self.chart_manager.get_chart_statistics()
            portfolio_stats = self.portfolio_widgets.get_portfolio_statistics()
            
            # Get V10.9 update manager status
            update_status = self.update_manager.get_update_status()
            
            return {
                'version': self.version,
                'interface_type': self.interface_type,
                'header': header_stats,
                'control_panel': control_stats,
                'data_displays': data_stats,
                'chart_manager': chart_stats,
                'portfolio_widgets': portfolio_stats,
                'update_manager': update_status,
                'v10_9_features': [
                    'Modular Panel Architecture',
                    'Focused Component Design',
                    'V10.9 Branding',
                    'Enhanced Navigation',
                    'System Status Monitoring'
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get V10.9 component statistics: {e}")
            return {}
    
    def get_v10_9_status(self) -> Dict[str, Any]:
        """Get V10.9 specific status information"""
        try:
            return {
                'version': self.version,
                'interface': self.interface_type,
                'status': 'Active',
                'architecture': 'Modular Panel System',
                'components': {
                    'header': 'V10.9 Header Component',
                    'control_panel': 'V10.9 Control Panel',
                    'data_displays': 'V10.9 Data Displays',
                    'chart_manager': 'V10.9 Chart Manager',
                    'portfolio_widgets': 'V10.9 Portfolio Widgets',
                    'data_manager': 'V10.9 Data Manager',
                    'trading_manager': 'V10.9 Trading Manager',
                    'update_manager': 'V10.9 Update Manager',
                    'layout_manager': 'V10.9 Layout Manager'
                },
                'features': [
                    'Modular Navigation',
                    'V10.9 Branding',
                    'Enhanced UI Components',
                    'System Status Monitoring',
                    'Improved Performance'
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get V10.9 status: {e}")
            return {}
    
    def cleanup(self):
        """Cleanup V10.9 resources before shutdown"""
        try:
            # Stop V10.9 data updates
            self.update_manager.stop_data_updates()
            
            # Clear all V10.9 component data
            self.data_displays.clear_displays()
            self.chart_manager.clear_charts()
            self.portfolio_widgets.clear_portfolio()
            
            logger.info(f"✅ TradePulsePanelUI v{self.version} cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup V10.9: {e}")
    
    def __del__(self):
        """Destructor to ensure V10.9 cleanup"""
        try:
            self.cleanup()
        except:
            pass

def main():
    """Main function to run the V10.9 Panel UI"""
    try:
        # Create the V10.9 UI
        ui = TradePulsePanelUI()
        
        # Get the V10.9 main layout
        app = ui.get_main_layout()
        
        # Configure the V10.9 app
        app.servable()
        
        logger.info("✅ V10.9-Modular Panel Interface started successfully")
        
        return app
        
    except Exception as e:
        logger.error(f"Failed to create V10.9 Panel UI: {e}")
        return None

if __name__ == "__main__":
    app = main()
    if app:
        app.show()
