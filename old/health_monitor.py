#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Health Monitor
Handles system health monitoring and metrics collection
"""

import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
import time

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Handles system health monitoring and metrics collection"""
    
    def __init__(self):
        self.health_metrics = {}
        self.performance_history = []
        self.alert_thresholds = {}
        
        # Initialize monitoring
        self.init_health_metrics()
        self.setup_alert_thresholds()
    
    def init_health_metrics(self):
        """Initialize health metrics"""
        try:
            self.health_metrics = {
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'disk_usage': 0.0,
                'network_io': {'bytes_sent': 0, 'bytes_recv': 0},
                'process_count': 0,
                'uptime': 0,
                'last_check': datetime.now()
            }
            
            logger.info("✅ Health metrics initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize health metrics: {e}")
    
    def setup_alert_thresholds(self):
        """Setup alert thresholds for system monitoring"""
        try:
            self.alert_thresholds = {
                'cpu_usage': 80.0,  # Alert if CPU usage > 80%
                'memory_usage': 85.0,  # Alert if memory usage > 85%
                'disk_usage': 90.0,  # Alert if disk usage > 90%
                'process_count': 200,  # Alert if process count > 200
                'response_time': 5.0,  # Alert if response time > 5 seconds
                'error_rate': 5.0  # Alert if error rate > 5%
            }
            
            logger.info("✅ Alert thresholds configured")
            
        except Exception as e:
            logger.error(f"Failed to setup alert thresholds: {e}")
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv
            }
            
            # Process count
            process_count = len(psutil.pids())
            
            # Uptime
            uptime = time.time() - psutil.boot_time()
            
            # Update metrics
            self.health_metrics.update({
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'network_io': network_io,
                'process_count': process_count,
                'uptime': uptime,
                'last_check': datetime.now()
            })
            
            # Add to history
            self.performance_history.append({
                'timestamp': datetime.now(),
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'process_count': process_count
            })
            
            # Keep only last 1000 records
            if len(self.performance_history) > 1000:
                self.performance_history = self.performance_history[-1000:]
            
            logger.debug(f"✅ System metrics collected: CPU={cpu_usage:.1f}%, Memory={memory_usage:.1f}%")
            
            return self.health_metrics.copy()
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return {}
    
    def check_health_alerts(self) -> List[Dict[str, Any]]:
        """Check for health alerts based on thresholds"""
        try:
            alerts = []
            
            # Check CPU usage
            if self.health_metrics['cpu_usage'] > self.alert_thresholds['cpu_usage']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'cpu_usage',
                    'message': f"High CPU usage: {self.health_metrics['cpu_usage']:.1f}%",
                    'value': self.health_metrics['cpu_usage'],
                    'threshold': self.alert_thresholds['cpu_usage'],
                    'timestamp': datetime.now()
                })
            
            # Check memory usage
            if self.health_metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'memory_usage',
                    'message': f"High memory usage: {self.health_metrics['memory_usage']:.1f}%",
                    'value': self.health_metrics['memory_usage'],
                    'threshold': self.alert_thresholds['memory_usage'],
                    'timestamp': datetime.now()
                })
            
            # Check disk usage
            if self.health_metrics['disk_usage'] > self.alert_thresholds['disk_usage']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'disk_usage',
                    'message': f"High disk usage: {self.health_metrics['disk_usage']:.1f}%",
                    'value': self.health_metrics['disk_usage'],
                    'threshold': self.alert_thresholds['disk_usage'],
                    'timestamp': datetime.now()
                })
            
            # Check process count
            if self.health_metrics['process_count'] > self.alert_thresholds['process_count']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'process_count',
                    'message': f"High process count: {self.health_metrics['process_count']}",
                    'value': self.health_metrics['process_count'],
                    'threshold': self.alert_thresholds['process_count'],
                    'timestamp': datetime.now()
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check health alerts: {e}")
            return []
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health monitoring summary"""
        try:
            return {
                'current_metrics': self.health_metrics.copy(),
                'alert_thresholds': self.alert_thresholds.copy(),
                'performance_history_count': len(self.performance_history),
                'last_check': self.health_metrics.get('last_check'),
                'system_status': self._get_system_status()
            }
            
        except Exception as e:
            logger.error(f"Failed to get health summary: {e}")
            return {}
    
    def _get_system_status(self) -> str:
        """Get overall system status"""
        try:
            alerts = self.check_health_alerts()
            
            if not alerts:
                return 'healthy'
            elif len(alerts) <= 2:
                return 'warning'
            else:
                return 'critical'
                
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return 'unknown'
    
    def get_performance_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get performance history for specified time period"""
        try:
            if not self.performance_history:
                return []
            
            # Filter history by time
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_history = [
                record for record in self.performance_history 
                if record['timestamp'] > cutoff_time
            ]
            
            return recent_history
            
        except Exception as e:
            logger.error(f"Failed to get performance history: {e}")
            return []
    
    def reset_metrics(self):
        """Reset all health metrics"""
        try:
            self.init_health_metrics()
            self.performance_history.clear()
            
            logger.info("✅ Health metrics reset")
            
        except Exception as e:
            logger.error(f"Failed to reset health metrics: {e}")
    
    def update_alert_thresholds(self, new_thresholds: Dict[str, float]):
        """Update alert thresholds"""
        try:
            self.alert_thresholds.update(new_thresholds)
            
            logger.info("✅ Alert thresholds updated")
            
        except Exception as e:
            logger.error(f"Failed to update alert thresholds: {e}")
