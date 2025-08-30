"""
BICIPO Model (BIC-based model selection wrapper)
Bayesian Information Criterion-based model selection for optimal model choice.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from typing import Optional, Dict, Any, List, Tuple
import warnings

warnings.filterwarnings('ignore')

from .bicipo_utilities import BICIPOUtilities
from .bicipo_analyzer import BICIPOAnalyzer


class BICIPOModel(BaseEstimator, RegressorMixin):
    """
    Bayesian Information Criterion (BIC) based model selection wrapper.
    
    This model automatically selects the best model from a collection of candidates
    using BIC for model selection, which balances goodness of fit with model complexity.
    """
    
    def __init__(
        self,
        candidate_models: Optional[List] = None,
        max_features: int = 50,
        random_state: Optional[int] = None
    ):
        """
        Initialize BICIPO model.
        
        Args:
            candidate_models: List of candidate models to evaluate
            max_features: Maximum number of features to consider
            random_state: Random seed for reproducibility
        """
        self.candidate_models = candidate_models or self._get_default_models()
        self.max_features = max_features
        self.random_state = random_state
        
        # Model state
        self.best_model_ = None
        self.best_model_name_ = None
        self.best_bic_ = None
        self.model_scores_ = {}
        self.feature_selector_ = None
        
        # Preprocessors
        self.scaler = StandardScaler()
        
        # Model state
        self.is_fitted_ = False
        self.feature_names_ = None
        self.n_features_ = None
        
        # Utilities and analyzer
        self.utilities = BICIPOUtilities()
        self.analyzer = BICIPOAnalyzer(self)
        
        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)
    
    def _get_default_models(self) -> List[Tuple[str, Any]]:
        """Get default candidate models."""
        return [
            ('linear', LinearRegression()),
            ('ridge', Ridge(alpha=1.0)),
            ('lasso', Lasso(alpha=0.1)),
            ('random_forest', RandomForestRegressor(n_estimators=100, random_state=self.random_state))
        ]
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BICIPOModel':
        """
        Fit the BICIPO model by selecting the best candidate.
        
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
        
        # Feature selection if needed
        if self.n_features_ > self.max_features:
            X = self.utilities.select_features(X, y, self.max_features, self.feature_names_)
            self.feature_selector_ = self.utilities.feature_selector_
            self.feature_names_ = self.utilities.feature_names_
            self.n_features_ = X.shape[1]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Evaluate all candidate models
        self.utilities.evaluate_models(X_scaled, y, self.candidate_models, self.n_features_)
        self.model_scores_ = self.utilities.model_scores_
        
        # Select best model
        self.utilities.select_best_model(self.model_scores_)
        self.best_model_ = self.utilities.best_model_
        self.best_model_name_ = self.utilities.best_model_name_
        self.best_bic_ = self.utilities.best_bic_
        
        # Fit the best model
        self.best_model_.fit(X_scaled, y)
        
        self.is_fitted_ = True
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the best selected model.
        
        Args:
            X: Feature matrix (n_samples, n_features)
        
        Returns:
            Predicted values (n_samples,)
        """
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before making predictions")
        
        X = np.asarray(X)
        
        # Apply feature selection if needed
        if self.feature_selector_ is not None:
            X = self.feature_selector_.transform(X)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        return self.best_model_.predict(X_scaled)
    
    def get_model_comparison(self) -> pd.DataFrame:
        """Get comparison of all candidate models."""
        return self.analyzer.get_model_comparison()
    
    def get_best_model_info(self) -> Dict[str, Any]:
        """Get information about the best selected model."""
        return self.analyzer.get_best_model_info()
    
    def get_feature_importance(self) -> pd.Series:
        """Get feature importance from the best model."""
        return self.analyzer.get_feature_importance()
    
    def get_model_performance(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Get performance metrics for the best model."""
        return self.analyzer.get_model_performance(X, y)
    
    def get_model_summary(self) -> str:
        """Get a human-readable summary of the model selection process."""
        return self.analyzer.get_model_summary()


# Convenience function for quick model creation
def create_bicipo_model(
    candidate_models: Optional[List] = None,
    max_features: int = 50,
    random_state: Optional[int] = None
) -> BICIPOModel:
    """
    Create a BICIPO model with specified parameters.
    
    Args:
        candidate_models: List of candidate models
        max_features: Maximum number of features
        random_state: Random seed
    
    Returns:
        Configured BICIPO model
    """
    return BICIPOModel(
        candidate_models=candidate_models,
        max_features=max_features,
        random_state=random_state
    )
