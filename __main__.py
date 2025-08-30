#!/usr/bin/env python3
"""
Models Grid Main Entry Point
Can run standalone or integrated with TradePulse.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models_grid.trainer import ModelTrainer
from models_grid.predictor import ModelPredictor
from models_grid.visualizer import ModelVisualizer
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for Models Grid."""
    try:
        logger.info("Starting Models Grid module...")
        
        # Load configuration
        config = ConfigLoader()
        
        # Initialize Message Bus client
        message_bus = MessageBusClient()
        
        # Initialize components
        trainer = ModelTrainer(config, message_bus)
        predictor = ModelPredictor(config, message_bus)
        visualizer = ModelVisualizer(config, message_bus)
        
        # Subscribe to relevant topics
        message_bus.subscribe("training_request")
        message_bus.subscribe("prediction_request")
        message_bus.subscribe("visualization_request")
        
        # Start heartbeat
        message_bus.start_listening()
        
        logger.info("Models Grid module started successfully")
        
        # Keep running until interrupted
        try:
            while True:
                message_bus.send_heartbeat("models_grid")
                time.sleep(30)  # Send heartbeat every 30 seconds
                
        except KeyboardInterrupt:
            logger.info("Models Grid module interrupted by user")
        
    except Exception as e:
        logger.error(f"Error in Models Grid module: {e}")
        sys.exit(1)
    finally:
        if 'message_bus' in locals():
            message_bus.close()
        logger.info("Models Grid module stopped")


if __name__ == "__main__":
    main()
