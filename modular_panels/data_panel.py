#!/usr/bin/env python3
"""
TradePulse Modular Panels - Data Panel
Enhanced data management and fetching panel with upload support
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .data_upload_component import DataUploadComponent
from .data.data_panel_core import DataPanelCore as RefactoredDataPanel

logger = logging.getLogger(__name__)

class DataPanel(BasePanel):
    """Enhanced data management and fetching panel with upload support"""
    
    def __init__(self, data_manager, data_access_manager=None):
        logger.info(f"🔧 DataPanel: data_manager = {data_manager}")
        logger.info(f"🔧 DataPanel: data_access_manager = {data_access_manager}")
        
        # Set up the refactored panel before calling parent init
        try:
            self._refactored_panel = RefactoredDataPanel(data_manager, data_access_manager)
            logger.info("✅ RefactoredDataPanel created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create RefactoredDataPanel: {e}")
            raise
        
        super().__init__("Data", data_manager)
    
    def init_panel(self):
        """Initialize enhanced data panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the enhanced data panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def get_uploaded_data(self):
        """Get data from the upload component"""
        return self._refactored_panel.get_uploaded_data()
