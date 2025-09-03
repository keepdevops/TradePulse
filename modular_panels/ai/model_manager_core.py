#!/usr/bin/env python3
"""
TradePulse AI Model Manager - Core Functionality
Core model manager class with basic functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .model_manager_components import ModelManagerComponents
from .model_manager_operations import ModelManagerOperations
from .model_manager_management import ModelManagerManagement
from .model_manager_training import ModelManagerTraining

logger = logging.getLogger(__name__)

class ModelManagerCore:
    """Core model manager functionality"""
    
    def __init__(self):
        self.models = {}
        self.model_counter = 0
        self.supported_models = [
            'ADM', 'CIPO', 'BICIPO', 'LSTM', 'Random Forest', 'XGBoost'
        ]
        
        # Initialize components
        self.components = ModelManagerComponents()
        self.operations = ModelManagerOperations()
        self.management = ModelManagerManagement()
        self.training = ModelManagerTraining()
    
    def create_model(self, model_config: Dict) -> str:
        """Create a new model with the given configuration"""
        try:
            self.model_counter += 1
            model_id = f"model_{self.model_counter}"
            
            model = {
                'id': model_id,
                'name': model_config.get('name', 'Unnamed Model'),
                'type': model_config.get('type', 'ADM'),
                'status': 'created',
                'created': pd.Timestamp.now(),
                'last_trained': None,
                'training_data': model_config.get('training_data', {}),
                'hyperparameters': model_config.get('hyperparameters', {}),
                'performance_metrics': {},
                'datasets': model_config.get('datasets', [])
            }
            
            self.models[model_id] = model
            logger.info(f"✅ Model created successfully: {model_id}")
            return model_id
            
        except Exception as e:
            logger.error(f"❌ Model creation failed: {e}")
            raise
    
    def get_model(self, model_id: str) -> Optional[Dict]:
        """Get model by ID"""
        return self.models.get(model_id)
    
    def update_model(self, model_id: str, updates: Dict) -> bool:
        """Update an existing model"""
        return self.operations.update_model(self.models, model_id, updates)
    
    def delete_model(self, model_id: str) -> bool:
        """Delete a model"""
        return self.operations.delete_model(self.models, model_id)
    
    def train_model(self, model_id: str, training_data: Dict, 
                   hyperparameters: Dict) -> bool:
        """Train a model with the given data and parameters"""
        return self.training.train_model(self.models, model_id, training_data, hyperparameters)
    
    def make_prediction(self, model_id: str, input_data: pd.DataFrame) -> Dict:
        """Make predictions using a trained model"""
        return self.training.make_prediction(self.models, model_id, input_data)
    
    def evaluate_model(self, model_id: str, test_data: Dict) -> Dict:
        """Evaluate a trained model on test data"""
        return self.training.evaluate_model(self.models, model_id, test_data)
    
    def get_model_performance(self, model_id: str) -> Dict:
        """Get performance metrics for a specific model"""
        return self.operations.get_model_performance(self.models, model_id)
    
    def get_all_models(self) -> List[Dict]:
        """Get all models"""
        return list(self.models.values())
    
    def get_models_by_type(self, model_type: str) -> List[Dict]:
        """Get all models of a specific type"""
        return self.operations.get_models_by_type(self.models, model_type)
    
    def get_trained_models(self) -> List[Dict]:
        """Get all trained models"""
        return self.operations.get_trained_models(self.models)
    
    def get_model_statistics(self) -> Dict:
        """Get comprehensive model statistics"""
        return self.operations.get_model_statistics(self.models)
    
    def validate_model_config(self, model_config: Dict) -> Tuple[bool, List[str]]:
        """Validate model configuration and return errors if any"""
        return self.operations.validate_model_config(model_config, self.supported_models)



