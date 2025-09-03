#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Activator (Refactored)
Handles dataset activation, deactivation, and management
Refactored to be under 200 lines
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .dataset_activator_core import DatasetActivatorCore

logger = logging.getLogger(__name__)

class DatasetActivator:
    """Handles dataset activation, deactivation, and management"""
    
    def __init__(self, data_manager, module_name: str):
        # Use the refactored implementation
        self._refactored_activator = DatasetActivatorCore(data_manager, module_name)
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add callback for dataset change events"""
        # Delegate to refactored implementation
        self._refactored_activator.add_dataset_change_callback(callback)
    
    def remove_dataset_change_callback(self, callback: Callable):
        """Remove dataset change callback"""
        # Delegate to refactored implementation
        self._refactored_activator.remove_dataset_change_callback(callback)
    
    def activate_dataset(self, event):
        """Activate a dataset for the current module"""
        # Delegate to refactored implementation
        self._refactored_activator.activate_dataset(event)
    
    def deactivate_dataset(self, event):
        """Deactivate a dataset for the current module"""
        # Delegate to refactored implementation
        self._refactored_activator.deactivate_dataset(event)
    
    def export_dataset(self, event):
        """Export the currently selected dataset"""
        # Delegate to refactored implementation
        self._refactored_activator.export_dataset(event)
    
    def get_active_datasets(self) -> set:
        """Get set of active dataset IDs"""
        # Delegate to refactored implementation
        return self._refactored_activator.get_active_datasets()
    
    def is_dataset_active(self, dataset_id: str) -> bool:
        """Check if a dataset is active"""
        # Delegate to refactored implementation
        return self._refactored_activator.is_dataset_active(dataset_id)
    
    def get_activation_history(self) -> List[Dict]:
        """Get activation/deactivation history"""
        # Delegate to refactored implementation
        return self._refactored_activator.get_activation_history()
    
    def get_activator_statistics(self) -> Dict:
        """Get activator statistics"""
        # Delegate to refactored implementation
        return self._refactored_activator.get_activator_statistics()
    
    def clear_activation_history(self) -> int:
        """Clear activation history and return count"""
        # Delegate to refactored implementation
        return self._refactored_activator.clear_activation_history()
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        # Delegate to refactored implementation
        return self._refactored_activator.get_components()



