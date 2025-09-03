#!/usr/bin/env python3
"""
TradePulse AI Model Manager - Components
UI components for the model manager
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelManagerComponents:
    """UI components for model manager"""
    
    def __init__(self):
        self.model_type_selector = None
        self.model_name_input = None
        self.hyperparameters_input = None
        self.create_model_button = None
        self.train_model_button = None
        self.evaluate_model_button = None
        self.delete_model_button = None
        self.model_list = None
        self.status_display = None
        self.performance_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Model type selector
        self.model_type_selector = pn.widgets.Select(
            name='Model Type',
            options=['ADM', 'CIPO', 'BICIPO', 'LSTM', 'Random Forest', 'XGBoost'],
            value='ADM',
            width=200
        )
        
        # Model name input
        self.model_name_input = pn.widgets.TextInput(
            name='Model Name',
            value='New Model',
            width=200
        )
        
        # Hyperparameters input
        self.hyperparameters_input = pn.widgets.TextAreaInput(
            name='Hyperparameters (JSON)',
            value='{"epochs": 100, "learning_rate": 0.001}',
            width=300,
            height=100
        )
        
        # Action buttons
        self.create_model_button = pn.widgets.Button(
            name='🔧 Create Model',
            button_type='primary',
            width=150
        )
        
        self.train_model_button = pn.widgets.Button(
            name='🚀 Train Model',
            button_type='success',
            width=150
        )
        
        self.evaluate_model_button = pn.widgets.Button(
            name='📊 Evaluate Model',
            button_type='warning',
            width=150
        )
        
        self.delete_model_button = pn.widgets.Button(
            name='🗑️ Delete Model',
            button_type='danger',
            width=150
        )
        
        # Model list
        self.model_list = pn.widgets.Select(
            name='Select Model',
            options=[],
            width=250
        )
        
        # Status display
        self.status_display = pn.pane.Markdown("""
        ### 🤖 Model Status
        No model selected
        """)
        
        # Performance display
        self.performance_display = pn.pane.Markdown("""
        ### 📈 Performance Metrics
        No performance data available
        """)
    
    def create_model_creation_section(self):
        """Create model creation section"""
        return pn.Column(
            pn.pane.Markdown("### 🔧 Model Creation"),
            pn.Row(
                self.model_type_selector,
                self.model_name_input,
                align='center'
            ),
            pn.Row(
                self.hyperparameters_input,
                align='center'
            ),
            pn.Row(
                self.create_model_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_model_actions_section(self):
        """Create model actions section"""
        return pn.Column(
            pn.pane.Markdown("### 🎯 Model Actions"),
            pn.Row(
                self.model_list,
                align='center'
            ),
            pn.Row(
                self.train_model_button,
                self.evaluate_model_button,
                self.delete_model_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_status_section(self):
        """Create status section"""
        return pn.Column(
            self.status_display,
            self.performance_display,
            sizing_mode='stretch_width'
        )
    
    def create_model_manager_panel(self):
        """Create complete model manager panel"""
        return pn.Column(
            pn.pane.Markdown("### 🤖 AI Model Manager"),
            self.create_model_creation_section(),
            pn.Spacer(height=10),
            self.create_model_actions_section(),
            pn.Spacer(height=10),
            self.create_status_section(),
            sizing_mode='stretch_width'
        )
    
    def update_model_list(self, models: list):
        """Update model list options"""
        from .model_manager_updates import ModelManagerUpdates
        ModelManagerUpdates.update_model_list(self.model_list, models)
    
    def update_status_display(self, model: dict):
        """Update status display"""
        from .model_manager_updates import ModelManagerUpdates
        ModelManagerUpdates.update_status_display(self.status_display, model)
    
    def update_performance_display(self, performance_metrics: dict):
        """Update performance display"""
        from .model_manager_updates import ModelManagerUpdates
        ModelManagerUpdates.update_performance_display(self.performance_display, performance_metrics)
    
    def update_button_states(self, can_create: bool, can_train: bool, 
                           can_evaluate: bool, can_delete: bool):
        """Update button enabled/disabled states"""
        from .model_manager_updates import ModelManagerUpdates
        ModelManagerUpdates.update_button_states(
            self.create_model_button, self.train_model_button,
            self.evaluate_model_button, self.delete_model_button,
            can_create, can_train, can_evaluate, can_delete
        )
