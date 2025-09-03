#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Operations
Performance-related operations for the performance display
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class PerformanceDisplayOperations:
    """Performance-related operations for performance display"""
    
    def refresh_display(self, display_core):
        """Refresh all display components"""
        try:
            logger.info("🔄 Refreshing performance display")
            
            # Update all components
            display_core.display_components['metrics_summary'] = display_core.create_metrics_summary()
            display_core.display_components['response_time_chart'] = display_core.create_response_time_chart()
            display_core.display_components['system_usage_chart'] = display_core.create_system_usage_chart()
            display_core.display_components['alerts_display'] = display_core.create_alerts_display()
            display_core.display_components['operations_table'] = display_core.create_operations_table()
            
            logger.info("✅ Performance display refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh display: {e}")
    
    def export_data(self, performance_metrics):
        """Export performance data"""
        try:
            logger.info("📤 Exporting performance data")
            
            filename = performance_metrics.export_metrics()
            if filename:
                logger.info(f"✅ Data exported to {filename}")
                return filename
            else:
                logger.error("❌ Failed to export data")
                return None
                
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            return None
    
    def reset_metrics(self, display_core):
        """Reset performance metrics"""
        try:
            logger.info("🔄 Resetting performance metrics")
            
            display_core.performance_metrics.reset_metrics()
            display_core.refresh_display()
            
            logger.info("✅ Performance metrics reset")
            
        except Exception as e:
            logger.error(f"Failed to reset metrics: {e}")
    
    def validate_performance_data(self, performance_metrics) -> bool:
        """Validate performance data"""
        try:
            metrics = performance_metrics.get_metrics_summary()
            current_metrics = metrics.get('current_metrics', {})
            
            # Check required fields
            required_fields = ['total_operations', 'average_response_time', 'success_rate']
            for field in required_fields:
                if field not in current_metrics:
                    return False
            
            # Validate ranges
            if current_metrics.get('success_rate', 0) < 0 or current_metrics.get('success_rate', 0) > 100:
                return False
            
            if current_metrics.get('average_response_time', 0) < 0:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate performance data: {e}")
            return False
    
    def get_performance_summary(self, performance_metrics) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            metrics = performance_metrics.get_metrics_summary()
            current_metrics = metrics.get('current_metrics', {})
            
            summary = {
                'total_operations': current_metrics.get('total_operations', 0),
                'average_response_time': current_metrics.get('average_response_time', 0),
                'success_rate': current_metrics.get('success_rate', 100),
                'memory_usage': current_metrics.get('memory_usage', 0),
                'cpu_usage': current_metrics.get('cpu_usage', 0),
                'active_connections': current_metrics.get('active_connections', 0),
                'queue_size': current_metrics.get('queue_size', 0)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {}
    
    def format_performance_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format performance metrics for display"""
        try:
            formatted_text = f"""
            ### 📊 Performance Metrics Summary
            
            **Total Operations:** {metrics.get('total_operations', 0)}  
            **Average Response Time:** {metrics.get('average_response_time', 0):.3f}s  
            **Success Rate:** {metrics.get('success_rate', 100):.1f}%  
            **Memory Usage:** {metrics.get('memory_usage', 0):.1f}%  
            **CPU Usage:** {metrics.get('cpu_usage', 0):.1f}%  
            **Active Connections:** {metrics.get('active_connections', 0)}  
            **Queue Size:** {metrics.get('queue_size', 0)}
            """
            
            return formatted_text
            
        except Exception as e:
            logger.error(f"Failed to format performance metrics: {e}")
            return "Error formatting metrics"
    
    def check_performance_alerts(self, performance_metrics) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        try:
            alerts = performance_metrics.get_performance_alerts()
            
            # Filter and format alerts
            formatted_alerts = []
            for alert in alerts:
                formatted_alert = {
                    'type': alert.get('type', 'warning'),
                    'metric': alert.get('metric', 'Unknown'),
                    'message': alert.get('message', 'No message'),
                    'timestamp': alert.get('timestamp', 'Unknown')
                }
                formatted_alerts.append(formatted_alert)
            
            return formatted_alerts
            
        except Exception as e:
            logger.error(f"Failed to check performance alerts: {e}")
            return []
    
    def export_performance_report(self, performance_metrics, filename: str = None) -> str:
        """Export comprehensive performance report"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"performance_report_{timestamp}.json"
            
            # Gather all performance data
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'metrics_summary': performance_metrics.get_metrics_summary(),
                'performance_alerts': performance_metrics.get_performance_alerts(),
                'metrics_history': performance_metrics.get_metrics_history(hours=24).to_dict('records')
            }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"📤 Performance report exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export performance report: {e}")
            return None



