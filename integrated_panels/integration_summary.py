#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Integration Summary
Handles integration summary functionality
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class IntegrationSummary:
    """Handles integration summary functionality"""
    
    def __init__(self, integration):
        self.integration = integration
    
    def get_summary(self) -> Dict[str, Any]:
        """Get integration summary"""
        try:
            status = self.integration.get_integration_status()
            
            return {
                'total_components': (
                    status.get('models', {}).get('count', 0) +
                    status.get('ai_handlers', {}).get('count', 0) +
                    status.get('data_components', {}).get('count', 0) +
                    status.get('portfolio_strategies', {}).get('count', 0) +
                    status.get('visualization_components', {}).get('count', 0)
                ),
                'message_bus_connected': status.get('message_bus', {}).get('connected', False),
                'database_connected': status.get('database', {}).get('connected', False),
                'last_updated': status.get('timestamp'),
                'integration_type': 'TradePulse Integration'
            }
            
        except Exception as e:
            logger.error(f"Failed to get integration summary: {e}")
            return {}
