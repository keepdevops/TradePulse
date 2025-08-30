"""
Subscription Manager
Handles message subscriptions and listening for the Message Bus client.
"""

import zmq
import time
import threading
from typing import Any, Dict, List, Optional, Callable
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SubscriptionManager:
    """Manages message subscriptions and listening for the Message Bus client."""
    
    def __init__(self, subscriber, client):
        """Initialize the subscription manager."""
        self.subscriber = subscriber
        self.client = client
        self.subscriptions: Dict[str, List[Callable]] = {}
        self.running = False
        self.listener_thread: Optional[threading.Thread] = None
    
    def subscribe(self, topic: str, callback: Optional[Callable] = None) -> bool:
        """
        Subscribe to a topic.
        
        Args:
            topic: Topic to subscribe to
            callback: Optional callback function for received messages
        
        Returns:
            True if subscription was successful
        """
        try:
            # Subscribe to topic
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
            
            # Store callback if provided
            if callback:
                if topic not in self.subscriptions:
                    self.subscriptions[topic] = []
                self.subscriptions[topic].append(callback)
            
            logger.info(f"Subscribed to topic: {topic}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to subscribe to topic '{topic}': {e}")
            return False
    
    def unsubscribe(self, topic: str) -> bool:
        """
        Unsubscribe from a topic.
        
        Args:
            topic: Topic to unsubscribe from
        
        Returns:
            True if unsubscription was successful
        """
        try:
            # Unsubscribe from topic
            self.subscriber.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            
            # Remove callbacks
            if topic in self.subscriptions:
                del self.subscriptions[topic]
            
            logger.info(f"Unsubscribed from topic: {topic}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unsubscribe from topic '{topic}': {e}")
            return False
    
    def start_listening(self) -> None:
        """Start the message listener thread."""
        if self.running:
            logger.warning("Message listener already running")
            return
        
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()
        logger.info("Message listener started")
    
    def stop_listening(self) -> None:
        """Stop the message listener thread."""
        self.running = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=5)
        logger.info("Message listener stopped")
    
    def _listen_loop(self) -> None:
        """Message listening loop for background processing."""
        while self.running:
            try:
                logger.debug("🔍 Checking for messages...")
                message = self.client.receive(timeout=1000)
                
                if message:
                    logger.info(f"📥 Raw message received: {message}")
                    logger.info(f"📥 Message type: {type(message)}")
                    logger.info(f"📥 Message keys: {list(message.keys()) if isinstance(message, dict) else 'Not a dict'}")
                    
                    if 'topic' in message:
                        topic = message['topic']
                        data = message.get('data', {})
                        
                        logger.info(f"📥 Processed message - Topic: '{topic}', Data: {data}")
                        
                        # Execute callbacks for this topic
                        if topic in self.subscriptions:
                            logger.info(f"🔍 Found {len(self.subscriptions[topic])} callbacks for topic '{topic}'")
                            for callback in self.subscriptions[topic]:
                                try:
                                    logger.info(f"⚡ Executing callback for topic '{topic}'")
                                    callback(topic, data)
                                    logger.info(f"✅ Callback executed successfully for topic '{topic}'")
                                except Exception as e:
                                    logger.error(f"❌ Error in callback for topic '{topic}': {e}")
                        else:
                            logger.warning(f"⚠️ No callbacks found for topic '{topic}'")
                            logger.info(f"📋 Available topics: {list(self.subscriptions.keys())}")
                    else:
                        logger.warning(f"⚠️ Message received but no 'topic' field: {message}")
                else:
                    logger.debug("⏳ No message received (timeout)")
                
            except Exception as e:
                if self.running:  # Only log if we're supposed to be running
                    logger.error(f"Error in message listener: {e}")
                time.sleep(0.1)
