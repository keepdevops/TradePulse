"""
BICIPO Analyzer
Contains analysis and reporting methods for the BICIPO model.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class BICIPOAnalyzer:
    """Handles analysis and reporting for the BICIPO model."""
    
    def __init__(self, model):
        """Initialize the BICIPO analyzer."""
        self.model = model
    
    def get_model_comparison(self) -> pd.DataFrame:
        """
        Get comparison of all candidate models.
        
        Returns:
            DataFrame with model comparison results
        """
        return self.model.utilities.get_model_comparison(
            self.model.model_scores_, self.model.best_model_name_
        )
    
    def get_best_model_info(self) -> Dict[str, Any]:
        """
        Get information about the best selected model.
        
        Returns:
            Dictionary with best model information
        """
        if not self.model.is_fitted_:
            return {"status": "not_fitted"}
        
        return self.model.utilities.get_best_model_info(
            self.model.model_scores_, self.model.best_model_name_, self.model.best_bic_, 
            self.model.n_features_, self.model.feature_names_
        )
    
    def get_feature_importance(self) -> pd.Series:
        """
        Get feature importance from the best model.
        
        Returns:
            Series with feature importance scores
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting feature importance")
        
        return self.model.utilities.get_feature_importance(
            self.model.best_model_, self.model.n_features_, self.model.feature_names_
        )
    
    def get_model_performance(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Get performance metrics for the best model.
        
        Args:
            X: Feature matrix
            y: True target values
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting performance metrics")
        
        # Apply feature selection if needed
        if self.model.feature_selector_ is not None:
            X = self.model.feature_selector_.transform(X)
        
        # Scale features
        X_scaled = self.model.scaler.transform(X)
        
        # Get predictions
        y_pred = self.model.best_model_.predict(X_scaled)
        
        return self.model.utilities.calculate_performance_metrics(y, y_pred)
    
    def get_model_summary(self) -> str:
        """
        Get a human-readable summary of the model selection process.
        
        Returns:
            String summary
        """
        if not self.model.is_fitted_:
            return "Model not fitted"
        
        return self.model.utilities.generate_model_summary(
            self.model.best_model_name_, self.model.best_bic_, self.model.n_features_, 
            self.model.max_features, self.model.model_scores_
        )
