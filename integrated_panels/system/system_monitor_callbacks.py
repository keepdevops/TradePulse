#!/usr/bin/env python3
"""
TradePulse System Monitor - Callbacks Manager
Callback management for the system monitor
"""

import threading
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemMonitorCallbacks:
    """Callback management for system monitor"""
    
    def __init__(self, core_monitor):
        self.core_monitor = core_monitor
    
    def start_monitoring(self):
        """Start system monitoring"""
        try:
            if not self.core_monitor.monitoring_active:
                self.core_monitor.monitoring_active = True
                logger.info("🔄 Starting system monitoring")
                
                # Start monitoring in background thread
                monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
                monitoring_thread.start()
                
                logger.info("✅ System monitoring started")
            else:
                logger.info("⚠️ System monitoring already active")
                
        except Exception as e:
            logger.error(f"Failed to start system monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        try:
            self.core_monitor.monitoring_active = False
            logger.info("🛑 System monitoring stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop system monitoring: {e}")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        try:
            while self.core_monitor.monitoring_active:
                # Collect system metrics
                self.core_monitor.health_monitor.collect_system_metrics()
                
                # Check for alerts
                alerts = self.core_monitor.health_monitor.check_health_alerts()
                if alerts:
                    self._handle_alerts(alerts)
                
                # Wait for next check
                time.sleep(self.core_monitor.monitoring_interval)
                
        except Exception as e:
            logger.error(f"Monitoring loop failed: {e}")
            self.core_monitor.monitoring_active = False
    
    def _handle_alerts(self, alerts: list):
        """Handle system alerts"""
        try:
            for alert in alerts:
                logger.warning(f"🚨 System Alert: {alert['message']}")
                
                # Here you would implement actual alert handling
                # (email notifications, logging, etc.)
                
        except Exception as e:
            logger.error(f"Failed to handle alerts: {e}")
    
    def _start_monitoring_callback(self, event=None):
        """Callback for starting monitoring"""
        try:
            self.start_monitoring()
            
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")
    
    def _stop_monitoring_callback(self, event=None):
        """Callback for stopping monitoring"""
        try:
            self.stop_monitoring()
            
        except Exception as e:
            logger.error(f"Failed to stop monitoring: {e}")
    
    def _refresh_status_callback(self, event=None):
        """Callback for refreshing status"""
        try:
            # Collect fresh metrics
            self.core_monitor.health_monitor.collect_system_metrics()
            
            logger.info("✅ System status refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh status: {e}")



