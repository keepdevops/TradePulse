#!/usr/bin/env python3
"""
TradePulse Modular Panels - Charts Panel
Refactored charts panel using focused components
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .charts_panel_refactored import ChartsPanel as RefactoredChartsPanel

logger = logging.getLogger(__name__)

class ChartsPanel(BasePanel):
    """Refactored charts panel using focused components"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Charts", data_manager)
        # Use the refactored implementation
        self._refactored_panel = RefactoredChartsPanel(data_manager, data_access_manager)
    
    def init_panel(self):
        """Initialize refactored charts panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the refactored charts panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    

