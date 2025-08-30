#!/usr/bin/env python3
"""
Message Handler for Data Grid Module
Processes incoming messages and sends appropriate responses.
"""

import json
import time
from typing import Dict, Any, Optional
from utils.logger import setup_logger
from utils.message_bus_client import MessageBusClient

logger = setup_logger(__name__)


class DataGridMessageHandler:
    """Handles incoming messages for the Data Grid module."""
    
    def __init__(self, message_bus: MessageBusClient, fetcher, visualizer):
        """Initialize the message handler."""
        self.message_bus = message_bus
        self.fetcher = fetcher
        self.visualizer = visualizer
        self.logger = setup_logger(__name__)
        
    def handle_data_request(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle data request messages."""
        try:
            self.logger.info(f"Processing data request: {data}")
            
            # Extract request details
            request_id = data.get('id', 'unknown')
            symbol = data.get('symbol', 'AAPL')
            period = data.get('period', '1d')
            interval = data.get('interval', '1h')
            limit = data.get('limit', 100)
            
            # Simulate data fetching (in real implementation, this would call fetcher)
            response = {
                "id": request_id,
                "type": "data_response",
                "status": "success",
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "data_points": limit,
                "timestamp": time.time(),
                "message": f"Data request for {symbol} processed successfully"
            }
            
            # Send response
            self.message_bus.publish("data_response", json.dumps(response))
            self.logger.info(f"Sent data response for request {request_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling data request: {e}")
            # Send error response
            error_response = {
                "id": data.get('id', 'unknown'),
                "type": "data_response",
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
            self.message_bus.publish("data_response", json.dumps(error_response))
    
    def handle_visualization_request(self, topic: str, data: Dict[str, Any]) -> None:
        """Handle visualization request messages."""
        try:
            self.logger.info(f"Processing visualization request: {data}")
            
            # Extract request details
            request_id = data.get('id', 'unknown')
            chart_type = data.get('chart_type', 'line')
            symbol = data.get('symbol', 'AAPL')
            indicators = data.get('indicators', [])
            
            # Simulate chart creation (in real implementation, this would call visualizer)
            response = {
                "id": request_id,
                "type": "visualization_response",
                "status": "success",
                "chart_type": chart_type,
                "symbol": symbol,
                "indicators": indicators,
                "chart_path": f"./data/charts/{symbol}_{chart_type}_{int(time.time())}.png",
                "timestamp": time.time(),
                "message": f"Chart created successfully for {symbol}"
            }
            
            # Send response
            self.message_bus.publish("visualization_response", json.dumps(response))
            self.logger.info(f"Sent visualization response for request {request_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling visualization request: {e}")
            # Send error response
            error_response = {
                "id": data.get('id', 'unknown'),
                "type": "visualization_response",
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
            self.message_bus.publish("visualization_response", json.dumps(error_response))
    
    def get_message_handlers(self) -> Dict[str, callable]:
        """Get the message handlers for this module."""
        return {
            "data_request": self.handle_data_request,
            "visualization_request": self.handle_visualization_request
        }
