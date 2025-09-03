#!/usr/bin/env python3
"""
TradePulse Modular Panels - Base Component
Base class for all UI components with common functionality
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Callable, Any
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseComponent(ABC):
    """Base class for all UI components with common functionality"""
    
    def __init__(self, name: str):
        self.name = name
        self.components = {}
        self.callbacks = {}
        self.metadata = {}
        
        # Initialize component
        self.create_components()
        self.setup_callbacks()
    
    @abstractmethod
    def create_components(self):
        """Create the component's UI elements"""
        pass
    
    @abstractmethod
    def get_layout(self):
        """Get the component's layout"""
        pass
    
    def setup_callbacks(self):
        """Setup component callbacks - can be overridden"""
        pass
    
    def add_callback(self, event_name: str, callback: Callable):
        """Add a callback for an event"""
        try:
            if event_name not in self.callbacks:
                self.callbacks[event_name] = []
            
            if callback not in self.callbacks[event_name]:
                self.callbacks[event_name].append(callback)
                logger.info(f"✅ Added callback for {event_name} in {self.name}")
            
        except Exception as e:
            logger.error(f"Failed to add callback: {e}")
    
    def remove_callback(self, event_name: str, callback: Callable):
        """Remove a callback for an event"""
        try:
            if event_name in self.callbacks and callback in self.callbacks[event_name]:
                self.callbacks[event_name].remove(callback)
                logger.info(f"✅ Removed callback for {event_name} in {self.name}")
            
        except Exception as e:
            logger.error(f"Failed to remove callback: {e}")
    
    def trigger_callback(self, event_name: str, *args, **kwargs):
        """Trigger callbacks for an event"""
        try:
            if event_name in self.callbacks:
                for callback in self.callbacks[event_name]:
                    try:
                        callback(*args, **kwargs)
                    except Exception as e:
                        logger.error(f"Callback execution failed: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to trigger callback: {e}")
    
    def register_component(self, component_name: str, component: Any):
        """Register a sub-component"""
        try:
            self.components[component_name] = component
            logger.info(f"✅ Registered component {component_name} in {self.name}")
            
        except Exception as e:
            logger.error(f"Failed to register component: {e}")
    
    def get_component(self, component_name: str) -> Optional[Any]:
        """Get a registered sub-component"""
        return self.components.get(component_name)
    
    def unregister_component(self, component_name: str):
        """Unregister a sub-component"""
        try:
            if component_name in self.components:
                del self.components[component_name]
                logger.info(f"✅ Unregistered component {component_name} from {self.name}")
                
        except Exception as e:
            logger.error(f"Failed to unregister component: {e}")
    
    def set_metadata(self, key: str, value: Any):
        """Set component metadata"""
        try:
            self.metadata[key] = value
            
        except Exception as e:
            logger.error(f"Failed to set metadata: {e}")
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get component metadata"""
        return self.metadata.get(key, default)
    
    def get_component_info(self) -> Dict[str, Any]:
        """Get component information"""
        try:
            return {
                'name': self.name,
                'type': self.__class__.__name__,
                'components_count': len(self.components),
                'callbacks_count': sum(len(callbacks) for callbacks in self.callbacks.values()),
                'metadata_keys': list(self.metadata.keys()),
                'has_layout': hasattr(self, 'get_layout')
            }
        except Exception as e:
            logger.error(f"Failed to get component info: {e}")
            return {}
    
    def validate_component(self) -> bool:
        """Validate component configuration"""
        try:
            # Check required methods
            if not hasattr(self, 'create_components'):
                logger.error(f"❌ Component {self.name} missing create_components method")
                return False
            
            if not hasattr(self, 'get_layout'):
                logger.error(f"❌ Component {self.name} missing get_layout method")
                return False
            
            # Check component creation
            if not hasattr(self, 'components'):
                logger.error(f"❌ Component {self.name} missing components attribute")
                return False
            
            logger.info(f"✅ Component {self.name} validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Component validation failed: {e}")
            return False
    
    def refresh_component(self):
        """Refresh component state and displays"""
        try:
            logger.info(f"🔄 Refreshing component {self.name}")
            
            # Trigger refresh callback
            self.trigger_callback('refresh')
            
            # Update displays if method exists
            if hasattr(self, 'update_displays'):
                self.update_displays()
            
            logger.info(f"✅ Component {self.name} refreshed successfully")
            
        except Exception as e:
            logger.error(f"Failed to refresh component: {e}")
    
    def clear_component(self):
        """Clear component data and state"""
        try:
            logger.info(f"🗑️ Clearing component {self.name}")
            
            # Trigger clear callback
            self.trigger_callback('clear')
            
            # Clear components if method exists
            if hasattr(self, 'clear_data'):
                self.clear_data()
            
            logger.info(f"✅ Component {self.name} cleared successfully")
            
        except Exception as e:
            logger.error(f"Failed to clear component: {e}")
    
    def export_component_data(self) -> Dict[str, Any]:
        """Export component data for external use"""
        try:
            export_data = {
                'name': self.name,
                'type': self.__class__.__name__,
                'metadata': self.metadata.copy(),
                'components': {name: comp.get_component_info() if hasattr(comp, 'get_component_info') else str(type(comp)) 
                             for name, comp in self.components.items()},
                'callbacks': {event: len(callbacks) for event, callbacks in self.callbacks.items()}
            }
            
            logger.info(f"📤 Component {self.name} data exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export component data: {e}")
            return {}
    
    def import_component_data(self, data: Dict[str, Any]):
        """Import component data from external source"""
        try:
            if 'metadata' in data:
                self.metadata.update(data['metadata'])
            
            logger.info(f"📥 Component {self.name} data imported")
            
        except Exception as e:
            logger.error(f"Failed to import component data: {e}")
    
    def get_component_statistics(self) -> Dict[str, Any]:
        """Get component statistics"""
        try:
            return {
                'name': self.name,
                'type': self.__class__.__name__,
                'components_registered': len(self.components),
                'callbacks_registered': sum(len(callbacks) for callbacks in self.callbacks.values()),
                'metadata_entries': len(self.metadata),
                'validation_status': self.validate_component(),
                'last_refresh': getattr(self, '_last_refresh', None)
            }
        except Exception as e:
            logger.error(f"Failed to get component statistics: {e}")
            return {}
    
    def __str__(self) -> str:
        """String representation of component"""
        return f"{self.__class__.__name__}({self.name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of component"""
        return f"{self.__class__.__name__}(name='{self.name}', components={len(self.components)}, callbacks={sum(len(callbacks) for callbacks in self.callbacks.values())})"
