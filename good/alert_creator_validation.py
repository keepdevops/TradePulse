#!/usr/bin/env python3
"""
TradePulse Alert Creator - Validation
Validation logic for the alert creator
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AlertCreatorValidation:
    """Validation logic for alert creator"""
    
    def validate_alert_config(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate alert configuration"""
        try:
            errors = []
            
            # Check required fields
            required_fields = ['alert_type', 'condition_operator', 'threshold_value']
            for field in required_fields:
                if field not in config or config[field] is None:
                    errors.append(f"Missing required field: {field}")
            
            # Validate threshold value
            if 'threshold_value' in config and config['threshold_value'] <= 0:
                errors.append("Threshold value must be positive")
            
            # Validate percentage change
            if 'percentage_change' in config and config['percentage_change'] <= 0:
                errors.append("Percentage change must be positive")
            
            # Validate notification types
            if 'notification_type' in config and not config['notification_type']:
                errors.append("At least one notification type must be selected")
            
            is_valid = len(errors) == 0
            return is_valid, errors
            
        except Exception as e:
            logger.error(f"Failed to validate alert config: {e}")
            return False, [f"Validation error: {e}"]
    
    def validate_alert_type(self, alert_type: str) -> bool:
        """Validate alert type"""
        try:
            valid_types = [
                'Price Alert', 'Volume Alert', 'Technical Indicator', 
                'Custom Condition', 'Pattern Recognition'
            ]
            return alert_type in valid_types
            
        except Exception as e:
            logger.error(f"Failed to validate alert type: {e}")
            return False
    
    def validate_condition_operator(self, operator: str) -> bool:
        """Validate condition operator"""
        try:
            valid_operators = [
                'Above', 'Below', 'Crosses Above', 'Crosses Below', 'Changes By'
            ]
            return operator in valid_operators
            
        except Exception as e:
            logger.error(f"Failed to validate condition operator: {e}")
            return False
    
    def validate_threshold_value(self, value: float) -> bool:
        """Validate threshold value"""
        try:
            if not isinstance(value, (int, float)):
                return False
            
            if value <= 0:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate threshold value: {e}")
            return False
    
    def validate_percentage_change(self, value: float) -> bool:
        """Validate percentage change value"""
        try:
            if not isinstance(value, (int, float)):
                return False
            
            if value <= 0:
                return False
            
            if value > 1000:  # Reasonable upper limit
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate percentage change: {e}")
            return False
    
    def validate_notification_types(self, notification_types: List[str]) -> bool:
        """Validate notification types"""
        try:
            if not isinstance(notification_types, list):
                return False
            
            if len(notification_types) == 0:
                return False
            
            valid_types = ['Email', 'SMS', 'Push', 'Sound', 'Desktop']
            
            for notification_type in notification_types:
                if notification_type not in valid_types:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate notification types: {e}")
            return False
    
    def get_validation_summary(self, config: Dict[str, Any]) -> str:
        """Get validation summary"""
        try:
            is_valid, errors = self.validate_alert_config(config)
            
            if is_valid:
                return "✅ Alert configuration is valid"
            else:
                error_list = "\n".join([f"- {error}" for error in errors])
                return f"❌ Alert configuration has errors:\n{error_list}"
                
        except Exception as e:
            logger.error(f"Failed to get validation summary: {e}")
            return f"❌ Validation error: {e}"
    
    def validate_alert_id(self, alert_id: str) -> bool:
        """Validate alert ID format"""
        try:
            if not alert_id or not isinstance(alert_id, str):
                return False
            
            # Check if it follows the expected format
            if not alert_id.startswith('alert_'):
                return False
            
            # Check if it has a timestamp
            if len(alert_id) < 20:  # Minimum length for alert_YYYYMMDD_HHMMSS
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate alert ID: {e}")
            return False

