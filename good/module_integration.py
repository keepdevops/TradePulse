#!/usr/bin/env python3
"""
TradePulse Modular Panels - Module Integration
Refactored module integration using focused components
"""

import logging
from typing import Dict, List, Optional, Any

from .module_registry import ModuleRegistry
from .shared_components import SharedComponents
from .integration_analyzer import IntegrationAnalyzer
from .integration_statistics import IntegrationStatistics

logger = logging.getLogger(__name__)

class ModuleIntegration:
    """Refactored module integration using focused components"""
    
    def __init__(self):
        # Initialize focused components
        self.module_registry = ModuleRegistry()
        self.shared_components = SharedComponents()
        self.integration_analyzer = IntegrationAnalyzer(self.module_registry)
        self.integration_statistics = IntegrationStatistics(
            self.module_registry, 
            self.shared_components, 
            self.integration_analyzer
        )
        
        logger.info("✅ Refactored module integration system initialized")
    
    def integrate_module(self, module_name: str, module_path: str, module_type: str = "custom"):
        """Integrate a module into the system"""
        try:
            # Use module registry to integrate module
            success = self.module_registry.integrate_module(module_name, module_path, module_type)
            
            if success:
                # Extract and register shared components
                module_info = self.module_registry.get_module_info(module_name)
                if module_info and module_info['module']:
                    shared_components = self.shared_components.extract_shared_components(
                        module_info['module'], module_name
                    )
                    self.shared_components.update_shared_components(module_name, shared_components)
                    
                    # Update module info with shared components
                    module_info['shared_components'] = shared_components
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to integrate module {module_name}: {e}")
            return False
    
    # Delegate to focused components
    def get_shared_component(self, component_name: str) -> Optional[Any]:
        """Get a shared component by name"""
        return self.shared_components.get_shared_component(component_name)
    
    def register_shared_component(self, component_name: str, component: Any):
        """Register a shared component"""
        self.shared_components.register_shared_component(component_name, component)
    
    def get_integrated_modules(self) -> Dict[str, Any]:
        """Get all integrated modules"""
        return self.module_registry.get_integrated_modules()
    
    def get_module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific module"""
        return self.module_registry.get_module_info(module_name)
    
    def remove_module(self, module_name: str) -> bool:
        """Remove an integrated module"""
        try:
            # Remove shared components first
            module_info = self.module_registry.get_module_info(module_name)
            if module_info and 'shared_components' in module_info:
                for component_name in module_info['shared_components']:
                    self.shared_components.remove_shared_component(component_name)
            
            # Remove module
            return self.module_registry.remove_module(module_name)
            
        except Exception as e:
            logger.error(f"Failed to remove module {module_name}: {e}")
            return False
    
    def detect_duplicate_functionality(self) -> Dict[str, List[str]]:
        """Detect duplicate functionality across modules"""
        return self.integration_analyzer.detect_duplicate_functionality()
    
    def consolidate_duplicates(self) -> int:
        """Consolidate duplicate functionality"""
        return self.integration_analyzer.consolidate_duplicates()
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics"""
        return self.integration_statistics.get_integration_statistics()
    
    def export_integration_state(self) -> Dict[str, Any]:
        """Export the complete integration state"""
        return self.integration_statistics.export_integration_state()
    
    def import_integration_state(self, integration_data: Dict[str, Any]):
        """Import integration state from external source"""
        self.integration_statistics.import_integration_state(integration_data)
    
    def get_modules_by_type(self, module_type: str) -> List[str]:
        """Get all module names of a specific type"""
        return self.module_registry.get_modules_by_type(module_type)
    
    def validate_module_integration(self, module_name: str) -> bool:
        """Validate that a module is properly integrated"""
        return self.module_registry.validate_module_integration(module_name)
