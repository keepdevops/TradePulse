#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Core Functionality
Core data displays class with basic functionality
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging

from .data_displays_components import DataDisplaysComponents
from .data_displays_operations import DataDisplaysOperations
from .data_displays_management import DataDisplaysManagement
from .data_displays_formatters import DataDisplaysFormatters

logger = logging.getLogger(__name__)

class DataDisplaysCore:
    """Core data displays functionality"""
    
    def __init__(self):
        self.current_price = 0.0
        self.price_change = 0.0
        self.price_change_percent = 0.0
        self.volume = 0
        self.market_cap = 0.0
        self.high_24h = 0.0
        self.low_24h = 0.0
        
        # Initialize components
        self.components = DataDisplaysComponents()
        self.operations = DataDisplaysOperations()
        self.management = DataDisplaysManagement()
        self.formatters = DataDisplaysFormatters()
        
        # Create display components
        self.price_display = self.components.create_price_display()
        self.change_display = self.components.create_change_display()
        self.volume_display = self.components.create_volume_display()
        self.market_info_display = self.components.create_market_info_display()
        self.summary_stats = self.components.create_summary_stats()
    
    def update_price_data(self, price: float, change: float, change_percent: float):
        """Update price and change data"""
        return self.operations.update_price_data(self, price, change, change_percent)
    
    def update_volume_data(self, volume: int):
        """Update volume data"""
        return self.operations.update_volume_data(self, volume)
    
    def update_market_data(self, market_cap: float, high_24h: float, low_24h: float):
        """Update market data"""
        return self.operations.update_market_data(self, market_cap, high_24h, low_24h)
    
    def update_summary_statistics(self, avg_volume: int, high_52w: float, low_52w: float, pe_ratio: float):
        """Update summary statistics"""
        return self.operations.update_summary_statistics(self, avg_volume, high_52w, low_52w, pe_ratio)
    
    def get_data_displays_layout(self):
        """Get the complete data displays layout"""
        return self.management.get_data_displays_layout(self)
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get current display data"""
        return self.operations.get_current_data(self)
    
    def get_display_statistics(self) -> Dict[str, Any]:
        """Get display component statistics"""
        return self.operations.get_display_statistics(self)
    
    def clear_displays(self):
        """Clear all display data"""
        return self.operations.clear_displays(self)
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'price_display': self.price_display,
            'change_display': self.change_display,
            'volume_display': self.volume_display,
            'market_info_display': self.market_info_display,
            'summary_stats': self.summary_stats
        }



