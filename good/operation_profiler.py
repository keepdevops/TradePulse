#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Operation Profiler
Handles operation profiling functionality
"""

import time
import logging

logger = logging.getLogger(__name__)

class OperationProfiler:
    """Context manager for profiling operations"""
    
    def __init__(self, tracker, name):
        self.tracker = tracker
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        """Start profiling the operation"""
        try:
            self.start_time = time.time()
            return self
            
        except Exception as e:
            logger.error(f"Failed to start profiling: {e}")
            return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop profiling and record the operation"""
        try:
            if self.start_time is not None:
                duration = time.time() - self.start_time
                success = exc_type is None
                self.tracker.record_operation(self.name, duration, success)
                
        except Exception as e:
            logger.error(f"Failed to stop profiling: {e}")
