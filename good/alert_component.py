#!/usr/bin/env python3
"""
TradePulse UI Alert Component
Component for alerts and notifications
"""

import panel as pn
from datetime import datetime
from typing import Callable
from .base_component import BaseComponent
from .data_manager import DataManager

class AlertComponent(BaseComponent):
    """Component for alerts and notifications"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("AlertComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create alert components"""
        self.components['alerts_list'] = pn.pane.Markdown("### 🔔 Recent Alerts\n\n- No alerts at this time")
        
        self.components['alert_price_high'] = pn.widgets.FloatInput(
            name='High Alert Price',
            value=0.0,
            width=120
        )
        
        self.components['alert_price_low'] = pn.widgets.FloatInput(
            name='Low Alert Price',
            value=0.0,
            width=120
        )
        
        self.components['add_alert_button'] = pn.widgets.Button(
            name='Add Alert',
            button_type='warning',
            width=100
        )
    
    def get_layout(self):
        """Get the alert layout"""
        return pn.Column(
            pn.pane.Markdown("### 🔔 Alerts & Notifications"),
            self.components['alerts_list'],
            pn.pane.Markdown("#### Add Price Alert"),
            pn.Row(
                self.components['alert_price_high'],
                self.components['alert_price_low'],
                self.components['add_alert_button']
            )
        )
    
    def add_alert_message(self, message: str):
        """Add message to alerts list"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        new_alert = f"- {timestamp}: {message}"
        
        current_alerts = self.components['alerts_list'].object
        if "No alerts at this time" in current_alerts:
            updated_alerts = current_alerts.replace("No alerts at this time", new_alert)
        else:
            updated_alerts = current_alerts + f"\n{new_alert}"
        
        self.components['alerts_list'].object = updated_alerts
    
    def set_add_alert_callback(self, callback: Callable):
        """Set callback for add alert button"""
        self.components['add_alert_button'].on_click(callback)
