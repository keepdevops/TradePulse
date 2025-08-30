"""
CIPO Utilities
Contains utility methods for creating and fitting CIPO model components.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Tuple, Optional
import warnings
from .cipo_metrics import CIPOMetrics
from utils.performance_metrics import PerformanceMetrics

warnings.filterwarnings('ignore')


class CIPOUtilities:
    """
    Utility class for creating and fitting CIPO model components.
    
    This class contains the utility methods that were extracted
    from CIPOModel to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the CIPO utilities."""
        self.technical_model = None
        self.pattern_model = None
        self.ensemble_model = None
        self.weight_model = None
        self.feature_scaler = StandardScaler()
        self.target_scaler = StandardScaler()
        self.metrics = CIPOMetrics()
        self.performance_metrics = PerformanceMetrics()
    
    def create_models(
        self, 
        n_estimators: int = 100, 
        max_depth: int = 3, 
        learning_rate: float = 0.1, 
        alpha: float = 0.1, 
        random_state: Optional[int] = None
    ) -> None:
        """Create the component models."""
        # Technical analysis model (Gradient Boosting)
        self.technical_model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state
        )
        
        # Pattern recognition model (Ridge Regression)
        self.pattern_model = Ridge(alpha=alpha, random_state=random_state)
        
        # Ensemble model (Gradient Boosting)
        self.ensemble_model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state
        )
        
        # Weight model (Ridge Regression for combining predictions)
        self.weight_model = Ridge(alpha=alpha, random_state=random_state)
    
    def fit_models(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        feature_names: List[str]
    ) -> None:
        """Fit all component models."""
        # Scale features
        X_scaled = self.feature_scaler.fit_transform(X)
        
        # Scale target
        y_scaled = self.target_scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        # Fit technical model
        self.technical_model.fit(X_scaled, y_scaled)
        
        # Fit pattern model
        self.pattern_model.fit(X_scaled, y_scaled)
        
        # Fit ensemble model
        self.ensemble_model.fit(X_scaled, y_scaled)
        
        # Fit weight model
        self._fit_weight_model(X_scaled, y_scaled)
    
    def _fit_weight_model(self, X_scaled: np.ndarray, y_scaled: np.ndarray) -> None:
        """Fit the weight model to combine predictions."""
        # Get predictions from component models
        pred_technical = self.technical_model.predict(X_scaled)
        pred_pattern = self.pattern_model.predict(X_scaled)
        pred_ensemble = self.ensemble_model.predict(X_scaled)
        
        # Create feature matrix for weight model
        X_weights = np.column_stack([pred_technical, pred_pattern, pred_ensemble])
        
        # Create target for weight model (optimal weights would minimize MSE)
        # For now, use equal weights as target
        optimal_weights = np.ones(X_weights.shape[1]) / X_weights.shape[1]
        y_weights = np.tile(optimal_weights, (X_scaled.shape[0], 1))
        
        # Fit weight model
        self.weight_model.fit(X_weights, y_weights)
    
    def get_feature_importance(
        self, 
        technical_model, 
        pattern_model, 
        ensemble_model, 
        feature_names: List[str]
    ) -> pd.DataFrame:
        """Get feature importance from all model components."""
        return self.metrics.get_feature_importance(
            technical_model, pattern_model, ensemble_model, feature_names
        )
    
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
        """Calculate performance metrics for each model component."""
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
        """Get comprehensive model information."""
        return self.metrics.get_model_info(
            n_features, n_estimators, max_depth, learning_rate, alpha, random_state, feature_names
        )
    
    def get_prediction_breakdown(
        self, 
        model_instance, 
        X_scaled: np.ndarray, 
        target_scaler
    ) -> Dict[str, np.ndarray]:
        """Get detailed breakdown of predictions from each component."""
        return self.metrics.get_prediction_breakdown(model_instance, X_scaled, target_scaler)
