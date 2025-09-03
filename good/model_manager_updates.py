#!/usr/bin/env python3
"""
TradePulse AI Model Manager - Updates
Update methods for the model manager components
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ModelManagerUpdates:
    """Update methods for model manager components"""
    
    @staticmethod
    def update_model_list(model_list, models: list):
        """Update model list options"""
        if model_list:
            model_options = [f"{model['id']} - {model['name']} ({model['type']})" for model in models]
            model_list.options = model_options
    
    @staticmethod
    def update_status_display(status_display, model: dict):
        """Update status display"""
        if status_display and model:
            status_text = f"""
            ### 🤖 Model Status
            
            **ID**: {model.get('id', 'Unknown')}  
            **Name**: {model.get('name', 'Unknown')}  
            **Type**: {model.get('type', 'Unknown')}  
            **Status**: {model.get('status', 'Unknown')}  
            **Created**: {model.get('created', 'Unknown')}  
            **Last Trained**: {model.get('last_trained', 'Never')}
            """
            status_display.object = status_text
    
    @staticmethod
    def update_performance_display(performance_display, performance_metrics: dict):
        """Update performance display"""
        if performance_display:
            if not performance_metrics:
                performance_display.object = """
                ### 📈 Performance Metrics
                No performance data available
                """
            else:
                metrics_text = f"""
                ### 📈 Performance Metrics
                
                **Accuracy**: {performance_metrics.get('accuracy', 'N/A'):.3f}  
                **Precision**: {performance_metrics.get('precision', 'N/A'):.3f}  
                **Recall**: {performance_metrics.get('recall', 'N/A'):.3f}  
                **F1 Score**: {performance_metrics.get('f1_score', 'N/A'):.3f}  
                **Training Time**: {performance_metrics.get('training_time', 'N/A'):.1f}s
                """
                performance_display.object = metrics_text
    
    @staticmethod
    def update_button_states(create_model_button, train_model_button, 
                           evaluate_model_button, delete_model_button,
                           can_create: bool, can_train: bool, 
                           can_evaluate: bool, can_delete: bool):
        """Update button enabled/disabled states"""
        if create_model_button:
            create_model_button.disabled = not can_create
        
        if train_model_button:
            train_model_button.disabled = not can_train
        
        if evaluate_model_button:
            evaluate_model_button.disabled = not can_evaluate
        
        if delete_model_button:
            delete_model_button.disabled = not can_delete

