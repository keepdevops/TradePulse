"""
Test Components
Contains detailed test logic for different TradePulse components.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

from utils.logger import LoggerMixin
from utils.message_bus_client import MessageBusClient
from data_grid.fetcher import DataFetcher
from data_grid.visualizer import DataVisualizer
from models_grid.adm import ADMModel
from models_grid.cipo import CIPOModel
from models_grid.bicipo import BICIPOModel
from ai_module.strategy_generator import AIStrategyGenerator


class TestComponents(LoggerMixin):
    """Test component class for detailed testing logic."""
    
    def __init__(self):
        """Initialize the test components."""
        super().__init__()
        self.log_info("Test Components initialized")
    
    def test_data_grid_integration(self, test_config: Dict[str, Any]) -> None:
        """Test data grid module integration."""
        try:
            # Create message bus for testing
            message_bus = MessageBusClient()
            
            # Test data fetcher
            fetcher = DataFetcher(test_config, message_bus)
            
            # Test data visualizer
            visualizer = DataVisualizer(test_config, message_bus)
            
            # Create test data
            test_data = pd.DataFrame({
                'date': pd.date_range('2023-01-01', periods=100, freq='D'),
                'open': [100 + i * 0.1 for i in range(100)],
                'high': [101 + i * 0.1 for i in range(100)],
                'low': [99 + i * 0.1 for i in range(100)],
                'close': [100.5 + i * 0.1 for i in range(100)],
                'volume': [1000 + i * 10 for i in range(100)]
            })
            
            # Test chart creation
            candlestick_chart = visualizer.create_candlestick_chart(test_data, 'TEST')
            assert candlestick_chart is not None
            
            line_chart = visualizer.create_price_line_chart(test_data, 'TEST')
            assert line_chart is not None
            
            volume_chart = visualizer.create_volume_chart(test_data, 'TEST')
            assert volume_chart is not None
            
            # Clean up
            fetcher.close()
            visualizer.close()
            message_bus.close()
            
        except Exception as e:
            self.log_error(f"Data grid integration test failed: {e}")
            raise
    
    def test_models_grid_integration(self) -> None:
        """Test models grid module integration."""
        try:
            # Create test data
            # Generate synthetic financial data
            np.random.seed(42)
            n_samples = 1000
            n_features = 20
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.randn(n_samples)
            
            # Test ADM model
            adm_model = ADMModel(lambda_param=0.1, random_state=42)
            adm_model.fit(X, y)
            adm_predictions = adm_model.predict(X[:100])
            assert len(adm_predictions) == 100
            
            # Test CIPO model
            cipo_model = CIPOModel(random_state=42)
            cipo_model.fit(X, y)
            cipo_predictions = cipo_model.predict(X[:100])
            assert len(cipo_predictions) == 100
            
            # Test BICIPO model
            bicipo_model = BICIPOModel(random_state=42)
            bicipo_model.fit(X, y)
            bicipo_predictions = bicipo_model.predict(X[:100])
            assert len(bicipo_predictions) == 100
            
        except Exception as e:
            self.log_error(f"Models grid integration test failed: {e}")
            raise
    
    def test_ai_module_integration(self, test_config: Dict[str, Any]) -> None:
        """Test AI module integration."""
        try:
            # Create message bus for testing
            message_bus = MessageBusClient()
            
            # Create AI strategy generator
            strategy_generator = AIStrategyGenerator(test_config, message_bus)
            
            # Create test market data
            dates = pd.date_range('2023-01-01', periods=200, freq='D')
            
            # Generate realistic price data
            base_price = 100
            returns = np.random.normal(0, 0.02, 200)
            prices = [base_price]
            
            for ret in returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(new_price)
            
            market_data = pd.DataFrame({
                'date': dates,
                'open': prices,
                'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'close': prices,
                'volume': np.random.randint(1000, 10000, 200)
            })
            
            # Test strategy generation
            strategy = strategy_generator.generate_strategy(
                market_data=market_data,
                strategy_type='trend_following',
                risk_tolerance='moderate'
            )
            
            assert strategy is not None
            assert 'type' in strategy
            assert strategy['type'] == 'trend_following'
            assert 'entry_signals' in strategy
            assert 'exit_signals' in strategy
            assert 'position_sizing' in strategy
            
            # Test strategy summary
            summary = strategy_generator.get_strategy_summary(strategy)
            assert summary is not None
            assert 'trend_following' in summary
            
            # Clean up
            strategy_generator.clear_cache()
            message_bus.close()
            
        except Exception as e:
            self.log_error(f"AI module integration test failed: {e}")
            raise
