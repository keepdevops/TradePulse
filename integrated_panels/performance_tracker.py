#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Performance Tracker
Handles performance tracking and optimization
"""

import panel as pn
import threading
import time
import psutil
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .performance_metrics import PerformanceMetrics
from .performance_display import PerformanceDisplay

logger = logging.getLogger(__name__)

class PerformanceTracker:
    """Handles performance tracking and optimization"""
    
    def __init__(self):
        self.tracking_active = False
        self.tracking_interval = 5  # seconds
        
        # Initialize components
        self.performance_metrics = PerformanceMetrics()
        self.performance_display = PerformanceDisplay(self.performance_metrics)
        
        # Setup tracker
        self.setup_performance_tracking()
    
    def setup_performance_tracking(self):
        """Setup performance tracking system"""
        try:
            logger.info("🔧 Setting up performance tracking")
            
            # Initialize system monitoring
            self.setup_system_monitoring()
            
            logger.info("✅ Performance tracking initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup performance tracking: {e}")
    
    def setup_system_monitoring(self):
        """Setup system monitoring"""
        try:
            # Initialize system metrics
            self.update_system_metrics()
            
            logger.info("✅ System monitoring setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup system monitoring: {e}")
    
    def start_tracking(self):
        """Start performance tracking"""
        try:
            if not self.tracking_active:
                self.tracking_active = True
                logger.info("🔄 Starting performance tracking")
                
                # Start tracking in background thread
                tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
                tracking_thread.start()
                
                logger.info("✅ Performance tracking started")
            
        except Exception as e:
            logger.error(f"Failed to start tracking: {e}")
    
    def stop_tracking(self):
        """Stop performance tracking"""
        try:
            self.tracking_active = False
            logger.info("🛑 Performance tracking stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop tracking: {e}")
    
    def _tracking_loop(self):
        """Main tracking loop"""
        try:
            while self.tracking_active:
                # Update system metrics
                self.update_system_metrics()
                
                # Wait for next update
                time.sleep(self.tracking_interval)
                
        except Exception as e:
            logger.error(f"Tracking loop failed: {e}")
            self.tracking_active = False
    
    def update_system_metrics(self):
        """Update system metrics"""
        try:
            # Get system information
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            
            # Update metrics
            self.performance_metrics.update_system_metrics(
                memory_usage=memory.percent,
                cpu_usage=cpu
            )
            
            logger.debug(f"System metrics updated: Memory={memory.percent:.1f}%, CPU={cpu:.1f}%")
            
        except Exception as e:
            logger.error(f"Failed to update system metrics: {e}")
    
    def record_operation(self, operation_name: str, duration: float, success: bool = True):
        """Record an operation's performance"""
        try:
            self.performance_metrics.record_operation(operation_name, duration, success)
            
        except Exception as e:
            logger.error(f"Failed to record operation: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            return self.performance_metrics.get_metrics_summary()
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {}
    
    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts"""
        try:
            return self.performance_metrics.get_performance_alerts()
            
        except Exception as e:
            logger.error(f"Failed to get performance alerts: {e}")
            return []
    
    def get_display_layout(self) -> pn.Column:
        """Get the performance display layout"""
        try:
            return self.performance_display.get_display_layout()
            
        except Exception as e:
            logger.error(f"Failed to get display layout: {e}")
            return pn.Column("Error: Failed to create display layout")
    
    def refresh_display(self):
        """Refresh the performance display"""
        try:
            self.performance_display.refresh_display()
            
        except Exception as e:
            logger.error(f"Failed to refresh display: {e}")
    
    def export_performance_data(self, filename: str = None) -> str:
        """Export performance data"""
        try:
            return self.performance_metrics.export_metrics(filename)
            
        except Exception as e:
            logger.error(f"Failed to export performance data: {e}")
            return ""
    
    def reset_performance_data(self):
        """Reset performance data"""
        try:
            self.performance_metrics.reset_metrics()
            self.refresh_display()
            
        except Exception as e:
            logger.error(f"Failed to reset performance data: {e}")
    
    def get_tracker_status(self) -> Dict[str, Any]:
        """Get tracker status"""
        try:
            return {
                'tracking_active': self.tracking_active,
                'tracking_interval': self.tracking_interval,
                'metrics_count': len(self.performance_metrics.history),
                'alerts_count': len(self.get_performance_alerts()),
                'last_update': self.performance_metrics.metrics.get('last_check'),
                'tracker_type': 'Performance Tracker'
            }
            
        except Exception as e:
            logger.error(f"Failed to get tracker status: {e}")
            return {}
    
    def profile_operation(self, operation_name: str):
        """Profile an operation using context manager"""
        try:
            from .operation_profiler import OperationProfiler
            return OperationProfiler(self, operation_name)
            
        except Exception as e:
            logger.error(f"Failed to create operation profiler: {e}")
            return None
