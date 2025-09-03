#!/usr/bin/env python3
"""
TradePulse System Monitor - Core Functionality
Core system monitor class with basic functionality
"""

import panel as pn
import pandas as pd
import threading
import time
import logging
from typing import Dict, Any
from datetime import datetime

from .system_monitor_components import SystemMonitorComponents
from .system_monitor_operations import SystemMonitorOperations
from .system_monitor_management import SystemMonitorManagement
from .system_monitor_callbacks import SystemMonitorCallbacks
from ..system_monitoring.health_monitor import HealthMonitor

logger = logging.getLogger(__name__)

class SystemMonitorCore:
    """Core system monitor functionality"""
    
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_interval = 10  # seconds
        
        # Initialize components
        self.components = SystemMonitorComponents()
        self.operations = SystemMonitorOperations()
        self.management = SystemMonitorManagement()
        self.callbacks = SystemMonitorCallbacks(self)
        
        # Initialize health monitor
        self.health_monitor = HealthMonitor()
        
        self.setup_monitoring()
    
    def setup_monitoring(self):
        """Setup system monitoring"""
        try:
            logger.info("🔧 Setting up system monitoring")
            
            # Initial health check
            self.health_monitor.collect_system_metrics()
            
            logger.info("✅ System monitoring initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup system monitoring: {e}")
    
    def start_monitoring(self):
        """Start system monitoring"""
        return self.callbacks.start_monitoring()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        return self.callbacks.stop_monitoring()
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health status"""
        try:
            return self.health_monitor.get_health_summary()
            
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return {}
    
    def get_system_alerts(self) -> list:
        """Get current system alerts"""
        try:
            return self.health_monitor.check_health_alerts()
            
        except Exception as e:
            logger.error(f"Failed to get system alerts: {e}")
            return []
    
    def get_performance_history(self, hours: int = 24) -> list:
        """Get performance history"""
        try:
            return self.health_monitor.get_performance_history(hours)
            
        except Exception as e:
            logger.error(f"Failed to get performance history: {e}")
            return []
    
    def reset_monitoring(self):
        """Reset monitoring data"""
        try:
            self.health_monitor.reset_metrics()
            
            logger.info("✅ System monitoring reset")
            
        except Exception as e:
            logger.error(f"Failed to reset monitoring: {e}")
    
    def update_alert_thresholds(self, new_thresholds: Dict[str, float]):
        """Update alert thresholds"""
        try:
            self.health_monitor.update_alert_thresholds(new_thresholds)
            
        except Exception as e:
            logger.error(f"Failed to update alert thresholds: {e}")
    
    def create_monitoring_dashboard(self) -> pn.Column:
        """Create system monitoring dashboard"""
        return self.management.create_monitoring_dashboard(self)
    
    def get_monitor_status(self) -> Dict[str, Any]:
        """Get monitor status information"""
        try:
            return {
                'monitoring_active': self.monitoring_active,
                'monitoring_interval': self.monitoring_interval,
                'health_monitor_status': self.health_monitor.get_health_summary(),
                'monitor_type': 'System Monitor'
            }
            
        except Exception as e:
            logger.error(f"Failed to get monitor status: {e}")
            return {}

