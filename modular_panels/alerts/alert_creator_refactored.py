#!/usr/bin/env python3
"""
TradePulse Modular Panels - Alert Creator (Refactored)
Handles alert creation and configuration
Refactored to be under 200 lines
"""

import panel as pn
import pandas as pd
from typing import Dict, Any, List
import logging

from .alert_creator_core import AlertCreatorCore

logger = logging.getLogger(__name__)

class AlertCreator:
    """Handles alert creation and configuration"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_creator = AlertCreatorCore()
    
    def get_alert_config(self) -> Dict[str, Any]:
        """Get current alert configuration"""
        # Delegate to refactored implementation
        return self._refactored_creator.get_alert_config()
    
    def validate_alert_config(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate alert configuration"""
        # Delegate to refactored implementation
        return self._refactored_creator.validate_alert_config(config)
    
    def create_alert_from_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create alert object from configuration"""
        # Delegate to refactored implementation
        return self._refactored_creator.create_alert_from_config(config)
    
    def get_components(self) -> Dict[str, Any]:
        """Get all alert creation components"""
        # Delegate to refactored implementation
        return self._refactored_creator.get_components()
    
    def setup_callbacks(self, create_callback, test_callback):
        """Setup component callbacks"""
        # Delegate to refactored implementation
        return self._refactored_creator.setup_callbacks(create_callback, test_callback)
    
    def reset_form(self):
        """Reset alert creation form to defaults"""
        # Delegate to refactored implementation
        return self._refactored_creator.reset_form()
    
    def get_form_layout(self) -> pn.Column:
        """Get the alert creation form layout"""
        # Delegate to refactored implementation
        return self._refactored_creator.get_form_layout()



