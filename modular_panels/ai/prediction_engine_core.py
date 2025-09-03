#!/usr/bin/env python3
"""
TradePulse AI Prediction Engine - Core Functionality
Core prediction engine class with basic functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .prediction_engine_components import PredictionEngineComponents
from .prediction_engine_operations import PredictionEngineOperations
from .prediction_engine_management import PredictionEngineManagement
from .prediction_engine_predictions import PredictionEnginePredictions

logger = logging.getLogger(__name__)

class PredictionEngineCore:
    """Core prediction engine functionality"""
    
    def __init__(self):
        self.prediction_history = []
        self.prediction_counter = 0
        
        # Initialize components
        self.components = PredictionEngineComponents()
        self.operations = PredictionEngineOperations()
        self.management = PredictionEngineManagement()
        self.predictions = PredictionEnginePredictions()
    
    def make_prediction(self, model: Dict, input_data: pd.DataFrame, 
                       prediction_type: str = 'regression') -> Dict:
        """Make predictions using a trained model"""
        try:
            self.prediction_counter += 1
            prediction_id = f"prediction_{self.prediction_counter}"
            
            logger.info(f"🔮 Making {prediction_type} prediction with {model['type']} model")
            
            # Validate model status
            if model['status'] != 'trained':
                raise ValueError(f"Model {model['id']} is not trained (status: {model['status']})")
            
            # Make prediction based on type
            prediction_result = self.predictions.make_prediction_by_type(model, input_data, prediction_type)
            
            # Create prediction record
            prediction_record = {
                'id': prediction_id,
                'model_id': model['id'],
                'model_type': model['type'],
                'prediction_type': prediction_type,
                'input_data_shape': input_data.shape,
                'predictions_count': len(prediction_result['predictions']),
                'confidence_scores': prediction_result['confidence_scores'],
                'prediction_time': pd.Timestamp.now(),
                'metadata': prediction_result.get('metadata', {})
            }
            
            self.prediction_history.append(prediction_record)
            
            logger.info(f"✅ Prediction {prediction_id} completed successfully")
            return prediction_result
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            raise
    
    def batch_predict(self, model: Dict, input_data: pd.DataFrame, 
                     batch_size: int = 1000) -> List[Dict]:
        """Make predictions in batches"""
        return self.operations.batch_predict(self, model, input_data, batch_size)
    
    def get_prediction_history(self, model_id: Optional[str] = None) -> List[Dict]:
        """Get prediction history, optionally filtered by model ID"""
        return self.operations.get_prediction_history(self.prediction_history, model_id)
    
    def get_prediction_statistics(self) -> Dict:
        """Get comprehensive prediction statistics"""
        return self.operations.get_prediction_statistics(self.prediction_history)
    
    def clear_prediction_history(self) -> int:
        """Clear prediction history and return count of cleared records"""
        return self.operations.clear_prediction_history(self.prediction_history)
    
    def validate_model_for_prediction(self, model: Dict) -> bool:
        """Validate model for prediction"""
        return self.operations.validate_model_for_prediction(model)
    
    def get_prediction_summary(self, prediction_result: Dict) -> str:
        """Get prediction summary for display"""
        return self.management.get_prediction_summary(prediction_result)



