#!/usr/bin/env python3
"""
TradePulse Message Bus Server v10.11
ZeroMQ-based message bus for inter-service communication
"""

import zmq
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageBusServer:
    """ZeroMQ-based message bus server for inter-service communication"""
    
    def __init__(self, port: int = 5555):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.running = False
        self.subscribers: Dict[str, list] = {}
        self.message_history: list = []
        
    def start(self):
        """Start the message bus server"""
        try:
            self.socket.bind(f"tcp://*:{self.port}")
            logger.info(f"Message Bus Server started on port {self.port}")
            self.running = True
            
            while self.running:
                try:
                    # Wait for message with timeout
                    message = self.socket.recv_json(flags=zmq.NOBLOCK)
                    response = self._handle_message(message)
                    self.socket.send_json(response)
                except zmq.Again:
                    # No message received, continue
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    self.socket.send_json({"status": "error", "message": str(e)})
                    
        except Exception as e:
            logger.error(f"Failed to start Message Bus Server: {e}")
            raise
        finally:
            self.stop()
    
    def stop(self):
        """Stop the message bus server"""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()
        logger.info("Message Bus Server stopped")
    
    def _handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming messages"""
        try:
            msg_type = message.get("type", "")
            msg_data = message.get("data", {})
            
            logger.info(f"Received message type: {msg_type}")
            
            if msg_type == "subscribe":
                return self._handle_subscribe(msg_data)
            elif msg_type == "publish":
                return self._handle_publish(msg_data)
            elif msg_type == "request":
                return self._handle_request(msg_data)
            elif msg_type == "ping":
                return {"status": "success", "message": "pong", "timestamp": datetime.now().isoformat()}
            else:
                return {"status": "error", "message": f"Unknown message type: {msg_type}"}
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {"status": "error", "message": str(e)}
    
    def _handle_subscribe(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription requests"""
        topic = data.get("topic", "")
        if topic:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            # In a real implementation, you'd store the subscriber's address
            logger.info(f"Subscription to topic: {topic}")
            return {"status": "success", "message": f"Subscribed to {topic}"}
        return {"status": "error", "message": "No topic specified"}
    
    def _handle_publish(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle publish requests"""
        topic = data.get("topic", "")
        message = data.get("message", {})
        
        if topic and message:
            # Store message in history
            self.message_history.append({
                "topic": topic,
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 1000 messages
            if len(self.message_history) > 1000:
                self.message_history = self.message_history[-1000:]
            
            logger.info(f"Published to topic: {topic}")
            return {"status": "success", "message": f"Published to {topic}"}
        
        return {"status": "error", "message": "Topic and message required"}
    
    def _handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general requests"""
        request_type = data.get("request_type", "")
        
        if request_type == "status":
            return {
                "status": "success",
                "data": {
                    "running": self.running,
                    "port": self.port,
                    "subscribers_count": len(self.subscribers),
                    "message_history_count": len(self.message_history),
                    "timestamp": datetime.now().isoformat()
                }
            }
        elif request_type == "history":
            return {
                "status": "success",
                "data": {
                    "history": self.message_history[-100:]  # Last 100 messages
                }
            }
        else:
            return {"status": "error", "message": f"Unknown request type: {request_type}"}

def main():
    """Main entry point for the message bus server"""
    # Get port from environment or use default
    port = int(os.getenv("ZMQ_PORT", "5555"))
    
    # Create and start server
    server = MessageBusServer(port=port)
    
    try:
        logger.info("Starting TradePulse Message Bus Server v10.11")
        server.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        server.stop()

if __name__ == "__main__":
    main()


