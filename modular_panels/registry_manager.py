#!/usr/bin/env python3
"""
TradePulse Modular Panels - Registry Manager
Manages component registration and lifecycle
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Callable, Any, Type
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RegistryManager:
    """Manages component registration and lifecycle"""
    
    def __init__(self):
        self.registration_history = []
        self.component_metadata = {}
        
    def register_component(self, registry: Dict, name: str, component: Any, category: str = "general") -> bool:
        """Register a component in the registry"""
        try:
            if name in registry:
                logger.warning(f"⚠️ Component {name} already registered, updating...")
            
            registry[name] = component
            self.component_metadata[name] = {
                'category': category,
                'registered_at': datetime.now(),
                'type': type(component).__name__
            }
            self.registration_history.append({
                'action': 'register',
                'name': name,
                'category': category,
                'timestamp': datetime.now()
            })
            
            logger.info(f"✅ Component {name} registered in category {category}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register component {name}: {e}")
            return False
    
    def unregister_component(self, registry: Dict, name: str) -> bool:
        """Unregister a component from the registry"""
        try:
            if name in registry:
                del registry[name]
                if name in self.component_metadata:
                    del self.component_metadata[name]
                
                self.registration_history.append({
                    'action': 'unregister',
                    'name': name,
                    'timestamp': datetime.now()
                })
                
                logger.info(f"✅ Component {name} unregistered")
                return True
            else:
                logger.warning(f"⚠️ Component {name} not found in registry")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to unregister component {name}: {e}")
            return False
    
    def get_component(self, registry: Dict, name: str) -> Optional[Any]:
        """Get a registered component"""
        try:
            component = registry.get(name)
            if component:
                logger.info(f"📋 Retrieved component {name}")
                return component
            else:
                logger.warning(f"⚠️ Component {name} not found")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get component {name}: {e}")
            return None
    
    def create_component(self, factories: Dict, type_name: str, **kwargs) -> Optional[Any]:
        """Create a component using a registered factory"""
        try:
            if type_name not in factories:
                logger.error(f"❌ Component type {type_name} not registered")
                return None
            
            factory = factories[type_name]
            component = factory(**kwargs)
            
            logger.info(f"✅ Created component of type {type_name}")
            return component
            
        except Exception as e:
            logger.error(f"❌ Failed to create component of type {type_name}: {e}")
            return None
    
    def register_component_template(self, templates: Dict, template_name: str, template_data: Dict) -> bool:
        """Register a component template for reuse"""
        try:
            templates[template_name] = template_data
            logger.info(f"✅ Template {template_name} registered")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register template {template_name}: {e}")
            return False
    
    def create_from_template(self, templates: Dict, factories: Dict, template_name: str, **kwargs) -> Optional[Any]:
        """Create a component from a template"""
        try:
            if template_name not in templates:
                logger.error(f"❌ Template {template_name} not found")
                return None
            
            template = templates[template_name]
            component_type = template.get('type')
            
            if component_type not in factories:
                logger.error(f"❌ Component type {component_type} not registered")
                return None
            
            # Merge template data with provided kwargs
            merged_kwargs = {**template.get('defaults', {}), **kwargs}
            component = factories[component_type](**merged_kwargs)
            
            logger.info(f"✅ Created component from template {template_name}")
            return component
            
        except Exception as e:
            logger.error(f"❌ Failed to create component from template {template_name}: {e}")
            return None
    
    def get_component_statistics(self, registry: Dict, factories: Dict, templates: Dict, duplicate_detector: Any) -> Dict[str, Any]:
        """Get comprehensive component registry statistics"""
        try:
            stats = {
                'total_components': len(registry),
                'total_factories': len(factories),
                'total_templates': len(templates),
                'categories': {},
                'recent_registrations': self.registration_history[-10:] if self.registration_history else [],
                'duplicate_analysis': duplicate_detector.detect_duplicates(registry) if duplicate_detector else {}
            }
            
            # Count components by category
            for name, metadata in self.component_metadata.items():
                category = metadata.get('category', 'unknown')
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            logger.info(f"📊 Registry statistics: {stats['total_components']} components, {stats['total_factories']} factories")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get registry statistics: {e}")
            return {}
