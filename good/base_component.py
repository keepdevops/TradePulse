#!/usr/bin/env python3
"""
TradePulse UI Base Component
Base class for all UI components
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict

class BaseComponent(ABC):
    """Base class for all UI components"""
    
    def __init__(self, name: str):
        self.name = name
        self.components = {}
        self.callbacks = {}
    
    @abstractmethod
    def create_components(self):
        """Create the component's UI elements"""
        pass
    
    @abstractmethod
    def get_layout(self):
        """Get the component's layout"""
        pass
    
    def add_callback(self, event_name: str, callback: Callable):
        """Add a callback for an event"""
        self.callbacks[event_name] = callback
    
    def trigger_callback(self, event_name: str, *args, **kwargs):
        """Trigger a callback"""
        if event_name in self.callbacks:
            self.callbacks[event_name](*args, **kwargs)
