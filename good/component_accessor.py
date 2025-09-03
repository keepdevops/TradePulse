#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Component Accessor
Handles component access functionality
"""

from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class ComponentAccessor:
    """Handles component access functionality"""
    
    def __init__(self, integration):
        self.integration = integration
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """Get a specific model"""
        try:
            return self.integration.models.get(model_name)
            
        except Exception as e:
            logger.error(f"Failed to get model {model_name}: {e}")
            return None
    
    def get_ai_handler(self, handler_name: str) -> Optional[Any]:
        """Get a specific AI handler"""
        try:
            return self.integration.ai_handlers.get(handler_name)
            
        except Exception as e:
            logger.error(f"Failed to get AI handler {handler_name}: {e}")
            return None
    
    def get_data_component(self, component_name: str) -> Optional[Any]:
        """Get a specific data component"""
        try:
            return self.integration.data_components.get(component_name)
            
        except Exception as e:
            logger.error(f"Failed to get data component {component_name}: {e}")
            return None
    
    def get_portfolio_strategy(self, strategy_name: str) -> Optional[Any]:
        """Get a specific portfolio strategy"""
        try:
            return self.integration.portfolio_strategies.get(strategy_name)
            
        except Exception as e:
            logger.error(f"Failed to get portfolio strategy {strategy_name}: {e}")
            return None
    
    def get_visualization_component(self, component_name: str) -> Optional[Any]:
        """Get a specific visualization component"""
        try:
            return self.integration.visualization_components.get(component_name)
            
        except Exception as e:
            logger.error(f"Failed to get visualization component {component_name}: {e}")
            return None
