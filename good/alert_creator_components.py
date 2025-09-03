#!/usr/bin/env python3
"""
TradePulse Alert Creator - Components
UI components for the alert creator
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class AlertCreatorComponents:
    """UI components for alert creator"""
    
    def __init__(self):
        self.alert_type = None
        self.condition_operator = None
        self.threshold_value = None
        self.percentage_change = None
        self.alert_enabled = None
        self.notification_type = None
        self.create_alert = None
        self.test_alert = None
        self.status_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Alert type selector
        self.alert_type = pn.widgets.Select(
            name='Alert Type',
            options=['Price Alert', 'Volume Alert', 'Technical Indicator', 'Custom Condition', 'Pattern Recognition'],
            value='Price Alert',
            width=200
        )
        
        # Condition operator
        self.condition_operator = pn.widgets.Select(
            name='Condition',
            options=['Above', 'Below', 'Crosses Above', 'Crosses Below', 'Changes By'],
            value='Above',
            width=150
        )
        
        # Threshold value
        self.threshold_value = pn.widgets.FloatInput(
            name='Threshold',
            start=0.01,
            value=100.0,
            width=150
        )
        
        # Percentage change
        self.percentage_change = pn.widgets.FloatInput(
            name='% Change',
            start=0.1,
            value=5.0,
            width=150
        )
        
        # Alert enabled
        self.alert_enabled = pn.widgets.Checkbox(
            name='Enable Alert',
            value=True,
            width=120
        )
        
        # Notification type
        self.notification_type = pn.widgets.MultiChoice(
            name='Notifications',
            options=['Email', 'SMS', 'Push', 'Sound', 'Desktop'],
            value=['Email', 'Push'],
            width=200
        )
        
        # Action buttons
        self.create_alert = pn.widgets.Button(
            name='🚨 Create Alert',
            button_type='danger',
            width=150
        )
        
        self.test_alert = pn.widgets.Button(
            name='🧪 Test Alert',
            button_type='warning',
            width=150
        )
        
        # Status display
        self.status_display = pn.pane.Markdown("""
        ### 📊 Alert Status
        **Status**: Ready to create alerts
        """)
    
    def create_alert_type_section(self):
        """Create alert type section"""
        return pn.Column(
            pn.pane.Markdown("### 🚨 Alert Type"),
            self.alert_type,
            sizing_mode='stretch_width'
        )
    
    def create_condition_section(self):
        """Create condition section"""
        return pn.Column(
            pn.pane.Markdown("### ⚙️ Alert Conditions"),
            pn.Row(
                self.condition_operator,
                self.threshold_value,
                self.percentage_change,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_settings_section(self):
        """Create settings section"""
        return pn.Column(
            pn.pane.Markdown("### 🔔 Alert Settings"),
            pn.Row(
                self.alert_enabled,
                self.notification_type,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_actions_section(self):
        """Create actions section"""
        return pn.Column(
            pn.pane.Markdown("### 🎯 Actions"),
            pn.Row(
                self.create_alert,
                self.test_alert,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_alert_form(self):
        """Create complete alert form"""
        return pn.Column(
            self.create_alert_type_section(),
            pn.Spacer(height=20),
            self.create_condition_section(),
            pn.Spacer(height=20),
            self.create_settings_section(),
            pn.Spacer(height=20),
            self.create_actions_section(),
            pn.Spacer(height=20),
            self.status_display,
            sizing_mode='stretch_width',
            margin=(10, 0)
        )
    
    def update_status_display(self, status: str, message: str = ""):
        """Update status display"""
        if self.status_display:
            self.status_display.object = f"""
            ### 📊 Alert Status
            **Status**: {status}
            {f"**Message**: {message}" if message else ""}
            """
    
    def update_button_states(self, can_create: bool, can_test: bool):
        """Update button enabled/disabled states"""
        if self.create_alert:
            self.create_alert.disabled = not can_create
        
        if self.test_alert:
            self.test_alert.disabled = not can_test

