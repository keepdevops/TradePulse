"""
CIPO Metrics
Contains performance metrics and analysis methods for the CIPO model.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from utils.performance_metrics import PerformanceMetrics


class CIPOMetrics:
    """Handles performance metrics and analysis for the CIPO model."""
    
    def __init__(self):
        """Initialize the CIPO metrics."""
        self.performance_metrics = PerformanceMetrics()
    
    def get_feature_importance(
        self, 
        technical_model, 
        pattern_model, 
        ensemble_model, 
        feature_names: List[str]
    ) -> pd.DataFrame:
        """
        Get feature importance from all model components.
        
        Returns:
            DataFrame with feature importance scores
        """
        importance_data = {}
        
        # Technical model importance
        if hasattr(technical_model, 'feature_importances_'):
            importance_data['technical'] = technical_model.feature_importances_
        
        # Pattern model importance (coefficients)
        if hasattr(pattern_model, 'coef_'):
            importance_data['pattern'] = np.abs(pattern_model.coef_)
        
        # Ensemble model importance
        if hasattr(ensemble_model, 'feature_importances_'):
            importance_data['ensemble'] = ensemble_model.feature_importances_
        
        # Create DataFrame
        df = pd.DataFrame(importance_data, index=feature_names)
        
        # Add average importance
        df['average'] = df.mean(axis=1)
        df = df.sort_values('average', ascending=False)
        
        return df
    
    def calculate_performance_metrics(
        self, 
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
        return self.performance_metrics.calculate_component_metrics(
            y, y_scaled, pred_technical, pred_pattern, pred_ensemble, pred_combined, target_scaler
        )
    
    def get_model_info(
        self, 
        n_features: int, 
        n_estimators: int, 
        max_depth: int, 
        learning_rate: float, 
        alpha: float, 
        random_state: Optional[int], 
        feature_names: List[str]
    ) -> Dict[str, Any]:
        """
        Get comprehensive model information.
        
        Returns:
            Dictionary with model information
        """
        return {
            "status": "fitted",
            "n_features": n_features,
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "alpha": alpha,
            "random_state": random_state,
            "feature_names": feature_names,
            "model_components": [
                "technical_model",
                "pattern_model", 
                "ensemble_model",
                "weight_model"
            ]
        }
    
    def get_prediction_breakdown(
        self, 
        model_instance, 
        X_scaled: np.ndarray, 
        target_scaler
    ) -> Dict[str, np.ndarray]:
        """
        Get detailed breakdown of predictions from each component.
        
        Args:
            model_instance: The CIPO model instance
            X_scaled: Scaled feature matrix
            target_scaler: Target scaler for inverse transformation
        
        Returns:
            Dictionary with predictions from each component
        """
        # Get component predictions
        pred_technical = model_instance.technical_model.predict(X_scaled)
        pred_pattern = model_instance.pattern_model.predict(X_scaled)
        pred_ensemble = model_instance.ensemble_model.predict(X_scaled)
        
        # Get weights
        weights = model_instance.weight_model.predict(X_scaled)
        weights = np.clip(weights, 0, 1)
        
        # Inverse transform component predictions
        pred_technical_orig = target_scaler.inverse_transform(pred_technical.reshape(-1, 1)).ravel()
        pred_pattern_orig = target_scaler.inverse_transform(pred_pattern.reshape(-1, 1)).ravel()
        pred_ensemble_orig = target_scaler.inverse_transform(pred_ensemble.reshape(-1, 1)).ravel()
        
        return {
            'technical_predictions': pred_technical_orig,
            'pattern_predictions': pred_pattern_orig,
            'ensemble_predictions': pred_ensemble_orig,
            'weights': weights,
            'technical_weights': weights[:, 0],
            'pattern_weights': weights[:, 1],
            'ensemble_weights': weights[:, 2]
        }
