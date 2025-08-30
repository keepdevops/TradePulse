#!/usr/bin/env python3
"""
Message Bus Client
ZeroMQ-based publish/subscribe messaging system for inter-module communication.
"""

import zmq
import json
import time
from typing import Any, Optional, Callable, Dict
from utils.logger import setup_logger
from utils.message_handlers import MessageHandlers
from utils.subscription_manager import SubscriptionManager

logger = setup_logger(__name__)


class MessageBusClient:
    """
    ZeroMQ-based Message Bus client for inter-module communication.
    
    Supports publish/subscribe pattern for seamless communication between
    TradePulse modules and the Redline utility.
    """
    
    def __init__(self, host: str = "localhost", port: int = 5555, timeout: int = 5000):
        """
        Initialize the Message Bus client.
        
        Args:
            host: Message Bus host address
            port: Message Bus port
            timeout: Timeout for receive operations (milliseconds)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.context = zmq.Context()
        
        # Socket for publishing messages (connect to publisher port)
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.connect(f"tcp://{host}:{port}")
        
        # Socket for subscribing to messages (connect to subscriber port)
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(f"tcp://{host}:{port + 1}")
        
        # Message handlers and subscription manager
        self.message_handlers = MessageHandlers()
        self.subscription_manager = SubscriptionManager(self.subscriber, self)
        
        logger.info(f"Message Bus client initialized for {host}:{port} (publish) and {host}:{port + 1} (subscribe)")
    
    def publish(self, topic: str, message: Any) -> bool:
        """
        Publish a message to a topic.
        
        Args:
            topic: Message topic (e.g., 'data_updated', 'trading_signal')
            message: Message data (will be JSON serialized)
        
        Returns:
            True if message was sent successfully
        """
        return self.message_handlers.publish_message(self.publisher, topic, message)
    
    def subscribe(self, topic: str, callback: Optional[Callable] = None) -> bool:
        """Subscribe to a topic."""
        return self.subscription_manager.subscribe(topic, callback)
    
    def unsubscribe(self, topic: str) -> bool:
        """Unsubscribe from a topic."""
        return self.subscription_manager.unsubscribe(topic)
    
    def receive(self, timeout: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Receive a message from subscribed topics.
        
        Args:
            timeout: Timeout in milliseconds (None for no timeout)
        
        Returns:
            Received message data or None if timeout
        """
        return self.message_handlers.receive_message(self.subscriber, timeout, self.timeout)
    
    def start_listening(self) -> None:
        """Start the message listener thread."""
        self.subscription_manager.start_listening()
    
    def stop_listening(self) -> None:
        """Stop the message listener thread."""
        self.subscription_manager.stop_listening()
    
    def send_heartbeat(self, module_name: str) -> bool:
        """
        Send a heartbeat message for module health monitoring.
        
        Args:
            module_name: Name of the module sending heartbeat
        
        Returns:
            True if heartbeat was sent successfully
        """
        heartbeat_data = {
            'module': module_name,
            'status': 'healthy',
            'timestamp': time.time()
        }
        return self.publish(f"{module_name}_heartbeat", heartbeat_data)
    
    def close(self) -> None:
        """Close the Message Bus client and clean up resources."""
        try:
            self.stop_listening()
            
            # Close sockets
            self.publisher.close()
            self.subscriber.close()
            
            # Terminate context
            self.context.term()
            
            logger.info("Message Bus client closed")
            
        except Exception as e:
            logger.error(f"Error closing Message Bus client: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()