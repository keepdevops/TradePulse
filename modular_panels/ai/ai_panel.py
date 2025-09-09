#!/usr/bin/env python3
"""
TradePulse AI - Main Panel
Refactored AI panel using focused components
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict
import logging

from .. import BasePanel
from ..dataset_selector_component import DatasetSelectorComponent
from .model_manager import ModelManager
from .ai_ui_components import AIUIComponents
from .ai_callbacks import AICallbacks
from .ai_operations import AIOperations

logger = logging.getLogger(__name__)

class AIPanel(BasePanel):
    """Refactored AI panel using focused components"""
    
    def __init__(self, data_manager, data_access_manager=None):
        self.data_access_manager = data_access_manager
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'ai')
        self.model_manager = ModelManager()
        self.ui_components = AIUIComponents()
        self.ai_operations = AIOperations(self.model_manager)
        self.ai_callbacks = AICallbacks(self.ai_operations, self.ui_components)
        super().__init__("AI", data_manager)
        self.init_panel()
    
    def init_panel(self):
        """Initialize refactored AI panel components"""
        self.components = self.ui_components.create_components()
        self.ai_callbacks.setup_callbacks(self.components, self.dataset_selector)
    
    def get_panel(self):
        """Get the refactored AI panel layout"""
        return self.ui_components.create_panel_layout(self.components, self.dataset_selector)
