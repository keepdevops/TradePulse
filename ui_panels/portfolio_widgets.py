#!/usr/bin/env python3
"""
TradePulse UI Panels - Portfolio Widgets
Handles portfolio display, management, and performance metrics
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging

from .portfolio_ui_components import PortfolioUIComponents
from .portfolio_operations import PortfolioOperations
from .portfolio_layout_manager import PortfolioLayoutManager

logger = logging.getLogger(__name__)

class PortfolioWidgets:
    """Handles portfolio display, management, and performance metrics"""
    
    def __init__(self):
        self.portfolio_data = {}
        self.positions = []
        self.total_value = 0.0
        self.total_pnl = 0.0
        self.total_pnl_percent = 0.0
        
        # Initialize components
        self.ui_components = PortfolioUIComponents()
        self.operations = PortfolioOperations()
        self.layout_manager = PortfolioLayoutManager()
        
        # Create portfolio components
        self.portfolio_summary = self.ui_components.create_portfolio_summary()
        self.positions_table = self.ui_components.create_positions_table()
        self.performance_metrics = self.ui_components.create_performance_metrics()
        self.portfolio_controls = self.ui_components.create_portfolio_controls(self.operations)
    
    def update_portfolio_data(self, portfolio_data: Dict):
        """Update portfolio data and displays"""
        try:
            self.portfolio_data = portfolio_data.copy()
            
            # Extract key metrics
            self.total_value = portfolio_data.get('total_value', 0.0)
            self.total_pnl = portfolio_data.get('total_pnl', 0.0)
            self.total_pnl_percent = portfolio_data.get('total_pnl_percent', 0.0)
            self.positions = portfolio_data.get('positions', [])
            
            # Update displays
            self.operations.update_portfolio_summary(self.portfolio_summary, self.total_value, self.total_pnl, self.total_pnl_percent, len(self.positions))
            self.operations.update_positions_table(self.positions_table, self.positions)
            self.operations.update_performance_metrics(self.performance_metrics, self.portfolio_data)
            
            logger.info(f"✅ Portfolio updated: ${self.total_value:.2f} total value, {len(self.positions)} positions")
            
        except Exception as e:
            logger.error(f"Failed to update portfolio data: {e}")
    
    def get_portfolio_layout(self):
        """Get the complete portfolio layout"""
        return self.layout_manager.create_portfolio_layout(self.portfolio_controls, self.portfolio_summary, self.performance_metrics, self.positions_table)
    
    def get_portfolio_statistics(self) -> Dict[str, Any]:
        """Get portfolio statistics"""
        return self.operations.get_portfolio_statistics(self.total_value, self.total_pnl, self.total_pnl_percent, self.positions, self.portfolio_data)
    
    def clear_portfolio(self):
        """Clear portfolio data and displays"""
        try:
            self.portfolio_data.clear()
            self.positions.clear()
            self.total_value = 0.0
            self.total_pnl = 0.0
            self.total_pnl_percent = 0.0
            
            # Reset displays
            self.operations.update_portfolio_summary(self.portfolio_summary, 0.0, 0.0, 0.0, 0)
            self.operations.update_positions_table(self.positions_table, [])
            self.operations.update_performance_metrics(self.performance_metrics, {})
            
            logger.info("🗑️ Portfolio cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear portfolio: {e}")
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'portfolio_summary': self.portfolio_summary,
            'positions_table': self.positions_table,
            'performance_metrics': self.performance_metrics,
            'portfolio_controls': self.portfolio_controls
        }
