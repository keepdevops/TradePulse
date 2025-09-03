#!/usr/bin/env python3
"""
TradePulse Models Panel - Management
Panel layout and management for the models panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelsPanelManagement:
    """Panel layout and management for models panel"""
    
    @staticmethod
    def create_main_layout(components, ui_components):
        """Create the models panel layout"""
        # Create UI components using the helper class
        dataset_section = ui_components.create_dataset_section(
            components['dataset_selector']
        )
        
        training_controls = ui_components.create_training_controls(
            components['model_selector'],
            components['epochs'],
            components['learning_rate'],
            components['batch_size'],
            components['hidden_layers']
        )
        
        action_buttons = ui_components.create_action_buttons(
            components['train_button'],
            components['predict_button'],
            components['refresh_data_button'],
            components['reset_performance_button'],
            components['view_saved_button']
        )
        
        return ui_components.create_main_layout(
            dataset_section,
            training_controls,
            action_buttons,
            components['training_progress'],
            components['performance_table'],
            components['model_status'],
            components['data_status']
        )
    
    @staticmethod
    def create_dataset_section(dataset_selector):
        """Create dataset selection section"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Dataset Selection"),
            dataset_selector,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_training_controls_section(model_selector, epochs, learning_rate, 
                                       batch_size, hidden_layers):
        """Create training controls section"""
        return pn.Column(
            pn.pane.Markdown("### ⚙️ Training Controls"),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("**Model Type**"),
                    model_selector,
                    width=200
                ),
                pn.Column(
                    pn.pane.Markdown("**Epochs**"),
                    epochs,
                    width=150
                ),
                pn.Column(
                    pn.pane.Markdown("**Learning Rate**"),
                    learning_rate,
                    width=150
                ),
                align='start'
            ),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("**Batch Size**"),
                    batch_size,
                    width=150
                ),
                pn.Column(
                    pn.pane.Markdown("**Hidden Layers**"),
                    hidden_layers,
                    width=150
                ),
                align='start'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_action_buttons_section(train_button, predict_button, refresh_button, 
                                     reset_button, view_button):
        """Create action buttons section"""
        return pn.Column(
            pn.pane.Markdown("### ⚡ Actions"),
            pn.Row(
                train_button,
                predict_button,
                refresh_button,
                align='center'
            ),
            pn.Row(
                reset_button,
                view_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_display_section(training_progress, performance_table, 
                              model_status, data_status):
        """Create display section"""
        return pn.Column(
            pn.pane.Markdown("### 📈 Training & Performance"),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("**Training Progress**"),
                    training_progress,
                    width=300
                ),
                pn.Column(
                    pn.pane.Markdown("**Model Status**"),
                    model_status,
                    width=300
                ),
                align='start'
            ),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("**Performance Metrics**"),
                    performance_table,
                    width=400
                ),
                pn.Column(
                    pn.pane.Markdown("**Data Status**"),
                    data_status,
                    width=200
                ),
                align='start'
            ),
            sizing_mode='stretch_width'
        )
    

