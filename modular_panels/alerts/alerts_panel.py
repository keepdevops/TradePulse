#!/usr/bin/env python3
"""
TradePulse Alerts - Main Panel
Refactored alerts panel using focused components
"""

import panel as pn
import pandas as pd
from typing import Dict
import logging

from .. import BasePanel
from ..dataset_selector_component import DatasetSelectorComponent
from .alert_manager import AlertManager
from .alert_conditions import AlertConditionChecker
from .alert_notifications import AlertNotificationSystem
from .alert_operations import AlertOperations
from .alert_display import AlertDisplay
from .alert_callbacks import AlertCallbacks
from .alert_layout import AlertLayout

logger = logging.getLogger(__name__)

class AlertsPanel(BasePanel):
    """Refactored alerts panel using focused components"""
    
    def __init__(self, data_manager):
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'alerts')
        self.alert_manager = AlertManager()
        self.condition_checker = AlertConditionChecker()
        self.notification_system = AlertNotificationSystem()
        
        # Initialize alert operations
        self.alert_operations = AlertOperations(
            self.alert_manager,
            self.condition_checker,
            self.notification_system,
            self.dataset_selector
        )
        
        # Initialize alert display
        self.alert_display = AlertDisplay(self.alert_manager, {})
        
        # Initialize alert callbacks
        self.alert_callbacks = AlertCallbacks(self.alert_operations, self.alert_display, self.alert_manager)
        
        # Initialize alert layout
        self.alert_layout = AlertLayout({}, self.dataset_selector)
        
        super().__init__("Alerts", data_manager)
    
    def init_panel(self):
        """Initialize refactored alerts panel components"""
        self._init_ui_components()
        self._setup_callbacks()
        
        # Update alert display with components
        self.alert_display.components = self.components
        
        # Update alert layout with components
        self.alert_layout.components = self.components
    
    def _init_ui_components(self):
        """Initialize UI components"""
        # Alert type selector
        self.components['alert_type'] = pn.widgets.Select(
            name='Alert Type',
            options=self.condition_checker.get_supported_conditions(),
            value='Price Alert',
            width=200
        )
        
        # Alert conditions
        self.components['condition_operator'] = pn.widgets.Select(
            name='Condition',
            options=['Above', 'Below', 'Crosses Above', 'Crosses Below', 'Changes By'],
            value='Above',
            width=150
        )
        
        self.components['threshold_value'] = pn.widgets.FloatInput(
            name='Threshold',
            start=0.01,
            value=100.0,
            width=150
        )
        
        self.components['percentage_change'] = pn.widgets.FloatInput(
            name='% Change',
            start=0.1,
            value=5.0,
            width=150
        )
        
        # Alert settings
        self.components['alert_enabled'] = pn.widgets.Checkbox(
            name='Enable Alert',
            value=True,
            width=120
        )
        
        self.components['notification_type'] = pn.widgets.MultiChoice(
            name='Notifications',
            options=self.notification_system.supported_channels,
            value=['Email', 'Push'],
            width=200
        )
        
        # Action buttons
        self.components['create_alert'] = pn.widgets.Button(
            name='🚨 Create Alert',
            button_type='danger',
            width=150
        )
        
        self.components['test_alert'] = pn.widgets.Button(
            name='🧪 Test Alert',
            button_type='warning',
            width=150
        )
        
        self.components['clear_alerts'] = pn.widgets.Button(
            name='🗑️ Clear All',
            button_type='light',
            width=150
        )
        
        # Active alerts table
        self.components['alerts_table'] = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Active Alerts'
        )
        
        # Alert history
        self.components['alert_history'] = pn.pane.Markdown("""
        ### 📋 Alert History
        No alerts triggered yet
        """)
        
        # Alert statistics
        self.components['alert_stats'] = pn.pane.Markdown("""
        **Alert Statistics:**
        - **Active Alerts**: 0
        - **Alerts Today**: 0
        - **Total Triggered**: 0
        """)
    
    def _setup_callbacks(self):
        """Setup component callbacks"""
        self.components['create_alert'].on_click(self.alert_callbacks.create_alert)
        self.components['test_alert'].on_click(self.alert_callbacks.test_alert)
        self.components['clear_alerts'].on_click(self.alert_callbacks.clear_alerts)
        
        # Dataset selector callback
        self.dataset_selector.add_dataset_change_callback(self.on_dataset_change)
    
    def get_panel(self):
        """Get the refactored alerts panel layout"""
        return self.alert_layout.create_panel_layout()
    

    
    def _get_alert_config_from_ui(self) -> Dict:
        """Get alert configuration from UI components"""
        return self.alert_operations.get_alert_config_from_ui(self.components)
    

    
    def monitor_datasets_for_alerts(self):
        """Monitor active datasets for alert conditions"""
        try:
            # Use alert operations to monitor datasets
            self.alert_operations.monitor_datasets_for_alerts()
            
            # Update displays after monitoring
            self.alert_display.update_all_displays()
            
        except Exception as e:
            logger.error(f"Failed to monitor datasets for alerts: {e}")
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for alert operations"""
        # Use alert operations to handle dataset changes
        self.alert_operations.handle_dataset_change(change_type, dataset_id)
        
        # Update displays after handling change
        self.alert_display.update_all_displays()
