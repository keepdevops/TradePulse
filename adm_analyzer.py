"""
ADM Analyzer
Contains analysis and reporting methods for the ADM model.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from utils.performance_metrics import PerformanceMetrics


class ADMAnalyzer:
    """Handles analysis and reporting for the ADM model."""
    
    def __init__(self, model):
        """Initialize the ADM analyzer."""
        self.model = model
        self.performance_metrics = PerformanceMetrics()
    
    def get_feature_importance(self) -> pd.Series:
        """
        Get feature importance scores.
        
        Returns:
            Series with feature importance scores
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting feature importance")
        
        importance = self.performance_metrics.get_feature_importance_common(
            self.model.best_model_, len(self.model.coef_), 
            [f"feature_{i}" for i in range(len(self.model.coef_))]
        )
        return pd.Series(importance, index=[f"feature_{i}" for i in range(len(self.model.coef_))])
    
    def get_sparsity_ratio(self) -> float:
        """
        Get the sparsity ratio (fraction of zero coefficients).
        
        Returns:
            Sparsity ratio between 0 and 1
        """
        if not self.model.is_fitted_:
            raise ValueError("Model must be fitted before getting sparsity ratio")
        
        return np.mean(self.model.coef_ == 0)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and statistics.
        
        Returns:
            Dictionary with model information
        """
        if not self.model.is_fitted_:
            return {"status": "not_fitted"}
        
        return {
            "status": "fitted",
            "n_features": len(self.model.coef_),
            "sparsity_ratio": self.get_sparsity_ratio(),
            "lambda_param": self.model.lambda_param,
            "rho": self.model.rho,
            "max_iter": self.model.max_iter,
            "tol": self.model.tol,
            "coefficient_norm": np.linalg.norm(self.model.coef_),
            "intercept": self.model.intercept_
        }
