#!/usr/bin/env python3
"""
TradePulse AI Panel - Layout Manager
Layout management for the AI panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class AILayout:
    """Layout management for AI panel"""
    
    @staticmethod
    def create_model_controls(components):
        """Create model controls section"""
        return pn.Column(
            pn.pane.Markdown("### 🤖 AI/ML Model Controls"),
            pn.Row(
                components.model_selector,
                components.epochs_input,
                components.learning_rate,
                align='center'
            ),
            pn.Row(
                components.train_button,
                components.predict_button,
                components.evaluate_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_training_section(components):
        """Create training section"""
        return pn.Column(
            pn.pane.Markdown("### 🚀 Model Training"),
            components.training_progress,
            components.performance_display,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_predictions_section(components):
        """Create predictions section"""
        return pn.Column(
            pn.pane.Markdown("### 🔮 Model Predictions"),
            components.predictions_table,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_main_layout(components, dataset_selector):
        """Create main AI layout"""
        # Create sections
        model_controls = AILayout.create_model_controls(components)
        training_section = AILayout.create_training_section(components)
        predictions_section = AILayout.create_predictions_section(components)
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

