#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Browser
Handles dataset browsing, searching, and filtering operations
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

from .dataset_browser_core import dataset_browser_core
from .dataset_browser_history import DatasetBrowserHistory

logger = logging.getLogger(__name__)

class DatasetBrowser:
    """Handles dataset browsing, searching, and filtering operations"""
    
    def __init__(self, data_manager, module_name: str):
        self.core = dataset_browser_core
        self.core.data_manager = data_manager
        self.core.module_name = module_name
        self.history = DatasetBrowserHistory(self.core)
        
        # Update core methods to use history module
        self.core._record_search = self.history._record_search
        self.core._record_filter = self.history._record_filter
        
        # Initial load
        self.core.refresh_datasets()
    
    def refresh_datasets(self):
        """Refresh the list of available datasets"""
        return self.core.refresh_datasets()
    
    def on_search_change(self, event):
        """Handle search input changes"""
        return self.core.on_search_change(event)
    
    def on_filter_change(self, event):
        """Handle type filter changes"""
        return self.core.on_filter_change(event)
    
    def on_dataset_selection(self, event):
        """Handle dataset selection"""
        return self.core.on_dataset_selection(event)
    
    def get_search_history(self) -> List[Dict]:
        """Get search history"""
        return self.history.get_search_history()
    
    def get_filter_history(self) -> List[Dict]:
        """Get filter history"""
        return self.history.get_filter_history()
    
    def get_browser_statistics(self) -> Dict:
        """Get browser statistics"""
        return self.history.get_browser_statistics()
    
    def clear_history(self) -> int:
        """Clear search and filter history"""
        return self.history.clear_history()
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return self.core.get_components()
