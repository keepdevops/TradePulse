#!/usr/bin/env python3
"""
TradePulse Base Component
Base class for all modular panel components
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseComponent(ABC):
    """Base class for all TradePulse modular components"""
    
    def __init__(self, data_manager=None, data_access_manager=None):
        self.data_manager = data_manager
        self.data_access_manager = data_access_manager
        self.components = {}
        self.callbacks = {}
        self.panel = None
        
        logger.info(f"🔧 Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def create_panel(self) -> pn.Column:
        """Create the main panel for this component"""
        pass
    
    def get_panel(self) -> pn.Column:
        """Get the component panel"""
        if self.panel is None:
            self.panel = self.create_panel()
        return self.panel
    
    def add_component(self, name: str, component: Any):
        """Add a component to the component registry"""
        self.components[name] = component
        logger.debug(f"📦 Added component: {name}")
    
    def get_component(self, name: str) -> Any:
        """Get a component by name"""
        return self.components.get(name)
    
    def add_callback(self, name: str, callback: callable):
        """Add a callback to the callback registry"""
        self.callbacks[name] = callback
        logger.debug(f"🔄 Added callback: {name}")
    
    def get_callback(self, name: str) -> callable:
        """Get a callback by name"""
        return self.callbacks.get(name)
    
    def update_data(self, new_data: Any):
        """Update component data"""
        if self.data_manager:
            logger.info("📊 Updating component data")
            # Override in subclasses for specific data update logic
            pass
    
    def refresh_panel(self):
        """Refresh the component panel"""
        if self.panel:
            logger.info("🔄 Refreshing component panel")
            # Override in subclasses for specific refresh logic
            pass
    
    def get_component_info(self) -> Dict[str, Any]:
        """Get component information"""
        return {
            'name': self.__class__.__name__,
            'components_count': len(self.components),
            'callbacks_count': len(self.callbacks),
            'has_data_manager': self.data_manager is not None,
            'has_data_access': self.data_access_manager is not None
        }
    
    def cleanup(self):
        """Cleanup component resources"""
        logger.info(f"🧹 Cleaning up {self.__class__.__name__}")
        self.components.clear()
        self.callbacks.clear()
        self.panel = None
