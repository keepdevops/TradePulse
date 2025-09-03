#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Layout
Handles alert panel layout creation
"""

import panel as pn
from typing import Dict

class AlertLayout:
    """Handles alert panel layout creation"""
    
    def __init__(self, components: Dict, dataset_selector):
        self.components = components
        self.dataset_selector = dataset_selector
    
    def create_panel_layout(self):
        """Create the refactored alerts panel layout"""
        # Alert creation
        alert_creation = pn.Column(
            pn.pane.Markdown("### 🚨 Alert Creation"),
            pn.Row(
                self.components['alert_type'],
                self.components['condition_operator'],
                align='center'
            ),
            pn.Row(
                self.components['threshold_value'],
                self.components['percentage_change'],
                align='center'
            ),
            pn.Row(
                self.components['alert_enabled'],
                self.components['notification_type'],
                align='center'
            ),
            pn.Row(
                self.components['create_alert'],
                self.components['test_alert'],
                self.components['clear_alerts'],
                align='center'
            ),
            sizing_mode='stretch_width'
        )
        
        # Alerts management
        alerts_management = pn.Column(
            pn.pane.Markdown("### 📊 Alerts Management"),
            self.components['alerts_table'],
            self.components['alert_history'],
            self.components['alert_stats'],
            sizing_mode='stretch_width'
        )
        
        # Dataset selector
        dataset_section = self.dataset_selector.get_component()
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('🚨 Create Alerts', alert_creation),
            ('📊 Manage Alerts', alerts_management),
            ('📁 Data Sources', dataset_section),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 🚨 Enhanced Alert Management"),
            pn.pane.Markdown("Create intelligent alerts based on uploaded data and market conditions"),
            tabs,
            sizing_mode='stretch_width'
        )
