#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Performance Metrics
Handles performance metrics calculation and storage
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Handles performance metrics calculation and storage"""
    
    def __init__(self):
        self.metrics = {}
        self.history = []
        self.thresholds = {}
        
        # Initialize metrics
        self.init_metrics()
        self.init_thresholds()
    
    def init_metrics(self):
        """Initialize performance metrics"""
        try:
            self.metrics = {
                'total_operations': 0,
                'average_response_time': 0.0,
                'slowest_operation': None,
                'fastest_operation': None,
                'error_count': 0,
                'success_rate': 100.0,
                'last_check': datetime.now(),
                'memory_usage': 0.0,
                'cpu_usage': 0.0,
                'active_connections': 0,
                'queue_size': 0
            }
            
            logger.info("✅ Performance metrics initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize metrics: {e}")
    
    def init_thresholds(self):
        """Initialize performance thresholds"""
        try:
            self.thresholds = {
                'slow_operation_threshold': 1.0,  # Operations taking > 1 second are slow
                'memory_warning_threshold': 80.0,  # Memory usage > 80% triggers warning
                'cpu_warning_threshold': 70.0,  # CPU usage > 70% triggers warning
                'error_rate_warning_threshold': 5.0,  # Error rate > 5% triggers warning
                'response_time_warning_threshold': 0.5  # Response time > 0.5s triggers warning
            }
            
            logger.info("✅ Performance thresholds configured")
            
        except Exception as e:
            logger.error(f"Failed to initialize thresholds: {e}")
    
    def record_operation(self, operation_name: str, duration: float, success: bool = True):
        """Record an operation's performance"""
        try:
            # Update operation count
            self.metrics['total_operations'] += 1
            
            # Update response time metrics
            if self.metrics['slowest_operation'] is None or duration > self.metrics['slowest_operation']['duration']:
                self.metrics['slowest_operation'] = {
                    'name': operation_name,
                    'duration': duration,
                    'timestamp': datetime.now()
                }
            
            if self.metrics['fastest_operation'] is None or duration < self.metrics['fastest_operation']['duration']:
                self.metrics['fastest_operation'] = {
                    'name': operation_name,
                    'duration': duration,
                    'timestamp': datetime.now()
                }
            
            # Update average response time
            total_time = self.metrics['average_response_time'] * (self.metrics['total_operations'] - 1) + duration
            self.metrics['average_response_time'] = total_time / self.metrics['total_operations']
            
            # Update error count and success rate
            if not success:
                self.metrics['error_count'] += 1
            
            self.metrics['success_rate'] = ((self.metrics['total_operations'] - self.metrics['error_count']) / 
                                          self.metrics['total_operations']) * 100
            
            # Add to history
            self.history.append({
                'operation': operation_name,
                'duration': duration,
                'success': success,
                'timestamp': datetime.now()
            })
            
            # Keep only last 1000 operations in history
            if len(self.history) > 1000:
                self.history = self.history[-1000:]
            
            logger.debug(f"Operation recorded: {operation_name} - {duration:.3f}s")
            
        except Exception as e:
            logger.error(f"Failed to record operation: {e}")
    
    def update_system_metrics(self, memory_usage: float, cpu_usage: float, 
                             active_connections: int = 0, queue_size: int = 0):
        """Update system-level metrics"""
        try:
            self.metrics['memory_usage'] = memory_usage
            self.metrics['cpu_usage'] = cpu_usage
            self.metrics['active_connections'] = active_connections
            self.metrics['queue_size'] = queue_size
            self.metrics['last_check'] = datetime.now()
            
            logger.debug(f"System metrics updated: Memory={memory_usage:.1f}%, CPU={cpu_usage:.1f}%")
            
        except Exception as e:
            logger.error(f"Failed to update system metrics: {e}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of current metrics"""
        try:
            return {
                'current_metrics': self.metrics.copy(),
                'thresholds': self.thresholds.copy(),
                'history_count': len(self.history),
                'last_operations': self.history[-10:] if self.history else []
            }
            
        except Exception as e:
            logger.error(f"Failed to get metrics summary: {e}")
            return {}
    
    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts based on thresholds"""
        try:
            from .alert_checker import AlertChecker
            checker = AlertChecker(self.metrics, self.thresholds)
            return checker.check_alerts()
            
        except Exception as e:
            logger.error(f"Failed to get performance alerts: {e}")
            return []
    
    def get_metrics_history(self, hours: int = 24) -> pd.DataFrame:
        """Get metrics history for specified time period"""
        try:
            if not self.history:
                return pd.DataFrame()
            
            # Filter history by time
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_history = [h for h in self.history if h['timestamp'] > cutoff_time]
            
            if not recent_history:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(recent_history)
            
            # Add time-based aggregations
            df['hour'] = df['timestamp'].dt.hour
            df['date'] = df['timestamp'].dt.date
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to get metrics history: {e}")
            return pd.DataFrame()
    
    def reset_metrics(self):
        """Reset all performance metrics"""
        try:
            self.init_metrics()
            self.history = []
            logger.info("✅ Performance metrics reset")
            
        except Exception as e:
            logger.error(f"Failed to reset metrics: {e}")
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to file"""
        try:
            from .metrics_exporter import MetricsExporter
            exporter = MetricsExporter(self.metrics, self.history)
            return exporter.export_metrics(filename)
            
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return ""
