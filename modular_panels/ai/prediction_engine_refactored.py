#!/usr/bin/env python3
"""
TradePulse AI - Prediction Engine (Refactored)
Handles AI/ML model prediction operations
Refactored to be under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .prediction_engine_core import PredictionEngineCore

logger = logging.getLogger(__name__)

class PredictionEngine:
    """Handles AI/ML model prediction operations"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_engine = PredictionEngineCore()
    
    def make_prediction(self, model: Dict, input_data: pd.DataFrame, 
                       prediction_type: str = 'regression') -> Dict:
        """Make predictions using a trained model"""
        # Delegate to refactored implementation
        return self._refactored_engine.make_prediction(model, input_data, prediction_type)
    
    def batch_predict(self, model: Dict, input_data: pd.DataFrame, 
                     batch_size: int = 1000) -> List[Dict]:
        """Make predictions in batches"""
        # Delegate to refactored implementation
        return self._refactored_engine.batch_predict(model, input_data, batch_size)
    
    def get_prediction_history(self, model_id: Optional[str] = None) -> List[Dict]:
        """Get prediction history, optionally filtered by model ID"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_prediction_history(model_id)
    
    def get_prediction_statistics(self) -> Dict:
        """Get comprehensive prediction statistics"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_prediction_statistics()
    
    def clear_prediction_history(self) -> int:
        """Clear prediction history and return count of cleared records"""
        # Delegate to refactored implementation
        return self._refactored_engine.clear_prediction_history()
    
    def validate_model_for_prediction(self, model: Dict) -> bool:
        """Validate model for prediction"""
        # Delegate to refactored implementation
        return self._refactored_engine.validate_model_for_prediction(model)
    
    def get_prediction_summary(self, prediction_result: Dict) -> str:
        """Get prediction summary for display"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_prediction_summary(prediction_result)



