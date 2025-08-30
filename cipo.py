"""
CIPO Model (Custom CIPO-inspired predictive model)
Advanced predictive model for stock price forecasting.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from typing import Optional, Tuple, Dict, Any, List
import warnings

warnings.filterwarnings('ignore')

from .cipo_utilities import CIPOUtilities
from .cipo_analyzer import CIPOAnalyzer


class CIPOModel(BaseEstimator, RegressorMixin):
    """
    Custom CIPO-inspired predictive model for stock price forecasting.
    
    This model combines multiple prediction strategies:
    - Technical indicator analysis
    - Pattern recognition
    - Ensemble learning
    - Adaptive weighting
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 10,
        learning_rate: float = 0.1,
        alpha: float = 1.0,
        random_state: Optional[int] = None
    ):
        """
        Initialize CIPO model.
        
        Args:
            n_estimators: Number of estimators in ensemble
            max_depth: Maximum depth of trees
            learning_rate: Learning rate for adaptive weighting
            alpha: Ridge regression regularization parameter
            random_state: Random seed for reproducibility
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.alpha = alpha
        self.random_state = random_state
        
        # Model components
        self.technical_model = None
        self.pattern_model = None
        self.ensemble_model = None
        self.weight_model = None
        
        # Preprocessors
        self.feature_scaler = StandardScaler()
        self.target_scaler = MinMaxScaler()
        
        # Model state
        self.is_fitted_ = False
        self.feature_names_ = None
        self.n_features_ = None
        
        # Utilities and analyzer
        self.utilities = CIPOUtilities()
        self.analyzer = CIPOAnalyzer(self)
        
        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'CIPOModel':
        """
        Fit the CIPO model.
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target vector (n_samples,)
        
        Returns:
            Self (fitted model)
        """
        # Input validation
        X = np.asarray(X)
        y = np.asarray(y).ravel()
        
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples")
        
        # Store feature information
        self.n_features_ = X.shape[1]
        self.feature_names_ = [f"feature_{i}" for i in range(self.n_features_)]
        
        # Scale features and target
        X_scaled = self.feature_scaler.fit_transform(X)
        y_scaled = self.target_scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        # Create and fit model components
        self.utilities.create_models(self)
        self.utilities.fit_models(self, X_scaled, y_scaled)
        
        # Fit adaptive weighting model
        self.utilities.fit_weight_model(self, X_scaled, y_scaled)
        
        self.is_fitted_ = True
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Feature matrix (n_samples, n_features)
        
        Returns:
            Predicted values (n_samples,)
        """
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before making predictions")
        
        X = np.asarray(X)
        X_scaled = self.feature_scaler.transform(X)
        
        # Get predictions from all models
        pred_technical = self.technical_model.predict(X_scaled)
        pred_pattern = self.pattern_model.predict(X_scaled)
        pred_ensemble = self.ensemble_model.predict(X_scaled)
        
        # Get adaptive weights
        weights = self.weight_model.predict(X_scaled)
        weights = np.clip(weights, 0, 1)  # Ensure weights are between 0 and 1
        
        # Combine predictions using adaptive weights
        predictions = (
            weights[:, 0:1] * pred_technical.reshape(-1, 1) +
            weights[:, 1:2] * pred_pattern.reshape(-1, 1) +
            weights[:, 2:3] * pred_ensemble.reshape(-1, 1)
        ).ravel()
        
        # Inverse transform predictions
        predictions = self.target_scaler.inverse_transform(predictions.reshape(-1, 1)).ravel()
        
        return predictions
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from all model components."""
        return self.analyzer.get_feature_importance()
    
    def get_model_performance(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Get performance metrics for each model component."""
        return self.analyzer.get_model_performance(X, y)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information."""
        return self.analyzer.get_model_info()
    
    def get_prediction_breakdown(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """Get detailed breakdown of predictions from each component."""
        return self.analyzer.get_prediction_breakdown(X)


# Convenience function for quick model creation
def create_cipo_model(
    n_estimators: int = 100,
    max_depth: int = 10,
    learning_rate: float = 0.1,
    alpha: float = 1.0,
    random_state: Optional[int] = None
) -> CIPOModel:
    """
    Create a CIPO model with specified parameters.
    
    Args:
        n_estimators: Number of estimators
        max_depth: Maximum depth of trees
        learning_rate: Learning rate
        alpha: Ridge regularization parameter
        random_state: Random seed
    
    Returns:
        Configured CIPO model
    """
    return CIPOModel(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        alpha=alpha,
        random_state=random_state
    )
