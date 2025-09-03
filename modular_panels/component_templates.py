#!/usr/bin/env python3
"""
TradePulse Modular Panels - Component Templates
Handles component template creation and management
"""

from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ComponentTemplates:
    """Handles component template creation and management"""
    
    def create_data_display_template(self, **kwargs) -> Dict:
        """Create a data display component template"""
        return {
            'type': 'data_display',
            'title': kwargs.get('title', 'Data Display'),
            'height': kwargs.get('height', 200),
            'width': kwargs.get('width', 'stretch'),
            'refreshable': kwargs.get('refreshable', True)
        }
    
    def create_chart_template(self, **kwargs) -> Dict:
        """Create a chart component template"""
        return {
            'type': 'chart',
            'chart_type': kwargs.get('chart_type', 'line'),
            'height': kwargs.get('height', 400),
            'width': kwargs.get('width', 'stretch'),
            'interactive': kwargs.get('interactive', True)
        }
    
    def create_control_template(self, **kwargs) -> Dict:
        """Create a control component template"""
        return {
            'type': 'control',
            'button_type': kwargs.get('button_type', 'primary'),
            'width': kwargs.get('width', 100),
            'height': kwargs.get('height', 35),
            'enabled': kwargs.get('enabled', True)
        }
    
    def create_table_template(self, **kwargs) -> Dict:
        """Create a table component template"""
        return {
            'type': 'table',
            'height': kwargs.get('height', 300),
            'width': kwargs.get('width', 'stretch'),
            'sortable': kwargs.get('sortable', True),
            'filterable': kwargs.get('filterable', True)
        }
