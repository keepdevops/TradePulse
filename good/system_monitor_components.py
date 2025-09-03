#!/usr/bin/env python3
"""
TradePulse System Monitor - Components
UI components for the system monitor
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class SystemMonitorComponents:
    """UI components for system monitor"""
    
    def __init__(self):
        self.start_monitoring_button = None
        self.stop_monitoring_button = None
        self.refresh_status_button = None
        self.monitoring_status = None
        self.health_display = None
        self.alerts_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Monitoring control buttons
        self.start_monitoring_button = pn.widgets.Button(
            name='🔄 Start Monitoring',
            button_type='success',
            width=150
        )
        
        self.stop_monitoring_button = pn.widgets.Button(
            name='⏹️ Stop Monitoring',
            button_type='danger',
            width=150
        )
        
        self.refresh_status_button = pn.widgets.Button(
            name='📊 Refresh Status',
            button_type='primary',
            width=150
        )
        
        # Status displays
        self.monitoring_status = pn.pane.Markdown("""
        ### 📊 Monitoring Status
        - **Status**: Inactive
        - **Last Check**: Never
        - **Active Alerts**: 0
        """)
        
        self.health_display = pn.pane.Markdown("""
        ### 🏥 System Health
        - **Overall Health**: Unknown
        - **Components**: 0 checked
        - **Issues**: 0 found
        """)
        
        self.alerts_display = pn.pane.Markdown("""
        ### 🚨 System Alerts
        No active alerts
        """)

