#!/usr/bin/env python3
"""
Data Grid Main Entry Point
Can run standalone or integrated with TradePulse.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_grid.fetcher import DataFetcher
from data_grid.visualizer import DataVisualizer
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for Data Grid."""
    try:
        logger.info("Starting Data Grid module...")
        
        # Load configuration
        config = ConfigLoader()
        
        # Initialize Message Bus client
        message_bus = MessageBusClient()
        
        # Initialize components
        fetcher = DataFetcher(config, message_bus)
        visualizer = DataVisualizer(config, message_bus)
        
        # Initialize message handler
        logger.info("Initializing message handler...")
        from data_grid.message_handler import DataGridMessageHandler
        message_handler = DataGridMessageHandler(message_bus, fetcher, visualizer)
        logger.info("Message handler initialized successfully")
        
        # Subscribe to relevant topics with handlers
        handlers = message_handler.get_message_handlers()
        logger.info(f"Available message handlers: {list(handlers.keys())}")
        for topic, handler in handlers.items():
            logger.info(f"Subscribing to topic '{topic}' with handler")
            message_bus.subscribe(topic, handler)
        logger.info("All message handlers subscribed successfully")
        
        # Start heartbeat
        message_bus.start_listening()
        
        logger.info("Data Grid module started successfully")
        
        # Keep running until interrupted
        try:
            while True:
                message_bus.send_heartbeat("data_grid")
                time.sleep(30)  # Send heartbeat every 30 seconds
                
        except KeyboardInterrupt:
            logger.info("Data Grid module interrupted by user")
        
    except Exception as e:
        logger.error(f"Error in Data Grid module: {e}")
        sys.exit(1)
    finally:
        if 'message_bus' in locals():
            message_bus.close()
        logger.info("Data Grid module stopped")


if __name__ == "__main__":
    main()
