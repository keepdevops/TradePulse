#!/usr/bin/env python3
"""
TradePulse Portfolio - Main Panel
Refactored portfolio panel using focused components
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict
import logging

from .. import BasePanel
from ..dataset_selector_component import DatasetSelectorComponent
from .portfolio_manager import PortfolioManager
from .portfolio_optimizer import PortfolioOptimizer
from .ui_components import PortfolioUIComponents
from .layout_manager import PortfolioLayoutManager
from .operations_manager import PortfolioOperationsManager

logger = logging.getLogger(__name__)

class PortfolioPanel(BasePanel):
    """Refactored portfolio panel using focused components"""
    
    def __init__(self, data_manager):
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'portfolio')
        self.portfolio_manager = PortfolioManager()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.ui_components = PortfolioUIComponents(self.portfolio_manager)
        super().__init__("Portfolio", data_manager)
    
    def init_panel(self):
        """Initialize refactored portfolio panel components"""
        self.ui_components.init_ui_components()
        self.components = self.ui_components.get_components()
        
        self.operations_manager = PortfolioOperationsManager(
            self.portfolio_manager, 
            self.portfolio_optimizer, 
            self.components
        )
        self.operations_manager.setup_callbacks()
        
        # Dataset selector callback
        self.dataset_selector.add_dataset_change_callback(self.on_dataset_change)
    
    def get_panel(self):
        """Get the refactored portfolio panel layout"""
        layout_manager = PortfolioLayoutManager(self.components, self.dataset_selector)
        return layout_manager.create_panel_layout()
    

    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for portfolio operations"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for portfolio module")
        
        if change_type == 'activated':
            # Dataset is now available for portfolio analysis
            logger.info(f"✅ Dataset {dataset_id} activated for portfolio analysis")
            
            # Update portfolio displays to show available data
            self._update_portfolio_displays()
            
        elif change_type == 'deactivated':
            # Dataset is no longer available
            logger.info(f"❌ Dataset {dataset_id} deactivated for portfolio analysis")
            
            # Update portfolio displays
            self._update_portfolio_displays()
