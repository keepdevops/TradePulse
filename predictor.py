#!/usr/bin/env python3
"""
Model Predictor for Models Grid
Consolidates prediction functionality for all models.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional, Union
import pandas as pd
import numpy as np
from utils.logger import setup_logger
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader

# Import model implementations
from models_grid.adm import ADMModel
from models_grid.cipo import CIPOModel
from models_grid.bicipo import BICIPOModel

logger = setup_logger(__name__)


class ModelPredictor:
    """Consolidated model predictor for all model types."""
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """Initialize the model predictor."""
        self.config = config
        self.message_bus = message_bus
        self.models = {}
        self.logger = setup_logger(__name__)
        
    def predict(self, model_type: str, data: pd.DataFrame, 
                model_instance: Optional[Any] = None) -> Dict[str, Any]:
        """
        Make predictions using a specific model type.
        
        Args:
            model_type: Type of model to use ('adm', 'cipo', 'bicipo')
            data: Input data for prediction
            model_instance: Pre-trained model instance (optional)
            
        Returns:
            Prediction results and confidence scores
        """
        try:
            if model_instance is None:
                model_instance = self.models.get(model_type)
            
            if model_instance is None:
                raise ValueError(f"No trained model available for {model_type}")
            
            if model_type == 'adm':
                predictions = model_instance.predict(data)
                confidence = model_instance.get_confidence(data) if hasattr(model_instance, 'get_confidence') else None
            elif model_type == 'cipo':
                predictions = model_instance.predict(data)
                confidence = model_instance.get_confidence(data) if hasattr(model_instance, 'get_confidence') else None
            elif model_type == 'bicipo':
                predictions = model_instance.predict(data)
                confidence = model_instance.get_confidence(data) if hasattr(model_instance, 'get_confidence') else None
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            results = {
                'predictions': predictions,
                'confidence': confidence,
                'model_type': model_type,
                'input_shape': data.shape
            }
            
            self.logger.info(f"Successfully made predictions using {model_type} model")
            return results
            
        except Exception as e:
            self.logger.error(f"Error making predictions with {model_type} model: {e}")
            raise
    
    def predict_all_models(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Make predictions using all available trained models.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Predictions from all available models
        """
        results = {}
        
        for model_type in ['adm', 'cipo', 'bicipo']:
            if model_type in self.models:
                try:
                    results[model_type] = self.predict(model_type, data)
                except Exception as e:
                    self.logger.error(f"Failed to predict with {model_type}: {e}")
                    results[model_type] = {'error': str(e)}
        
        return results
    
    def ensemble_predict(self, data: pd.DataFrame, 
                        weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Make ensemble predictions using multiple models.
        
        Args:
            data: Input data for prediction
            weights: Optional weights for each model type
            
        Returns:
            Ensemble prediction results
        """
        try:
            if weights is None:
                weights = {model_type: 1.0 for model_type in ['adm', 'cipo', 'bicipo']}
            
            individual_predictions = self.predict_all_models(data)
            ensemble_pred = None
            total_weight = 0
            
            for model_type, pred_result in individual_predictions.items():
                if 'error' not in pred_result:
                    weight = weights.get(model_type, 1.0)
                    if ensemble_pred is None:
                        ensemble_pred = weight * pred_result['predictions']
                    else:
                        ensemble_pred += weight * pred_result['predictions']
                    total_weight += weight
            
            if ensemble_pred is not None and total_weight > 0:
                ensemble_pred /= total_weight
                
                results = {
                    'ensemble_predictions': ensemble_pred,
                    'individual_predictions': individual_predictions,
                    'weights': weights,
                    'input_shape': data.shape
                }
                
                self.logger.info("Successfully made ensemble predictions")
                return results
            else:
                raise ValueError("No valid predictions available for ensemble")
                
        except Exception as e:
            self.logger.error(f"Error making ensemble predictions: {e}")
            raise
    
    def add_model(self, model_type: str, model_instance: Any) -> None:
        """Add a trained model instance."""
        self.models[model_type] = model_instance
        self.logger.info(f"Added {model_type} model instance")
    
    def get_model_info(self, model_type: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        model = self.models.get(model_type)
        if model:
            info = {
                'type': model_type,
                'has_predict': hasattr(model, 'predict'),
                'has_confidence': hasattr(model, 'get_confidence'),
                'model_attributes': [attr for attr in dir(model) if not attr.startswith('_')]
            }
            return info
        return None
