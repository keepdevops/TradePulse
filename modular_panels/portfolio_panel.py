#!/usr/bin/env python3
"""
TradePulse Modular Panels - Portfolio Panel
Enhanced portfolio management panel with dataset integration
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .portfolio_panel_refactored import PortfolioPanel as RefactoredPortfolioPanel

logger = logging.getLogger(__name__)

class PortfolioPanel(BasePanel):
    """Enhanced portfolio management panel with dataset integration"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Portfolio", data_manager)
        # Use the refactored implementation
        self._refactored_panel = RefactoredPortfolioPanel(data_manager, data_access_manager)
    
    def init_panel(self):
        """Initialize enhanced portfolio panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the enhanced portfolio panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using selected strategy and uploaded data"""
        # Delegate to refactored implementation
        self._refactored_panel.optimize_portfolio(event)
    
    def rebalance_portfolio(self, event):
        """Rebalance portfolio based on current allocations"""
        # Delegate to refactored implementation
        self._refactored_panel.rebalance_portfolio(event)
    
    def place_order(self, event):
        """Place a new order"""
        # Delegate to refactored implementation
        self._refactored_panel.place_order(event)
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for portfolio optimization"""
        # Delegate to refactored implementation
        self._refactored_panel.on_dataset_change(change_type, dataset_id)
    
    def refresh_data(self, event):
        """Refresh available data and update portfolio display"""
        # Delegate to refactored implementation
        self._refactored_panel.refresh_data(event)
    
    def update_portfolio_display(self):
        """Update portfolio display with current data"""
        # Delegate to refactored implementation
        self._refactored_panel.update_portfolio_display()
