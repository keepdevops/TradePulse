#!/usr/bin/env python3
"""
TradePulse Modular Panels - Component Registry
Manages component registration and eliminates duplicate code
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Callable, Any, Type
import logging
from datetime import datetime

from .component_templates import ComponentTemplates
from .duplicate_detector import DuplicateDetector
from .registry_manager import RegistryManager

logger = logging.getLogger(__name__)

class ComponentRegistry:
    """Manages component registration and eliminates duplicate code"""
    
    def __init__(self):
        self.registered_components = {}
        self.component_factories = {}
        self.component_templates = {}
        self.usage_statistics = {}
        
        # Initialize components
        self.templates = ComponentTemplates()
        self.duplicate_detector = DuplicateDetector()
        self.registry_manager = RegistryManager()
        
        # Initialize registry
        self._setup_default_components()
    
    def _setup_default_components(self):
        """Setup default component types and templates"""
        try:
            # Register common component types
            self.register_component_type('data_display', self.templates.create_data_display_template)
            self.register_component_type('chart', self.templates.create_chart_template)
            self.register_component_type('control', self.templates.create_control_template)
            self.register_component_type('table', self.templates.create_table_template)
            
            logger.info("✅ Default component types registered")
            
        except Exception as e:
            logger.error(f"Failed to setup default components: {e}")
    
    def register_component(self, name: str, component: Any, category: str = "general"):
        """Register a component in the registry"""
        return self.registry_manager.register_component(self.registered_components, name, component, category)
    
    def unregister_component(self, name: str):
        """Unregister a component from the registry"""
        return self.registry_manager.unregister_component(self.registered_components, name)
    
    def get_component(self, name: str) -> Optional[Any]:
        """Get a registered component"""
        return self.registry_manager.get_component(self.registered_components, name)
    
    def register_component_type(self, type_name: str, factory_function: Callable):
        """Register a component factory function"""
        try:
            self.component_factories[type_name] = factory_function
            logger.info(f"✅ Component type {type_name} registered")
            
        except Exception as e:
            logger.error(f"Failed to register component type {type_name}: {e}")
    
    def create_component(self, type_name: str, **kwargs) -> Optional[Any]:
        """Create a component using a registered factory"""
        return self.registry_manager.create_component(self.component_factories, type_name, **kwargs)
    
    def register_component_template(self, template_name: str, template_data: Dict):
        """Register a component template for reuse"""
        return self.registry_manager.register_component_template(self.component_templates, template_name, template_data)
    
    def get_component_template(self, template_name: str) -> Optional[Dict]:
        """Get a registered component template"""
        return self.component_templates.get(template_name)
    
    def create_from_template(self, template_name: str, **kwargs) -> Optional[Any]:
        """Create a component from a template"""
        return self.registry_manager.create_from_template(self.component_templates, self.component_factories, template_name, **kwargs)
    
    def detect_duplicates(self) -> Dict[str, List[str]]:
        """Detect duplicate component implementations"""
        return self.duplicate_detector.detect_duplicates(self.registered_components)
    
    def eliminate_duplicates(self) -> int:
        """Eliminate duplicate components by consolidating them"""
        return self.duplicate_detector.eliminate_duplicates(self.registered_components)
    
    def get_component_statistics(self) -> Dict[str, Any]:
        """Get comprehensive component registry statistics"""
        return self.registry_manager.get_component_statistics(
            self.registered_components, self.component_factories, 
            self.component_templates, self.duplicate_detector
        )
    
    def cleanup_unused_components(self, days_threshold: int = 30) -> int:
        """Clean up components that haven't been used recently"""
        return self.registry_manager.cleanup_unused_components(self.registered_components, days_threshold)
    
    def export_registry(self) -> Dict[str, Any]:
        """Export the complete registry state"""
        return self.registry_manager.export_registry(
            self.registered_components, self.component_factories,
            self.component_templates, self.usage_statistics,
            self.duplicate_detector
        )
    
    def import_registry(self, registry_data: Dict[str, Any]):
        """Import registry state from external source"""
        return self.registry_manager.import_registry(
            self.registered_components, self.component_templates, registry_data
        )
    
    def get_components_by_category(self, category: str) -> List[str]:
        """Get all component names in a specific category"""
        return self.registry_manager.get_components_by_category(self.registered_components, category)
    
    def get_most_used_components(self, limit: int = 10) -> List[tuple]:
        """Get the most frequently used components"""
        return self.registry_manager.get_most_used_components(self.registered_components, limit)
