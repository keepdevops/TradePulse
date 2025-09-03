#!/usr/bin/env python3
"""
TradePulse Demo Panels - Main Demo Panel UI
Main orchestrator for the refactored demo panel system
"""

import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import threading
from typing import Dict, List, Optional, Any
import logging

# Import demo panel components
from .demo_data_generator import DemoDataGenerator
from .demo_ui_components import DemoUIComponents
from .demo_chart_manager import DemoChartManager
from .demo_controller import DemoController
from .tab_creators import TabCreators
from .demo_operations import DemoOperations

logger = logging.getLogger(__name__)

class TradePulseDemo:
    """Refactored demo class to showcase Panel UI features"""
    
    def __init__(self):
        # Configure Panel
        pn.extension('plotly', 'tabulator', sizing_mode='stretch_width')
        pn.config.theme = 'dark'
        
        # Initialize demo components
        self.data_generator = DemoDataGenerator()
        self.ui_components = DemoUIComponents(self.data_generator)
        self.chart_manager = DemoChartManager(self.data_generator)
        self.demo_controller = DemoController(self.data_generator, self.ui_components, self.chart_manager)
        
        # Initialize helper classes
        self.tab_creators = TabCreators(self.ui_components, self.chart_manager, self.demo_controller, self.data_generator)
        self.demo_operations = DemoOperations(self.demo_controller, self.ui_components, self.chart_manager)
        
        # Initialize demo UI
        self.init_demo_ui()
    
    def init_demo_ui(self):
        """Initialize the demo UI system"""
        try:
            logger.info("🔧 Initializing refactored TradePulse demo UI")
            
            # Create main layout
            self.main_layout = self._create_main_layout()
            
            # Setup initial displays
            self._setup_initial_displays()
            
            logger.info("✅ Refactored TradePulse demo UI initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize demo UI: {e}")
    
    def _create_main_layout(self) -> pn.Column:
        """Create the main demo UI layout"""
        try:
            # Create tabbed interface
            tabs = pn.Tabs(
                ('Main Demo', self.tab_creators.create_main_demo_tab()),
                ('Charts', self.tab_creators.create_charts_tab()),
                ('Portfolio', self.tab_creators.create_portfolio_tab()),
                ('Trading', self.tab_creators.create_trading_tab()),
                ('Statistics', self.tab_creators.create_statistics_tab()),
                sizing_mode='stretch_width'
            )
            
            # Create main layout
            main_layout = pn.Column(
                self.ui_components.get_component('header'),
                pn.Spacer(height=20),
                tabs,
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return main_layout
            
        except Exception as e:
            logger.error(f"Failed to create main layout: {e}")
            return pn.Column("Error: Failed to create demo layout")
    
    # Tab creation methods moved to TabCreators class
    
    # Charts tab creation moved to TabCreators class
    
    # Portfolio tab creation moved to TabCreators class
    
    # Trading tab creation moved to TabCreators class
    
    # Statistics tab creation moved to TabCreators class
    
    def _setup_initial_displays(self):
        """Setup initial display values"""
        self.demo_operations.setup_initial_displays()
    
    def get_layout(self) -> pn.Column:
        """Get the complete demo UI layout"""
        try:
            return self.main_layout
        except Exception as e:
            logger.error(f"Failed to get layout: {e}")
            return pn.Column("Error: Failed to get demo layout")
    
    def start_demo(self):
        """Start the demo system"""
        self.demo_operations.start_demo()
    
    def stop_demo(self):
        """Stop the demo system"""
        self.demo_operations.stop_demo()
    
    def reset_demo(self):
        """Reset the demo system"""
        self.demo_operations.reset_demo()
    
    def refresh_demo(self):
        """Refresh the demo system"""
        self.demo_operations.refresh_demo()
        self._setup_initial_displays()
    
    def get_demo_status(self) -> Dict[str, Any]:
        """Get comprehensive demo status"""
        status = self.demo_operations.get_demo_status()
        status['data_generator'] = self.data_generator.get_demo_statistics()
        return status
    
    def test_demo_system(self) -> Dict[str, bool]:
        """Test the demo system functionality"""
        test_results = self.demo_operations.test_demo_system()
        
        # Test data generator
        try:
            data_stats = self.data_generator.get_demo_statistics()
            test_results['data_generator'] = bool(data_stats)
        except Exception:
            test_results['data_generator'] = False
        
        # Overall test result
        test_results['overall'] = all(test_results.values())
        return test_results
    
    def export_demo_data(self) -> Dict[str, Any]:
        """Export demo data"""
        return self.demo_operations.export_demo_data(self.data_generator)
    
    def import_demo_data(self, demo_data: Dict[str, Any]):
        """Import demo data"""
        self.demo_operations.import_demo_data(demo_data, self.data_generator)
        self.refresh_demo()
    
    def cleanup_demo_system(self):
        """Cleanup the demo system"""
        self.demo_operations.cleanup_demo_system()
    
    def get_app(self):
        """Get the Panel app for launching"""
        return self.main_layout
    
    def show(self):
        """Show the demo UI"""
        if hasattr(self, 'main_layout'):
            self.main_layout.show()
        else:
            logger.error("No main layout available to show")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.cleanup_demo_system()
        except Exception:
            pass
