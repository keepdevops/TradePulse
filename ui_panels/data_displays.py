#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays
Handles data visualization, price displays, and market information
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging

from .data_displays_refactored import DataDisplays as RefactoredDataDisplays

logger = logging.getLogger(__name__)

class DataDisplays:
    """Handles data visualization, price displays, and market information"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_displays = RefactoredDataDisplays()
    
    def update_price_data(self, price: float, change: float, change_percent: float):
        """Update price and change data"""
        # Delegate to refactored implementation
        return self._refactored_displays.update_price_data(price, change, change_percent)
    
    def update_volume_data(self, volume: int):
        """Update volume data"""
        # Delegate to refactored implementation
        return self._refactored_displays.update_volume_data(volume)
    
    def update_market_data(self, market_cap: float, high_24h: float, low_24h: float):
        """Update market data"""
        # Delegate to refactored implementation
        return self._refactored_displays.update_market_data(market_cap, high_24h, low_24h)
    
    def update_summary_statistics(self, avg_volume: int, high_52w: float, low_52w: float, pe_ratio: float):
        """Update summary statistics"""
        # Delegate to refactored implementation
        return self._refactored_displays.update_summary_statistics(avg_volume, high_52w, low_52w, pe_ratio)
    
    def get_data_displays_layout(self):
        """Get the complete data displays layout"""
        # Delegate to refactored implementation
        return self._refactored_displays.get_data_displays_layout()
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get current display data"""
        # Delegate to refactored implementation
        return self._refactored_displays.get_current_data()
    
    def get_display_statistics(self) -> Dict[str, Any]:
        """Get display component statistics"""
        # Delegate to refactored implementation
        return self._refactored_displays.get_display_statistics()
    
    def clear_displays(self):
        """Clear all display data"""
        # Delegate to refactored implementation
        return self._refactored_displays.clear_displays()
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        # Delegate to refactored implementation
        return self._refactored_displays.get_components()
