#!/usr/bin/env python3
"""
TradePulse Modular Panels - Alerts Panel (Refactored)
Enhanced alerts and notifications panel with dataset integration
Refactored to be under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .alerts.alerts_panel_core import AlertsPanelCore

logger = logging.getLogger(__name__)

class AlertsPanel(BasePanel):
    """Enhanced alerts and notifications panel with dataset integration"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Alerts", data_manager)
        # Use the refactored implementation
        self._refactored_panel = AlertsPanelCore(data_manager, data_access_manager)
    
    def init_panel(self):
        """Initialize enhanced alerts panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the alerts panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def create_alert_callback(self, event=None):
        """Callback for creating alerts"""
        # Delegate to refactored implementation
        self._refactored_panel.create_alert_callback(event)
    
    def test_alert_callback(self, event=None):
        """Callback for testing alerts"""
        # Delegate to refactored implementation
        self._refactored_panel.test_alert_callback(event)
    
    def clear_all_alerts_callback(self, event=None):
        """Callback for clearing all alerts"""
        # Delegate to refactored implementation
        self._refactored_panel.clear_all_alerts_callback(event)
    
    def simulate_alert_trigger(self, config):
        """Simulate alert trigger for testing"""
        # Delegate to refactored implementation
        self._refactored_panel.simulate_alert_trigger(config)
    
    def update_alerts_table(self):
        """Update the active alerts table"""
        # Delegate to refactored implementation
        self._refactored_panel.update_alerts_table()
    
    def update_alert_history(self):
        """Update the alert history display"""
        # Delegate to refactored implementation
        self._refactored_panel.update_alert_history()
    
    def get_panel_status(self):
        """Get panel status information"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel_status()

