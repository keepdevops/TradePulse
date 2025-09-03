#!/usr/bin/env python3
"""
TradePulse Modular Panels - Registry Manager
Handles component registry management operations
"""

import pandas as pd
from typing import Dict, List, Optional, Callable, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RegistryManager:
    """Handles component registry management operations"""
    
    def register_component(self, registered_components: Dict, name: str, component: Any, category: str = "general"):
        """Register a component in the registry"""
        try:
            if name in registered_components:
                logger.warning(f"⚠️ Component {name} already registered, updating...")
            
            registered_components[name] = {
                'component': component,
                'category': category,
                'registration_time': datetime.now(),
                'usage_count': 0,
                'last_used': None
            }
            
            logger.info(f"✅ Component {name} registered in category {category}")
            
        except Exception as e:
            logger.error(f"Failed to register component {name}: {e}")
    
    def unregister_component(self, registered_components: Dict, name: str):
        """Unregister a component from the registry"""
        try:
            if name in registered_components:
                del registered_components[name]
                logger.info(f"✅ Component {name} unregistered")
            else:
                logger.warning(f"⚠️ Component {name} not found in registry")
                
        except Exception as e:
            logger.error(f"Failed to unregister component {name}: {e}")
    
    def get_component(self, registered_components: Dict, name: str) -> Optional[Any]:
        """Get a registered component"""
        try:
            if name in registered_components:
                # Update usage statistics
                registered_components[name]['usage_count'] += 1
                registered_components[name]['last_used'] = datetime.now()
                
                return registered_components[name]['component']
            else:
                logger.warning(f"⚠️ Component {name} not found in registry")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get component {name}: {e}")
            return None
    
    def create_component(self, component_factories: Dict, type_name: str, **kwargs) -> Optional[Any]:
        """Create a component using a registered factory"""
        try:
            if type_name in component_factories:
                component = component_factories[type_name](**kwargs)
                logger.info(f"✅ Component of type {type_name} created")
                return component
            else:
                logger.error(f"❌ Component type {type_name} not registered")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create component of type {type_name}: {e}")
            return None
    
    def register_component_template(self, component_templates: Dict, template_name: str, template_data: Dict):
        """Register a component template for reuse"""
        try:
            component_templates[template_name] = template_data
            logger.info(f"✅ Component template {template_name} registered")
            
        except Exception as e:
            logger.error(f"Failed to register template {template_name}: {e}")
    
    def create_from_template(self, component_templates: Dict, component_factories: Dict, template_name: str, **kwargs) -> Optional[Any]:
        """Create a component from a template"""
        try:
            template = component_templates.get(template_name)
            if template:
                # Merge template with provided kwargs
                component_data = template.copy()
                component_data.update(kwargs)
                
                # Create component using template data
                component_type = component_data.get('type', 'general')
                return self.create_component(component_factories, component_type, **component_data)
            else:
                logger.error(f"❌ Template {template_name} not found")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create from template {template_name}: {e}")
            return None
    
    def get_component_statistics(self, registered_components: Dict, component_factories: Dict, 
                               component_templates: Dict, duplicate_detector) -> Dict[str, Any]:
        """Get comprehensive component registry statistics"""
        try:
            total_components = len(registered_components)
            total_types = len(component_factories)
            total_templates = len(component_templates)
            
            # Calculate usage statistics
            total_usage = sum(info['usage_count'] for info in registered_components.values())
            avg_usage = total_usage / total_components if total_components > 0 else 0
            
            # Get category breakdown
            categories = {}
            for info in registered_components.values():
                category = info['category']
                categories[category] = categories.get(category, 0) + 1
            
            return {
                'total_components': total_components,
                'total_types': total_types,
                'total_templates': total_templates,
                'total_usage': total_usage,
                'average_usage': avg_usage,
                'categories': categories,
                'duplicates_detected': len(duplicate_detector.duplicate_detection),
                'last_duplicate_check': getattr(duplicate_detector, '_last_duplicate_check', None)
            }
            
        except Exception as e:
            logger.error(f"Failed to get registry statistics: {e}")
            return {}
    
    def cleanup_unused_components(self, registered_components: Dict, days_threshold: int = 30) -> int:
        """Clean up components that haven't been used recently"""
        try:
            cleanup_count = 0
            threshold_date = datetime.now() - pd.Timedelta(days=days_threshold)
            
            components_to_remove = []
            for name, info in registered_components.items():
                if info['last_used'] and info['last_used'] < threshold_date:
                    components_to_remove.append(name)
            
            for name in components_to_remove:
                self.unregister_component(registered_components, name)
                cleanup_count += 1
            
            if cleanup_count > 0:
                logger.info(f"🗑️ Cleaned up {cleanup_count} unused components")
            
            return cleanup_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup unused components: {e}")
            return 0
    
    def export_registry(self, registered_components: Dict, component_factories: Dict,
                       component_templates: Dict, usage_statistics: Dict, duplicate_detector) -> Dict[str, Any]:
        """Export the complete registry state"""
        try:
            export_data = {
                'registered_components': registered_components.copy(),
                'component_factories': list(component_factories.keys()),
                'component_templates': component_templates.copy(),
                'usage_statistics': usage_statistics.copy(),
                'duplicate_detection': duplicate_detector.duplicate_detection.copy(),
                'export_timestamp': datetime.now()
            }
            
            logger.info("📤 Component registry exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export registry: {e}")
            return {}
    
    def import_registry(self, registered_components: Dict, component_templates: Dict, registry_data: Dict[str, Any]):
        """Import registry state from external source"""
        try:
            if 'registered_components' in registry_data:
                registered_components.update(registry_data['registered_components'])
            
            if 'component_templates' in registry_data:
                component_templates.update(registry_data['component_templates'])
            
            logger.info("📥 Component registry imported")
            
        except Exception as e:
            logger.error(f"Failed to import registry: {e}")
    
    def get_components_by_category(self, registered_components: Dict, category: str) -> List[str]:
        """Get all component names in a specific category"""
        try:
            return [name for name, info in registered_components.items() 
                   if info['category'] == category]
        except Exception as e:
            logger.error(f"Failed to get components by category: {e}")
            return []
    
    def get_most_used_components(self, registered_components: Dict, limit: int = 10) -> List[tuple]:
        """Get the most frequently used components"""
        try:
            sorted_components = sorted(
                registered_components.items(),
                key=lambda x: x[1]['usage_count'],
                reverse=True
            )
            
            return [(name, info['usage_count']) for name, info in sorted_components[:limit]]
            
        except Exception as e:
            logger.error(f"Failed to get most used components: {e}")
            return []
