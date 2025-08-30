#!/usr/bin/env python3
"""
AI Module Main Entry Point
Can run standalone or integrated with TradePulse.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_module.strategy_generator import AIStrategyGenerator
from ai_module.risk_manager import RiskManager
from ai_module.strategy_calculations import StrategyCalculations
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for AI Module."""
    try:
        logger.info("Starting AI Module...")
        
        # Load configuration
        config = ConfigLoader()
        
        # Initialize Message Bus client
        message_bus = MessageBusClient()
        
        # Initialize components
        strategy_generator = AIStrategyGenerator(config, message_bus)
        risk_manager = RiskManager()
        strategy_calculations = StrategyCalculations()
        
        # Initialize portfolio optimizer
        from .portfolio_optimizer import PortfolioOptimizer
        portfolio_optimizer = PortfolioOptimizer()
        
        # Initialize message handler
        from .message_handler import AIModuleMessageHandler
        message_handler = AIModuleMessageHandler(
            message_bus, strategy_generator, risk_manager, portfolio_optimizer
        )
        
        # Subscribe to relevant topics with handlers
        handlers = message_handler.get_message_handlers()
        for topic, handler in handlers.items():
            message_bus.subscribe(topic, handler)
        
        # Start heartbeat
        message_bus.start_listening()
        
        logger.info("AI Module started successfully")
        
        # Keep running until interrupted
        try:
            while True:
                message_bus.send_heartbeat("ai_module")
                time.sleep(30)  # Send heartbeat every 30 seconds
                
        except KeyboardInterrupt:
            logger.info("AI Module interrupted by user")
        
    except Exception as e:
        logger.error(f"Error in AI Module: {e}")
        sys.exit(1)
    finally:
        if 'message_bus' in locals():
            message_bus.close()
        logger.info("AI Module stopped")


if __name__ == "__main__":
    main()
