#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Dashboard Creator
Handles creation of system monitoring dashboard
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DashboardCreator:
    """Handles creation of system monitoring dashboard"""
    
    def __init__(self, system_monitor):
        self.system_monitor = system_monitor
    
    def create_dashboard(self) -> pn.Column:
        """Create system monitoring dashboard"""
        try:
            # Get current health status
            health_summary = self.system_monitor.get_system_health()
            current_metrics = health_summary.get('current_metrics', {})
            
            # Create status display
            status_display = self._create_status_display(health_summary, current_metrics)
            
            # Create control buttons
            buttons = self._create_control_buttons()
            
            # Create dashboard layout
            dashboard = pn.Column(
                status_display,
                pn.Spacer(height=20),
                buttons,
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            return pn.Column("Error: Failed to create monitoring dashboard")
    
    def _create_status_display(self, health_summary: Dict[str, Any], current_metrics: Dict[str, Any]) -> pn.Column:
        """Create status display section"""
        try:
            status_display = pn.Column(
                pn.pane.Markdown("# 🖥️ System Monitor Dashboard"),
                pn.pane.Markdown(f"**System Status:** {health_summary.get('system_status', 'Unknown')}"),
                pn.pane.Markdown(f"**CPU Usage:** {current_metrics.get('cpu_usage', 0):.1f}%"),
                pn.pane.Markdown(f"**Memory Usage:** {current_metrics.get('memory_usage', 0):.1f}%"),
                pn.pane.Markdown(f"**Disk Usage:** {current_metrics.get('disk_usage', 0):.1f}%"),
                pn.pane.Markdown(f"**Process Count:** {current_metrics.get('process_count', 0)}"),
                pn.pane.Markdown(f"**Uptime:** {current_metrics.get('uptime', 0):.0f} seconds"),
                sizing_mode='stretch_width',
                background='#2d2d2d',
                margin=(10, 0)
            )
            
            return status_display
            
        except Exception as e:
            logger.error(f"Failed to create status display: {e}")
            return pn.Column("Error: Failed to create status display")
    
    def _create_control_buttons(self) -> pn.Row:
        """Create control buttons section"""
        try:
            # Create control buttons
            start_button = pn.widgets.Button(
                name='🔄 Start Monitoring',
                button_type='success',
                width=150
            )
            
            stop_button = pn.widgets.Button(
                name='🛑 Stop Monitoring',
                button_type='danger',
                width=150
            )
            
            refresh_button = pn.widgets.Button(
                name='📊 Refresh Status',
                button_type='primary',
                width=150
            )
            
            # Setup button callbacks
            start_button.on_click(self.system_monitor._start_monitoring_callback)
            stop_button.on_click(self.system_monitor._stop_monitoring_callback)
            refresh_button.on_click(self.system_monitor._refresh_status_callback)
            
            buttons = pn.Row(
                start_button,
                stop_button,
                refresh_button,
                align='center'
            )
            
            return buttons
            
        except Exception as e:
            logger.error(f"Failed to create control buttons: {e}")
            return pn.Row("Error: Failed to create control buttons")
