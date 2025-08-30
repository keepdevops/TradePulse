"""
Test Utilities
Helper functions and utilities for testing TradePulse components.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any
from .test_data_creator import TestDataCreator


class TestUtilities:
    """Utility class for test setup and helper functions."""
    
    def __init__(self):
        """Initialize test utilities."""
        self.data_creator = TestDataCreator()
    
    def create_test_config(self, temp_dir: str) -> Dict[str, Any]:
        """
        Create a test configuration for testing.
        
        Args:
            temp_dir: Temporary directory for test files
        
        Returns:
            Test configuration dictionary
        """
        test_config = {
            'database': {
                'type': 'sqlite',
                'path': f'{temp_dir}/test_data.db',
                'sqlite_path': f'{temp_dir}/test_data.db',
                'postgresql': {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'test_tradepulse',
                    'username': 'test_user',
                    'password': 'test_password'
                }
            },
            'redline': {
                'utility_path': f'{temp_dir}/redline_utility',
                'output_format': 'sqlite',
                'data_path': f'{temp_dir}/test_data.db'
            },
            'live_feed': {
                'enabled': False,
                'api_endpoint': 'https://test.api.com',
                'update_interval': 5,
                'max_tickers': 10
            },
            'broker': {
                'type': 'test',
                'live_feed_api': 'https://test.api.com',
                'demo_mode': True,
                'api_key': 'test_key',
                'secret_key': 'test_secret',
                'base_url': 'https://test.api.com'
            },
            'models': {
                'enabled_models': ['lstm', 'xgboost', 'random_forest', 'linear_regression', 'adm', 'cipo', 'bicipo'],
                'training': {
                    'test_size': 0.2,
                    'validation_size': 0.1,
                    'random_state': 42,
                    'max_features': 20
                },
                'prediction': {
                    'horizon': 5,
                    'confidence_threshold': 0.7
                }
            },
            'visualization': {
                'theme': 'plotly_white',
                'candlestick_charts': True,
                '3d_plots': True,
                'interactive': True,
                'export_formats': ['png', 'html', 'pdf']
            },
            'alerts': {
                'enabled': False,
                'desktop_notifications': False,
                'email_notifications': False,
                'price_thresholds': {
                    'default': 0.05
                },
                'indicator_signals': {
                    'rsi_overbought': 70,
                    'rsi_oversold': 30
                }
            },
            'backtest': {
                'enabled': False,
                'initial_capital': 10000,
                'commission': 0.001,
                'slippage': 0.0005
            },
            'sentiment': {
                'enabled': False,
                'sources': ['twitter', 'news'],
                'update_interval': 15
            },
            'portfolio': {
                'max_positions': 5,
                'position_sizing': 0.05,
                'risk_management': {
                    'max_drawdown': 0.15,
                    'stop_loss': 0.02,
                    'take_profit': 0.06
                }
            },
            'ai_module': {
                'enabled': True,
                'strategies': ['trend_following', 'mean_reversion', 'momentum', 'risk_parity'],
                'risk_management': {
                    'max_correlation': 0.7,
                    'volatility_target': 0.15
                }
            },
            'message_bus': {
                'host': 'localhost',
                'port': 5556,  # Use different port for testing
                'timeout': 1000
            },
            'logging': {
                'level': 'DEBUG',
                'file_path': f'{temp_dir}/logs',
                'max_size': '1MB',
                'backup_count': 2
            },
            'performance': {
                'cache_size': 100,
                'max_workers': 2,
                'batch_size': 50
            }
        }
        
        return test_config
    
    def create_test_market_data(self, n_days: int = 100) -> Dict[str, Any]:
        """
        Create synthetic test market data.
        
        Args:
            n_days: Number of days of data to generate
        
        Returns:
            Dictionary containing test market data
        """
        return self.data_creator.create_test_market_data(n_days)
    
    def create_test_ml_data(self, n_samples: int = 1000, n_features: int = 20) -> Dict[str, Any]:
        """
        Create synthetic test data for ML models.
        
        Args:
            n_samples: Number of samples
            n_features: Number of features
        
        Returns:
            Dictionary containing test ML data
        """
        return self.data_creator.create_test_ml_data(n_samples, n_features)
    
    def cleanup_test_files(self, file_paths: list) -> None:
        """
        Clean up test files.
        
        Args:
            file_paths: List of file paths to remove
        """
        import os
        
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
            except Exception as e:
                print(f"Warning: Could not remove {file_path}: {e}")
    
    def assert_performance_requirements(self, training_time: float, prediction_time: float) -> None:
        """
        Assert that performance requirements are met.
        
        Args:
            training_time: Time taken for training in seconds
            prediction_time: Time taken for prediction in seconds
        """
        # Training should complete within 10 seconds on M3 Silicon
        assert training_time < 10.0, f"Training took {training_time:.2f} seconds, should be < 10 seconds"
        
        # Prediction should be very fast
        assert prediction_time < 1.0, f"Prediction took {prediction_time:.2f} seconds, should be < 1 second"
    
    def assert_memory_requirements(self, initial_memory: float, final_memory: float, data_size_mb: float) -> None:
        """
        Assert that memory requirements are met.
        
        Args:
            initial_memory: Initial memory usage in MB
            final_memory: Final memory usage in MB
            data_size_mb: Size of data in MB
        """
        # Memory overhead should be < 5% of data size
        memory_overhead = final_memory - initial_memory
        overhead_percentage = (memory_overhead / data_size_mb) * 100
        
        assert overhead_percentage < 5.0, f"Memory overhead is {overhead_percentage:.2f}%, should be < 5%"
