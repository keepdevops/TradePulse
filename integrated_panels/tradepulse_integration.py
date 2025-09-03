#!/usr/bin/env python3
"""
TradePulse Integrated Panels - TradePulse Integration
Handles integration with TradePulse system components
"""

import panel as pn
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .system_integrators import SystemIntegrators

logger = logging.getLogger(__name__)

class TradePulseIntegration:
    """Handles integration with TradePulse system components"""
    
    def __init__(self):
        from .integration_initializer import IntegrationInitializer
        initializer = IntegrationInitializer()
        initializer.initialize_integration(self)
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        try:
            return self.system_integrators.get_integration_status()
            
        except Exception as e:
            logger.error(f"Failed to get integration status: {e}")
            return {}
    
    def test_integrations(self) -> Dict[str, bool]:
        """Test all integrations"""
        try:
            return self.system_integrators.test_integrations()
            
        except Exception as e:
            logger.error(f"Failed to test integrations: {e}")
            return {}
    
    def send_message(self, message: Dict[str, Any]) -> bool:
        """Send message via message bus"""
        try:
            from .message_handler import MessageHandler
            handler = MessageHandler(self.message_bus)
            return handler.send_message(message)
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive message via message bus"""
        try:
            from .message_handler import MessageHandler
            handler = MessageHandler(self.message_bus)
            return handler.receive_message()
            
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            return None
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute database query"""
        try:
            from .database_handler import DatabaseHandler
            handler = DatabaseHandler(self.database)
            return handler.execute_query(query)
            
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            return []
    
    def store_data(self, table: str, data: Dict[str, Any]) -> bool:
        """Store data in database"""
        try:
            from .database_handler import DatabaseHandler
            handler = DatabaseHandler(self.database)
            return handler.store_data(table, data)
            
        except Exception as e:
            logger.error(f"Failed to store data: {e}")
            return False
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """Get a specific model"""
        try:
            from .component_accessor import ComponentAccessor
            accessor = ComponentAccessor(self)
            return accessor.get_model(model_name)
            
        except Exception as e:
            logger.error(f"Failed to get model {model_name}: {e}")
            return None
    
    def get_ai_handler(self, handler_name: str) -> Optional[Any]:
        """Get a specific AI handler"""
        try:
            from .component_accessor import ComponentAccessor
            accessor = ComponentAccessor(self)
            return accessor.get_ai_handler(handler_name)
            
        except Exception as e:
            logger.error(f"Failed to get AI handler {handler_name}: {e}")
            return None
    
    def get_data_component(self, component_name: str) -> Optional[Any]:
        """Get a specific data component"""
        try:
            from .component_accessor import ComponentAccessor
            accessor = ComponentAccessor(self)
            return accessor.get_data_component(component_name)
            
        except Exception as e:
            logger.error(f"Failed to get data component {component_name}: {e}")
            return None
    
    def get_portfolio_strategy(self, strategy_name: str) -> Optional[Any]:
        """Get a specific portfolio strategy"""
        try:
            from .component_accessor import ComponentAccessor
            accessor = ComponentAccessor(self)
            return accessor.get_portfolio_strategy(strategy_name)
            
        except Exception as e:
            logger.error(f"Failed to get portfolio strategy {strategy_name}: {e}")
            return None
    
    def get_visualization_component(self, component_name: str) -> Optional[Any]:
        """Get a specific visualization component"""
        try:
            from .component_accessor import ComponentAccessor
            accessor = ComponentAccessor(self)
            return accessor.get_visualization_component(component_name)
            
        except Exception as e:
            logger.error(f"Failed to get visualization component {component_name}: {e}")
            return None
    
    def create_integration_dashboard(self) -> pn.Column:
        """Create integration status dashboard"""
        try:
            from .integration_dashboard import IntegrationDashboard
            dashboard = IntegrationDashboard(self)
            return dashboard.create_dashboard()
            
        except Exception as e:
            logger.error(f"Failed to create integration dashboard: {e}")
            return pn.Column("Error: Failed to create integration dashboard")
    
    def _test_integrations_callback(self, event=None):
        """Callback for testing integrations"""
        try:
            from .integration_callbacks import IntegrationCallbacks
            callbacks = IntegrationCallbacks(self)
            callbacks.test_integrations()
            
        except Exception as e:
            logger.error(f"Failed to test integrations: {e}")
    
    def _refresh_status_callback(self, event=None):
        """Callback for refreshing status"""
        try:
            from .integration_callbacks import IntegrationCallbacks
            callbacks = IntegrationCallbacks(self)
            callbacks.refresh_status()
            
        except Exception as e:
            logger.error(f"Failed to refresh integration status: {e}")
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get integration summary"""
        try:
            from .integration_summary import IntegrationSummary
            summary = IntegrationSummary(self)
            return summary.get_summary()
            
        except Exception as e:
            logger.error(f"Failed to get integration summary: {e}")
            return {}
    
    def get_component_status(self) -> Dict[str, Any]:
        """Get component status"""
        try:
            return {
                'message_bus': self.message_bus is not None,
                'database': self.database is not None,
                'models_count': len(self.models),
                'ai_handlers_count': len(self.ai_handlers),
                'data_components_count': len(self.data_components),
                'portfolio_strategies_count': len(self.portfolio_strategies),
                'visualization_components_count': len(self.visualization_components),
                'integration_type': 'TradePulse Integration'
            }
            
        except Exception as e:
            logger.error(f"Failed to get component status: {e}")
            return {}
