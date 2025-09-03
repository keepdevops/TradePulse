#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Callbacks
Handles dataset selector callback operations and event handling
"""

import logging
from typing import Callable

logger = logging.getLogger(__name__)

class DatasetSelectorCallbacks:
    """Handles dataset selector callback operations and event handling"""
    
    def __init__(self):
        self.on_dataset_change_callbacks = []
    
    def setup_callbacks(self, search_input, type_filter, datasets_list, 
                       activate_button, deactivate_button, export_button, operations):
        """Setup component callbacks"""
        try:
            # Search change callback
            search_input.param.watch(
                lambda event: operations.on_search_change(event, datasets_list, operations.active_datasets_display), 
                'value'
            )
            
            # Filter change callback
            type_filter.param.watch(
                lambda event: operations.on_filter_change(event, datasets_list, operations.active_datasets_display), 
                'value'
            )
            
            # Dataset selection callback
            datasets_list.param.watch(
                lambda event: operations.on_dataset_selection(event, operations.dataset_info, operations.preview_table, 
                                                           activate_button, deactivate_button, operations.export_button), 
                'value'
            )
            
            # Button callbacks
            activate_button.on_click(
                lambda event: operations.activate_dataset(event, datasets_list, operations.active_datasets_display,
                                                        operations.dataset_info, operations.preview_table,
                                                        activate_button, deactivate_button)
            )
            
            deactivate_button.on_click(
                lambda event: operations.deactivate_dataset(event, datasets_list, operations.active_datasets_display,
                                                         operations.dataset_info, operations.preview_table,
                                                         activate_button, deactivate_button)
            )
            
            export_button.on_click(
                lambda event: operations.export_dataset(event, datasets_list)
            )
            
            logger.info("✅ Dataset selector callbacks setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup dataset selector callbacks: {e}")
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add a callback for dataset changes"""
        self.on_dataset_change_callbacks.append(callback)
    
    def notify_dataset_change(self, change_type: str, dataset_id: str):
        """Notify all callbacks of dataset changes"""
        for callback in self.on_dataset_change_callbacks:
            try:
                callback(change_type, dataset_id)
            except Exception as e:
                logger.error(f"Callback error: {e}")
