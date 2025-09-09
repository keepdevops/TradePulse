#!/usr/bin/env python3
"""
TradePulse Portfolio Dataset Selector Component
Component for dataset selection in portfolio panel
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any, Callable

from ..base_component import BaseComponent
from ..dataset_selector_operations import DatasetSelectorOperations

logger = logging.getLogger(__name__)

class DatasetSelectorComponent(BaseComponent):
    """Dataset selector component for portfolio panel"""
    
    def __init__(self, data_manager, module_name: Optional[str] = None):
        super().__init__(data_manager)
        self.module_name = module_name or 'portfolio'
        self.operations = DatasetSelectorOperations(data_manager, self.module_name)
        self.selected_dataset = None
        
        # Create UI components
        self.dataset_selector = pn.widgets.Select(
            name='📊 Select Dataset',
            options=[],
            width=300
        )
        
        self.dataset_info = pn.pane.Markdown("**Dataset Info:** No dataset selected")
        
        self.select_button = pn.widgets.Button(
            name='✅ Select',
            button_type='primary',
            width=100
        )
        
        self.deselect_button = pn.widgets.Button(
            name='❌ Deselect',
            button_type='danger',
            width=100
        )
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Load initial datasets
        self.refresh_datasets()
        
        logger.info("🔧 Dataset Selector Component initialized")
    
    def setup_callbacks(self):
        """Setup component callbacks"""
        self.select_button.on_click(self.on_select_dataset)
        self.deselect_button.on_click(self.on_deselect_dataset)
        self.dataset_selector.param.watch(self.on_dataset_change, 'value')
    
    def refresh_datasets(self):
        """Refresh the list of available datasets"""
        try:
            datasets = self.operations.get_available_datasets(self.module_name)
            options = []
            
            for dataset in datasets:
                display_name = f"{dataset['name']} ({dataset['rows']} rows, {dataset['columns']} cols)"
                options.append((display_name, dataset['id']))
            
            self.dataset_selector.options = options
            
            if options:
                logger.info(f"✅ Loaded {len(options)} datasets")
            else:
                logger.info("ℹ️ No datasets available")
                
        except Exception as e:
            logger.error(f"❌ Error refreshing datasets: {e}")
    
    def on_dataset_change(self, event):
        """Handle dataset selection change"""
        try:
            dataset_id = event.new
            if dataset_id:
                datasets = self.operations.get_available_datasets(self.module_name)
                dataset_info = next((d for d in datasets if d['id'] == dataset_id), None)
                
                if dataset_info:
                    info_text = f"""
                    **Dataset Info:**
                    
                    **Name:** {dataset_info['name']}
                    **Rows:** {dataset_info['rows']:,}
                    **Columns:** {dataset_info['columns']}
                    **Type:** {dataset_info['type']}
                    **Columns:** {', '.join(dataset_info['columns_list'][:5])}{'...' if len(dataset_info['columns_list']) > 5 else ''}
                    """
                    self.dataset_info.object = info_text
                else:
                    self.dataset_info.object = "**Dataset Info:** Dataset not found"
        except Exception as e:
            logger.error(f"❌ Error handling dataset change: {e}")
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add a callback for dataset changes"""
        self.dataset_selector.param.watch(callback, 'value')
    
    def on_select_dataset(self, event):
        """Handle dataset selection"""
        try:
            dataset_id = self.dataset_selector.value
            if not dataset_id:
                logger.warning("⚠️ No dataset selected")
                return
            
            result = self.operations.select_dataset(dataset_id, 'portfolio')
            
            if result['success']:
                self.selected_dataset = dataset_id
                logger.info(f"✅ Dataset {dataset_id} selected for portfolio")
                
                # Update UI
                self.select_button.button_type = 'success'
                self.select_button.name = '✅ Selected'
                
                # Show success message
                pn.state.notifications.success(f"Dataset {dataset_id} selected successfully")
            else:
                logger.error(f"❌ Failed to select dataset: {result.get('error', 'Unknown error')}")
                pn.state.notifications.error(f"Failed to select dataset: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Error selecting dataset: {e}")
            pn.state.notifications.error(f"Error selecting dataset: {str(e)}")
    
    def on_deselect_dataset(self, event):
        """Handle dataset deselection"""
        try:
            if not self.selected_dataset:
                logger.warning("⚠️ No dataset to deselect")
                return
            
            result = self.operations.deselect_dataset(self.selected_dataset, 'portfolio')
            
            if result['success']:
                logger.info(f"✅ Dataset {self.selected_dataset} deselected")
                self.selected_dataset = None
                
                # Update UI
                self.select_button.button_type = 'primary'
                self.select_button.name = '✅ Select'
                
                # Show success message
                pn.state.notifications.success(f"Dataset deselected successfully")
            else:
                logger.error(f"❌ Failed to deselect dataset: {result.get('error', 'Unknown error')}")
                pn.state.notifications.error(f"Failed to deselect dataset: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Error deselecting dataset: {e}")
            pn.state.notifications.error(f"Error deselecting dataset: {str(e)}")
    
    def create_panel(self) -> pn.Column:
        """Create the component panel"""
        return pn.Column(
            pn.pane.Markdown("## 📊 Dataset Selector"),
            pn.Row(
                self.dataset_selector,
                pn.Spacer(width=20),
                self.select_button,
                self.deselect_button
            ),
            self.dataset_info,
            width=400
        )
    
    def get_component(self):
        """Get the component layout"""
        return self.create_panel()
    
    def get_selected_dataset(self) -> Optional[str]:
        """Get the currently selected dataset"""
        return self.selected_dataset
    
    def get_component_stats(self) -> Dict[str, Any]:
        """Get component statistics"""
        return {
            'selected_dataset': self.selected_dataset,
            'available_datasets': len(self.dataset_selector.options),
            'selection_history': len(self.operations.get_selection_history()),
            'active_selections': len(self.operations.get_active_datasets('portfolio'))
        }
