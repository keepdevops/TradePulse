#!/usr/bin/env python3
"""
TradePulse Alerts Panel - Core Functionality
Core alerts panel class with basic functionality
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict, Any

from .. import BasePanel
from .alerts_components import AlertsComponents
from .alerts_operations import AlertsOperations
from .alerts_management import AlertsManagement
from .alerts_callbacks import AlertsCallbacks
from ..dataset_selector_component import DatasetSelectorComponent
from .alert_creator import AlertCreator
from ui_components.module_data_access import ModuleDataAccess

logger = logging.getLogger(__name__)

class AlertsPanelCore(BasePanel):
    """Core alerts panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Alerts", data_manager)
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'alerts')
        self.alert_creator = AlertCreator()
        self.data_access = ModuleDataAccess(data_manager, data_access_manager, 'alerts')
        
        # Initialize components
        self.components = AlertsComponents()
        self.operations = AlertsOperations()
        self.management = AlertsManagement()
        self.callbacks = AlertsCallbacks(self)
        
        # Initialize alerts storage
        self.active_alerts = []
        self.alert_history = []
        
        self.init_panel()
        self.setup_callbacks()
    
    def init_panel(self):
        """Initialize core panel components"""
        try:
            # Get alert creation components
            creator_components = self.alert_creator.get_components()
            self.components.create_basic_components(creator_components)
            
            logger.info("✅ Alerts panel components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize alerts panel: {e}")
    
    def setup_callbacks(self):
        """Setup component callbacks"""
        try:
            # Setup alert creator callbacks
            self.alert_creator.setup_callbacks(
                create_callback=self.callbacks.create_alert_callback,
                test_callback=self.callbacks.test_alert_callback
            )
            
            # Setup additional callbacks
            if hasattr(self.components, 'clear_alerts'):
                self.components.clear_alerts.on_click(self.callbacks.clear_all_alerts_callback)
            
            logger.info("✅ Alerts panel callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup alerts panel callbacks: {e}")
    
    def get_panel(self):
        """Get the alerts panel layout"""
        return self.management.create_panel_layout(
            self.dataset_selector,
            self.alert_creator,
            self.components
        )
    
    def create_alert_callback(self, event=None):
        """Callback for creating alerts"""
        return self.callbacks.create_alert_callback(event)
    
    def test_alert_callback(self, event=None):
        """Callback for testing alerts"""
        return self.callbacks.test_alert_callback(event)
    
    def clear_all_alerts_callback(self, event=None):
        """Callback for clearing all alerts"""
        return self.callbacks.clear_all_alerts_callback(event)
    
    def simulate_alert_trigger(self, config: Dict[str, Any]):
        """Simulate alert trigger for testing"""
        return self.callbacks.simulate_alert_trigger(config)
    
    def update_alerts_table(self):
        """Update the active alerts table"""
        try:
            if not self.active_alerts:
                # Create empty DataFrame
                df = pd.DataFrame(columns=[
                    'ID', 'Type', 'Condition', 'Status', 'Created', 'Triggered'
                ])
            else:
                # Convert alerts to DataFrame
                data = []
                for alert in self.active_alerts:
                    data.append({
                        'ID': alert['id'],
                        'Type': alert['type'],
                        'Condition': f"{alert['condition']['operator']} {alert['condition']['threshold']}",
                        'Status': alert['status'],
                        'Created': alert['created_at'][:10],  # Date only
                        'Triggered': alert['triggered_count']
                    })
                
                df = pd.DataFrame(data)
            
            # Update table
            if hasattr(self.components, 'alerts_table'):
                self.components.alerts_table.value = df
            
        except Exception as e:
            logger.error(f"Failed to update alerts table: {e}")
    
    def update_alert_history(self):
        """Update the alert history display"""
        try:
            if not self.alert_history:
                history_text = """
                ### 📋 Alert History
                No alerts triggered yet
                """
            else:
                # Create history text
                history_lines = ["### 📋 Alert History"]
                
                for trigger in self.alert_history[-10:]:  # Show last 10
                    history_lines.append(
                        f"- **{trigger['type']}** triggered at {trigger['triggered_at'][:16]} "
                        f"(Value: {trigger['current_value']:.2f})"
                    )
                
                history_text = "\n".join(history_lines)
            
            # Update history display
            if hasattr(self.components, 'alert_history'):
                self.components.alert_history.object = history_text
            
        except Exception as e:
            logger.error(f"Failed to update alert history: {e}")
    
    def get_panel_status(self) -> Dict[str, Any]:
        """Get panel status information"""
        try:
            return {
                'active_alerts_count': len(self.active_alerts),
                'alert_history_count': len(self.alert_history),
                'dataset_selector_active': self.dataset_selector.is_active(),
                'panel_type': 'Alerts Panel'
            }
            
        except Exception as e:
            logger.error(f"Failed to get panel status: {e}")
            return {}
