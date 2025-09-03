#!/usr/bin/env python3
"""
TradePulse Dataset Activator - Callbacks Manager
Callback management for the dataset activator
"""

import logging
from typing import List, Callable

logger = logging.getLogger(__name__)

class DatasetActivatorCallbacks:
    """Callback management for dataset activator"""
    
    def __init__(self, core_activator):
        self.core_activator = core_activator
        self.on_dataset_change_callbacks = []
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add callback for dataset change events"""
        if callback not in self.on_dataset_change_callbacks:
            self.on_dataset_change_callbacks.append(callback)
            logger.info(f"✅ Added dataset change callback for {self.core_activator.module_name}")
    
    def remove_dataset_change_callback(self, callback: Callable):
        """Remove dataset change callback"""
        if callback in self.on_dataset_change_callbacks:
            self.on_dataset_change_callbacks.remove(callback)
            logger.info(f"✅ Removed dataset change callback for {self.core_activator.module_name}")
    
    def notify_dataset_change(self, change_type: str, dataset_id: str):
        """Notify all callbacks of dataset changes"""
        try:
            for callback in self.on_dataset_change_callbacks:
                try:
                    callback(change_type, dataset_id)
                except Exception as e:
                    logger.error(f"Callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify dataset change: {e}")
    
    def get_callbacks(self) -> List[Callable]:
        """Get list of registered callbacks"""
        return self.on_dataset_change_callbacks.copy()
    
    def clear_callbacks(self):
        """Clear all registered callbacks"""
        try:
            count = len(self.on_dataset_change_callbacks)
            self.on_dataset_change_callbacks.clear()
            logger.info(f"🗑️ Cleared {count} dataset change callbacks")
        except Exception as e:
            logger.error(f"Failed to clear callbacks: {e}")
    
    def get_callback_count(self) -> int:
        """Get number of registered callbacks"""
        return len(self.on_dataset_change_callbacks)
    
    def has_callbacks(self) -> bool:
        """Check if any callbacks are registered"""
        return len(self.on_dataset_change_callbacks) > 0
    
    def validate_callback(self, callback: Callable) -> bool:
        """Validate callback function"""
        try:
            # Check if it's callable
            if not callable(callback):
                return False
            
            # Check if it has the right signature (optional)
            import inspect
            sig = inspect.signature(callback)
            params = list(sig.parameters.keys())
            
            # Should accept at least 2 parameters (change_type, dataset_id)
            if len(params) < 2:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate callback: {e}")
            return False
    
    def register_callback_safely(self, callback: Callable) -> bool:
        """Safely register a callback with validation"""
        try:
            if not self.validate_callback(callback):
                logger.warning(f"⚠️ Invalid callback provided: {callback}")
                return False
            
            self.add_dataset_change_callback(callback)
            return True
            
        except Exception as e:
            logger.error(f"Failed to register callback safely: {e}")
            return False

