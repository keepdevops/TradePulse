#!/usr/bin/env python3
"""
TradePulse Message Bus Client v10.11
ZeroMQ-based message bus client for inter-service communication
"""

import zmq
import json
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MessageBusClient:
    """ZeroMQ-based message bus client for inter-service communication"""
    
    def __init__(self, host: str = "localhost", port: int = 5555):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.connected = False
        self.timeout = 5000  # 5 seconds
        
    def connect(self) -> bool:
        """Connect to the message bus server"""
        try:
            self.socket.connect(f"tcp://{self.host}:{self.port}")
            self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
            self.socket.setsockopt(zmq.SNDTIMEO, self.timeout)
            self.connected = True
            logger.info(f"Connected to Message Bus Server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Message Bus Server: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the message bus server"""
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()
        self.connected = False
        logger.info("Disconnected from Message Bus Server")
    
    def send_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a message to the message bus server"""
        if not self.connected:
            if not self.connect():
                return None
        
        try:
            self.socket.send_json(message)
            response = self.socket.recv_json()
            return response
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.connected = False
            return None
    
    def subscribe(self, topic: str) -> bool:
        """Subscribe to a topic"""
        message = {
            "type": "subscribe",
            "data": {"topic": topic}
        }
        response = self.send_message(message)
        return response and response.get("status") == "success"
    
    def publish(self, topic: str, message: Dict[str, Any]) -> bool:
        """Publish a message to a topic"""
        msg_data = {
            "type": "publish",
            "data": {
                "topic": topic,
                "message": message
            }
        }
        response = self.send_message(msg_data)
        return response and response.get("status") == "success"
    
    def request_status(self) -> Optional[Dict[str, Any]]:
        """Request server status"""
        message = {
            "type": "request",
            "data": {"request_type": "status"}
        }
        response = self.send_message(message)
        if response and response.get("status") == "success":
            return response.get("data")
        return None
    
    def ping(self) -> bool:
        """Ping the server to check connectivity"""
        message = {
            "type": "ping",
            "data": {}
        }
        response = self.send_message(message)
        return response and response.get("status") == "success"
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

class MockMessageBusClient:
    """Mock message bus client for testing and development"""
    
    def __init__(self):
        self.connected = True
        self.message_history = []
        
    def connect(self) -> bool:
        return True
    
    def disconnect(self):
        self.connected = False
    
    def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        self.message_history.append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        return {"status": "success", "message": "Mock response"}
    
    def subscribe(self, topic: str) -> bool:
        return True
    
    def publish(self, topic: str, message: Dict[str, Any]) -> bool:
        self.message_history.append({
            "topic": topic,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def request_status(self) -> Dict[str, Any]:
        return {
            "running": True,
            "port": 5555,
            "subscribers_count": 0,
            "message_history_count": len(self.message_history),
            "timestamp": datetime.now().isoformat()
        }
    
    def ping(self) -> bool:
        return True


