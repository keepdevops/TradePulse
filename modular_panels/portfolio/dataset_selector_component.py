#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Main Component
Refactored dataset selector component using focused components
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .dataset_browser import DatasetBrowser
from .dataset_activator import DatasetActivator
from .dataset_preview import DatasetPreview

logger = logging.getLogger(__name__)

class DatasetSelectorComponent:
    """Refactored dataset selector component using focused components"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.selected_datasets = set()
        
        # Initialize focused components
        self.browser = DatasetBrowser(data_manager, module_name)
        self.activator = DatasetActivator(data_manager, module_name)
        self.preview = DatasetPreview(data_manager)
        
        # Connect components
        self._connect_components()
        
        # Setup callbacks
        self._setup_callbacks()
        
        logger.info(f"✅ DatasetSelectorComponent initialized for {module_name}")
    
    def _connect_components(self):
        """Connect the focused components together"""
        try:
            # Connect browser selection to activator
            self.browser.datasets_list.param.watch(self._on_dataset_selection_change, 'value')
            
            # Connect activator to preview
            self.activator.add_dataset_change_callback(self._on_dataset_activation_change)
            
            logger.info("✅ Dataset selector components connected successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect components: {e}")
    
    def _setup_callbacks(self):
        """Setup component callbacks"""
        try:
            # Override the activator's _get_selected_dataset method to get from browser
            self.activator._get_selected_dataset = self._get_selected_dataset
            
            logger.info("✅ Dataset selector callbacks setup completed")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup callbacks: {e}")
    
    def _on_dataset_selection_change(self, event):
        """Handle dataset selection changes from browser"""
        try:
            selected_option = event.new
            if selected_option and selected_option != 'No datasets available' and 'Error' not in selected_option:
                # Extract dataset ID from display option
                dataset_id = self.browser._extract_dataset_id(selected_option)
                if dataset_id:
                    logger.info(f"📊 Dataset selection changed: {dataset_id}")
                    
                    # Update preview
                    self.preview.update_preview(dataset_id)
                    
                    # Update activator button states
                    self.activator._update_button_states()
                    
                    return dataset_id
            else:
                # Clear preview if no valid selection
                self.preview.update_preview(None)
                self.activator._update_button_states()
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Dataset selection change failed: {e}")
            return None
    
    def _on_dataset_activation_change(self, change_type: str, dataset_id: str):
        """Handle dataset activation/deactivation changes"""
        try:
            logger.info(f"🔄 Dataset {change_type}: {dataset_id} for {self.module_name}")
            
            if change_type == 'activated':
                self.selected_datasets.add(dataset_id)
            elif change_type == 'deactivated':
                self.selected_datasets.discard(dataset_id)
            
            # Update browser to reflect changes
            self.browser.refresh_datasets()
            
        except Exception as e:
            logger.error(f"❌ Dataset activation change handling failed: {e}")
    
    def _get_selected_dataset(self) -> Optional[str]:
        """Get the currently selected dataset ID from browser"""
        try:
            selected_option = self.browser.datasets_list.value
            if selected_option and selected_option != 'No datasets available' and 'Error' not in selected_option:
                return self.browser._extract_dataset_id(selected_option)
            return None
        except Exception as e:
            logger.error(f"Failed to get selected dataset: {e}")
            return None
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add callback for dataset change events"""
        self.activator.add_dataset_change_callback(callback)
    
    def remove_dataset_change_callback(self, callback: Callable):
        """Remove dataset change callback"""
        self.activator.remove_dataset_change_callback(callback)
    
    def get_component(self):
        """Get the main dataset selector component layout"""
        try:
            # Create the main layout
            browser_section = pn.Column(
                pn.pane.Markdown("### 🔍 Dataset Browser"),
                pn.Row(
                    self.browser.search_input,
                    self.browser.type_filter,
                    align='center'
                ),
                self.browser.datasets_list,
                sizing_mode='stretch_width'
            )
            
            preview_section = pn.Column(
                pn.pane.Markdown("### 📊 Dataset Preview"),
                self.preview.dataset_info,
                self.preview.preview_table,
                pn.Row(
                    self.preview.metadata_display,
                    self.preview.statistics_display,
                    align='start'
                ),
                sizing_mode='stretch_width'
            )
            
            activator_section = pn.Column(
                pn.pane.Markdown("### ⚡ Dataset Actions"),
                pn.Row(
                    self.activator.activate_button,
                    self.activator.deactivate_button,
                    self.activator.export_button,
                    align='center'
                ),
                self.activator.active_datasets_display,
                sizing_mode='stretch_width'
            )
            
            # Main layout with tabs
            tabs = pn.Tabs(
                ('🔍 Browse', browser_section),
                ('📊 Preview', preview_section),
                ('⚡ Actions', activator_section),
                sizing_mode='stretch_width'
            )
            
            return pn.Column(
                pn.pane.Markdown(f"### 📁 Dataset Selector for {self.module_name.title()} Module"),
                pn.pane.Markdown("Browse, preview, and manage datasets for this module"),
                tabs,
                sizing_mode='stretch_width'
            )
            
        except Exception as e:
            logger.error(f"Failed to create component layout: {e}")
            return pn.pane.Markdown("**Error:** Failed to create dataset selector component")
    
    def refresh_datasets(self):
        """Refresh the dataset list"""
        self.browser.refresh_datasets()
    
    def get_selected_datasets(self) -> set:
        """Get set of selected dataset IDs"""
        return self.selected_datasets.copy()
    
    def get_active_datasets(self) -> set:
        """Get set of active dataset IDs"""
        return self.activator.get_active_datasets()
    
    def is_dataset_active(self, dataset_id: str) -> bool:
        """Check if a dataset is active"""
        return self.activator.is_dataset_active(dataset_id)
    
    def get_component_statistics(self) -> Dict:
        """Get comprehensive statistics from all components"""
        try:
            browser_stats = self.browser.get_browser_statistics()
            activator_stats = self.activator.get_activator_statistics()
            preview_stats = self.preview.get_preview_statistics()
            
            return {
                'browser': browser_stats,
                'activator': activator_stats,
                'preview': preview_stats,
                'module': self.module_name,
                'total_selected': len(self.selected_datasets)
            }
            
        except Exception as e:
            logger.error(f"Failed to get component statistics: {e}")
            return {}
    
    def clear_all_history(self) -> int:
        """Clear all history from all components"""
        try:
            browser_cleared = self.browser.clear_history()
            activator_cleared = self.activator.clear_activation_history()
            preview_cleared = self.preview.clear_preview_history()
            
            total_cleared = browser_cleared + activator_cleared + preview_cleared
            
            logger.info(f"🗑️ Cleared {total_cleared} total history records")
            return total_cleared
            
        except Exception as e:
            logger.error(f"Failed to clear all history: {e}")
            return 0
