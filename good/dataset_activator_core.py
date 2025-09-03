#!/usr/bin/env python3
"""
TradePulse Dataset Activator - Core Functionality
Core dataset activator class with basic functionality
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .dataset_activator_components import DatasetActivatorComponents
from .dataset_activator_operations import DatasetActivatorOperations
from .dataset_activator_management import DatasetActivatorManagement
from .dataset_activator_callbacks import DatasetActivatorCallbacks

logger = logging.getLogger(__name__)

class DatasetActivatorCore:
    """Core dataset activator functionality"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.active_datasets = set()
        self.activation_history = []
        
        # Initialize components
        self.components = DatasetActivatorComponents()
        self.operations = DatasetActivatorOperations()
        self.management = DatasetActivatorManagement()
        self.callbacks = DatasetActivatorCallbacks(self)
        
        # Create UI components
        self._create_ui_components()
    
    def _create_ui_components(self):
        """Create UI components"""
        self.activate_button = pn.widgets.Button(
            name='✅ Activate for Module',
            button_type='primary',
            width=150,
            disabled=True
        )
        
        self.deactivate_button = pn.widgets.Button(
            name='❌ Deactivate',
            button_type='warning',
            width=150,
            disabled=True
        )
        
        self.export_button = pn.widgets.Button(
            name='📤 Export',
            button_type='success',
            width=100,
            disabled=True
        )
        
        self.active_datasets_display = pn.pane.Markdown("**Active Datasets:** None")
        
        # Setup callbacks
        self.activate_button.on_click(self.activate_dataset)
        self.deactivate_button.on_click(self.deactivate_dataset)
        self.export_button.on_click(self.export_dataset)
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add callback for dataset change events"""
        return self.callbacks.add_dataset_change_callback(callback)
    
    def remove_dataset_change_callback(self, callback: Callable):
        """Remove dataset change callback"""
        return self.callbacks.remove_dataset_change_callback(callback)
    
    def activate_dataset(self, event):
        """Activate a dataset for the current module"""
        return self.operations.activate_dataset(
            self._get_selected_dataset(),
            self.active_datasets,
            self.activation_history,
            self.module_name,
            self.callbacks
        )
    
    def deactivate_dataset(self, event):
        """Deactivate a dataset for the current module"""
        return self.operations.deactivate_dataset(
            self._get_selected_dataset(),
            self.active_datasets,
            self.activation_history,
            self.module_name,
            self.callbacks
        )
    
    def export_dataset(self, event):
        """Export the currently selected dataset"""
        return self.operations.export_dataset(
            self._get_selected_dataset(),
            self.data_manager,
            self.module_name,
            self.active_datasets_display
        )
    
    def _get_selected_dataset(self) -> Optional[str]:
        """Get the currently selected dataset ID"""
        # This method should be implemented to get the selected dataset from the browser
        # For now, return None - will be connected by the main component
        return None
    
    def get_active_datasets(self) -> set:
        """Get set of active dataset IDs"""
        return self.active_datasets.copy()
    
    def is_dataset_active(self, dataset_id: str) -> bool:
        """Check if a dataset is active"""
        return dataset_id in self.active_datasets
    
    def get_activation_history(self) -> List[Dict]:
        """Get activation/deactivation history"""
        return self.activation_history.copy()
    
    def get_activator_statistics(self) -> Dict:
        """Get activator statistics"""
        return self.operations.get_activator_statistics(
            self.activation_history,
            self.active_datasets,
            self.callbacks
        )
    
    def clear_activation_history(self) -> int:
        """Clear activation history and return count"""
        return self.operations.clear_activation_history(self.activation_history)
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'activate_button': self.activate_button,
            'deactivate_button': self.deactivate_button,
            'export_button': self.export_button,
            'active_datasets_display': self.active_datasets_display
        }

