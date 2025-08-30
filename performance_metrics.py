"""
Performance Metrics Utility
Consolidated performance metrics calculation for all models.
"""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Any


class PerformanceMetrics:
    """Consolidated performance metrics calculator for all models."""
    
    @staticmethod
    def calculate_basic_metrics(y: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate basic performance metrics.
        
        Args:
            y: True target values
            y_pred: Predicted target values
        
        Returns:
            Dictionary with basic performance metrics
        """
        return {
            'mse': mean_squared_error(y, y_pred),
            'mae': mean_absolute_error(y, y_pred),
            'r2': r2_score(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred))
        }
    
    @staticmethod
    def calculate_component_metrics(
        y: np.ndarray, 
        y_scaled: np.ndarray, 
        pred_technical: np.ndarray, 
        pred_pattern: np.ndarray, 
        pred_ensemble: np.ndarray, 
        pred_combined: np.ndarray, 
        target_scaler
    ) -> Dict[str, float]:
        """
        Calculate performance metrics for each model component.
        
        Args:
            y: True target values (original scale)
            y_scaled: True target values (scaled)
            pred_technical: Technical model predictions
            pred_pattern: Pattern model predictions
            pred_ensemble: Ensemble model predictions
            pred_combined: Combined model predictions
            target_scaler: Target scaler for inverse transformation
        
        Returns:
            Dictionary with performance metrics for each component
        """
        metrics = {}
        for name, pred in [
            ('technical', pred_technical),
            ('pattern', pred_pattern),
            ('ensemble', pred_ensemble),
            ('combined', pred_combined)
        ]:
            if name == 'combined':
                # Use original scale for combined predictions
                metrics[f'{name}_mse'] = mean_squared_error(y, pred)
                metrics[f'{name}_mae'] = mean_absolute_error(y, pred)
                metrics[f'{name}_r2'] = r2_score(y, pred)
            else:
                # Use scaled predictions for component models
                pred_original = target_scaler.inverse_transform(pred.reshape(-1, 1)).ravel()
                metrics[f'{name}_mse'] = mean_squared_error(y, pred_original)
                metrics[f'{name}_mae'] = mean_absolute_error(y, pred_original)
                metrics[f'{name}_r2'] = r2_score(y, pred_original)
        
        return metrics
    
    @staticmethod
    def get_feature_importance_common(best_model: Any, n_features: int, feature_names: list) -> np.ndarray:
        """
        Get feature importance from a model (common implementation).
        
        Args:
            best_model: The fitted model
            n_features: Number of features
            feature_names: List of feature names
        
        Returns:
            Array of feature importance scores
        """
        if hasattr(best_model, 'coef_'):
            # Linear models
            return np.abs(best_model.coef_)
        elif hasattr(best_model, 'feature_importances_'):
            # Tree-based models
            return best_model.feature_importances_
        else:
            # Default: uniform importance
            return np.ones(n_features)
