#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Alert Checker
Handles performance alert checking
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class AlertChecker:
    """Handles performance alert checking"""
    
    def __init__(self, metrics: Dict[str, Any], thresholds: Dict[str, Any]):
        self.metrics = metrics
        self.thresholds = thresholds
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts based on thresholds"""
        try:
            alerts = []
            
            # Check response time
            if self.metrics['average_response_time'] > self.thresholds['response_time_warning_threshold']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'response_time',
                    'message': f"Average response time ({self.metrics['average_response_time']:.3f}s) exceeds threshold",
                    'value': self.metrics['average_response_time'],
                    'threshold': self.thresholds['response_time_warning_threshold']
                })
            
            # Check memory usage
            if self.metrics['memory_usage'] > self.thresholds['memory_warning_threshold']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'memory_usage',
                    'message': f"Memory usage ({self.metrics['memory_usage']:.1f}%) exceeds threshold",
                    'value': self.metrics['memory_usage'],
                    'threshold': self.thresholds['memory_warning_threshold']
                })
            
            # Check CPU usage
            if self.metrics['cpu_usage'] > self.thresholds['cpu_warning_threshold']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'cpu_usage',
                    'message': f"CPU usage ({self.metrics['cpu_usage']:.1f}%) exceeds threshold",
                    'value': self.metrics['cpu_usage'],
                    'threshold': self.thresholds['cpu_warning_threshold']
                })
            
            # Check error rate
            if self.metrics['success_rate'] < (100 - self.thresholds['error_rate_warning_threshold']):
                alerts.append({
                    'type': 'warning',
                    'metric': 'error_rate',
                    'message': f"Error rate ({100 - self.metrics['success_rate']:.1f}%) exceeds threshold",
                    'value': 100 - self.metrics['success_rate'],
                    'threshold': self.thresholds['error_rate_warning_threshold']
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check alerts: {e}")
            return []
