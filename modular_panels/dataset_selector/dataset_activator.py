#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Activator
Main dataset activator component for dataset selection
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any

from ..base_component import BaseComponent
from ..dataset_selector_operations import DatasetSelectorOperations

logger = logging.getLogger(__name__)

class DatasetActivator(BaseComponent):
    """Dataset activator component for dataset selection and activation"""
    
    def __init__(self, data_manager):
        super().__init__(data_manager, None)
        self.operations = DatasetSelectorOperations(data_manager)
        self.active_datasets = {}
        
        # Create UI components
        self.dataset_list = pn.widgets.Select(
            name='📊 Available Datasets',
            options=[],
            size=8,
            width=300
        )
        
        self.activate_button = pn.widgets.Button(
            name='✅ Activate',
            button_type='primary',
            width=100
        )
        
        self.deactivate_button = pn.widgets.Button(
            name='❌ Deactivate',
            button_type='danger',
            width=100
        )
        
        self.status_display = pn.pane.Markdown("**Status:** No datasets activated")
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Load initial datasets
        self.refresh_datasets()
        
        logger.info("🔧 Dataset Activator initialized")
    
    def setup_callbacks(self):
        """Setup component callbacks"""
        self.activate_button.on_click(self.on_activate_dataset)
        self.deactivate_button.on_click(self.on_deactivate_dataset)
        self.dataset_list.param.watch(self.on_dataset_selection, 'value')
    
    def refresh_datasets(self):
        """Refresh the list of available datasets"""
        try:
            datasets = self.operations.get_available_datasets()
            options = []
            
            for dataset in datasets:
                display_name = f"{dataset['name']} ({dataset['rows']} rows, {dataset['columns']} cols)"
                options.append((display_name, dataset['id']))
            
            self.dataset_list.options = options
            
            if options:
                logger.info(f"✅ Loaded {len(options)} datasets")
            else:
                logger.info("ℹ️ No datasets available")
                
        except Exception as e:
            logger.error(f"❌ Error refreshing datasets: {e}")
    
    def on_dataset_selection(self, event):
        """Handle dataset selection change"""
        try:
            dataset_id = event.new
            if dataset_id:
                datasets = self.operations.get_available_datasets()
                dataset_info = next((d for d in datasets if d['id'] == dataset_id), None)
                
                if dataset_info:
                    status_text = f"""
                    **Selected Dataset:**
                    
                    **Name:** {dataset_info['name']}
                    **Rows:** {dataset_info['rows']:,}
                    **Columns:** {dataset_info['columns']}
                    **Type:** {dataset_info['type']}
                    **Status:** {'✅ Active' if dataset_id in self.active_datasets else '⏸️ Inactive'}
                    """
                    self.status_display.object = status_text
                else:
                    self.status_display.object = "**Status:** Dataset not found"
            else:
                self.status_display.object = "**Status:** No dataset selected"
                
        except Exception as e:
            logger.error(f"❌ Error updating dataset status: {e}")
            self.status_display.object = f"**Error:** {str(e)}"
    
    def on_activate_dataset(self, event):
        """Handle dataset activation"""
        try:
            dataset_id = self.dataset_list.value
            if not dataset_id:
                logger.warning("⚠️ No dataset selected")
                return
            
            result = self.operations.select_dataset(dataset_id, 'default')
            
            if result['success']:
                self.active_datasets[dataset_id] = {
                    'activated_at': result.get('selection_time', 'Unknown'),
                    'rows': result.get('rows', 0),
                    'columns': result.get('columns', 0)
                }
                logger.info(f"✅ Dataset {dataset_id} activated")
                
                # Update UI
                self.activate_button.button_type = 'success'
                self.activate_button.name = '✅ Activated'
                
                # Update status
                self.on_dataset_selection(type('Event', (), {'new': dataset_id})())
                
                # Show success message
                pn.state.notifications.success(f"Dataset {dataset_id} activated successfully")
            else:
                logger.error(f"❌ Failed to activate dataset: {result.get('error', 'Unknown error')}")
                pn.state.notifications.error(f"Failed to activate dataset: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Error activating dataset: {e}")
            pn.state.notifications.error(f"Error activating dataset: {str(e)}")
    
    def on_deactivate_dataset(self, event):
        """Handle dataset deactivation"""
        try:
            dataset_id = self.dataset_list.value
            if not dataset_id:
                logger.warning("⚠️ No dataset selected")
                return
            
            if dataset_id not in self.active_datasets:
                logger.warning("⚠️ Dataset not active")
                return
            
            result = self.operations.deselect_dataset(dataset_id, 'default')
            
            if result['success']:
                del self.active_datasets[dataset_id]
                logger.info(f"✅ Dataset {dataset_id} deactivated")
                
                # Update UI
                self.activate_button.button_type = 'primary'
                self.activate_button.name = '✅ Activate'
                
                # Update status
                self.on_dataset_selection(type('Event', (), {'new': dataset_id})())
                
                # Show success message
                pn.state.notifications.success(f"Dataset {dataset_id} deactivated successfully")
            else:
                logger.error(f"❌ Failed to deactivate dataset: {result.get('error', 'Unknown error')}")
                pn.state.notifications.error(f"Failed to deactivate dataset: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Error deactivating dataset: {e}")
            pn.state.notifications.error(f"Error deactivating dataset: {str(e)}")
    
    def create_panel(self) -> pn.Column:
        """Create the component panel"""
        return pn.Column(
            pn.pane.Markdown("## 📊 Dataset Activator"),
            pn.Row(
                self.dataset_list,
                pn.Spacer(width=20),
                pn.Column(
                    self.activate_button,
                    self.deactivate_button
                )
            ),
            self.status_display,
            width=400
        )
    
    def get_active_datasets(self) -> Dict[str, Any]:
        """Get currently active datasets"""
        return self.active_datasets.copy()
    
    def get_component_stats(self) -> Dict[str, Any]:
        """Get component statistics"""
        return {
            'active_datasets': len(self.active_datasets),
            'available_datasets': len(self.dataset_list.options),
            'selection_history': len(self.operations.get_selection_history()),
            'active_dataset_ids': list(self.active_datasets.keys())
        }
