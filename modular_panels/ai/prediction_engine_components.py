#!/usr/bin/env python3
"""
TradePulse AI Prediction Engine - Components
UI components for the prediction engine
"""

import panel as pn
import logging
import numpy as np

logger = logging.getLogger(__name__)

class PredictionEngineComponents:
    """UI components for prediction engine"""
    
    def __init__(self):
        self.prediction_type_selector = None
        self.model_selector = None
        self.batch_size_input = None
        self.predict_button = None
        self.batch_predict_button = None
        self.status_display = None
        self.results_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Prediction type selector
        self.prediction_type_selector = pn.widgets.Select(
            name='Prediction Type',
            options=['classification', 'regression', 'time_series', 'portfolio'],
            value='regression',
            width=200
        )
        
        # Model selector
        self.model_selector = pn.widgets.Select(
            name='Model',
            options=['Random Forest', 'XGBoost', 'LSTM', 'ADM', 'CIPO', 'BICIPO'],
            value='Random Forest',
            width=200
        )
        
        # Batch size input
        self.batch_size_input = pn.widgets.IntInput(
            name='Batch Size',
            start=100,
            value=1000,
            width=150
        )
        
        # Action buttons
        self.predict_button = pn.widgets.Button(
            name='🔮 Make Prediction',
            button_type='primary',
            width=150
        )
        
        self.batch_predict_button = pn.widgets.Button(
            name='📦 Batch Predict',
            button_type='success',
            width=150
        )
        
        # Status display
        self.status_display = pn.pane.Markdown("""
        ### 📊 Prediction Status
        **Status**: Ready to make predictions
        """)
        
        # Results display
        self.results_display = pn.pane.Markdown("""
        ### 📈 Prediction Results
        No predictions made yet
        """)
    
    def create_prediction_controls(self):
        """Create prediction control section"""
        return pn.Column(
            pn.pane.Markdown("### 🎛️ Prediction Controls"),
            pn.Row(
                self.prediction_type_selector,
                self.model_selector,
                align='center'
            ),
            pn.Row(
                self.batch_size_input,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_action_buttons(self):
        """Create action buttons section"""
        return pn.Column(
            pn.pane.Markdown("### 🎯 Actions"),
            pn.Row(
                self.predict_button,
                self.batch_predict_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_status_section(self):
        """Create status section"""
        return pn.Column(
            self.status_display,
            self.results_display,
            sizing_mode='stretch_width'
        )
    
    def create_prediction_panel(self):
        """Create complete prediction panel"""
        return pn.Column(
            pn.pane.Markdown("### 🤖 AI Prediction Engine"),
            self.create_prediction_controls(),
            pn.Spacer(height=10),
            self.create_action_buttons(),
            pn.Spacer(height=10),
            self.create_status_section(),
            sizing_mode='stretch_width'
        )
    
    def update_status_display(self, status: str, message: str = ""):
        """Update status display"""
        if self.status_display:
            self.status_display.object = f"""
            ### 📊 Prediction Status
            **Status**: {status}
            {f"**Message**: {message}" if message else ""}
            """
    
    def update_results_display(self, results: dict):
        """Update results display"""
        if self.results_display:
            if not results:
                self.results_display.object = """
                ### 📈 Prediction Results
                No predictions made yet
                """
            else:
                pred_type = results.get('prediction_type', 'Unknown')
                pred_count = len(results.get('predictions', []))
                avg_confidence = np.mean(results.get('confidence_scores', [0]))
                
                self.results_display.object = f"""
                ### 📈 Prediction Results
                **Type**: {pred_type}
                **Predictions**: {pred_count}
                **Avg Confidence**: {avg_confidence:.3f}
                **Metadata**: {results.get('metadata', {})}
                """
    
    def update_button_states(self, can_predict: bool, can_batch: bool):
        """Update button enabled/disabled states"""
        if self.predict_button:
            self.predict_button.disabled = not can_predict
        
        if self.batch_predict_button:
            self.batch_predict_button.disabled = not can_batch



