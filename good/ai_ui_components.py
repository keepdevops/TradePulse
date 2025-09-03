#!/usr/bin/env python3
"""
TradePulse AI - UI Components
Handles AI panel UI component creation and layout
"""

import panel as pn
import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class AIUIComponents:
    """Handles AI panel UI component creation and layout"""
    
    def __init__(self):
        self.supported_models = ['ADM', 'LSTM', 'GRU', 'Transformer', 'Random Forest', 'XGBoost']
    
    def create_components(self) -> Dict:
        """Create AI panel UI components"""
        components = {}
        
        # Model selection
        components['model_selector'] = pn.widgets.Select(
            name='ML Model',
            options=self.supported_models,
            value='ADM',
            width=200
        )
        
        # Training parameters
        components['epochs_input'] = pn.widgets.IntInput(
            name='Training Epochs',
            start=1,
            end=1000,
            value=100,
            width=150
        )
        
        components['learning_rate'] = pn.widgets.FloatInput(
            name='Learning Rate',
            start=0.001,
            end=1.0,
            value=0.01,
            step=0.001,
            width=150
        )
        
        # Action buttons
        components['train_button'] = pn.widgets.Button(
            name='🚀 Train Model',
            button_type='primary',
            width=150
        )
        
        components['predict_button'] = pn.widgets.Button(
            name='🔮 Make Prediction',
            button_type='success',
            width=150
        )
        
        components['evaluate_button'] = pn.widgets.Button(
            name='📊 Evaluate Model',
            button_type='warning',
            width=150
        )
        
        # Model performance display
        components['performance_display'] = pn.pane.Markdown("""
        ### 📊 Model Performance
        - **Accuracy**: Not trained yet
        - **Precision**: Not trained yet
        - **Recall**: Not trained yet
        - **F1 Score**: Not trained yet
        """)
        
        # Training progress
        components['training_progress'] = pn.widgets.Progress(
            name='Training Progress',
            value=0,
            width=300
        )
        
        # Predictions table
        components['predictions_table'] = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Model Predictions'
        )
        
        return components
    
    def create_panel_layout(self, components: Dict, dataset_selector) -> pn.Column:
        """Create the AI panel layout"""
        # Model controls
        model_controls = pn.Column(
            pn.pane.Markdown("### 🤖 AI/ML Model Controls"),
            pn.Row(
                components['model_selector'],
                components['epochs_input'],
                components['learning_rate'],
                align='center'
            ),
            pn.Row(
                components['train_button'],
                components['predict_button'],
                components['evaluate_button'],
                align='center'
            ),
            sizing_mode='stretch_width'
        )
        
        # Training and performance
        training_section = pn.Column(
            pn.pane.Markdown("### 🚀 Model Training"),
            components['training_progress'],
            components['performance_display'],
            sizing_mode='stretch_width'
        )
        
        # Predictions
        predictions_section = pn.Column(
            pn.pane.Markdown("### 🔮 Model Predictions"),
            components['predictions_table'],
            sizing_mode='stretch_width'
        )
        
        # Dataset selector
        dataset_section = dataset_selector.get_component()
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('🤖 Model Controls', model_controls),
            ('🚀 Training', training_section),
            ('🔮 Predictions', predictions_section),
            ('📁 Data Sources', dataset_section),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 🤖 Enhanced AI/ML Management"),
            pn.pane.Markdown("Train and deploy ML models using uploaded data"),
            tabs,
            sizing_mode='stretch_width'
        )
