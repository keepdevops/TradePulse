"""
Message Handlers
Contains methods for handling message publishing and receiving.
"""

import zmq
import json
import time
from typing import Any, Dict, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageHandlers:
    """
    Class for handling message publishing and receiving.
    
    This class contains the message handling methods that were extracted
    from MessageBusClient to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the message handlers."""
        pass
    
    def publish_message(self, publisher: zmq.Socket, topic: str, message: Any) -> bool:
        """
        Publish a message to a topic.
        
        Args:
            publisher: ZMQ publisher socket
            topic: Message topic (e.g., 'data_updated', 'trading_signal')
            message: Message data (will be JSON serialized)
        
        Returns:
            True if message was sent successfully
        """
        try:
            # Prepare message with topic and data
            message_data = {
                'topic': topic,
                'timestamp': time.time(),
                'data': message
            }
            
            # Serialize to JSON
            json_message = json.dumps(message_data)
            
            # Send message
            publisher.send_string(f"{topic} {json_message}")
            
            logger.debug(f"Published message to topic '{topic}': {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish message to topic '{topic}': {e}")
            return False
    
    def receive_message(self, subscriber: zmq.Socket, timeout: Optional[int], default_timeout: int) -> Optional[Dict[str, Any]]:
        """
        Receive a message from subscribed topics.
        
        Args:
            subscriber: ZMQ subscriber socket
            timeout: Timeout in milliseconds (None for no timeout)
            default_timeout: Default timeout value
        
        Returns:
            Received message data or None if timeout
        """
        try:
            # Set timeout
            if timeout is not None:
                subscriber.setsockopt(zmq.RCVTIMEO, timeout)
            else:
                subscriber.setsockopt(zmq.RCVTIMEO, default_timeout)
            
            # Receive message
            message = subscriber.recv_string()
            
            # Parse message
            if ' ' in message:
                topic, json_data = message.split(' ', 1)
                try:
                    data = json.loads(json_data)
                    logger.debug(f"Received message on topic '{topic}': {data}")
                    return data
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in message: {json_data}")
                    return None
            else:
                logger.warning(f"Invalid message format: {message}")
                return None
                
        except zmq.Again:
            # Timeout
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return None
