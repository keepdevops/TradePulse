#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Callbacks
Handles alert callback operations and event handling
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class AlertCallbacks:
    """Handles alert callback operations and event handling"""
    
    def __init__(self, alert_operations, alert_display, alert_manager):
        self.alert_operations = alert_operations
        self.alert_display = alert_display
        self.alert_manager = alert_manager
    
    def create_alert(self, event):
        """Create a new alert using the alert manager"""
        try:
            # Get alert configuration from UI
            alert_config = self.alert_operations.get_alert_config_from_ui(self.alert_display.components)
            
            # Create alert using alert operations
            alert_id = self.alert_operations.create_alert(alert_config)
            
            if alert_id:
                # Update displays
                self.alert_display.update_all_displays()
                
        except Exception as e:
            logger.error(f"❌ Alert creation failed: {e}")
    
    def test_alert(self, event):
        """Test the alert system using the notification system"""
        try:
            # Test alert using alert operations
            success = self.alert_operations.test_alert()
            
            if success:
                # Update alert history
                self.alert_display.update_alert_history("Test Alert", "System test completed successfully")
                
        except Exception as e:
            logger.error(f"❌ Alert test failed: {e}")
    
    def clear_alerts(self, event):
        """Clear all active alerts using the alert manager"""
        try:
            logger.info("🗑️ Clearing all alerts...")
            
            # Clear alerts using alert manager
            cleared_count = self.alert_manager.clear_all_alerts()
            
            # Update displays
            self.alert_display.update_all_displays()
            
            logger.info(f"✅ {cleared_count} alerts cleared successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to clear alerts: {e}")
