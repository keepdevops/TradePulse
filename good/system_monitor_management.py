#!/usr/bin/env python3
"""
TradePulse System Monitor - Management
Dashboard creation and management for the system monitor
"""

import panel as pn
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemMonitorManagement:
    """Dashboard creation and management for system monitor"""
    
    @staticmethod
    def create_monitoring_dashboard(monitor):
        """Create system monitoring dashboard"""
        try:
            # Create main sections
            controls_section = SystemMonitorManagement.create_controls_section(monitor)
            status_section = SystemMonitorManagement.create_status_section(monitor)
            health_section = SystemMonitorManagement.create_health_section(monitor)
            alerts_section = SystemMonitorManagement.create_alerts_section(monitor)
            
            # Main layout
            dashboard = pn.Column(
                pn.pane.Markdown("### 📊 System Monitoring Dashboard"),
                controls_section,
                pn.Spacer(height=20),
                status_section,
                pn.Spacer(height=20),
                health_section,
                pn.Spacer(height=20),
                alerts_section,
                sizing_mode='stretch_width'
            )
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to create monitoring dashboard: {e}")
            return pn.Column("Error: Failed to create monitoring dashboard")
    
    @staticmethod
    def create_controls_section(monitor):
        """Create monitoring controls section"""
        return pn.Column(
            pn.pane.Markdown("### ⚡ Monitoring Controls"),
            pn.Row(
                monitor.components.start_monitoring_button,
                monitor.components.stop_monitoring_button,
                monitor.components.refresh_status_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_status_section(monitor):
        """Create monitoring status section"""
        return pn.Column(
            monitor.components.monitoring_status,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_health_section(monitor):
        """Create system health section"""
        return pn.Column(
            monitor.components.health_display,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_alerts_section(monitor):
        """Create system alerts section"""
        return pn.Column(
            monitor.components.alerts_display,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_monitoring_summary_section(monitoring_active: bool, alerts_count: int):
        """Create monitoring summary section"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Monitoring Summary"),
            pn.pane.Markdown(f"""
            - **Status**: {'Active' if monitoring_active else 'Inactive'}
            - **Active Alerts**: {alerts_count}
            - **Last Update**: {datetime.now().strftime('%H:%M:%S')}
            """),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_monitoring_filters_section():
        """Create monitoring filters section"""
        return pn.Column(
            pn.pane.Markdown("### 🔍 Monitoring Filters"),
            pn.Row(
                pn.widgets.Select(
                    name='Filter by Component',
                    options=['All', 'Message Bus', 'Database', 'ML Models', 'Data Feed', 'Web Server'],
                    value='All',
                    width=150
                ),
                pn.widgets.Select(
                    name='Filter by Status',
                    options=['All', 'Success', 'Failed', 'Warning'],
                    value='All',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_monitoring_actions_section():
        """Create monitoring actions section"""
        return pn.Column(
            pn.pane.Markdown("### ⚡ Quick Actions"),
            pn.Row(
                pn.widgets.Button(
                    name='📊 Export Data',
                    button_type='light',
                    width=150
                ),
                pn.widgets.Button(
                    name='🔄 Reset Metrics',
                    button_type='warning',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )

