#!/usr/bin/env python3
"""
TradePulse Models Panel - Components
UI components for the models panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelsPanelComponents:
    """UI components for models panel"""
    
    def __init__(self):
        self.components = {}
    
    def __getitem__(self, key):
        """Get component by key"""
        return self.components.get(key)
    
    def __setitem__(self, key, value):
        """Set component by key"""
        self.components[key] = value
    
    def update(self, components_dict):
        """Update components with dictionary"""
        self.components.update(components_dict)
    
    def get_component(self, key):
        """Get component by key"""
        return self.components.get(key)
    
    def set_component(self, key, value):
        """Set component by key"""
        self.components[key] = value
    
    def get_all_components(self):
        """Get all components"""
        return self.components
    
    def has_component(self, key):
        """Check if component exists"""
        return key in self.components
    
    def remove_component(self, key):
        """Remove component by key"""
        if key in self.components:
            del self.components[key]
    
    def clear_components(self):
        """Clear all components"""
        self.components.clear()
    
    def get_component_keys(self):
        """Get all component keys"""
        return list(self.components.keys())
    
    def get_component_count(self):
        """Get number of components"""
        return len(self.components)



