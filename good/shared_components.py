#!/usr/bin/env python3
"""
TradePulse Modular Panels - Shared Components
Handles shared component management and registry
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class SharedComponents:
    """Handles shared component management and registry"""
    
    def __init__(self):
        self.shared_components = {}
        self._setup_shared_components()
    
    def _setup_shared_components(self):
        """Setup shared component registry"""
        try:
            # Setup shared component registry
            self.shared_components = {
                'data_manager': None,
                'chart_manager': None,
                'portfolio_manager': None,
                'ai_manager': None,
                'alert_manager': None
            }
            
            logger.info("✅ Shared components registry initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup shared components: {e}")
    
    def extract_shared_components(self, module: Any, module_name: str) -> Dict[str, Any]:
        """Extract shared components from a module"""
        try:
            shared_components = {}
            
            # Look for common component patterns
            component_patterns = {
                'manager': ['Manager', 'Handler', 'Controller'],
                'processor': ['Processor', 'Processor', 'Transformer'],
                'fetcher': ['Fetcher', 'Loader', 'Retriever'],
                'optimizer': ['Optimizer', 'Optimizer', 'Solver']
            }
            
            for pattern, suffixes in component_patterns.items():
                for suffix in suffixes:
                    for attr_name in dir(module):
                        if attr_name.endswith(suffix) and not attr_name.startswith('_'):
                            try:
                                component = getattr(module, attr_name)
                                if callable(component):
                                    shared_components[f"{pattern}_{attr_name}"] = component
                            except Exception:
                                continue
            
            return shared_components
            
        except Exception as e:
            logger.error(f"Failed to extract shared components: {e}")
            return {}
    
    def update_shared_components(self, module_name: str, shared_components: Dict[str, Any]):
        """Update shared components registry from a module"""
        try:
            for component_name, component in shared_components.items():
                if component_name not in self.shared_components:
                    self.shared_components[component_name] = component
                    logger.info(f"✅ Shared component {component_name} registered from {module_name}")
            
        except Exception as e:
            logger.error(f"Failed to update shared components: {e}")
    
    def get_shared_component(self, component_name: str) -> Optional[Any]:
        """Get a shared component by name"""
        return self.shared_components.get(component_name)
    
    def register_shared_component(self, component_name: str, component: Any):
        """Register a shared component"""
        try:
            self.shared_components[component_name] = component
            logger.info(f"✅ Shared component {component_name} registered")
            
        except Exception as e:
            logger.error(f"Failed to register shared component: {e}")
    
    def remove_shared_component(self, component_name: str) -> bool:
        """Remove a shared component"""
        try:
            if component_name in self.shared_components:
                del self.shared_components[component_name]
                logger.info(f"✅ Shared component {component_name} removed")
                return True
            else:
                logger.warning(f"⚠️ Shared component {component_name} not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to remove shared component {component_name}: {e}")
            return False
    
    def get_all_shared_components(self) -> Dict[str, Any]:
        """Get all shared components"""
        return self.shared_components.copy()
    
    def get_shared_component_names(self) -> List[str]:
        """Get list of all shared component names"""
        return list(self.shared_components.keys())
    
    def clear_shared_components(self):
        """Clear all shared components"""
        try:
            self.shared_components.clear()
            self._setup_shared_components()
            logger.info("✅ All shared components cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear shared components: {e}")
