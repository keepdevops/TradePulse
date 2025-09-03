#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Manager
Manages alert creation, storage, and lifecycle
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AlertManager:
    """Manages alert creation, storage, and lifecycle"""
    
    def __init__(self):
        self.alerts = []
        self.alert_counter = 0
    
    def create_alert(self, alert_config: Dict) -> str:
        """Create a new alert with the given configuration"""
        try:
            self.alert_counter += 1
            alert_id = f"alert_{self.alert_counter}"
            
            alert = {
                'id': alert_id,
                'type': alert_config.get('type', 'Price Alert'),
                'condition': alert_config.get('condition', 'Above'),
                'threshold': alert_config.get('threshold', 100.0),
                'percentage': alert_config.get('percentage', 5.0),
                'enabled': alert_config.get('enabled', True),
                'notifications': alert_config.get('notifications', ['Email']),
                'datasets': alert_config.get('datasets', []),
                'created': pd.Timestamp.now(),
                'triggered': False,
                'triggered_time': None,
                'description': alert_config.get('description', '')
            }
            
            self.alerts.append(alert)
            logger.info(f"✅ Alert created successfully: {alert_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"❌ Alert creation failed: {e}")
            raise
    
    def get_alert(self, alert_id: str) -> Optional[Dict]:
        """Get alert by ID"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                return alert
        return None
    
    def update_alert(self, alert_id: str, updates: Dict) -> bool:
        """Update an existing alert"""
        try:
            alert = self.get_alert(alert_id)
            if alert:
                alert.update(updates)
                logger.info(f"✅ Alert {alert_id} updated successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to update alert {alert_id}: {e}")
            return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """Delete an alert"""
        try:
            for i, alert in enumerate(self.alerts):
                if alert['id'] == alert_id:
                    del self.alerts[i]
                    logger.info(f"✅ Alert {alert_id} deleted successfully")
                    return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to delete alert {alert_id}: {e}")
            return False
    
    def clear_all_alerts(self) -> int:
        """Clear all alerts and return count of cleared alerts"""
        try:
            count = len(self.alerts)
            self.alerts.clear()
            logger.info(f"🗑️ Cleared {count} alerts successfully")
            return count
        except Exception as e:
            logger.error(f"❌ Failed to clear alerts: {e}")
            return 0
    
    def get_alerts_for_dataset(self, dataset_id: str) -> List[Dict]:
        """Get all alerts that monitor a specific dataset"""
        return [alert for alert in self.alerts if dataset_id in alert['datasets']]
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all enabled alerts"""
        return [alert for alert in self.alerts if alert['enabled']]
    
    def get_triggered_alerts(self) -> List[Dict]:
        """Get all triggered alerts"""
        return [alert for alert in self.alerts if alert['triggered']]
    
    def get_alerts_by_type(self, alert_type: str) -> List[Dict]:
        """Get all alerts of a specific type"""
        return [alert for alert in self.alerts if alert['type'] == alert_type]
    
    def get_alert_statistics(self) -> Dict:
        """Get comprehensive alert statistics"""
        try:
            active_count = sum(1 for alert in self.alerts if alert['enabled'])
            triggered_count = sum(1 for alert in self.alerts if alert['triggered'])
            
            # Count today's alerts
            today = pd.Timestamp.now().date()
            today_count = sum(1 for alert in self.alerts 
                           if alert['created'].date() == today)
            
            # Count by type
            type_counts = {}
            for alert in self.alerts:
                alert_type = alert['type']
                type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
            
            return {
                'total_alerts': len(self.alerts),
                'active_alerts': active_count,
                'triggered_alerts': triggered_count,
                'alerts_today': today_count,
                'type_distribution': type_counts
            }
            
        except Exception as e:
            logger.error(f"Failed to get alert statistics: {e}")
            return {}
    
    def export_alerts_to_dataframe(self) -> pd.DataFrame:
        """Export all alerts to a pandas DataFrame"""
        try:
            if not self.alerts:
                return pd.DataFrame()
            
            alerts_data = []
            for alert in self.alerts:
                alerts_data.append({
                    'ID': alert['id'],
                    'Type': alert['type'],
                    'Condition': alert['condition'],
                    'Threshold': alert['threshold'],
                    'Status': 'Active' if alert['enabled'] else 'Disabled',
                    'Datasets': len(alert['datasets']),
                    'Created': alert['created'].strftime('%Y-%m-%d %H:%M:%S'),
                    'Triggered': 'Yes' if alert['triggered'] else 'No',
                    'Description': alert.get('description', '')
                })
            
            return pd.DataFrame(alerts_data)
            
        except Exception as e:
            logger.error(f"Failed to export alerts to DataFrame: {e}")
            return pd.DataFrame()
