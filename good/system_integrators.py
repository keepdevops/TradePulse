#!/usr/bin/env python3
"""
TradePulse Integrated Panels - System Integrators
Handles integration with various TradePulse system components
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemIntegrators:
    """Handles integration with various TradePulse system components"""
    
    def __init__(self):
        self.message_bus = None
        self.database = None
        self.models = {}
        self.ai_handlers = {}
        self.data_components = {}
        self.portfolio_strategies = {}
        self.visualization_components = {}
        
        # Initialize integrations
        self.init_message_bus()
        self.init_database()
        self.init_models()
        self.init_ai_handlers()
        self.init_data_components()
        self.init_portfolio_strategies()
        self.init_visualization_components()
    
    def init_message_bus(self):
        """Initialize message bus integration"""
        try:
            from utils.message_bus_client import MessageBusClient
            self.message_bus = MessageBusClient()
            logger.info("✅ MessageBusClient initialized successfully")
        except ImportError:
            logger.warning("⚠️ MessageBusClient not available, using mock")
            self.message_bus = self._create_mock_message_bus()
        except Exception as e:
            logger.error(f"Failed to initialize message bus: {e}")
            self.message_bus = self._create_mock_message_bus()
    
    def init_database(self):
        """Initialize database integration"""
        try:
            from utils.database import Database
            self.database = Database()
            logger.info("✅ Database initialized successfully")
        except ImportError:
            logger.warning("⚠️ Database not available, using mock")
            self.database = self._create_mock_database()
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            self.database = self._create_mock_database()
    
    def init_models(self):
        """Initialize model integrations"""
        try:
            from .import_managers.model_importer import ModelImporter
            importer = ModelImporter()
            self.models = importer.import_models()
            
            logger.info(f"✅ {len(self.models)} models initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
    
    def init_ai_handlers(self):
        """Initialize AI handler integrations"""
        try:
            from .import_managers.ai_handler_importer import AIHandlerImporter
            importer = AIHandlerImporter()
            self.ai_handlers = importer.import_handlers()
            
            logger.info(f"✅ {len(self.ai_handlers)} AI handlers initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI handlers: {e}")
    
    def init_data_components(self):
        """Initialize data component integrations"""
        try:
            from .import_managers.data_component_importer import DataComponentImporter
            importer = DataComponentImporter()
            self.data_components = importer.import_components()
            
            logger.info(f"✅ {len(self.data_components)} data components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize data components: {e}")
    
    def init_portfolio_strategies(self):
        """Initialize portfolio strategy integrations"""
        try:
            from .import_managers.portfolio_strategy_importer import PortfolioStrategyImporter
            importer = PortfolioStrategyImporter()
            self.portfolio_strategies = importer.import_strategies()
            
            logger.info(f"✅ {len(self.portfolio_strategies)} portfolio strategies initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize portfolio strategies: {e}")
    
    def init_visualization_components(self):
        """Initialize visualization component integrations"""
        try:
            from .import_managers.visualization_component_importer import VisualizationComponentImporter
            importer = VisualizationComponentImporter()
            self.visualization_components = importer.import_components()
            
            logger.info(f"✅ {len(self.visualization_components)} visualization components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize visualization components: {e}")
    
    def _create_mock_message_bus(self):
        """Create mock message bus for testing"""
        from .mock_components import MockMessageBus
        return MockMessageBus()
    
    def _create_mock_database(self):
        """Create mock database for testing"""
        from .mock_components import MockDatabase
        return MockDatabase()
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status for all components"""
        try:
            return {
                'message_bus': {
                    'available': self.message_bus is not None,
                    'connected': getattr(self.message_bus, 'connected', False) if self.message_bus else False
                },
                'database': {
                    'available': self.database is not None,
                    'connected': getattr(self.database, 'connected', False) if self.database else False
                },
                'models': {
                    'count': len(self.models),
                    'available': list(self.models.keys())
                },
                'ai_handlers': {
                    'count': len(self.ai_handlers),
                    'available': list(self.ai_handlers.keys())
                },
                'data_components': {
                    'count': len(self.data_components),
                    'available': list(self.data_components.keys())
                },
                'portfolio_strategies': {
                    'count': len(self.portfolio_strategies),
                    'available': list(self.portfolio_strategies.keys())
                },
                'visualization_components': {
                    'count': len(self.visualization_components),
                    'available': list(self.visualization_components.keys())
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get integration status: {e}")
            return {}
    
    def test_integrations(self) -> Dict[str, bool]:
        """Test all integrations"""
        try:
            from .integration_tester import IntegrationTester
            tester = IntegrationTester(self)
            return tester.test_all_integrations()
            
        except Exception as e:
            logger.error(f"Failed to test integrations: {e}")
            return {}
