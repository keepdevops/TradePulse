#!/usr/bin/env python3
"""
TradePulse System Monitor - Operations
Monitor-related operations for the system monitor
"""

import pandas as pd
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemMonitorOperations:
    """Monitor-related operations for system monitor"""
    
    def validate_monitoring_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate monitoring configuration"""
        errors = []
        
        # Check required fields
        required_fields = ['interval', 'components']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate interval
        if 'interval' in config:
            interval = config['interval']
            if not isinstance(interval, (int, float)) or interval <= 0:
                errors.append("Interval must be a positive number")
        
        # Validate components
        if 'components' in config:
            components = config['components']
            if not isinstance(components, list) or len(components) == 0:
                errors.append("Components must be a non-empty list")
        
        return len(errors) == 0, errors
    
    def create_monitoring_id(self) -> str:
        """Create unique monitoring session ID"""
        import uuid
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"monitor_{timestamp}_{unique_id}"
    
    def get_monitoring_info(self) -> Dict[str, Any]:
        """Get information about monitoring capabilities"""
        return {
            'supported_components': [
                'Message Bus', 'Database', 'ML Models', 'Data Feed', 'Web Server'
            ],
            'monitoring_types': [
                'Health Check', 'Performance Metrics', 'Resource Usage', 'Error Tracking'
            ],
            'alert_types': [
                'High CPU Usage', 'High Memory Usage', 'Service Down', 'Error Rate'
            ],
            'data_retention': '24 hours'
        }
    
    def get_monitoring_statistics(self, monitoring_data: List[Dict]) -> Dict[str, Any]:
        """Get statistics about monitoring data"""
        if not monitoring_data:
            return {
                'total_checks': 0,
                'successful_checks': 0,
                'failed_checks': 0,
                'alerts_generated': 0,
                'components_monitored': 0
            }
        
        stats = {
            'total_checks': len(monitoring_data),
            'successful_checks': len([d for d in monitoring_data if d.get('status') == 'success']),
            'failed_checks': len([d for d in monitoring_data if d.get('status') == 'failed']),
            'alerts_generated': len([d for d in monitoring_data if d.get('alert')]),
            'components_monitored': len(set(d.get('component', '') for d in monitoring_data))
        }
        
        return stats
    
    def filter_monitoring_data(self, data: List[Dict], component: str = None, 
                             status: str = None, time_range: str = None) -> List[Dict]:
        """Filter monitoring data by various criteria"""
        filtered_data = data
        
        if component:
            filtered_data = [d for d in filtered_data if d.get('component') == component]
        
        if status:
            filtered_data = [d for d in filtered_data if d.get('status') == status]
        
        if time_range:
            # Filter by time range (implement time-based filtering)
            pass
        
        return filtered_data
    
    def sort_monitoring_data(self, data: List[Dict], sort_by: str = 'timestamp', 
                           reverse: bool = True) -> List[Dict]:
        """Sort monitoring data"""
        return sorted(data, key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    def get_monitoring_summary(self, monitoring_data: List[Dict]) -> str:
        """Get summary of monitoring data"""
        if not monitoring_data:
            return "No monitoring data available"
        
        stats = self.get_monitoring_statistics(monitoring_data)
        
        summary_lines = [
            f"**Total Checks**: {stats['total_checks']}",
            f"**Successful**: {stats['successful_checks']}",
            f"**Failed**: {stats['failed_checks']}",
            f"**Alerts**: {stats['alerts_generated']}",
            f"**Components**: {stats['components_monitored']}"
        ]
        
        return "\n".join(summary_lines)



