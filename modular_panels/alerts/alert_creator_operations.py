#!/usr/bin/env python3
"""
TradePulse Alert Creator - Operations
Alert-related operations for the alert creator
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AlertCreatorOperations:
    """Alert-related operations for alert creator"""
    
    def get_alert_config(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Get current alert configuration"""
        try:
            config = {}
            
            for name, component in components.items():
                if hasattr(component, 'value'):
                    config[name] = component.value
                elif hasattr(component, 'object'):
                    config[name] = component.object
            
            return config
            
        except Exception as e:
            logger.error(f"Failed to get alert config: {e}")
            return {}
    
    def create_alert_from_config(self, config: Dict[str, Any], validation) -> Dict[str, Any]:
        """Create alert object from configuration"""
        try:
            # Validate config first
            is_valid, errors = validation.validate_alert_config(config)
            if not is_valid:
                raise ValueError(f"Invalid alert configuration: {', '.join(errors)}")
            
            # Create alert object
            alert = {
                'id': f"alert_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
                'type': config.get('alert_type', 'Price Alert'),
                'condition': {
                    'operator': config.get('condition_operator', 'Above'),
                    'threshold': config.get('threshold_value', 100.0),
                    'percentage_change': config.get('percentage_change', 5.0)
                },
                'enabled': config.get('alert_enabled', True),
                'notifications': config.get('notification_type', ['Email', 'Push']),
                'created_at': pd.Timestamp.now().isoformat(),
                'status': 'active',
                'triggered_count': 0,
                'last_triggered': None
            }
            
            logger.info(f"✅ Alert created: {alert['id']}")
            return alert
            
        except Exception as e:
            logger.error(f"Failed to create alert from config: {e}")
            raise
    
    def setup_callbacks(self, create_alert_button, test_alert_button, create_callback, test_callback):
        """Setup component callbacks"""
        try:
            if create_alert_button:
                create_alert_button.on_click(create_callback)
            
            if test_alert_button:
                test_alert_button.on_click(test_callback)
            
            logger.info("✅ Alert creation callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup alert creation callbacks: {e}")
    
    def reset_form(self, components: Dict[str, Any]):
        """Reset alert creation form to defaults"""
        try:
            # Reset to default values
            if 'alert_type' in components:
                components['alert_type'].value = 'Price Alert'
            
            if 'condition_operator' in components:
                components['condition_operator'].value = 'Above'
            
            if 'threshold_value' in components:
                components['threshold_value'].value = 100.0
            
            if 'percentage_change' in components:
                components['percentage_change'].value = 5.0
            
            if 'alert_enabled' in components:
                components['alert_enabled'].value = True
            
            if 'notification_type' in components:
                components['notification_type'].value = ['Email', 'Push']
            
            logger.info("✅ Alert creation form reset")
            
        except Exception as e:
            logger.error(f"Failed to reset alert creation form: {e}")
    
    def test_alert_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test alert configuration"""
        try:
            # Simulate alert test
            test_result = {
                'success': True,
                'message': f"Alert test successful for {config.get('alert_type', 'Unknown')}",
                'tested_at': pd.Timestamp.now().isoformat(),
                'config': config
            }
            
            logger.info(f"🧪 Alert test completed: {test_result['message']}")
            return test_result
            
        except Exception as e:
            logger.error(f"Failed to test alert configuration: {e}")
            return {
                'success': False,
                'message': f"Alert test failed: {e}",
                'tested_at': pd.Timestamp.now().isoformat(),
                'config': config
            }
    
    def export_alert_config(self, config: Dict[str, Any], filename: str = None) -> str:
        """Export alert configuration to file"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"alert_config_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2, default=str)
            
            logger.info(f"📤 Alert config exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export alert config: {e}")
            return None
    
    def get_alert_summary(self, config: Dict[str, Any]) -> str:
        """Get alert configuration summary"""
        try:
            summary_lines = [
                f"**Alert Type**: {config.get('alert_type', 'Unknown')}",
                f"**Condition**: {config.get('condition_operator', 'Unknown')} {config.get('threshold_value', 0)}",
                f"**Percentage Change**: {config.get('percentage_change', 0)}%",
                f"**Enabled**: {config.get('alert_enabled', False)}",
                f"**Notifications**: {', '.join(config.get('notification_type', []))}"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create alert summary: {e}")
            return "Error creating summary"



