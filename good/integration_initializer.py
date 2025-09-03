#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Integration Initializer
Handles integration initialization
"""

import logging

logger = logging.getLogger(__name__)

class IntegrationInitializer:
    """Handles integration initialization"""
    
    def __init__(self):
        pass
    
    def initialize_integration(self, integration):
        """Initialize the integration system"""
        try:
            # Initialize system integrators
            from .system_integrators import SystemIntegrators
            integration.system_integrators = SystemIntegrators()
            
            # Get component references
            integration.message_bus = integration.system_integrators.message_bus
            integration.database = integration.system_integrators.database
            integration.models = integration.system_integrators.models
            integration.ai_handlers = integration.system_integrators.ai_handlers
            integration.data_components = integration.system_integrators.data_components
            integration.portfolio_strategies = integration.system_integrators.portfolio_strategies
            integration.visualization_components = integration.system_integrators.visualization_components
            
            # Setup integration
            self._setup_integration(integration)
            
        except Exception as e:
            logger.error(f"Failed to initialize integration: {e}")
    
    def _setup_integration(self, integration):
        """Setup the integration system"""
        try:
            logger.info("🔧 Setting up TradePulse integration")
            
            # Test all integrations
            test_results = integration.system_integrators.test_integrations()
            
            # Log integration status
            self._log_integration_status(test_results)
            
            logger.info("✅ TradePulse integration setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup integration: {e}")
    
    def _log_integration_status(self, test_results):
        """Log integration status"""
        try:
            logger.info("📊 Integration Status:")
            
            for component, status in test_results.items():
                status_emoji = "✅" if status else "❌"
                logger.info(f"  {status_emoji} {component}: {'Available' if status else 'Not Available'}")
            
        except Exception as e:
            logger.error(f"Failed to log integration status: {e}")
