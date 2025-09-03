#!/usr/bin/env python3
"""
TradePulse AI Training Engine - Components
UI components for the training engine
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class TrainingEngineComponents:
    """UI components for training engine"""
    
    def __init__(self):
        self.model_type_selector = None
        self.epochs_input = None
        self.learning_rate_input = None
        self.batch_size_input = None
        self.start_training_button = None
        self.cancel_training_button = None
        self.job_list = None
        self.progress_display = None
        self.metrics_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Model type selector
        self.model_type_selector = pn.widgets.Select(
            name='Model Type',
            options=['ADM', 'CIPO', 'BICIPO', 'LSTM', 'Random Forest', 'XGBoost'],
            value='ADM',
            width=200
        )
        
        # Training parameters
        self.epochs_input = pn.widgets.IntInput(
            name='Epochs',
            start=1,
            value=100,
            width=150
        )
        
        self.learning_rate_input = pn.widgets.FloatInput(
            name='Learning Rate',
            start=0.001,
            value=0.01,
            width=150
        )
        
        self.batch_size_input = pn.widgets.IntInput(
            name='Batch Size',
            start=16,
            value=32,
            width=150
        )
        
        # Action buttons
        self.start_training_button = pn.widgets.Button(
            name='🚀 Start Training',
            button_type='primary',
            width=150
        )
        
        self.cancel_training_button = pn.widgets.Button(
            name='⏹️ Cancel Training',
            button_type='warning',
            width=150
        )
        
        # Job list
        self.job_list = pn.widgets.Select(
            name='Training Jobs',
            options=[],
            width=300
        )
        
        # Progress display
        self.progress_display = pn.pane.Markdown("""
        ### 📊 Training Progress
        No active training jobs
        """)
        
        # Metrics display
        self.metrics_display = pn.pane.Markdown("""
        ### 📈 Training Metrics
        No metrics available
        """)
    
    def create_training_controls(self):
        """Create training control section"""
        return pn.Column(
            pn.pane.Markdown("### 🎛️ Training Controls"),
            pn.Row(
                self.model_type_selector,
                align='center'
            ),
            pn.Row(
                self.epochs_input,
                self.learning_rate_input,
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
                self.start_training_button,
                self.cancel_training_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_job_monitoring(self):
        """Create job monitoring section"""
        return pn.Column(
            pn.pane.Markdown("### 📋 Job Monitoring"),
            pn.Row(
                self.job_list,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_progress_section(self):
        """Create progress section"""
        return pn.Column(
            self.progress_display,
            self.metrics_display,
            sizing_mode='stretch_width'
        )
    
    def create_training_engine_panel(self):
        """Create complete training engine panel"""
        return pn.Column(
            pn.pane.Markdown("### 🚀 AI Training Engine"),
            self.create_training_controls(),
            pn.Spacer(height=10),
            self.create_action_buttons(),
            pn.Spacer(height=10),
            self.create_job_monitoring(),
            pn.Spacer(height=10),
            self.create_progress_section(),
            sizing_mode='stretch_width'
        )
    
    def update_job_list(self, jobs: list):
        """Update job list options"""
        if self.job_list:
            job_options = [f"{job['id']} - {job['model_config']['type']} ({job['status']})" for job in jobs]
            self.job_list.options = job_options
    
    def update_progress_display(self, job: dict):
        """Update progress display"""
        if self.progress_display and job:
            progress_text = f"""
            ### 📊 Training Progress
            
            **Job ID**: {job.get('id', 'Unknown')}  
            **Model Type**: {job.get('model_config', {}).get('type', 'Unknown')}  
            **Status**: {job.get('status', 'Unknown')}  
            **Progress**: {job.get('progress', 0):.1f}%  
            **Current Epoch**: {job.get('current_epoch', 0)} / {job.get('total_epochs', 0)}  
            **Started**: {job.get('started_at', 'Unknown')}
            """
            self.progress_display.object = progress_text
    
    def update_metrics_display(self, metrics: dict):
        """Update metrics display"""
        if self.metrics_display:
            if not metrics:
                self.metrics_display.object = """
                ### 📈 Training Metrics
                No metrics available
                """
            else:
                final_metrics = metrics.get('final', {})
                metrics_text = f"""
                ### 📈 Training Metrics
                
                **Final Loss**: {final_metrics.get('loss', 'N/A'):.4f}  
                **Final Accuracy**: {final_metrics.get('accuracy', 'N/A'):.3f}  
                **Training Time**: {final_metrics.get('training_time', 'N/A'):.1f}s
                """
                self.metrics_display.object = metrics_text
    
    def update_button_states(self, can_start: bool, can_cancel: bool):
        """Update button enabled/disabled states"""
        if self.start_training_button:
            self.start_training_button.disabled = not can_start
        
        if self.cancel_training_button:
            self.cancel_training_button.disabled = not can_cancel

