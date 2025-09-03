#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Operations
Handles alert operations and management
"""

import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertOperations:
    """Handles alert operations and management"""
    
    def __init__(self, alert_manager, condition_checker, notification_system, dataset_selector):
        self.alert_manager = alert_manager
        self.condition_checker = condition_checker
        self.notification_system = notification_system
        self.dataset_selector = dataset_selector
    
    def create_alert(self, alert_config: Dict) -> str:
        """Create a new alert using the alert manager"""
        try:
            # Validate alert configuration
            is_valid, errors = self.condition_checker.validate_alert_config(alert_config)
            
            if not is_valid:
                logger.error(f"❌ Invalid alert configuration: {errors}")
                return None
            
            # Get active datasets for alert monitoring
            active_datasets = self.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"🚨 Creating {alert_config['type']} alert with {len(active_datasets)} active datasets")
                
                # Add datasets to alert config
                alert_config['datasets'] = list(active_datasets.keys())
                
                # Create alert using alert manager
                alert_id = self.alert_manager.create_alert(alert_config)
                
                logger.info(f"✅ Alert created successfully: {alert_id}")
                return alert_id
            else:
                logger.info("⚠️ No active datasets - alert will use default data")
                return None
                
        except Exception as e:
            logger.error(f"❌ Alert creation failed: {e}")
            return None
    
    def test_alert(self):
        """Test the alert system using the notification system"""
        try:
            logger.info("🧪 Testing alert system...")
            
            # Get active datasets for testing
            active_datasets = self.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"📊 Testing alerts with {len(active_datasets)} active datasets")
                
                # Test notifications on uploaded data
                for dataset_id, data in active_datasets.items():
                    logger.info(f"📊 Testing alerts on dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                    
                    # Test notification system
                    test_alert = {
                        'id': 'test_alert',
                        'type': 'Test Alert',
                        'notifications': ['Email', 'Push']
                    }
                    
                    test_trigger_info = {
                        'comparison': 'Test condition met',
                        'current_price': 100.0,
                        'threshold': 95.0
                    }
                    
                    self.notification_system.send_notification(test_alert, test_trigger_info)
                
                logger.info("✅ Alert test completed successfully")
                return True
            else:
                logger.info("⚠️ No active datasets - testing with default data")
                return False
                
        except Exception as e:
            logger.error(f"❌ Alert test failed: {e}")
            return False
    
    def clear_alerts(self) -> int:
        """Clear all active alerts using the alert manager"""
        try:
            logger.info("🗑️ Clearing all alerts...")
            
            # Clear alerts using alert manager
            cleared_count = self.alert_manager.clear_all_alerts()
            
            logger.info(f"✅ {cleared_count} alerts cleared successfully")
            return cleared_count
            
        except Exception as e:
            logger.error(f"❌ Failed to clear alerts: {e}")
            return 0
    
    def monitor_datasets_for_alerts(self):
        """Monitor active datasets for alert conditions"""
        try:
            active_datasets = self.dataset_selector.get_active_datasets()
            active_alerts = self.alert_manager.get_active_alerts()
            
            if not active_datasets or not active_alerts:
                return
            
            logger.info(f"🔍 Monitoring {len(active_datasets)} datasets for {len(active_alerts)} alerts")
            
            for alert in active_alerts:
                if not alert['enabled'] or alert['triggered']:
                    continue
                
                # Check each dataset for alert conditions
                for dataset_id, data in active_datasets.items():
                    if dataset_id in alert['datasets']:
                        triggered, trigger_info = self.condition_checker.check_alert_condition(alert, data)
                        
                        if triggered:
                            self._trigger_alert(alert, dataset_id, trigger_info)
                            
        except Exception as e:
            logger.error(f"Failed to monitor datasets for alerts: {e}")
    
    def _trigger_alert(self, alert: Dict, dataset_id: str, trigger_info: Dict):
        """Trigger an alert using the notification system"""
        try:
            logger.info(f"🚨 ALERT TRIGGERED: {alert['id']} - {alert['type']}")
            
            # Mark alert as triggered using alert manager
            self.alert_manager.update_alert(alert['id'], {
                'triggered': True,
                'triggered_time': datetime.now()
            })
            
            # Send notification using notification system
            self.notification_system.send_notification(alert, trigger_info)
            
            logger.info(f"✅ Alert {alert['id']} triggered and processed")
            return True
            
        except Exception as e:
            logger.error(f"Failed to trigger alert: {e}")
            return False
    
    def handle_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for alert operations"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for alerts module")
        
        if change_type == 'activated':
            logger.info(f"✅ Dataset {dataset_id} activated for alert monitoring")
            self.monitor_datasets_for_alerts()
        elif change_type == 'deactivated':
            logger.info(f"❌ Dataset {dataset_id} deactivated for alert monitoring")
            alerts_for_dataset = self.alert_manager.get_alerts_for_dataset(dataset_id)
            for alert in alerts_for_dataset:
                if dataset_id in alert['datasets']:
                    alert['datasets'].remove(dataset_id)
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics from alert manager"""
        try:
            return self.alert_manager.get_alert_statistics()
        except Exception as e:
            logger.error(f"Failed to get alert statistics: {e}")
            return {}
    
    def export_alerts_to_dataframe(self) -> pd.DataFrame:
        """Export alerts to dataframe from alert manager"""
        try:
            return self.alert_manager.export_alerts_to_dataframe()
        except Exception as e:
            logger.error(f"Failed to export alerts to dataframe: {e}")
            return pd.DataFrame()
    
    def get_alert_config_from_ui(self, components: Dict) -> Dict:
        """Get alert configuration from UI components"""
        return {
            'type': components['alert_type'].value,
            'condition': components['condition_operator'].value,
            'threshold': components['threshold_value'].value,
            'percentage': components['percentage_change'].value,
            'enabled': components['alert_enabled'].value,
            'notifications': components['notification_type'].value,
            'description': f"Alert created via UI at {datetime.now()}"
        }
