#!/usr/bin/env python3
"""
TradePulse UI ML Component
Component for ML model controls
"""

import panel as pn
from typing import Callable
from .base_component import BaseComponent
from .data_manager import DataManager

class MLComponent(BaseComponent):
    """Component for ML model controls"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("MLComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create ML components"""
        self.components['ml_model_selector'] = pn.widgets.Select(
            name='ML Model',
            options=['ADM', 'CIPO', 'BICIPO', 'Ensemble'],
            value='Ensemble',
            width=120
        )
        
        self.components['predict_button'] = pn.widgets.Button(
            name='Generate Prediction',
            button_type='warning',
            width=140
        )
    
    def get_layout(self):
        """Get the ML layout"""
        return pn.Column(
            pn.pane.Markdown("### 🤖 ML Model Controls"),
            pn.Row(self.components['ml_model_selector'], self.components['predict_button'])
        )
    
    def set_predict_callback(self, callback: Callable):
        """Set callback for predict button"""
        self.components['predict_button'].on_click(callback)
    
    def get_selected_model(self) -> str:
        """Get selected ML model"""
        return self.components['ml_model_selector'].value
