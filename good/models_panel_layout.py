#!/usr/bin/env python3
"""
TradePulse Models Panel - Layout
Additional layout methods for the models panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelsPanelLayout:
    """Additional layout methods for models panel"""
    
    @staticmethod
    def create_model_summary_section(model_count: int, trained_count: int, 
                                   active_count: int, avg_accuracy: float):
        """Create model summary section"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Model Summary"),
            pn.pane.Markdown(f"""
            - **Total Models**: {model_count}
            - **Trained Models**: {trained_count}
            - **Active Models**: {active_count}
            - **Average Accuracy**: {avg_accuracy:.2%}
            """),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_model_filters_section():
        """Create model filters section"""
        return pn.Column(
            pn.pane.Markdown("### 🔍 Model Filters"),
            pn.Row(
                pn.widgets.Select(
                    name='Filter by Type',
                    options=['All', 'LSTM', 'GRU', 'Transformer', 'CNN', 'RNN'],
                    value='All',
                    width=150
                ),
                pn.widgets.Select(
                    name='Filter by Status',
                    options=['All', 'Trained', 'Untrained', 'Active'],
                    value='All',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_model_actions_section():
        """Create model actions section"""
        return pn.Column(
            pn.pane.Markdown("### ⚡ Quick Actions"),
            pn.Row(
                pn.widgets.Button(
                    name='📊 Export Models',
                    button_type='light',
                    width=150
                ),
                pn.widgets.Button(
                    name='🔄 Compare Models',
                    button_type='primary',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_model_details_section(model_info: dict):
        """Create model details section"""
        return pn.Column(
            pn.pane.Markdown("### 📋 Model Details"),
            pn.pane.Markdown(f"""
            - **Name**: {model_info.get('name', 'N/A')}
            - **Type**: {model_info.get('type', 'N/A')}
            - **Status**: {model_info.get('status', 'N/A')}
            - **Accuracy**: {model_info.get('accuracy', 'N/A')}
            - **Created**: {model_info.get('created', 'N/A')}
            """),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_training_history_section(history_data: list):
        """Create training history section"""
        if not history_data:
            return pn.Column(
                pn.pane.Markdown("### 📈 Training History"),
                pn.pane.Markdown("No training history available"),
                sizing_mode='stretch_width'
            )
        
        history_text = "### 📈 Training History\n"
        for entry in history_data:
            history_text += f"- **{entry.get('date', 'N/A')}**: {entry.get('model', 'N/A')} - {entry.get('accuracy', 'N/A')}\n"
        
        return pn.Column(
            pn.pane.Markdown(history_text),
            sizing_mode='stretch_width'
        )

