#!/usr/bin/env python3
"""
TradePulse Modular Panels - Models Panel
ML models management and training panel
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging
from typing import Dict

from . import BasePanel
from .models_panel_refactored import ModelsPanel as RefactoredModelsPanel

logger = logging.getLogger(__name__)

class ModelsPanel(BasePanel):
    """ML models management and training panel"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Models", data_manager)
        
        # Use the refactored implementation
        self._refactored_panel = RefactoredModelsPanel(data_manager, data_access_manager)
    
    def init_panel(self):
        """Initialize models panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the models panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def train_model(self, event):
        """Train the selected model using uploaded data"""
        # Delegate to refactored implementation
        self._refactored_panel.train_model(event)
    
    def make_prediction(self, event):
        """Make prediction with selected model using uploaded data"""
        # Delegate to refactored implementation
        self._refactored_panel.make_prediction(event)
    
    def __post_init__(self):
        """Post-initialization tasks"""
        # Delegate to refactored implementation
        self._refactored_panel.__post_init__()
