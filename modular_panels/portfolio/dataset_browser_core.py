#!/usr/bin/env python3
"""
TradePulse Dataset Browser - Core
Core dataset browsing functionality
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)

class DatasetBrowser:
    """Handles dataset browsing, searching, and filtering operations"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.search_history = []
        self.filter_history = []
        
        # Create UI components
        self.search_input = pn.widgets.TextInput(
            name='🔍 Search Datasets',
            placeholder='Search by name, columns, or content...',
            width=250
        )
        
        self.type_filter = pn.widgets.Select(
            name='📁 Type Filter',
            options=['All Types', 'Uploaded', 'Price Data', 'ML Predictions'],
            value='All Types',
            width=150
        )
        
        self.datasets_list = pn.widgets.Select(
            name='📊 Available Datasets',
            options=[],
            size=8,
            width=300
        )
        
        # Setup callbacks
        self.search_input.param.watch(self.on_search_change, 'value')
        self.type_filter.param.watch(self.on_filter_change, 'value')
        self.datasets_list.param.watch(self.on_dataset_selection, 'value')
        
        # Initial load
        self.refresh_datasets()
    
    def refresh_datasets(self):
        """Refresh the list of available datasets"""
        try:
            # Get available datasets for this module
            available_datasets = self.data_manager.get_available_datasets(self.module_name)
            
            if not available_datasets:
                self.datasets_list.options = ['No datasets available']
                self.datasets_list.value = 'No datasets available'
                return
            
            # Format dataset options for display
            dataset_options = []
            for dataset in available_datasets:
                dataset_id = dataset.get('id', 'Unknown')
                dataset_name = dataset.get('name', 'Unnamed')
                dataset_type = dataset.get('type', 'Unknown')
                
                # Create display option
                display_option = f"{dataset_name} ({dataset_type}) - {dataset_id}"
                dataset_options.append(display_option)
            
            self.datasets_list.options = dataset_options
            
            if dataset_options:
                self.datasets_list.value = dataset_options[0]
            
            logger.info(f"✅ Refreshed datasets: {len(dataset_options)} available for {self.module_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to refresh datasets: {e}")
            self.datasets_list.options = ['Error loading datasets']
    
    def on_search_change(self, event):
        """Handle search input changes"""
        try:
            search_query = event.new
            if search_query:
                logger.info(f"🔍 Searching datasets for: {search_query}")
                
                # Record search
                self._record_search(search_query)
                
                # Perform search
                search_results = self.data_manager.search_datasets(search_query)
                
                if search_results:
                    # Update datasets list with search results
                    self._update_datasets_from_search(search_results)
                else:
                    logger.info(f"📁 No search results for: {search_query}")
                    self.datasets_list.options = [f'No results for "{search_query}"']
            else:
                # Clear search, show all datasets
                self.refresh_datasets()
                
        except Exception as e:
            logger.error(f"❌ Search change handling failed: {e}")
    
    def on_filter_change(self, event):
        """Handle type filter changes"""
        try:
            filter_type = event.new
            if filter_type == 'All Types':
                self.refresh_datasets()
                return
            
            logger.info(f"📁 Filtering datasets by type: {filter_type}")
            
            # Record filter
            self._record_filter(filter_type)
            
            # Apply filter
            self._apply_type_filter(filter_type)
            
        except Exception as e:
            logger.error(f"❌ Filter change handling failed: {e}")
    
    def on_dataset_selection(self, event):
        """Handle dataset selection"""
        try:
            selected_dataset = event.new
            if selected_dataset and selected_dataset != 'No datasets available':
                dataset_id = self._extract_dataset_id(selected_dataset)
                if dataset_id:
                    logger.info(f"📊 Dataset selected: {dataset_id}")
                    # Trigger dataset selection callback if available
                    if hasattr(self, 'on_dataset_selected'):
                        self.on_dataset_selected(dataset_id)
                        
        except Exception as e:
            logger.error(f"❌ Dataset selection handling failed: {e}")
    
    def _update_datasets_from_search(self, search_results: List[Dict]):
        """Update datasets list from search results"""
        try:
            dataset_options = []
            for result in search_results:
                dataset_id = result.get('id', 'Unknown')
                dataset_name = result.get('name', 'Unnamed')
                dataset_type = result.get('type', 'Unknown')
                
                display_option = f"{dataset_name} ({dataset_type}) - {dataset_id}"
                dataset_options.append(display_option)
            
            self.datasets_list.options = dataset_options
            
            if dataset_options:
                self.datasets_list.value = dataset_options[0]
                
        except Exception as e:
            logger.error(f"❌ Failed to update datasets from search: {e}")
    
    def _apply_type_filter(self, filter_type: str):
        """Apply type filter to datasets"""
        try:
            if hasattr(self.data_manager, 'get_datasets_by_type'):
                filtered_datasets = self.data_manager.get_datasets_by_type(filter_type.lower())
            else:
                # Fallback to filtering from available datasets
                available_datasets = self.data_manager.get_available_datasets(self.module_name)
                filtered_datasets = [ds for ds in available_datasets if ds.get('type', '').lower() == filter_type.lower()]
            
            if filtered_datasets:
                self._update_datasets_from_search(filtered_datasets)
                logger.info(f"✅ Type filter applied: {len(filtered_datasets)} datasets of type {filter_type}")
            else:
                logger.info(f"📁 No datasets found for type: {filter_type}")
                self.datasets_list.options = [f'No {filter_type} datasets available']
                
        except Exception as e:
            logger.error(f"Failed to apply type filter: {e}")
    
    def _extract_dataset_id(self, display_option: str) -> Optional[str]:
        """Extract dataset ID from display option string"""
        try:
            # Format: "Name (Type) - ID"
            if ' - ' in display_option:
                return display_option.split(' - ')[-1]
            return None
        except Exception as e:
            logger.error(f"Failed to extract dataset ID: {e}")
            return None
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'search_input': self.search_input,
            'type_filter': self.type_filter,
            'datasets_list': self.datasets_list
        }

# Global instance
dataset_browser_core = DatasetBrowser(None, 'default')
