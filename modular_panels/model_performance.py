#!/usr/bin/env python3
"""
TradePulse Model Performance Module
Handles model performance tracking and metrics
"""

import pandas as pd
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ModelPerformanceTracker:
    """Tracks and manages model performance metrics"""
    
    def __init__(self):
        # Initialize model performance tracking dictionary
        self.model_performance = {
            'ADM': {'accuracy': None, 'precision': None, 'recall': None, 'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}},
            'CIPO': {'accuracy': None, 'precision': None, 'recall': None, 'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}},
            'BICIPO': {'accuracy': None, 'precision': None, 'recall': None, 'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}},
            'Ensemble': {'accuracy': None, 'precision': None, 'recall': None, 'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}}
        }
    
    def update_model_performance(self, model_name: str, metrics: Dict, hyperparameters: Dict = None):
        """Update performance metrics for a specific model"""
        try:
            if model_name in self.model_performance:
                self.model_performance[model_name].update(metrics)
                if hyperparameters:
                    self.model_performance[model_name]['hyperparameters'] = hyperparameters
                self.model_performance[model_name]['status'] = 'Trained'
                logger.info(f"✅ Updated performance for {model_name}: {metrics}")
                if hyperparameters:
                    logger.info(f"📊 Hyperparameters for {model_name}: {hyperparameters}")
            else:
                logger.warning(f"⚠️ Unknown model: {model_name}")
        except Exception as e:
            logger.error(f"❌ Error updating model performance: {e}")
    
    def get_model_performance(self, model_name: str = None) -> Dict:
        """Get performance metrics for a specific model or all models"""
        try:
            if model_name:
                return self.model_performance.get(model_name, {})
            return self.model_performance
        except Exception as e:
            logger.error(f"❌ Error getting model performance: {e}")
            return {}
    
    def reset_model_performance(self, model_name: str = None):
        """Reset performance metrics for a specific model or all models"""
        try:
            if model_name and model_name in self.model_performance:
                self.model_performance[model_name] = {
                    'accuracy': None, 'precision': None, 'recall': None, 
                    'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}
                }
                logger.info(f"🔄 Reset performance for {model_name}")
            elif not model_name:
                # Reset all models
                for model in self.model_performance:
                    self.model_performance[model] = {
                        'accuracy': None, 'precision': None, 'recall': None, 
                        'f1_score': None, 'status': 'Not Trained', 'hyperparameters': {}
                    }
                logger.info("🔄 Reset performance for all models")
        except Exception as e:
            logger.error(f"❌ Error resetting model performance: {e}")
    
    def create_performance_data(self) -> pd.DataFrame:
        """Create model performance data from the performance dictionary"""
        try:
            performance_data = []
            for model_name, metrics in self.model_performance.items():
                row = {
                    'Model': model_name,
                    'Accuracy': f"{metrics['accuracy']:.1f}%" if metrics['accuracy'] is not None else 'N/A',
                    'Precision': f"{metrics['precision']:.1f}%" if metrics['precision'] is not None else 'N/A',
                    'Recall': f"{metrics['recall']:.1f}%" if metrics['recall'] is not None else 'N/A',
                    'F1-Score': f"{metrics['f1_score']:.1f}%" if metrics['f1_score'] is not None else 'N/A',
                    'Status': metrics['status']
                }
                performance_data.append(row)
            
            return pd.DataFrame(performance_data)
        except Exception as e:
            logger.error(f"❌ Error creating performance data: {e}")
            # Fallback to empty data
            return pd.DataFrame({
                'Model': ['ADM', 'CIPO', 'BICIPO', 'Ensemble'],
                'Accuracy': ['N/A', 'N/A', 'N/A', 'N/A'],
                'Precision': ['N/A', 'N/A', 'N/A', 'N/A'],
                'Recall': ['N/A', 'N/A', 'N/A', 'N/A'],
                'F1-Score': ['N/A', 'N/A', 'N/A', 'N/A'],
                'Status': ['Not Trained', 'Not Trained', 'Not Trained', 'Not Trained']
            })
    
    def get_reset_status_message(self) -> str:
        """Get the status message for reset performance"""
        return """
        ### 🤖 Model Status
        - **ADM**: ⏳ Not Trained
        - **CIPO**: ⏳ Not Trained
        - **BICIPO**: ⏳ Not Trained
        - **Ensemble**: ⏳ Not Trained
        
        **All performance metrics have been reset. Train models to see new metrics.**
        """
    
    def get_initial_status_message(self) -> str:
        """Get the initial status message"""
        return """
        ### 🤖 Model Status
        - **ADM**: ⏳ Not Trained
        - **CIPO**: ⏳ Not Trained
        - **BICIPO**: ⏳ Not Trained
        - **Ensemble**: ⏳ Not Trained
        
        **Train models to see performance metrics.**
        """
