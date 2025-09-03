#!/usr/bin/env python3
"""
TradePulse Dataset Selector Component
Allows all modules to browse, select, and activate uploaded datasets
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .dataset_selector_ui_components import DatasetSelectorUIComponents
from .dataset_selector_operations import DatasetSelectorOperations
from .dataset_selector_callbacks import DatasetSelectorCallbacks

logger = logging.getLogger(__name__)

class DatasetSelectorComponent:
    """Component for selecting and managing datasets across all modules"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.selected_datasets = set()
        
        # Initialize components
        self.ui_components = DatasetSelectorUIComponents()
        self.operations = DatasetSelectorOperations(data_manager, module_name)
        self.callbacks = DatasetSelectorCallbacks()
        
        # Create components
        self.create_components()
    
    def create_components(self):
        """Create the dataset selector interface"""
        # Create UI components
        self.search_input = self.ui_components.create_search_input()
        self.type_filter = self.ui_components.create_type_filter()
        self.datasets_list = self.ui_components.create_datasets_list()
        self.dataset_info = self.ui_components.create_dataset_info()
        self.preview_table = self.ui_components.create_preview_table()
        self.activate_button = self.ui_components.create_activate_button()
        self.deactivate_button = self.ui_components.create_deactivate_button()
        self.export_button = self.ui_components.create_export_button()
        self.active_datasets_display = self.ui_components.create_active_datasets_display()
        
        # Set UI component references in operations
        self.operations.dataset_info = self.dataset_info
        self.operations.preview_table = self.preview_table
        self.operations.active_datasets_display = self.active_datasets_display
        self.operations.export_button = self.export_button
        
        # Setup callbacks
        self.callbacks.setup_callbacks(
            self.search_input, self.type_filter, self.datasets_list,
            self.activate_button, self.deactivate_button, self.export_button,
            self.operations
        )
        
        # Initial load
        self.operations.refresh_datasets(self.datasets_list, self.active_datasets_display)
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add a callback for dataset changes"""
        self.callbacks.add_dataset_change_callback(callback)
    
    def get_active_datasets(self) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for this module"""
        return self.operations.get_active_datasets()
    
    def get_component(self):
        """Get the dataset selector component layout"""
        return self.ui_components.create_component_layout(
            self.module_name, self.search_input, self.type_filter,
            self.datasets_list, self.dataset_info, self.preview_table,
            self.activate_button, self.deactivate_button, self.export_button,
            self.active_datasets_display
        )
