"""
Integration Tests for TradePulse
Tests the integration between different modules and components.
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config_loader import ConfigLoader
from utils.database import Database
from utils.message_bus_client import MessageBusClient
from utils.logger import setup_logger
from data_grid.fetcher import DataFetcher
from data_grid.visualizer import DataVisualizer
from models_grid.adm import ADMModel
from models_grid.cipo import CIPOModel
from models_grid.bicipo import BICIPOModel
from ai_module.strategy_generator import AIStrategyGenerator
from .test_utilities import TestUtilities
from .test_components import TestComponents
from .end_to_end_tester import EndToEndTester


class TestTradePulseIntegration:
    """Integration tests for TradePulse components."""
    
    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.test_utilities = TestUtilities()
        cls.test_components = TestComponents()
        cls.end_to_end_tester = EndToEndTester()
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_config = cls.test_utilities.create_test_config(cls.temp_dir)
        cls.logger = setup_logger(__name__)
        
        # Create test data directory
        test_data_dir = Path(cls.temp_dir) / "data"
        test_data_dir.mkdir(exist_ok=True)
        
        # Create test logs directory
        test_logs_dir = Path(cls.temp_dir) / "logs"
        test_logs_dir.mkdir(exist_ok=True)
        
        cls.logger.info("Test environment set up")
    
    @classmethod
    def teardown_class(cls):
        """Clean up test environment."""
        try:
            shutil.rmtree(cls.temp_dir)
            cls.logger.info("Test environment cleaned up")
        except Exception as e:
            cls.logger.warning(f"Error cleaning up test environment: {e}")
    
    def test_config_loader_integration(self):
        """Test configuration loader integration."""
        try:
            # Test config loading
            config = ConfigLoader()
            config._config = self.test_config  # Inject test config
            
            # Verify key sections exist
            assert 'database' in config.load_config()
            assert 'models' in config.load_config()
            assert 'ai_module' in config.load_config()
            
            # Test nested key access
            db_type = config.get('database.type')
            assert db_type == 'sqlite'
            
            self.logger.info("Config loader integration test passed")
            
        except Exception as e:
            self.logger.error(f"Config loader integration test failed: {e}")
            raise
    
    def test_database_integration(self):
        """Test database integration."""
        try:
            # Create database instance
            db = Database()
            
            # Test table creation
            test_schema = {
                'id': 'INTEGER PRIMARY KEY',
                'name': 'TEXT',
                'value': 'REAL'
            }
            
            success = db.create_table('test_table', test_schema)
            assert success is True
            
            # Test data insertion
            import pandas as pd
            test_data = pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['A', 'B', 'C'],
                'value': [1.1, 2.2, 3.3]
            })
            
            success = db.insert_data('test_table', test_data)
            assert success is True
            
            # Test query execution
            result = db.execute_query("SELECT * FROM test_table")
            assert len(result) == 3
            assert result['name'].iloc[0] == 'A'
            
            # Clean up
            db.close()
            
            self.logger.info("Database integration test passed")
            
        except Exception as e:
            self.logger.error(f"Database integration test failed: {e}")
            raise
    
    def test_message_bus_integration(self):
        """Test message bus integration."""
        try:
            # Create message bus client
            message_bus = MessageBusClient()
            
            # Test message publishing
            test_message = {'test': 'data', 'timestamp': 1234567890}
            success = message_bus.publish('test_topic', test_message)
            assert success is True
            
            # Test subscription
            received_messages = []
            def test_callback(topic, data):
                received_messages.append((topic, data))
            
            success = message_bus.subscribe('test_topic', test_callback)
            assert success is True
            
            # Start listening
            message_bus.start_listening()
            
            # Publish another message
            message_bus.publish('test_topic', {'test': 'data2'})
            
            # Wait a bit for message processing
            import time
            time.sleep(0.1)
            
            # Stop listening
            message_bus.stop_listening()
            
            # Clean up
            message_bus.close()
            
            self.logger.info("Message bus integration test passed")
            
        except Exception as e:
            self.logger.error(f"Message bus integration test failed: {e}")
            raise
    
    def test_data_grid_integration(self):
        """Test data grid module integration."""
        try:
            # Use test components for data grid testing
            self.test_components.test_data_grid_integration(self.test_config)
            self.logger.info("Data grid integration test passed")
            
        except Exception as e:
            self.logger.error(f"Data grid integration test failed: {e}")
            raise
    
    def test_models_grid_integration(self):
        """Test models grid module integration."""
        try:
            # Use test components for models grid testing
            self.test_components.test_models_grid_integration()
            self.logger.info("Models grid integration test passed")
            
        except Exception as e:
            self.logger.error(f"Models grid integration test failed: {e}")
            raise
    
    def test_ai_module_integration(self):
        """Test AI module integration."""
        try:
            # Use test components for AI module testing
            self.test_components.test_ai_module_integration(self.test_config)
            self.logger.info("AI module integration test passed")
            
        except Exception as e:
            self.logger.error(f"AI module integration test failed: {e}")
            raise
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        try:
            self.end_to_end_tester.test_end_to_end_workflow(self.test_config)
            self.logger.info("End-to-end workflow test passed")
            
        except Exception as e:
            self.logger.error(f"End-to-end workflow test failed: {e}")
            raise


def main():
    """Run tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    main()
