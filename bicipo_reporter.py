"""
BICIPO Reporter
Contains reporting and performance metrics methods for BIC-based model selection.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from utils.performance_metrics import PerformanceMetrics


class BICIPOReporter:
    """Handles reporting and performance metrics for BIC-based model selection."""
    
    def __init__(self):
        """Initialize the BICIPO reporter."""
        self.performance_metrics = PerformanceMetrics()
    
    def get_model_comparison(
        self, 
        model_scores: Dict[str, Any], 
        best_model_name: str
    ) -> pd.DataFrame:
        """
        Get comparison of all candidate models.
        
        Returns:
            DataFrame with model comparison results
        """
        if not model_scores:
            return pd.DataFrame()
        
        comparison_data = []
        for model_name, scores in model_scores.items():
            comparison_data.append({
                'model_name': model_name,
                'mse': scores['mse'],
                'bic': scores['bic'],
                'n_parameters': scores['n_parameters'],
                'is_best': model_name == best_model_name
            })
        
        df = pd.DataFrame(comparison_data)
        df = df.sort_values('bic')
        
        return df
    
    def get_best_model_info(
        self, 
        model_scores: Dict[str, Any], 
        best_model_name: str, 
        best_bic: float, 
        n_features: int, 
        feature_names: List[str]
    ) -> Dict[str, Any]:
        """
        Get information about the best selected model.
        
        Returns:
            Dictionary with best model information
        """
        best_scores = model_scores[best_model_name]
        
        return {
            "status": "fitted",
            "best_model_name": best_model_name,
            "best_model_type": type(best_scores['model']).__name__,
            "best_bic": best_bic,
            "best_mse": best_scores['mse'],
            "n_parameters": best_scores['n_parameters'],
            "n_features": n_features,
            "feature_names": feature_names,
            "candidate_models": list(model_scores.keys())
        }
    
    def get_feature_importance(
        self, 
        best_model: Any, 
        n_features: int, 
        feature_names: List[str]
    ) -> pd.Series:
        """
        Get feature importance from the best model.
        
        Returns:
            Series with feature importance scores
        """
        importance = self.performance_metrics.get_feature_importance_common(best_model, n_features, feature_names)
        return pd.Series(importance, index=feature_names)
    
    def calculate_performance_metrics(self, y: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate performance metrics for the model.
        
        Args:
            y: True target values
            y_pred: Predicted target values
        
        Returns:
            Dictionary with performance metrics
        """
        return self.performance_metrics.calculate_basic_metrics(y, y_pred)
    
    def generate_model_summary(
        self, 
        best_model_name: str, 
        best_bic: float, 
        n_features: int, 
        max_features: int, 
        model_scores: Dict[str, Any]
    ) -> str:
        """
        Generate a human-readable summary of the model selection process.
        
        Returns:
            String summary
        """
        summary = f"""
BICIPO Model Selection Summary
==============================

Best Model: {best_model_name}
Best BIC Score: {best_bic:.4f}

Feature Information:
- Total Features: {n_features}
- Max Features: {max_features}

Model Comparison:
"""
        
        comparison_df = self.get_model_comparison(model_scores, best_model_name)
        for _, row in comparison_df.iterrows():
            marker = "★" if row['is_best'] else " "
            summary += f"{marker} {row['model_name']:15} - BIC: {row['bic']:8.4f}, MSE: {row['mse']:8.4f}\n"
        
        return summary
