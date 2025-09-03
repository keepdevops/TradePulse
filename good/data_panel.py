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
from .data_panel_refactored import DataPanel as RefactoredDataPanel

logger = logging.getLogger(__name__)

class DataPanel(BasePanel):
    """Enhanced data management and fetching panel with upload support"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Data", data_manager)
        # Use the refactored implementation
        self._refactored_panel = RefactoredDataPanel(data_manager, data_access_manager)
    
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
