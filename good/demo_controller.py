#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Controller
Handles demo system orchestration and control
"""

import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import threading
from typing import Dict, List, Optional, Any, Callable
import logging

# Import helper classes
from .demo_callbacks import DemoCallbacks
from .demo_operations_manager import DemoOperationsManager

logger = logging.getLogger(__name__)

class DemoController:
    """Handles demo system orchestration and control"""
    
    def __init__(self, data_generator, ui_components, chart_manager):
        self.data_generator = data_generator
        self.ui_components = ui_components
        self.chart_manager = chart_manager
        
        # Initialize helper classes
        self.demo_callbacks = DemoCallbacks(self, ui_components, chart_manager, data_generator)
        self.operations_manager = DemoOperationsManager(data_generator, ui_components, chart_manager)
        
        # Initialize controller
        self.setup_demo_controller()
    
    def setup_demo_controller(self):
        """Setup the demo controller"""
        try:
            logger.info("🔧 Setting up demo controller")
            
            # Setup UI callbacks
            self.demo_callbacks.setup_ui_callbacks()
            
            logger.info("✅ Demo controller setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup demo controller: {e}")
    
    # Callback methods moved to DemoCallbacks class
    
    def start_demo(self):
        """Start the demo system"""
        self.operations_manager.start_demo()
    
    def stop_demo(self):
        """Stop the demo system"""
        self.operations_manager.stop_demo()
    
    def reset_demo(self):
        """Reset the demo system"""
        self.operations_manager.reset_demo()
    
    def pause_demo(self):
        """Pause the demo system"""
        self.operations_manager.pause_demo()
    
    def resume_demo(self):
        """Resume the demo system"""
        self.operations_manager.resume_demo()
    
    def set_demo_interval(self, interval: float):
        """Set the demo update interval"""
        self.operations_manager.set_demo_interval(interval)
    
    def get_demo_status(self) -> Dict[str, Any]:
        """Get demo system status"""
        status = self.operations_manager.get_demo_status()
        status['callbacks_count'] = self.demo_callbacks.get_callbacks_count()
        return status
    
    def add_demo_callback(self, event_name: str, callback: Callable):
        """Add a custom demo callback"""
        self.demo_callbacks.add_demo_callback(event_name, callback)
    
    def remove_demo_callback(self, event_name: str, callback: Callable):
        """Remove a demo callback"""
        self.demo_callbacks.remove_demo_callback(event_name, callback)
    
    def get_demo_statistics(self) -> Dict[str, Any]:
        """Get comprehensive demo statistics"""
        try:
            # Get data generator statistics
            data_stats = self.data_generator.get_demo_statistics()
            
            # Get UI component statistics
            ui_stats = self.ui_components.get_component_status()
            
            # Get chart statistics
            chart_stats = self.chart_manager.get_chart_status()
            
            # Get demo controller statistics
            controller_stats = self.get_demo_status()
            
            # Combine all statistics
            combined_stats = {
                'data_generator': data_stats,
                'ui_components': ui_stats,
                'chart_manager': chart_stats,
                'demo_controller': controller_stats,
                'combined_timestamp': datetime.now()
            }
            
            return combined_stats
            
        except Exception as e:
            logger.error(f"Failed to get demo statistics: {e}")
            return {}
    
    def export_demo_state(self) -> Dict[str, Any]:
        """Export complete demo state"""
        try:
            export_data = {
                'data_generator': self.data_generator.export_demo_data(),
                'demo_controller': self.get_demo_status(),
                'export_timestamp': datetime.now().isoformat()
            }
            
            logger.info("📤 Demo state exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export demo state: {e}")
            return {}
    
    def import_demo_state(self, demo_state: Dict[str, Any]):
        """Import demo state from external source"""
        try:
            if 'data_generator' in demo_state:
                self.data_generator.import_demo_data(demo_state['data_generator'])
            
            logger.info("📥 Demo state imported")
            
        except Exception as e:
            logger.error(f"Failed to import demo state: {e}")
    
    def cleanup_demo_system(self):
        """Cleanup the demo system"""
        try:
            logger.info("🧹 Cleaning up demo system")
            
            # Cleanup operations manager
            self.operations_manager.cleanup_demo_system()
            
            # Clear callbacks
            self.demo_callbacks.clear_callbacks()
            
            logger.info("✅ Demo system cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup demo system: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.cleanup_demo_system()
        except Exception:
            pass
