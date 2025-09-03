#!/usr/bin/env python3
"""
TradePulse Alerts Panel - Operations
Alert-related operations for the alerts panel
"""

import pandas as pd
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class AlertsOperations:
    """Alert-related operations for alerts panel"""
    
    def validate_alert_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate alert configuration"""
        errors = []
        
        # Check required fields
        required_fields = ['alert_type', 'condition', 'threshold_value']
        for field in required_fields:
            if field not in config or not config[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate alert type
        valid_types = ['Price Alert', 'Volume Alert', 'Technical Indicator', 'Custom']
        if 'alert_type' in config and config['alert_type'] not in valid_types:
            errors.append(f"Invalid alert type: {config['alert_type']}")
        
        # Validate threshold value
        if 'threshold_value' in config:
            try:
                threshold = float(config['threshold_value'])
                if threshold <= 0:
                    errors.append("Threshold value must be positive")
            except (ValueError, TypeError):
                errors.append("Invalid threshold value")
        
        # Validate condition
        valid_conditions = ['>', '<', '>=', '<=', '==', '!=']
        if 'condition' in config and config['condition'] not in valid_conditions:
            errors.append(f"Invalid condition: {config['condition']}")
        
        return len(errors) == 0, errors
    
    def create_alert_id(self, alert_type: str) -> str:
        """Create unique alert ID"""
        import uuid
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"{alert_type.replace(' ', '_').lower()}_{timestamp}_{unique_id}"
    
    def format_alert_condition(self, condition: str, threshold: float) -> str:
        """Format alert condition for display"""
        return f"{condition} {threshold}"
    
    def get_alert_statistics(self, alerts: List[Dict]) -> Dict[str, Any]:
        """Get statistics about alerts"""
        if not alerts:
            return {
                'total_alerts': 0,
                'active_alerts': 0,
                'triggered_alerts': 0,
                'alert_types': {}
            }
        
        stats = {
            'total_alerts': len(alerts),
            'active_alerts': len([a for a in alerts if a.get('status') == 'active']),
            'triggered_alerts': len([a for a in alerts if a.get('triggered_count', 0) > 0]),
            'alert_types': {}
        }
        
        # Count alert types
        for alert in alerts:
            alert_type = alert.get('type', 'Unknown')
            stats['alert_types'][alert_type] = stats['alert_types'].get(alert_type, 0) + 1
        
        return stats
    
    def filter_alerts_by_type(self, alerts: List[Dict], alert_type: str) -> List[Dict]:
        """Filter alerts by type"""
        return [alert for alert in alerts if alert.get('type') == alert_type]
    
    def filter_alerts_by_status(self, alerts: List[Dict], status: str) -> List[Dict]:
        """Filter alerts by status"""
        return [alert for alert in alerts if alert.get('status') == status]
    
    def sort_alerts_by_date(self, alerts: List[Dict], reverse: bool = True) -> List[Dict]:
        """Sort alerts by creation date"""
        return sorted(alerts, key=lambda x: x.get('created_at', ''), reverse=reverse)
    
    def get_alert_summary(self, alerts: List[Dict]) -> str:
        """Get summary of alerts"""
        if not alerts:
            return "No alerts configured"
        
        stats = self.get_alert_statistics(alerts)
        
        summary_lines = [
            f"**Total Alerts**: {stats['total_alerts']}",
            f"**Active Alerts**: {stats['active_alerts']}",
            f"**Triggered Alerts**: {stats['triggered_alerts']}",
            "",
            "**Alert Types**:"
        ]
        
        for alert_type, count in stats['alert_types'].items():
            summary_lines.append(f"- {alert_type}: {count}")
        
        return "\n".join(summary_lines)



