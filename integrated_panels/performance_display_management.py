#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Management
UI management for the performance display
"""

import panel as pn
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class PerformanceDisplayManagement:
    """UI management for performance display"""
    
    @staticmethod
    def get_display_layout(display_components: Dict) -> pn.Column:
        """Get the complete display layout"""
        try:
            layout = pn.Column(
                display_components['metrics_summary'],
                pn.Spacer(height=20),
                display_components['response_time_chart'],
                pn.Spacer(height=20),
                display_components['system_usage_chart'],
                pn.Spacer(height=20),
                display_components['alerts_display'],
                pn.Spacer(height=20),
                display_components['operations_table'],
                pn.Spacer(height=20),
                display_components['control_buttons'],
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to get display layout: {e}")
            return pn.Column("Error: Failed to create display layout")
    
    @staticmethod
    def create_metrics_display(metrics: Dict[str, Any]):
        """Create metrics display"""
        try:
            if not metrics:
                return pn.pane.Markdown("""
                ### 📊 Performance Metrics Summary
                No metrics available
                """)
            
            metrics_text = f"""
            ### 📊 Performance Metrics Summary
            
            **Total Operations:** {metrics.get('total_operations', 0)}  
            **Average Response Time:** {metrics.get('average_response_time', 0):.3f}s  
            **Success Rate:** {metrics.get('success_rate', 100):.1f}%  
            **Memory Usage:** {metrics.get('memory_usage', 0):.1f}%  
            **CPU Usage:** {metrics.get('cpu_usage', 0):.1f}%  
            **Active Connections:** {metrics.get('active_connections', 0)}  
            **Queue Size:** {metrics.get('queue_size', 0)}
            """
            
            return pn.pane.Markdown(metrics_text)
            
        except Exception as e:
            logger.error(f"Failed to create metrics display: {e}")
            return pn.pane.Markdown("Error: Failed to create metrics display")
    
    @staticmethod
    def create_alerts_display(alerts: List[Dict[str, Any]]):
        """Create alerts display"""
        try:
            if not alerts:
                return pn.pane.Markdown("""
                ### 🚨 Performance Alerts
                ✅ No performance alerts
                """)
            
            alerts_text = "### 🚨 Performance Alerts\n\n"
            for alert in alerts:
                alert_color = 'orange' if alert.get('type') == 'warning' else 'red'
                alerts_text += f"⚠️ **{alert.get('metric', 'Unknown').title()}:** {alert.get('message', 'No message')}\n"
            
            return pn.pane.Markdown(alerts_text)
            
        except Exception as e:
            logger.error(f"Failed to create alerts display: {e}")
            return pn.pane.Markdown("Error: Failed to create alerts display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Loading Performance Data...
        Please wait while we gather the latest performance metrics.
        """)
    
    @staticmethod
    def create_performance_summary_display(summary: Dict[str, Any]):
        """Create performance summary display"""
        try:
            if not summary:
                return pn.pane.Markdown("""
                ### 📊 Performance Summary
                No summary data available
                """)
            
            summary_text = f"""
            ### 📊 Performance Summary
            
            **Status**: {'🟢 Healthy' if summary.get('success_rate', 100) > 95 else '🟡 Warning' if summary.get('success_rate', 100) > 80 else '🔴 Critical'}  
            **Total Operations**: {summary.get('total_operations', 0)}  
            **Average Response Time**: {summary.get('average_response_time', 0):.3f}s  
            **Success Rate**: {summary.get('success_rate', 100):.1f}%  
            **System Load**: {summary.get('cpu_usage', 0):.1f}% CPU, {summary.get('memory_usage', 0):.1f}% Memory
            """
            
            return pn.pane.Markdown(summary_text)
            
        except Exception as e:
            logger.error(f"Failed to create performance summary display: {e}")
            return pn.pane.Markdown("Error: Failed to create performance summary display")
    
    @staticmethod
    def create_performance_status_display(status: str, details: Dict[str, Any]):
        """Create performance status display"""
        try:
            status_emoji = {
                'healthy': '🟢',
                'warning': '🟡', 
                'critical': '🔴',
                'unknown': '⚪'
            }.get(status.lower(), '⚪')
            
            status_text = f"""
            ### {status_emoji} Performance Status: {status.title()}
            
            **Last Updated**: {details.get('last_updated', 'Unknown')}  
            **Monitoring Active**: {'✅ Yes' if details.get('monitoring_active', False) else '❌ No'}  
            **Alerts Count**: {details.get('alerts_count', 0)}  
            **Uptime**: {details.get('uptime', 'Unknown')}
            """
            
            return pn.pane.Markdown(status_text)
            
        except Exception as e:
            logger.error(f"Failed to create performance status display: {e}")
            return pn.pane.Markdown("Error: Failed to create performance status display")



