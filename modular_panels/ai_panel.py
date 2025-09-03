#!/usr/bin/env python3
"""
TradePulse Modular Panels - AI Panel
Enhanced AI and ML panel with dataset integration
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging

from . import BasePanel
from .ai.ai_panel import AIPanel as RefactoredAIPanel

logger = logging.getLogger(__name__)

class AIPanel(BasePanel):
    """Enhanced AI and ML panel with dataset integration"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("AI", data_manager)
        # Use the refactored implementation
        self._refactored_panel = RefactoredAIPanel(data_manager, data_access_manager)
    
    def init_panel(self):
        """Initialize enhanced AI panel components"""
        # Delegate to refactored implementation
        self._refactored_panel.init_panel()
    
    def get_panel(self):
        """Get the enhanced AI panel layout"""
        # Delegate to refactored implementation
        return self._refactored_panel.get_panel()
    
    def train_model(self, event):
        """Train the selected ML model using uploaded data"""
        # Delegate to refactored implementation
        self._refactored_panel.train_model(event)
    
    def make_prediction(self, event):
        """Make predictions using the trained model"""
        # Delegate to refactored implementation
        self._refactored_panel.make_prediction(event)
    
    def evaluate_model(self, event):
        """Evaluate the trained model performance"""
        # Delegate to refactored implementation
        self._refactored_panel.evaluate_model(event)
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for AI/ML operations"""
        # Delegate to refactored implementation
        self._refactored_panel.on_dataset_change(change_type, dataset_id)
    
    def update_performance_display(self, model_name: str, active_datasets):
        """Update the model performance display"""
        # Delegate to refactored implementation
        self._refactored_panel.update_performance_display(model_name, active_datasets)
