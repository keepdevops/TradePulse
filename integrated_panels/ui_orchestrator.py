#!/usr/bin/env python3
"""
TradePulse Integrated Panels - UI Orchestrator
Manages UI component orchestration and layout management
"""

import panel as pn
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .ui_components import UIComponents
from .layout_manager import LayoutManager
from .update_manager import UpdateManager

logger = logging.getLogger(__name__)

class UIOrchestrator:
    """Manages UI component orchestration and layout management"""
    
    def __init__(self):
        self.update_interval = 5  # seconds
        
        # Initialize components
        self.ui_components_manager = UIComponents()
        self.ui_components = self.ui_components_manager.get_all_components()
        
        # Initialize managers
        self.layout_manager = LayoutManager(self.ui_components)
        self.update_manager = UpdateManager(self.ui_components, self.update_interval)
        
        # Setup orchestrator
        self.setup_orchestrator()
    
    def setup_orchestrator(self):
        """Setup the orchestrator"""
        try:
            logger.info("🔧 Setting up UI Orchestrator")
            
            # Setup component callbacks
            self.setup_component_callbacks()
            
            # Setup export functionality
            self.setup_export_functionality()
            
            logger.info("✅ UI Orchestrator setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup orchestrator: {e}")
    
    def setup_component_callbacks(self):
        """Setup component callbacks"""
        try:
            # Setup export button callback
            if 'export_button' in self.ui_components:
                self.ui_components['export_button'].on_click(self.export_data)
            
            # Setup settings button callback
            if 'settings_button' in self.ui_components:
                self.ui_components['settings_button'].on_click(self.open_settings)
            
            logger.info("✅ Component callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup component callbacks: {e}")
    
    def setup_export_functionality(self):
        """Setup export functionality"""
        try:
            from .export_manager import ExportManager
            self.export_manager = ExportManager()
            
            logger.info("✅ Export functionality setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup export functionality: {e}")
    
    def export_data(self, event=None):
        """Export current data"""
        try:
            logger.info("📤 Exporting data")
            
            # Use export manager
            self.export_manager.export_data(self.ui_components)
            
            logger.info("✅ Data export complete")
            
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
    
    def open_settings(self, event=None):
        """Open settings panel"""
        try:
            logger.info("⚙️ Opening settings")
            
            # Placeholder for settings functionality
            logger.info("Settings panel would open here")
            
        except Exception as e:
            logger.error(f"Failed to open settings: {e}")
    
    def get_layout(self) -> pn.Column:
        """Get the complete UI layout"""
        try:
            return self.layout_manager.get_layout()
        except Exception as e:
            logger.error(f"Failed to get layout: {e}")
            return pn.Column("Error: Failed to create layout")
    
    def start_updates(self):
        """Start the update system"""
        try:
            self.update_manager.start_updates()
        except Exception as e:
            logger.error(f"Failed to start updates: {e}")
    
    def stop_updates(self):
        """Stop the update system"""
        try:
            self.update_manager.stop_updates()
        except Exception as e:
            logger.error(f"Failed to stop updates: {e}")
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status information"""
        try:
            update_status = self.update_manager.get_update_status()
            
            return {
                **update_status,
                'components_count': len(self.ui_components),
                'sections_count': len(self.layout_manager.get_layout_sections()),
                'orchestrator_type': 'UI Orchestrator'
            }
        except Exception as e:
            logger.error(f"Failed to get orchestrator status: {e}")
            return {}
    
    def refresh_components(self):
        """Refresh all UI components"""
        try:
            logger.info("🔄 Refreshing UI components")
            
            # Trigger update manager refresh
            self.update_manager._update_data_displays()
            self.update_manager._update_chart()
            self.update_manager._update_portfolio()
            
            logger.info("✅ UI components refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh components: {e}")
    
    def get_component_info(self) -> Dict[str, Any]:
        """Get information about all components"""
        try:
            component_info = {}
            
            for name, component in self.ui_components.items():
                component_info[name] = {
                    'type': type(component).__name__,
                    'has_value': hasattr(component, 'value'),
                    'has_object': hasattr(component, 'object'),
                    'has_name': hasattr(component, 'name')
                }
            
            return component_info
            
        except Exception as e:
            logger.error(f"Failed to get component info: {e}")
            return {}
