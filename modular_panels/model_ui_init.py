#!/usr/bin/env python3
"""
TradePulse Model UI Initialization Module
Handles UI component initialization for the Models Panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelUIInitializer:
    """Handles UI component initialization for the Models Panel"""
    
    @staticmethod
    def create_model_selector():
        """Create model selector widget"""
        return pn.widgets.Select(
            name='Model',
            options=['ADM', 'CIPO', 'BICIPO', 'Ensemble'],
            value='ADM',
            width=120
        )
    
    @staticmethod
    def create_training_parameters():
        """Create training parameter widgets"""
        return {
            'epochs': pn.widgets.IntInput(
                name='Epochs',
                value=100,
                width=80
            ),
            'learning_rate': pn.widgets.FloatInput(
                name='Learning Rate',
                value=0.001,
                width=100
            ),
            'batch_size': pn.widgets.IntInput(
                name='Batch Size',
                value=32,
                width=100
            ),
            'hidden_layers': pn.widgets.IntInput(
                name='Hidden Layers',
                value=3,
                start=1,
                end=10,
                width=100
            )
        }
    
    @staticmethod
    def create_action_buttons():
        """Create action button widgets"""
        return {
            'train_button': pn.widgets.Button(
                name='📈 Train Model',
                button_type='success',
                width=120
            ),
            'predict_button': pn.widgets.Button(
                name='🔮 Predict',
                button_type='warning',
                width=120
            ),
            'refresh_data_button': pn.widgets.Button(
                name='🔄 Refresh Data',
                button_type='primary',
                width=120
            ),
            'reset_performance_button': pn.widgets.Button(
                name='🔄 Reset Performance',
                button_type='warning',
                width=120
            ),
            'view_saved_button': pn.widgets.Button(
                name='📂 View Saved Data',
                button_type='primary',
                width=120
            )
        }
    
    @staticmethod
    def create_display_components(performance_tracker):
        """Create display component widgets"""
        return {
            'performance_table': pn.widgets.Tabulator(
                performance_tracker.create_performance_data(),
                height=200
            ),
            'training_progress': pn.indicators.Progress(
                name='Training Progress',
                value=0,
                width=400
            ),
            'model_status': pn.pane.Markdown(
                performance_tracker.get_initial_status_message()
            ),
            'data_status': pn.pane.Markdown("""
            ### 📊 Available Data
            Click "Refresh Data" to update the list of available datasets.
            """)
        }
    
    @staticmethod
    def setup_callbacks(components, callbacks, data_access, data_manager_helper, model_storage):
        """Setup all component callbacks"""
        components['train_button'].on_click(callbacks.train_model)
        components['predict_button'].on_click(callbacks.make_prediction)
        components['refresh_data_button'].on_click(
            lambda e: callbacks.refresh_data(e, data_access, data_manager_helper)
        )
        components['reset_performance_button'].on_click(callbacks.reset_performance)
        components['view_saved_button'].on_click(
            lambda e: callbacks.view_saved_model_data(e, model_storage)
        )
        components['model_selector'].param.watch(callbacks.on_model_change, 'value')
