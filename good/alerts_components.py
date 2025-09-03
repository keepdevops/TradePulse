#!/usr/bin/env python3
"""
TradePulse Alerts Panel - Components
UI components for the alerts panel
"""

import panel as pn
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class AlertsComponents:
    """UI components for alerts panel"""
    
    def __init__(self):
        self.clear_alerts = None
        self.alerts_table = None
        self.alert_history = None
    
    def create_basic_components(self, creator_components):
        """Create basic UI components"""
        # Additional components
        self.clear_alerts = pn.widgets.Button(
            name='🗑️ Clear All',
            button_type='light',
            width=150
        )
        
        # Active alerts table
        self.alerts_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Active Alerts'
        )
        
        # Alert history
        self.alert_history = pn.pane.Markdown("""
        ### 📋 Alert History
        No alerts triggered yet
        """)
        
        # Store creator components as attributes for easy access
        for key, component in creator_components.items():
            setattr(self, key, component)

