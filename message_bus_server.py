#!/usr/bin/env python3
"""
Message Bus Server
Simple ZeroMQ broker that routes messages between modules.
"""

import zmq
import json
import time
import threading
from typing import Dict, Set
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageBusServer:
    """Simple ZeroMQ message broker for routing messages between modules."""
    
    def __init__(self, host: str = "localhost", port: int = 5555):
        """Initialize the message bus server."""
        self.host = host
        self.port = port
        self.context = zmq.Context()
        
        # Socket for receiving from publishers
        self.publisher_socket = self.context.socket(zmq.SUB)
        self.publisher_socket.bind(f"tcp://{host}:{port}")
        self.publisher_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        
        # Socket for sending to subscribers
        self.subscriber_socket = self.context.socket(zmq.PUB)
        self.subscriber_socket.bind(f"tcp://{host}:{port + 1}")
        
        self.running = False
        
        logger.info(f"Message Bus Server initialized on {host}:{port} (publishers) and {host}:{port + 1} (subscribers)")
    
    def start(self):
        """Start the message bus server."""
        if self.running:
            logger.warning("Message Bus Server already running")
            return
        
        self.running = True
        logger.info("Starting Message Bus Server...")
        
        # Start message routing thread
        self.routing_thread = threading.Thread(target=self._route_messages, daemon=True)
        self.routing_thread.start()
        
        logger.info("Message Bus Server started successfully")
    
    def stop(self):
        """Stop the message bus server."""
        self.running = False
        if hasattr(self, 'routing_thread'):
            self.routing_thread.join(timeout=5)
        
        self.publisher_socket.close()
        self.subscriber_socket.close()
        self.context.term()
        
        logger.info("Message Bus Server stopped")
    
    def _route_messages(self):
        """Route messages from publishers to subscribers."""
        logger.info("Message routing started")
        
        while self.running:
            try:
                # Receive message from publisher
                message = self.publisher_socket.recv_string(flags=zmq.NOBLOCK)
                if message:
                    logger.info(f"📥 Received from publisher: {message}")
                    
                    # Forward to all subscribers
                    self.subscriber_socket.send_string(message)
                    logger.info(f"📤 Forwarded to subscribers: {message}")
                
            except zmq.Again:
                # No message available
                pass
            except Exception as e:
                if self.running:
                    logger.error(f"Error in message routing: {e}")
                time.sleep(0.1)
    
    def run_forever(self):
        """Run the server forever."""
        try:
            self.start()
            logger.info("Message Bus Server running. Press Ctrl+C to stop.")
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()


def main():
    """Main entry point for the Message Bus Server."""
    server = MessageBusServer()
    server.run_forever()


if __name__ == "__main__":
    main()