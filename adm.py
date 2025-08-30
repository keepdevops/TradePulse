"""
ADM Model (ADMM-based optimization)
Sparse regression model for stock price prediction.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.preprocessing import StandardScaler
from typing import Optional, Tuple, Dict, Any
import warnings

warnings.filterwarnings('ignore')

from .adm_analyzer import ADMAnalyzer


class ADMModel(BaseEstimator, RegressorMixin):
    """
    Alternating Direction Method of Multipliers (ADMM) based sparse regression model.
    
    This model uses ADMM optimization to perform sparse regression, which is useful
    for feature selection in high-dimensional financial data.
    """
    
    def __init__(
        self, 
        lambda_param: float = 0.1,
        rho: float = 1.0,
        max_iter: int = 1000,
        tol: float = 1e-6,
        random_state: Optional[int] = None
    ):
        """
        Initialize ADM model.
        
        Args:
            lambda_param: L1 regularization parameter (sparsity control)
            rho: ADMM penalty parameter
            max_iter: Maximum number of ADMM iterations
            tol: Convergence tolerance
            random_state: Random seed for reproducibility
        """
        self.lambda_param = lambda_param
        self.rho = rho
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        
        # Model parameters
        self.coef_ = None
        self.intercept_ = None
        self.scaler_ = StandardScaler()
        self.is_fitted_ = False
        
        # Analyzer
        self.analyzer = ADMAnalyzer(self)
        
        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ADMModel':
        """
        Fit the ADM model.
        
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
        
        # Scale features
        X_scaled = self.scaler_.fit_transform(X)
        
        # Initialize variables
        n_samples, n_features = X_scaled.shape
        beta = np.zeros(n_features)  # Main variable
        alpha = np.zeros(n_features)  # Dual variable
        u = np.zeros(n_features)     # Scaled dual variable
        
        # Precompute matrices
        XtX = X_scaled.T @ X_scaled
        Xty = X_scaled.T @ y
        
        # ADMM iterations
        for iteration in range(self.max_iter):
            beta_old = beta.copy()
            
            # Update beta (ridge regression with penalty)
            A = XtX + self.rho * np.eye(n_features)
            b = Xty + self.rho * (alpha - u)
            beta = np.linalg.solve(A, b)
            
            # Update alpha (soft thresholding)
            alpha_old = alpha.copy()
            alpha = self._soft_threshold(beta + u, self.lambda_param / self.rho)
            
            # Update u (dual variable)
            u = u + beta - alpha
            
            # Check convergence
            if (np.linalg.norm(beta - beta_old) < self.tol and 
                np.linalg.norm(alpha - alpha_old) < self.tol):
                break
        
        # Store coefficients
        self.coef_ = beta
        self.intercept_ = np.mean(y) - np.mean(X_scaled @ beta)
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
        X_scaled = self.scaler_.transform(X)
        
        return X_scaled @ self.coef_ + self.intercept_
    
    def _soft_threshold(self, x: np.ndarray, threshold: float) -> np.ndarray:
        """
        Apply soft thresholding operator.
        
        Args:
            x: Input array
            threshold: Threshold value
        
        Returns:
            Thresholded array
        """
        return np.sign(x) * np.maximum(np.abs(x) - threshold, 0)
    
    def get_feature_importance(self) -> pd.Series:
        """Get feature importance scores."""
        return self.analyzer.get_feature_importance()
    
    def get_sparsity_ratio(self) -> float:
        """Get the sparsity ratio (fraction of zero coefficients)."""
        return self.analyzer.get_sparsity_ratio()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and statistics."""
        return self.analyzer.get_model_info()


# Convenience function for quick model creation
def create_adm_model(
    lambda_param: float = 0.1,
    rho: float = 1.0,
    max_iter: int = 1000,
    tol: float = 1e-6,
    random_state: Optional[int] = None
) -> ADMModel:
    """
    Create an ADM model with specified parameters.
    
    Args:
        lambda_param: L1 regularization parameter
        rho: ADMM penalty parameter
        max_iter: Maximum iterations
        tol: Convergence tolerance
        random_state: Random seed
    
    Returns:
        Configured ADM model
    """
    return ADMModel(
        lambda_param=lambda_param,
        rho=rho,
        max_iter=max_iter,
        tol=tol,
        random_state=random_state
    )
