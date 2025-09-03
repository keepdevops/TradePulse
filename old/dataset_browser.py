#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Browser
Handles dataset browsing, searching, and filtering operations
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
                    logger.info(f"✅ Search found {len(search_results)} datasets")
                else:
                    logger.info("🔍 No datasets found matching search query")
                    self.datasets_list.options = ['No matching datasets']
            else:
                # Reset to all datasets if search is cleared
                self.refresh_datasets()
                
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
    
    def on_filter_change(self, event):
        """Handle filter changes"""
        try:
            filter_type = event.new
            logger.info(f"📁 Filtering datasets by type: {filter_type}")
            
            # Record filter
            self._record_filter(filter_type)
            
            if filter_type == 'All Types':
                self.refresh_datasets()
            else:
                # Apply type filter
                self._apply_type_filter(filter_type)
                
        except Exception as e:
            logger.error(f"❌ Filter failed: {e}")
    
    def on_dataset_selection(self, event):
        """Handle dataset selection changes"""
        try:
            selected_option = event.new
            if selected_option and selected_option != 'No datasets available' and 'Error' not in selected_option:
                # Extract dataset ID from display option
                dataset_id = self._extract_dataset_id(selected_option)
                if dataset_id:
                    logger.info(f"📊 Dataset selected: {dataset_id}")
                    return dataset_id
            return None
            
        except Exception as e:
            logger.error(f"❌ Dataset selection failed: {e}")
            return None
    
    def _update_datasets_from_search(self, search_results: List[Dict]):
        """Update datasets list with search results"""
        try:
            dataset_options = []
            for dataset in search_results:
                dataset_id = dataset.get('id', 'Unknown')
                dataset_name = dataset.get('name', 'Unnamed')
                dataset_type = dataset.get('type', 'Unknown')
                
                display_option = f"{dataset_name} ({dataset_type}) - {dataset_id}"
                dataset_options.append(display_option)
            
            self.datasets_list.options = dataset_options
            
            if dataset_options:
                self.datasets_list.value = dataset_options[0]
                
        except Exception as e:
            logger.error(f"Failed to update datasets from search: {e}")
    
    def _apply_type_filter(self, filter_type: str):
        """Apply type filter to datasets"""
        try:
            # Get datasets by type
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
    
    def _record_search(self, query: str):
        """Record search operation"""
        try:
            search_record = {
                'timestamp': pd.Timestamp.now(),
                'query': query,
                'module': self.module_name
            }
            self.search_history.append(search_record)
            
        except Exception as e:
            logger.error(f"Failed to record search: {e}")
    
    def _record_filter(self, filter_type: str):
        """Record filter operation"""
        try:
            filter_record = {
                'timestamp': pd.Timestamp.now(),
                'filter_type': filter_type,
                'module': self.module_name
            }
            self.filter_history.append(filter_record)
            
        except Exception as e:
            logger.error(f"Failed to record filter: {e}")
    
    def get_search_history(self) -> List[Dict]:
        """Get search history"""
        return self.search_history.copy()
    
    def get_filter_history(self) -> List[Dict]:
        """Get filter history"""
        return self.filter_history.copy()
    
    def get_browser_statistics(self) -> Dict:
        """Get browser statistics"""
        try:
            return {
                'total_searches': len(self.search_history),
                'total_filters': len(self.filter_history),
                'available_datasets': len(self.data_manager.get_available_datasets(self.module_name)),
                'last_search': self.search_history[-1]['timestamp'] if self.search_history else None,
                'last_filter': self.filter_history[-1]['timestamp'] if self.filter_history else None
            }
        except Exception as e:
            logger.error(f"Failed to get browser statistics: {e}")
            return {}
    
    def clear_history(self) -> int:
        """Clear search and filter history"""
        try:
            search_count = len(self.search_history)
            filter_count = len(self.filter_history)
            
            self.search_history.clear()
            self.filter_history.clear()
            
            logger.info(f"🗑️ Cleared {search_count} searches and {filter_count} filters")
            return search_count + filter_count
            
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
            return 0
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'search_input': self.search_input,
            'type_filter': self.type_filter,
            'datasets_list': self.datasets_list
        }
