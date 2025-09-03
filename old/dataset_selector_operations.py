#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Operations
Handles dataset selector operations and data management
"""

import pandas as pd
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class DatasetSelectorOperations:
    """Handles dataset selector operations and data management"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.selected_datasets = set()
        # UI component references (will be set by main component)
        self.dataset_info = None
        self.preview_table = None
        self.active_datasets_display = None
        self.export_button = None
    
    def refresh_datasets(self, datasets_list, active_datasets_display):
        """Refresh the list of available datasets"""
        try:
            # Get available datasets for this module
            available_datasets = self.data_manager.get_available_datasets(self.module_name)
            
            # Get all datasets if no module-specific filtering
            if not available_datasets:
                available_datasets = self.data_manager.get_available_datasets()
            
            # Create options list
            options = []
            for dataset_id, info in available_datasets.items():
                if hasattr(self.data_manager, 'uploaded_datasets') and dataset_id in self.data_manager.uploaded_datasets:
                    dataset_info = self.data_manager.uploaded_datasets[dataset_id]
                    display_name = f"{info.get('name', dataset_id)} ({dataset_info['shape'][0]} rows × {dataset_info['shape'][1]} cols)"
                    options.append((display_name, dataset_id))
                else:
                    display_name = f"{info.get('name', dataset_id)}"
                    options.append((display_name, dataset_id))
            
            datasets_list.options = options
            
            # Update active datasets display
            self.update_active_datasets_display(active_datasets_display)
            
        except Exception as e:
            logger.error(f"Failed to refresh datasets: {e}")
    
    def on_search_change(self, event, datasets_list, active_datasets_display):
        """Handle search input changes"""
        query = event.new
        if query:
            # Search datasets
            search_results = self.data_manager.search_datasets(query, self.module_name)
            self.update_datasets_list(search_results, datasets_list)
        else:
            # Show all available datasets
            self.refresh_datasets(datasets_list, active_datasets_display)
    
    def on_filter_change(self, event, datasets_list, active_datasets_display):
        """Handle type filter changes"""
        filter_type = event.new
        self.refresh_datasets(datasets_list, active_datasets_display)
    
    def on_dataset_selection(self, event, dataset_info, preview_table, activate_button, deactivate_button, export_button):
        """Handle dataset selection"""
        selected_id = event.new
        if selected_id:
            self.show_dataset_info(selected_id, dataset_info, preview_table, activate_button, deactivate_button, export_button)
        else:
            dataset_info.object = "**Dataset Info:** Select a dataset to view details"
            preview_table.value = pd.DataFrame()
            activate_button.disabled = True
            export_button.disabled = True
    
    def show_dataset_info(self, dataset_id: str, dataset_info, preview_table, activate_button, deactivate_button, export_button):
        """Display information about the selected dataset"""
        try:
            if hasattr(self.data_manager, 'uploaded_datasets') and dataset_id in self.data_manager.uploaded_datasets:
                dataset_data = self.data_manager.uploaded_datasets[dataset_id]
                
                # Create info text
                info_text = f"""
                **Dataset: {dataset_id}**
                
                **Basic Info:**
                - **Shape:** {dataset_data['shape'][0]} rows × {dataset_data['shape'][1]} columns
                - **Columns:** {', '.join(dataset_data['columns'])}
                - **Memory Usage:** {dataset_data['memory_usage'] / 1024:.2f} KB
                - **Upload Time:** {dataset_data['upload_time'].strftime('%Y-%m-%d %H:%M:%S')}
                - **Access Count:** {dataset_data['access_count']}
                
                **Data Types:**
                {', '.join([f'{col}: {dtype}' for col, dtype in dataset_data['dtypes'].items()])}
                
                **Metadata:**
                {', '.join([f'{k}: {v}' for k, v in dataset_data['metadata'].items()])}
                """
                
                dataset_info.object = info_text
                
                # Show preview
                preview_data = dataset_data['data'].head(10)
                preview_table.value = preview_data
                
                # Check if dataset is already active
                if self.is_dataset_active(dataset_id):
                    activate_button.disabled = True
                    deactivate_button.disabled = False
                else:
                    activate_button.disabled = False
                    deactivate_button.disabled = True
                    
                export_button.disabled = False
                    
        except Exception as e:
            logger.error(f"Failed to show dataset info: {e}")
            dataset_info.object = f"**Error:** {str(e)}"
    
    def is_dataset_active(self, dataset_id: str) -> bool:
        """Check if a dataset is active for this module"""
        try:
            active_datasets = self.data_manager.get_active_datasets_for_module(self.module_name)
            return dataset_id in active_datasets
        except Exception as e:
            logger.error(f"Failed to check dataset activation status: {e}")
            return False
    
    def activate_dataset(self, event, datasets_list, active_datasets_display, dataset_info, preview_table, activate_button, deactivate_button):
        """Activate the selected dataset for this module"""
        try:
            selected_id = datasets_list.value
            if selected_id:
                success = self.data_manager.activate_dataset_for_module(selected_id, self.module_name)
                if success:
                    self.selected_datasets.add(selected_id)
                    self.update_active_datasets_display(active_datasets_display)
                    self.show_dataset_info(selected_id, dataset_info, preview_table, activate_button, deactivate_button, None)
                    
                    logger.info(f"✅ Dataset {selected_id} activated for {self.module_name}")
                else:
                    logger.error(f"❌ Failed to activate dataset {selected_id}")
                    
        except Exception as e:
            logger.error(f"Failed to activate dataset: {e}")
    
    def deactivate_dataset(self, event, datasets_list, active_datasets_display, dataset_info, preview_table, activate_button, deactivate_button):
        """Deactivate the selected dataset for this module"""
        try:
            selected_id = datasets_list.value
            if selected_id and selected_id in self.selected_datasets:
                # Remove from active datasets
                self.selected_datasets.discard(selected_id)
                self.update_active_datasets_display(active_datasets_display)
                self.show_dataset_info(selected_id, dataset_info, preview_table, activate_button, deactivate_button, None)
                
                logger.info(f"✅ Dataset {selected_id} deactivated for {self.module_name}")
                
        except Exception as e:
            logger.error(f"Failed to deactivate dataset: {e}")
    
    def export_dataset(self, event, datasets_list):
        """Export the selected dataset"""
        try:
            selected_id = datasets_list.value
            if selected_id:
                logger.info(f"Export functionality would show dialog for {selected_id}")
                
        except Exception as e:
            logger.error(f"Failed to export dataset: {e}")
    
    def update_active_datasets_display(self, active_datasets_display):
        """Update the display of active datasets"""
        try:
            active_datasets = self.data_manager.get_active_datasets_for_module(self.module_name)
            
            if active_datasets:
                display_text = "**Active Datasets:**\n"
                for dataset_id, data in active_datasets.items():
                    display_text += f"- {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols\n"
            else:
                display_text = "**Active Datasets:** None"
            
            active_datasets_display.object = display_text
            
        except Exception as e:
            logger.error(f"Failed to update active datasets display: {e}")
    
    def update_datasets_list(self, search_results, datasets_list):
        """Update datasets list with search results"""
        try:
            options = []
            for dataset_id, info in search_results.items():
                display_name = f"{info.get('name', dataset_id)}"
                options.append((display_name, dataset_id))
            
            datasets_list.options = options
            
        except Exception as e:
            logger.error(f"Failed to update datasets list: {e}")
    
    def get_active_datasets(self) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for this module"""
        try:
            return self.data_manager.get_active_datasets_for_module(self.module_name)
        except Exception as e:
            logger.error(f"Failed to get active datasets: {e}")
            return {}
