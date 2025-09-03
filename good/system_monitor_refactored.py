#!/usr/bin/env python3
"""
TradePulse Integrated Panels - System Monitor (Refactored)
Handles system monitoring and health checks
Refactored to be under 200 lines
"""

import panel as pn
import logging

from .system.system_monitor_core import SystemMonitorCore

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Handles system monitoring and health checks"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_monitor = SystemMonitorCore()
    
    def setup_monitoring(self):
        """Setup system monitoring"""
        # Delegate to refactored implementation
        self._refactored_monitor.setup_monitoring()
    
    def start_monitoring(self):
        """Start system monitoring"""
        # Delegate to refactored implementation
        self._refactored_monitor.start_monitoring()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        # Delegate to refactored implementation
        self._refactored_monitor.stop_monitoring()
    
    def get_system_health(self):
        """Get current system health status"""
        # Delegate to refactored implementation
        return self._refactored_monitor.get_system_health()
    
    def get_system_alerts(self):
        """Get current system alerts"""
        # Delegate to refactored implementation
        return self._refactored_monitor.get_system_alerts()
    
    def get_performance_history(self, hours: int = 24):
        """Get performance history"""
        # Delegate to refactored implementation
        return self._refactored_monitor.get_performance_history(hours)
    
    def reset_monitoring(self):
        """Reset monitoring data"""
        # Delegate to refactored implementation
        self._refactored_monitor.reset_monitoring()
    
    def update_alert_thresholds(self, new_thresholds):
        """Update alert thresholds"""
        # Delegate to refactored implementation
        self._refactored_monitor.update_alert_thresholds(new_thresholds)
    
    def create_monitoring_dashboard(self):
        """Create system monitoring dashboard"""
        # Delegate to refactored implementation
        return self._refactored_monitor.create_monitoring_dashboard()
    
    def get_monitor_status(self):
        """Get monitor status information"""
        # Delegate to refactored implementation
        return self._refactored_monitor.get_monitor_status()

