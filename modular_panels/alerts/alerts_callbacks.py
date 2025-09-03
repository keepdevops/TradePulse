#!/usr/bin/env python3
"""
TradePulse Alerts Panel - Callbacks Manager
Callback management for the alerts panel
"""

import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AlertsCallbacks:
    """Callback management for alerts panel"""
    
    def __init__(self, core_panel):
        self.core_panel = core_panel
    
    def create_alert_callback(self, event=None):
        """Callback for creating alerts"""
        try:
            logger.info("🚨 Creating new alert")
            
            # Get alert configuration
            config = self.core_panel.alert_creator.get_alert_config()
            
            # Create alert
            alert = self.core_panel.alert_creator.create_alert_from_config(config)
            
            # Add to active alerts
            self.core_panel.active_alerts.append(alert)
            
            # Update alerts table
            self.core_panel.update_alerts_table()
            
            # Reset form
            self.core_panel.alert_creator.reset_form()
            
            logger.info(f"✅ Alert created successfully: {alert['id']}")
            
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
    
    def test_alert_callback(self, event=None):
        """Callback for testing alerts"""
        try:
            logger.info("🧪 Testing alert")
            
            # Get alert configuration
            config = self.core_panel.alert_creator.get_alert_config()
            
            # Validate config
            is_valid, errors = self.core_panel.alert_creator.validate_alert_config(config)
            
            if is_valid:
                # Simulate alert trigger
                self.simulate_alert_trigger(config)
                logger.info("✅ Alert test successful")
            else:
                logger.warning(f"⚠️ Alert validation failed: {', '.join(errors)}")
            
        except Exception as e:
            logger.error(f"Failed to test alert: {e}")
    
    def clear_all_alerts_callback(self, event=None):
        """Callback for clearing all alerts"""
        try:
            logger.info("🗑️ Clearing all alerts")
            
            # Clear active alerts
            self.core_panel.active_alerts.clear()
            
            # Clear alert history
            self.core_panel.alert_history.clear()
            
            # Update displays
            self.core_panel.update_alerts_table()
            self.core_panel.update_alert_history()
            
            logger.info("✅ All alerts cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear alerts: {e}")
    
    def simulate_alert_trigger(self, config: Dict[str, Any]):
        """Simulate alert trigger for testing"""
        try:
            # Create test alert trigger
            trigger = {
                'alert_id': f"test_{pd.Timestamp.now().strftime('%H%M%S')}",
                'type': config.get('alert_type', 'Test Alert'),
                'triggered_at': pd.Timestamp.now().isoformat(),
                'condition_met': True,
                'current_value': config.get('threshold_value', 100.0),
                'threshold': config.get('threshold_value', 100.0)
            }
            
            # Add to history
            self.core_panel.alert_history.append(trigger)
            
            # Update history display
            self.core_panel.update_alert_history()
            
            logger.info(f"✅ Alert trigger simulated: {trigger['alert_id']}")
            
        except Exception as e:
            logger.error(f"Failed to simulate alert trigger: {e}")



