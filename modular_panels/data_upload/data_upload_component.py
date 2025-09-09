#!/usr/bin/env python3
"""
TradePulse Data Upload - Main Component
Refactored data upload component using focused components
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import logging

from .data_upload_core import data_upload_component_core
from .data_upload_ui import DataUploadUI

logger = logging.getLogger(__name__)

class DataUploadComponent:
    """Refactored data upload component using focused components"""
    
    def __init__(self, data_manager):
        self.core = data_upload_component_core
        self.core.data_manager = data_manager
        self.ui = DataUploadUI(self.core)
        
        # Initialize focused components
        self.core.format_detector = self.core.format_detector
        self.core.file_processor = self.core.file_processor
        self.core.upload_manager = self.core.upload_manager
        
        # Connect components
        self.core._connect_components()
        
        logger.info("✅ DataUploadComponent initialized with focused components")
    
    def get_panel(self):
        """Get the component panel"""
        return self.ui.create_component_layout()
    
    def get_uploaded_data(self) -> Dict:
        """Get all uploaded data"""
        return self.core.get_uploaded_data()
    
    def get_component_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from all components"""
        return self.ui.get_component_statistics()
    
    def clear_all_history(self) -> int:
        """Clear all history from all components"""
        return self.ui.clear_all_history()
    
    def refresh_displays(self):
        """Refresh all UI displays"""
        return self.ui.refresh_displays()
