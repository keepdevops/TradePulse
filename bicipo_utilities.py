"""
BICIPO Utilities
Contains utility methods for BIC-based model selection and evaluation.
"""

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from typing import Dict, Any, List, Tuple, Optional
import warnings
from .bicipo_reporter import BICIPOReporter
from utils.performance_metrics import PerformanceMetrics

warnings.filterwarnings('ignore')


class BICIPOUtilities:
    """
    Utility class for BIC-based model selection and evaluation.
    
    This class contains the utility methods that were extracted
    from BICIPOModel to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the BICIPO utilities."""
        self.feature_selector_ = None
        self.feature_names_ = None
        self.model_scores_ = {}
        self.best_model_ = None
        self.best_model_name_ = None
        self.best_bic_ = None
        self.reporter = BICIPOReporter()
        self.performance_metrics = PerformanceMetrics()
    
    def select_features(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        max_features: int, 
        feature_names: List[str]
    ) -> np.ndarray:
        """Select the most important features."""
        # Use F-regression for feature selection
        self.feature_selector_ = SelectKBest(score_func=f_regression, k=max_features)
        X_selected = self.feature_selector_.fit_transform(X, y)
        
        # Update feature names
        selected_indices = self.feature_selector_.get_support(indices=True)
        self.feature_names_ = [feature_names[i] for i in selected_indices]
        
        return X_selected
    
    def evaluate_models(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        candidate_models: List[Tuple[str, Any]], 
        n_features: int
    ) -> None:
        """Evaluate all candidate models using BIC."""
        n_samples = X.shape[0]
        
        for model_name, model in candidate_models:
            try:
                # Fit the model
                model.fit(X, y)
                
                # Get predictions
                y_pred = model.predict(X)
                
                # Calculate MSE
                mse = self.performance_metrics.calculate_basic_metrics(y, y_pred)['mse']
                
                # Calculate BIC
                # BIC = n * log(MSE) + k * log(n)
                # where k is the number of parameters
                k = self._count_parameters(model, n_features)
                bic = n_samples * np.log(mse) + k * np.log(n_samples)
                
                # Store results
                self.model_scores_[model_name] = {
                    'model': model,
                    'mse': mse,
                    'bic': bic,
                    'n_parameters': k
                }
                
            except Exception as e:
                # Skip models that fail
                print(f"Warning: Model {model_name} failed to evaluate: {e}")
                continue
    
    def _count_parameters(self, model, n_features: int) -> int:
        """Count the number of parameters in a model."""
        try:
            if hasattr(model, 'coef_'):
                # Linear models
                return len(model.coef_) + 1  # +1 for intercept
            elif hasattr(model, 'feature_importances_'):
                # Tree-based models
                return len(model.feature_importances_)
            elif hasattr(model, 'n_parameters_'):
                # Models with explicit parameter count
                return model.n_parameters_
            else:
                # Default: assume number of features + 1
                return n_features + 1
        except:
            # Fallback
            return n_features + 1
    
    def select_best_model(self, model_scores: Dict[str, Any]) -> None:
        """Select the model with the lowest BIC score."""
        if not model_scores:
            raise ValueError("No models were successfully evaluated")
        
        # Find model with lowest BIC
        best_model_name = min(model_scores.keys(), 
                            key=lambda x: model_scores[x]['bic'])
        
        self.best_model_ = model_scores[best_model_name]['model']
        self.best_model_name_ = best_model_name
        self.best_bic_ = model_scores[best_model_name]['bic']
    
    def get_model_comparison(
        self, 
        model_scores: Dict[str, Any], 
        best_model_name: str
    ) -> pd.DataFrame:
        """Get comparison of all candidate models."""
        return self.reporter.get_model_comparison(model_scores, best_model_name)
    
    def get_best_model_info(
        self, 
        model_scores: Dict[str, Any], 
        best_model_name: str, 
        best_bic: float, 
        n_features: int, 
        feature_names: List[str]
    ) -> Dict[str, Any]:
        """Get information about the best selected model."""
        return self.reporter.get_best_model_info(
            model_scores, best_model_name, best_bic, n_features, feature_names
        )
    
    def get_feature_importance(
        self, 
        best_model: Any, 
        n_features: int, 
        feature_names: List[str]
    ) -> pd.Series:
        """Get feature importance from the best model."""
        return self.reporter.get_feature_importance(best_model, n_features, feature_names)
    
    def calculate_performance_metrics(self, y: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate performance metrics for the model."""
        return self.performance_metrics.calculate_basic_metrics(y, y_pred)
    
    def generate_model_summary(
        self, 
        best_model_name: str, 
        best_bic: float, 
        n_features: int, 
        max_features: int, 
        model_scores: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary of the model selection process."""
        return self.reporter.generate_model_summary(
            best_model_name, best_bic, n_features, max_features, model_scores
        )
