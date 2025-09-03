#!/usr/bin/env python3
"""
TradePulse Modular Panels - Duplicate Detector
Handles duplicate component detection and elimination
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DuplicateDetector:
    """Handles duplicate component detection and elimination"""
    
    def __init__(self):
        self.duplicate_detection = {}
    
    def detect_duplicates(self, registered_components: Dict) -> Dict[str, List[str]]:
        """Detect duplicate component implementations"""
        try:
            duplicates = {}
            
            # Group components by type
            component_types = {}
            for name, info in registered_components.items():
                component_type = type(info['component']).__name__
                if component_type not in component_types:
                    component_types[component_type] = []
                component_types[component_type].append(name)
            
            # Find duplicates
            for component_type, names in component_types.items():
                if len(names) > 1:
                    duplicates[component_type] = names
            
            self.duplicate_detection = duplicates
            
            if duplicates:
                logger.warning(f"⚠️ Found {len(duplicates)} duplicate component types")
            else:
                logger.info("✅ No duplicate components detected")
            
            return duplicates
            
        except Exception as e:
            logger.error(f"Failed to detect duplicates: {e}")
            return {}
    
    def eliminate_duplicates(self, registered_components: Dict) -> int:
        """Eliminate duplicate components by consolidating them"""
        try:
            duplicates = self.detect_duplicates(registered_components)
            eliminated_count = 0
            
            for component_type, names in duplicates.items():
                if len(names) > 1:
                    # Keep the first component, remove others
                    keep_name = names[0]
                    remove_names = names[1:]
                    
                    for remove_name in remove_names:
                        if remove_name in registered_components:
                            del registered_components[remove_name]
                            eliminated_count += 1
                    
                    logger.info(f"✅ Eliminated {len(remove_names)} duplicate {component_type} components, keeping {keep_name}")
            
            return eliminated_count
            
        except Exception as e:
            logger.error(f"Failed to eliminate duplicates: {e}")
            return 0
