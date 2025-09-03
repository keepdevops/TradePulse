#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Integration Callbacks
Handles integration callback functionality
"""

import logging

logger = logging.getLogger(__name__)

class IntegrationCallbacks:
    """Handles integration callback functionality"""
    
    def __init__(self, integration):
        self.integration = integration
    
    def test_integrations(self):
        """Callback for testing integrations"""
        try:
            logger.info("🧪 Testing integrations...")
            
            test_results = self.integration.test_integrations()
            self.integration._log_integration_status(test_results)
            
            logger.info("✅ Integration testing complete")
            
        except Exception as e:
            logger.error(f"Failed to test integrations: {e}")
    
    def refresh_status(self):
        """Callback for refreshing status"""
        try:
            logger.info("🔄 Refreshing integration status...")
            
            # Update status
            status = self.integration.get_integration_status()
            self.integration._log_integration_status(status)
            
            logger.info("✅ Integration status refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh integration status: {e}")
