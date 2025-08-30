"""
Forward Pass Module for ADM Model
Separate inference logic for efficient prediction.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional, Dict, Any
from models_grid.adm import ADMModel


def forward_pass_adm(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame],
    return_confidence: bool = False,
    return_features: bool = False
) -> Union[np.ndarray, Dict[str, np.ndarray]]:
    """
    Forward pass for ADM model.
    
    Args:
        model: Trained ADM model instance
        X: Input features (n_samples, n_features)
        return_confidence: Whether to return confidence scores
        return_features: Whether to return feature importance
    
    Returns:
        Predictions or dictionary with predictions and additional info
    """
    if not model.is_fitted_:
        raise ValueError("Model must be fitted before forward pass")
    
    # Convert input to numpy array
    if isinstance(X, pd.DataFrame):
        X = X.values
    
    # Make predictions
    predictions = model.predict(X)
    
    # Prepare return value
    if return_confidence or return_features:
        result = {'predictions': predictions}
        
        if return_confidence:
            # Calculate confidence based on feature importance and sparsity
            feature_importance = model.get_feature_importance()
            sparsity_ratio = model.get_sparsity_ratio()
            
            # Confidence is higher when more features are used (lower sparsity)
            # and when important features are present
            confidence = (1 - sparsity_ratio) * np.mean(feature_importance.values)
            result['confidence'] = np.full(len(predictions), confidence)
        
        if return_features:
            result['feature_importance'] = model.get_feature_importance()
            result['sparsity_ratio'] = model.get_sparsity_ratio()
        
        return result
    else:
        return predictions


def forward_pass_adm_batch(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame],
    batch_size: int = 1000,
    return_confidence: bool = False,
    return_features: bool = False
) -> Union[np.ndarray, Dict[str, np.ndarray]]:
    """
    Batch forward pass for ADM model.
    
    Args:
        model: Trained ADM model instance
        X: Input features (n_samples, n_features)
        batch_size: Size of batches for processing
        return_confidence: Whether to return confidence scores
        return_features: Whether to return feature importance
    
    Returns:
        Predictions or dictionary with predictions and additional info
    """
    if not model.is_fitted_:
        raise ValueError("Model must be fitted before forward pass")
    
    # Convert input to numpy array
    if isinstance(X, pd.DataFrame):
        X = X.values
    
    n_samples = X.shape[0]
    all_predictions = []
    
    # Process in batches
    for i in range(0, n_samples, batch_size):
        batch_end = min(i + batch_size, n_samples)
        X_batch = X[i:batch_end]
        
        batch_predictions = forward_pass_adm(
            model, X_batch, return_confidence=False, return_features=False
        )
        all_predictions.append(batch_predictions)
    
    # Concatenate all predictions
    predictions = np.concatenate(all_predictions)
    
    # Prepare return value
    if return_confidence or return_features:
        result = {'predictions': predictions}
        
        if return_confidence:
            # Calculate confidence for the entire dataset
            feature_importance = model.get_feature_importance()
            sparsity_ratio = model.get_sparsity_ratio()
            confidence = (1 - sparsity_ratio) * np.mean(feature_importance.values)
            result['confidence'] = np.full(len(predictions), confidence)
        
        if return_features:
            result['feature_importance'] = model.get_feature_importance()
            result['sparsity_ratio'] = model.get_sparsity_ratio()
        
        return result
    else:
        return predictions


def forward_pass_adm_with_uncertainty(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame],
    n_bootstrap: int = 100
) -> Dict[str, np.ndarray]:
    """
    Forward pass with uncertainty estimation using bootstrap.
    
    Args:
        model: Trained ADM model instance
        X: Input features (n_samples, n_features)
        n_bootstrap: Number of bootstrap samples
    
    Returns:
        Dictionary with predictions, mean, std, and confidence intervals
    """
    if not model.is_fitted_:
        raise ValueError("Model must be fitted before forward pass")
    
    # Convert input to numpy array
    if isinstance(X, pd.DataFrame):
        X = X.values
    
    n_samples = X.shape[0]
    bootstrap_predictions = []
    
    # Generate bootstrap predictions
    for _ in range(n_bootstrap):
        # Add small noise to features for bootstrap effect
        X_noisy = X + np.random.normal(0, 0.01, X.shape)
        pred = model.predict(X_noisy)
        bootstrap_predictions.append(pred)
    
    # Calculate statistics
    bootstrap_predictions = np.array(bootstrap_predictions)
    mean_predictions = np.mean(bootstrap_predictions, axis=0)
    std_predictions = np.std(bootstrap_predictions, axis=0)
    
    # Calculate confidence intervals (95%)
    lower_ci = np.percentile(bootstrap_predictions, 2.5, axis=0)
    upper_ci = np.percentile(bootstrap_predictions, 97.5, axis=0)
    
    return {
        'predictions': mean_predictions,
        'std': std_predictions,
        'lower_ci': lower_ci,
        'upper_ci': upper_ci,
        'bootstrap_predictions': bootstrap_predictions
    }


# Convenience functions for quick access
def predict_adm(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame]
) -> np.ndarray:
    """Quick prediction using ADM model."""
    return forward_pass_adm(model, X)


def predict_adm_with_confidence(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame]
) -> Dict[str, np.ndarray]:
    """Prediction with confidence scores."""
    return forward_pass_adm(model, X, return_confidence=True)


def predict_adm_with_features(
    model: ADMModel,
    X: Union[np.ndarray, pd.DataFrame]
) -> Dict[str, np.ndarray]:
    """Prediction with feature importance information."""
    return forward_pass_adm(model, X, return_features=True)
