#!/usr/bin/env python3
"""
TradePulse Modular Panels - Charts Panel (Refactored)
Enhanced charts and visualization panel with dataset integration
Refactored to be under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .charts.charts_panel_core import ChartsPanelCore

logger = logging.getLogger(__name__)

class ChartsPanel(BasePanel):
    """Enhanced charts and visualization panel with dataset integration"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Charts", data_manager)
        # Use the refactored implementation
        self._refactored_panel = ChartsPanelCore(data_manager)
    
    def init_panel(self):
        """Initialize enhanced charts panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the enhanced charts panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def update_chart(self, event):
        """Update the chart using the chart manager and data processor"""
        # Delegate to refactored implementation
        self._refactored_panel.update_chart(event)
    
    def export_chart(self, event):
        """Export the current chart"""
        # Delegate to refactored implementation
        self._refactored_panel.export_chart(event)
    
    def save_chart(self, event):
        """Save the current chart configuration"""
        # Delegate to refactored implementation
        self._refactored_panel.save_chart(event)
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for chart operations"""
        # Delegate to refactored implementation
        self._refactored_panel.on_dataset_change(change_type, dataset_id)



