"""
End-to-End Tester
Contains methods for testing complete workflows.
"""

import pandas as pd
from utils.config_loader import ConfigLoader
from utils.database import Database
from utils.message_bus_client import MessageBusClient
from data_grid.visualizer import DataVisualizer
from ai_module.strategy_generator import AIStrategyGenerator
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EndToEndTester:
    """
    Class for testing complete end-to-end workflows.
    
    This class contains the end-to-end workflow test that was extracted
    from TestTradePulseIntegration to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the end-to-end tester."""
        pass
    
    def test_end_to_end_workflow(self, test_config):
        """
        Test complete end-to-end workflow.
        
        Args:
            test_config: Test configuration dictionary
        """
        # This test simulates a complete workflow from data to strategy
        logger.info("Starting end-to-end workflow test")
        
        # 1. Load configuration
        config = ConfigLoader()
        config._config = test_config
        
        # 2. Initialize database
        db = Database()
        
        # 3. Create test data table
        schema = {
            'date': 'TEXT',
            'ticker': 'TEXT',
            'open': 'REAL',
            'high': 'REAL',
            'low': 'REAL',
            'close': 'REAL',
            'volume': 'INTEGER'
        }
        
        db.create_table('stock_data', schema)
        
        # 4. Insert test data
        test_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'ticker': ['AAPL', 'AAPL', 'AAPL'],
            'open': [100.0, 101.0, 102.0],
            'high': [101.0, 102.0, 103.0],
            'low': [99.0, 100.0, 101.0],
            'close': [100.5, 101.5, 102.5],
            'volume': [1000, 1100, 1200]
        })
        
        db.insert_data('stock_data', test_data)
        
        # 5. Query data
        result = db.execute_query("SELECT * FROM stock_data WHERE ticker = 'AAPL'")
        assert len(result) == 3
        
        # 6. Create visualization
        message_bus = MessageBusClient()
        visualizer = DataVisualizer(config, message_bus)
        
        chart = visualizer.create_candlestick_chart(test_data, 'AAPL')
        assert chart is not None
        
        # 7. Generate AI strategy
        strategy_generator = AIStrategyGenerator(config, message_bus)
        strategy = strategy_generator.generate_strategy(
            market_data=test_data,
            strategy_type='mean_reversion',
            risk_tolerance='low'
        )
        
        assert strategy is not None
        assert strategy['type'] == 'mean_reversion'
        
        # 8. Clean up
        db.close()
        visualizer.close()
        strategy_generator.clear_cache()
        message_bus.close()
        
        logger.info("End-to-end workflow test passed")
