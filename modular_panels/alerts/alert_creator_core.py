#!/usr/bin/env python3
"""
TradePulse Alert Creator - Core Functionality
Core alert creator class with basic functionality
"""

import panel as pn
import pandas as pd
from typing import Dict, Any, List
import logging

from .alert_creator_components import AlertCreatorComponents
from .alert_creator_operations import AlertCreatorOperations
from .alert_creator_management import AlertCreatorManagement
from .alert_creator_validation import AlertCreatorValidation

logger = logging.getLogger(__name__)

class AlertCreatorCore:
    """Core alert creator functionality"""
    
    def __init__(self):
        self.alert_types = [
            'Price Alert', 'Volume Alert', 'Technical Indicator', 
            'Custom Condition', 'Pattern Recognition'
        ]
        self.condition_operators = [
            'Above', 'Below', 'Crosses Above', 'Crosses Below', 'Changes By'
        ]
        self.notification_types = [
            'Email', 'SMS', 'Push', 'Sound', 'Desktop'
        ]
        
        # Initialize components
        self.components = AlertCreatorComponents()
        self.operations = AlertCreatorOperations()
        self.management = AlertCreatorManagement()
        self.validation = AlertCreatorValidation()
        
        # Create UI components
        self._create_components()
    
    def _create_components(self):
        """Create alert creation components"""
        try:
            logger.info("🔧 Creating alert creation components")
            
            # Alert type selector
            self.alert_type = pn.widgets.Select(
                name='Alert Type',
                options=self.alert_types,
                value='Price Alert',
                width=200
            )
            
            # Alert conditions
            self.condition_operator = pn.widgets.Select(
                name='Condition',
                options=self.condition_operators,
                value='Above',
                width=150
            )
            
            self.threshold_value = pn.widgets.FloatInput(
                name='Threshold',
                start=0.01,
                value=100.0,
                width=150
            )
            
            self.percentage_change = pn.widgets.FloatInput(
                name='% Change',
                start=0.1,
                value=5.0,
                width=150
            )
            
            # Alert settings
            self.alert_enabled = pn.widgets.Checkbox(
                name='Enable Alert',
                value=True,
                width=120
            )
            
            self.notification_type = pn.widgets.MultiChoice(
                name='Notifications',
                options=self.notification_types,
                value=['Email', 'Push'],
                width=200
            )
            
            # Action buttons
            self.create_alert = pn.widgets.Button(
                name='🚨 Create Alert',
                button_type='danger',
                width=150
            )
            
            self.test_alert = pn.widgets.Button(
                name='🧪 Test Alert',
                button_type='warning',
                width=150
            )
            
            logger.info("✅ Alert creation components created")
            
        except Exception as e:
            logger.error(f"Failed to create alert creation components: {e}")
    
    def get_alert_config(self) -> Dict[str, Any]:
        """Get current alert configuration"""
        return self.operations.get_alert_config({
            'alert_type': self.alert_type,
            'condition_operator': self.condition_operator,
            'threshold_value': self.threshold_value,
            'percentage_change': self.percentage_change,
            'alert_enabled': self.alert_enabled,
            'notification_type': self.notification_type
        })
    
    def validate_alert_config(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate alert configuration"""
        return self.validation.validate_alert_config(config)
    
    def create_alert_from_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create alert object from configuration"""
        return self.operations.create_alert_from_config(config, self.validation)
    
    def get_components(self) -> Dict[str, Any]:
        """Get all alert creation components"""
        return {
            'alert_type': self.alert_type,
            'condition_operator': self.condition_operator,
            'threshold_value': self.threshold_value,
            'percentage_change': self.percentage_change,
            'alert_enabled': self.alert_enabled,
            'notification_type': self.notification_type,
            'create_alert': self.create_alert,
            'test_alert': self.test_alert
        }
    
    def setup_callbacks(self, create_callback, test_callback):
        """Setup component callbacks"""
        return self.operations.setup_callbacks(
            self.create_alert, self.test_alert, create_callback, test_callback
        )
    
    def reset_form(self):
        """Reset alert creation form to defaults"""
        return self.operations.reset_form({
            'alert_type': self.alert_type,
            'condition_operator': self.condition_operator,
            'threshold_value': self.threshold_value,
            'percentage_change': self.percentage_change,
            'alert_enabled': self.alert_enabled,
            'notification_type': self.notification_type
        })
    
    def get_form_layout(self) -> pn.Column:
        """Get the alert creation form layout"""
        return self.management.get_form_layout(self.get_components())



