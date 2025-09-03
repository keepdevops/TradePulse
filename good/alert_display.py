#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Display
Handles alert display operations and updates
"""

import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertDisplay:
    """Handles alert display operations and updates"""
    
    def __init__(self, alert_manager, components: Dict):
        self.alert_manager = alert_manager
        self.components = components
    
    def update_alerts_display(self):
        """Update the alerts table display"""
        try:
            # Get alerts data from alert manager
            alerts_df = self.alert_manager.export_alerts_to_dataframe()
            self.components['alerts_table'].value = alerts_df
            
        except Exception as e:
            logger.error(f"Failed to update alerts display: {e}")
    
    def update_alert_statistics(self):
        """Update the alert statistics display"""
        try:
            stats = self.alert_manager.get_alert_statistics()
            
            stats_text = f"""
            **Alert Statistics:**
            - **Active Alerts**: {stats.get('active_alerts', 0)}
            - **Alerts Today**: {stats.get('alerts_today', 0)}
            - **Total Triggered**: {stats.get('triggered_alerts', 0)}
            - **Total Alerts**: {stats.get('total_alerts', 0)}
            """
            
            self.components['alert_stats'].object = stats_text
            
        except Exception as e:
            logger.error(f"Failed to update alert statistics: {e}")
    
    def update_alert_history(self, alert_type: str, message: str):
        """Update the alert history display"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            history_text = f"""
            ### 📋 Alert History
            
            **{timestamp}** - {alert_type}: {message}
            
            **Recent Activity:**
            - **{timestamp}**: {alert_type} - {message}
            - **Previous alerts would appear here**
            """
            
            self.components['alert_history'].object = history_text
            
        except Exception as e:
            logger.error(f"Failed to update alert history: {e}")
    
    def update_all_displays(self):
        """Update all alert displays"""
        try:
            self.update_alerts_display()
            self.update_alert_statistics()
        except Exception as e:
            logger.error(f"Failed to update all displays: {e}")
