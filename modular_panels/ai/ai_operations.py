#!/usr/bin/env python3
"""
TradePulse AI - Operations
Handles AI panel operations and model management
"""

import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class AIOperations:
    """Handles AI panel operations and model management"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    def update_performance_display(self, model_name: str, active_datasets: Dict, components: Dict):
        """Update the model performance display"""
        try:
            if active_datasets:
                # Get model performance from model manager
                trained_models = self.model_manager.get_models_by_type(model_name)
                trained_models = [m for m in trained_models if m['status'] == 'trained']
                
                if trained_models:
                    # Use the most recently trained model
                    model = trained_models[-1]
                    performance = model.get('performance_metrics', {})
                    
                    total_rows = sum(data.shape[0] for data in active_datasets.values())
                    
                    performance_text = f"""
                    ### 📊 Model Performance - {model_name}
                    - **Training Data**: {len(active_datasets)} datasets, {total_rows} total rows
                    - **Accuracy**: {performance.get('accuracy', 0):.3f}
                    - **Precision**: {performance.get('precision', 0):.3f}
                    - **Recall**: {performance.get('recall', 0):.3f}
                    - **F1 Score**: {performance.get('f1_score', 0):.3f}
                    - **Last Updated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """
                else:
                    performance_text = f"""
                    ### 📊 Model Performance - {model_name}
                    - **Training Data**: {len(active_datasets)} datasets, {sum(data.shape[0] for data in active_datasets.values())} total rows
                    - **Status**: No trained models found
                    - **Last Updated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """
            else:
                performance_text = f"""
                ### 📊 Model Performance - {model_name}
                - **Training Data**: No active datasets
                - **Accuracy**: Not trained yet
                - **Precision**: Not trained yet
                - **Recall**: Not trained yet
                - **F1 Score**: Not trained yet
                """
            
            components['performance_display'].object = performance_text
            
        except Exception as e:
            logger.error(f"❌ Failed to update performance display: {e}")
