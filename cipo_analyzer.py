"""
CIPO Analyzer
Contains analysis and reporting methods for the CIPO model.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class CIPOAnalyzer:
    """Handles analysis and reporting for the CIPO model."""
    
    def __init__(self, model):
        """Initialize the CIPO analyzer."""
        self.model = model
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from all model components.
        
        Returns:
            DataFrame with feature importance scores
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting feature importance")
        
        return self.model.utilities.get_feature_importance(
            self.model.technical_model, self.model.pattern_model, 
            self.model.ensemble_model, self.model.feature_names_
        )
    
    def get_model_performance(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Get performance metrics for each model component.
        
        Args:
            X: Feature matrix
            y: True target values
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting performance metrics")
        
        X_scaled = self.model.feature_scaler.transform(X)
        y_scaled = self.model.target_scaler.transform(y.reshape(-1, 1)).ravel()
        
        # Get predictions
        pred_technical = self.model.technical_model.predict(X_scaled)
        pred_pattern = self.model.pattern_model.predict(X_scaled)
        pred_ensemble = self.model.ensemble_model.predict(X_scaled)
        pred_combined = self.model.predict(X)
        
        return self.model.utilities.calculate_performance_metrics(
            y, y_scaled, pred_technical, pred_pattern, pred_ensemble, 
            pred_combined, self.model.target_scaler
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information.
        
        Returns:
            Dictionary with model information
        """
        if not self.model.is_fitted_:
            return {"status": "not_fitted"}
        
        return self.model.utilities.get_model_info(
            self.model.n_features_, self.model.n_estimators, self.model.max_depth, 
            self.model.learning_rate, self.model.alpha, self.model.random_state, 
            self.model.feature_names_
        )
    
    def get_prediction_breakdown(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Get detailed breakdown of predictions from each component.
        
        Args:
            X: Feature matrix
        
        Returns:
            Dictionary with predictions from each component
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting prediction breakdown")
        
        X_scaled = self.model.feature_scaler.transform(X)
        
        return self.model.utilities.get_prediction_breakdown(
            self.model, X_scaled, self.model.target_scaler
        )
