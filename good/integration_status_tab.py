#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Integration Status Tab
Handles creation of integration status tab
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class IntegrationStatusTab:
    """Handles creation of integration status tab"""
    
    def __init__(self, integrated_ui):
        self.integrated_ui = integrated_ui
    
    def create_status_tab(self) -> pn.Column:
        """Create the integration status tab"""
        try:
            # Get integration status
            integration_status = self.integrated_ui.tradepulse_integration.get_component_status()
            integration_summary = self.integrated_ui.tradepulse_integration.get_integration_summary()
            
            # Get system health
            system_health = self.integrated_ui.system_monitor.get_system_health()
            
            # Get performance summary
            performance_summary = self.integrated_ui.performance_tracker.get_performance_summary()
            
            # Create status displays
            integration_display = pn.pane.Markdown(
                f"## TradePulse Integration Status\n{integration_summary}",
                style={'color': 'white'}
            )
            
            system_display = pn.pane.Markdown(
                f"## System Health\n"
                f"**Status:** {system_health.get('status', 'Unknown')}\n"
                f"**Alerts:** {system_health.get('alerts_count', 0)}\n"
                f"**Monitoring:** {'Active' if system_health.get('monitoring_active') else 'Inactive'}",
                style={'color': 'white'}
            )
            
            performance_display = pn.pane.Markdown(
                f"## Performance Status\n"
                f"**Tracking:** {'Active' if performance_summary.get('tracking_active') else 'Inactive'}\n"
                f"**Operations:** {performance_summary.get('operation_count', 0)}\n"
                f"**Success Rate:** {performance_summary.get('performance_metrics', {}).get('success_rate', 0):.1f}%",
                style={'color': 'white'}
            )
            
            # Control buttons
            refresh_button = pn.widgets.Button(
                name='Refresh Status',
                button_type='primary',
                width=150
            )
            
            export_button = pn.widgets.Button(
                name='Export Status',
                button_type='light',
                width=150
            )
            
            # Setup button callbacks
            refresh_button.on_click(lambda event: self._refresh_integration_status())
            export_button.on_click(lambda event: self._export_integration_status())
            
            # Create status layout
            status_layout = pn.Column(
                pn.Row(integration_display, system_display, sizing_mode='stretch_width'),
                pn.Spacer(height=20),
                performance_display,
                pn.Spacer(height=20),
                pn.Row(refresh_button, export_button, sizing_mode='stretch_width'),
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return status_layout
            
        except Exception as e:
            logger.error(f"Failed to create integration status tab: {e}")
            return pn.Column("Error: Failed to create integration status tab")
    
    def _refresh_integration_status(self):
        """Refresh the integration status display"""
        try:
            logger.info("🔄 Refreshing integration status")
            
            # Force refresh of status displays
            self.create_status_tab()
            
            logger.info("✅ Integration status refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh integration status: {e}")
    
    def _export_integration_status(self):
        """Export the current integration status"""
        try:
            logger.info("📤 Exporting integration status")
            
            # Export status data
            status_data = self._export_all_component_data()
            
            # Create status summary
            status_summary = {
                'integration_status': self.integrated_ui.tradepulse_integration.get_component_status(),
                'system_health': self.integrated_ui.system_monitor.get_system_health(),
                'performance_summary': self.integrated_ui.performance_tracker.get_performance_summary(),
                'export_timestamp': self._get_current_timestamp()
            }
            
            logger.info(f"📊 Integration status exported: {len(status_summary)} sections")
            
        except Exception as e:
            logger.error(f"Failed to export integration status: {e}")
    
    def _export_all_component_data(self) -> Dict[str, Any]:
        """Export data from all components"""
        try:
            export_data = {}
            
            # Export TradePulse integration data
            if hasattr(self.integrated_ui.tradepulse_integration, 'export_integration_state'):
                export_data['tradepulse_integration'] = self.integrated_ui.tradepulse_integration.export_integration_state()
            
            # Export UI orchestrator data
            if hasattr(self.integrated_ui.ui_orchestrator, 'export_component_data'):
                export_data['ui_orchestrator'] = self.integrated_ui.ui_orchestrator.export_component_data()
            
            # Export system monitor data
            if hasattr(self.integrated_ui.system_monitor, 'export_monitoring_data'):
                export_data['system_monitor'] = self.integrated_ui.system_monitor.export_monitoring_data()
            
            # Export performance tracker data
            if hasattr(self.integrated_ui.performance_tracker, 'export_performance_data'):
                export_data['performance_tracker'] = self.integrated_ui.performance_tracker.export_performance_data()
            
            # Add export metadata
            export_data['export_metadata'] = {
                'export_timestamp': self._get_current_timestamp(),
                'component_count': len(export_data),
                'export_version': '1.0'
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export all component data: {e}")
            return {}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
