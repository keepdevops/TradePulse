#!/usr/bin/env python3
"""
TradePulse AI Model Manager - Management
UI management for the model manager
"""

import panel as pn
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ModelManagerManagement:
    """UI management for model manager"""
    
    @staticmethod
    def create_model_display(model: Dict):
        """Create model display"""
        try:
            if not model:
                return pn.pane.Markdown("""
                ### 🤖 Model Information
                No model selected
                """)
            
            display_text = f"""
            ### 🤖 Model Information
            
            **ID**: {model.get('id', 'Unknown')}  
            **Name**: {model.get('name', 'Unknown')}  
            **Type**: {model.get('type', 'Unknown')}  
            **Status**: {model.get('status', 'Unknown')}  
            **Created**: {model.get('created', 'Unknown')}  
            **Last Trained**: {model.get('last_trained', 'Never')}  
            **Datasets**: {len(model.get('datasets', []))}
            """
            
            return pn.pane.Markdown(display_text)
            
        except Exception as e:
            logger.error(f"Failed to create model display: {e}")
            return pn.pane.Markdown("Error: Failed to create model display")
    
    @staticmethod
    def create_performance_display(performance_metrics: Dict):
        """Create performance metrics display"""
        try:
            if not performance_metrics:
                return pn.pane.Markdown("""
                ### 📈 Performance Metrics
                No performance data available
                """)
            
            metrics_text = f"""
            ### 📈 Performance Metrics
            
            **Accuracy**: {performance_metrics.get('accuracy', 'N/A'):.3f}  
            **Precision**: {performance_metrics.get('precision', 'N/A'):.3f}  
            **Recall**: {performance_metrics.get('recall', 'N/A'):.3f}  
            **F1 Score**: {performance_metrics.get('f1_score', 'N/A'):.3f}  
            **Training Time**: {performance_metrics.get('training_time', 'N/A'):.1f}s  
            **Epochs**: {performance_metrics.get('epochs_completed', 'N/A')}  
            **Final Loss**: {performance_metrics.get('final_loss', 'N/A'):.4f}
            """
            
            return pn.pane.Markdown(metrics_text)
            
        except Exception as e:
            logger.error(f"Failed to create performance display: {e}")
            return pn.pane.Markdown("Error: Failed to create performance display")
    
    @staticmethod
    def create_statistics_display(statistics: Dict):
        """Create statistics display"""
        try:
            if not statistics or statistics.get('total_models', 0) == 0:
                return pn.pane.Markdown("""
                ### 📊 Model Statistics
                No models available
                """)
            
            total_models = statistics.get('total_models', 0)
            status_dist = statistics.get('status_distribution', {})
            type_dist = statistics.get('type_distribution', {})
            trained_models = statistics.get('trained_models', 0)
            
            stats_text = f"""
            ### 📊 Model Statistics
            
            **Total Models**: {total_models}  
            **Trained Models**: {trained_models}  
            
            **Status Distribution**: {status_dist}  
            **Type Distribution**: {type_dist}
            """
            
            return pn.pane.Markdown(stats_text)
            
        except Exception as e:
            logger.error(f"Failed to create statistics display: {e}")
            return pn.pane.Markdown("Error: Failed to create statistics display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Processing...
        Please wait while we process your request.
        """)
    
    @staticmethod
    def create_hyperparameters_display(hyperparameters: Dict):
        """Create hyperparameters display"""
        try:
            if not hyperparameters:
                return pn.pane.Markdown("""
                ### ⚙️ Hyperparameters
                No hyperparameters set
                """)
            
            params_text = "### ⚙️ Hyperparameters\n\n"
            for key, value in hyperparameters.items():
                params_text += f"**{key}**: {value}\n"
            
            return pn.pane.Markdown(params_text)
            
        except Exception as e:
            logger.error(f"Failed to create hyperparameters display: {e}")
            return pn.pane.Markdown("Error: Failed to create hyperparameters display")
    
    @staticmethod
    def create_model_list_display(models: List[Dict]):
        """Create model list display"""
        try:
            if not models:
                return pn.pane.Markdown("""
                ### 📋 Model List
                No models available
                """)
            
            list_text = "### 📋 Model List\n\n"
            for model in models:
                list_text += f"**{model.get('id', 'Unknown')}** - {model.get('name', 'Unknown')} ({model.get('type', 'Unknown')}) - {model.get('status', 'Unknown')}\n"
            
            return pn.pane.Markdown(list_text)
            
        except Exception as e:
            logger.error(f"Failed to create model list display: {e}")
            return pn.pane.Markdown("Error: Failed to create model list display")



