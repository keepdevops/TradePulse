#!/usr/bin/env python3
"""
TradePulse Modular Panels - Integration Analyzer
Handles integration analysis, duplicate detection, and consolidation
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class IntegrationAnalyzer:
    """Handles integration analysis, duplicate detection, and consolidation"""
    
    def __init__(self, module_registry):
        self.module_registry = module_registry
    
    def detect_duplicate_functionality(self) -> Dict[str, List[str]]:
        """Detect duplicate functionality across modules"""
        try:
            duplicates = {}
            
            # Group modules by type
            module_types = {}
            for name, info in self.module_registry.integrated_modules.items():
                module_type = info['type']
                if module_type not in module_types:
                    module_types[module_type] = []
                module_types[module_type].append(name)
            
            # Find potential duplicates
            for module_type, names in module_types.items():
                if len(names) > 1:
                    duplicates[module_type] = names
            
            if duplicates:
                logger.warning(f"⚠️ Found {len(duplicates)} duplicate module types")
            else:
                logger.info("✅ No duplicate functionality detected")
            
            return duplicates
            
        except Exception as e:
            logger.error(f"Failed to detect duplicate functionality: {e}")
            return {}
    
    def consolidate_duplicates(self) -> int:
        """Consolidate duplicate functionality"""
        try:
            duplicates = self.detect_duplicate_functionality()
            consolidated_count = 0
            
            for module_type, names in duplicates.items():
                if len(names) > 1:
                    # Keep the first module, remove others
                    keep_name = names[0]
                    remove_names = names[1:]
                    
                    for remove_name in remove_names:
                        if self.module_registry.remove_module(remove_name):
                            consolidated_count += 1
                    
                    logger.info(f"✅ Consolidated {len(remove_names)} duplicate {module_type} modules, keeping {keep_name}")
            
            return consolidated_count
            
        except Exception as e:
            logger.error(f"Failed to consolidate duplicates: {e}")
            return 0
    
    def analyze_module_dependencies(self) -> Dict[str, List[str]]:
        """Analyze module dependencies"""
        try:
            dependencies = {}
            
            for name, info in self.module_registry.integrated_modules.items():
                module_deps = info.get('dependencies', [])
                if module_deps:
                    dependencies[name] = module_deps
            
            return dependencies
            
        except Exception as e:
            logger.error(f"Failed to analyze module dependencies: {e}")
            return {}
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies between modules"""
        try:
            # This is a simplified implementation
            # In a real system, you'd use a proper graph algorithm
            circular_deps = []
            
            # For now, just return empty list
            # This would implement a proper cycle detection algorithm
            
            return circular_deps
            
        except Exception as e:
            logger.error(f"Failed to find circular dependencies: {e}")
            return []
    
    def get_module_health_score(self, module_name: str) -> float:
        """Calculate a health score for a module (0.0 to 1.0)"""
        try:
            if module_name not in self.module_registry.integrated_modules:
                return 0.0
            
            module_info = self.module_registry.integrated_modules[module_name]
            score = 1.0
            
            # Deduct points for various issues
            if module_info['status'] != 'active':
                score -= 0.5
            
            if not module_info['dependencies']:
                score -= 0.1
            
            if not module_info['shared_components']:
                score -= 0.2
            
            # Ensure score is between 0.0 and 1.0
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"Failed to calculate module health score: {e}")
            return 0.0
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get overall system health summary"""
        try:
            total_modules = len(self.module_registry.integrated_modules)
            
            if total_modules == 0:
                return {'overall_health': 0.0, 'issues': ['No modules integrated']}
            
            # Calculate average health score
            total_health = 0.0
            issues = []
            
            for module_name in self.module_registry.integrated_modules:
                health_score = self.get_module_health_score(module_name)
                total_health += health_score
                
                if health_score < 0.5:
                    issues.append(f"Module {module_name} has low health score: {health_score:.2f}")
            
            avg_health = total_health / total_modules
            
            # Check for duplicates
            duplicates = self.detect_duplicate_functionality()
            if duplicates:
                issues.append(f"Found {len(duplicates)} duplicate module types")
                avg_health *= 0.8  # Penalize for duplicates
            
            return {
                'overall_health': avg_health,
                'total_modules': total_modules,
                'issues': issues,
                'duplicates_detected': len(duplicates)
            }
            
        except Exception as e:
            logger.error(f"Failed to get system health summary: {e}")
            return {'overall_health': 0.0, 'issues': [f'Error: {e}']}
