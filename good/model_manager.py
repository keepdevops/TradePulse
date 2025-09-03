#!/usr/bin/env python3
"""
TradePulse AI - Model Manager
Manages AI/ML models and their configurations
REFACTORED: Now uses modular components to stay under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .model_manager_refactored import ModelManager as RefactoredModelManager

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages AI/ML models and their configurations"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_manager = RefactoredModelManager()
    
    def create_model(self, model_config: Dict) -> str:
        """Create a new model with the given configuration"""
        # Delegate to refactored implementation
        return self._refactored_manager.create_model(model_config)
    
    def get_model(self, model_id: str) -> Optional[Dict]:
        """Get model by ID"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_model(model_id)
    
    def update_model(self, model_id: str, updates: Dict) -> bool:
        """Update an existing model"""
        # Delegate to refactored implementation
        return self._refactored_manager.update_model(model_id, updates)
    
    def delete_model(self, model_id: str) -> bool:
        """Delete a model"""
        # Delegate to refactored implementation
        return self._refactored_manager.delete_model(model_id)
    
    def train_model(self, model_id: str, training_data: Dict, 
                   hyperparameters: Dict) -> bool:
        """Train a model with the given data and parameters"""
        # Delegate to refactored implementation
        return self._refactored_manager.train_model(model_id, training_data, hyperparameters)
    
    def make_prediction(self, model_id: str, input_data: pd.DataFrame) -> Dict:
        """Make predictions using a trained model"""
        # Delegate to refactored implementation
        return self._refactored_manager.make_prediction(model_id, input_data)
    
    def evaluate_model(self, model_id: str, test_data: Dict) -> Dict:
        """Evaluate a trained model on test data"""
        # Delegate to refactored implementation
        return self._refactored_manager.evaluate_model(model_id, test_data)
    
    def get_model_performance(self, model_id: str) -> Dict:
        """Get performance metrics for a specific model"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_model_performance(model_id)
    
    def get_all_models(self) -> List[Dict]:
        """Get all models"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_all_models()
    
    def get_models_by_type(self, model_type: str) -> List[Dict]:
        """Get all models of a specific type"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_models_by_type(model_type)
    
    def get_trained_models(self) -> List[Dict]:
        """Get all trained models"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_trained_models()
    
    def get_model_statistics(self) -> Dict:
        """Get comprehensive model statistics"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_model_statistics()
    
    def validate_model_config(self, model_config: Dict) -> Tuple[bool, List[str]]:
        """Validate model configuration and return errors if any"""
        # Delegate to refactored implementation
        return self._refactored_manager.validate_model_config(model_config)
