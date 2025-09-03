#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Message Handler
Handles message bus operations
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    """Handles message bus operations"""
    
    def __init__(self, message_bus):
        self.message_bus = message_bus
    
    def send_message(self, message: Dict[str, Any]) -> bool:
        """Send message via message bus"""
        try:
            if self.message_bus and hasattr(self.message_bus, 'send_message'):
                return self.message_bus.send_message(message)
            else:
                logger.warning("Message bus not available")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive message via message bus"""
        try:
            if self.message_bus and hasattr(self.message_bus, 'receive_message'):
                return self.message_bus.receive_message()
            else:
                logger.warning("Message bus not available")
                return None
                
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            return None
