#!/usr/bin/env python3
"""
TradePulse Data Panel - Core Functionality
Core data panel class with basic functionality
"""

import panel as pn
import pandas as pd
import numpy as np
import logging
import os
from typing import Dict, Optional

from .. import BasePanel
from .data_components import DataComponents
from .data_operations import DataOperations
from .data_export import DataExport
from .m3_file_browser import m3_file_browser
from ui_components.module_data_access import ModuleDataAccess
from .data_panel_core_main import data_panel_core_main
from .data_panel_callbacks import DataPanelCallbacks

logger = logging.getLogger(__name__)

class DataPanelCore(BasePanel):
    """Core data panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        logger.info(f"🔧 DataPanelCore: data_manager = {data_manager}")
        logger.info(f"🔧 DataPanelCore: data_access_manager = {data_access_manager}")
        
        super().__init__("Data", data_manager)
        
        # Get the global instance properly
        from .data_panel_core_main import get_data_panel_core_main
        self.core = get_data_panel_core_main(data_manager, data_access_manager)
        
        try:
            self.core.data_access = ModuleDataAccess(data_manager, data_access_manager, 'data')
            logger.info("✅ ModuleDataAccess created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create ModuleDataAccess: {e}")
            raise
        
        self.callbacks = DataPanelCallbacks(self.core)
        
        # Update core callbacks to use callbacks module
        self.core.on_symbol_change = self.callbacks.on_symbol_change
        self.core.on_date_range_change = self.callbacks.on_date_range_change
        self.core.quick_export = self.callbacks.quick_export
        self.core.clear_data = self.callbacks.clear_data
        
        self.init_panel()
    
    def init_panel(self):
        """Initialize core panel components"""
        self.core.init_panel()
    
    def setup_callbacks(self):
        """Setup basic callbacks"""
        self.core.setup_callbacks()
    
    def get_panel(self):
        """Get the core panel layout"""
        return self.core.get_panel()
    
    def fetch_data(self, event):
        """Fetch data from selected source"""
        return self.core.fetch_data(event)
    
    def get_available_files_section(self):
        """Get available files section"""
        return self.core.get_available_files_section()
    
    def get_uploaded_data(self):
        """Get data from the upload component"""
        return self.core.get_uploaded_data()
