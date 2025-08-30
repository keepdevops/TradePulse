"""
Test Data Creator
Helper functions for creating synthetic test data for TradePulse testing.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


class TestDataCreator:
    """Class for creating synthetic test data for testing."""
    
    def create_test_market_data(self, n_days: int = 100) -> Dict[str, Any]:
        """
        Create synthetic test market data.
        
        Args:
            n_days: Number of days of data to generate
        
        Returns:
            Dictionary containing test market data
        """
        # Generate dates
        dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
        
        # Generate realistic price data
        np.random.seed(42)
        base_price = 100.0
        trend = 0.001  # Daily trend
        volatility = 0.02  # Daily volatility
        
        prices = []
        for i in range(n_days):
            if i == 0:
                price = base_price
            else:
                price = prices[-1] * (1 + trend + np.random.normal(0, volatility))
            prices.append(price)
        
        # Create OHLCV data
        test_data = pd.DataFrame({
            'date': dates,
            'open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, n_days),
            'ticker': 'TEST'
        })
        
        return {
            'data': test_data,
            'metadata': {
                'n_days': n_days,
                'base_price': base_price,
                'trend': trend,
                'volatility': volatility
            }
        }
    
    def create_test_ml_data(self, n_samples: int = 1000, n_features: int = 20) -> Dict[str, Any]:
        """
        Create synthetic test data for ML models.
        
        Args:
            n_samples: Number of samples
            n_features: Number of features
        
        Returns:
            Dictionary containing test ML data
        """
        np.random.seed(42)
        
        # Generate features
        X = np.random.randn(n_samples, n_features)
        
        # Generate target with some correlation to features
        weights = np.random.randn(n_features)
        noise = np.random.normal(0, 0.1, n_samples)
        y = X @ weights + noise
        
        return {
            'X': X,
            'y': y,
            'weights': weights,
            'metadata': {
                'n_samples': n_samples,
                'n_features': n_features,
                'noise_level': 0.1
            }
        }
