#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Integration Dashboard
Handles creation of integration status dashboard
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class IntegrationDashboard:
    """Handles creation of integration status dashboard"""
    
    def __init__(self, integration):
        self.integration = integration
    
    def create_dashboard(self) -> pn.Column:
        """Create integration status dashboard"""
        try:
            # Get integration status
            status = self.integration.get_integration_status()
            
            # Create status display
            status_display = self._create_status_display(status)
            
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
            logger.error(f"Failed to create integration dashboard: {e}")
            return pn.Column("Error: Failed to create integration dashboard")
    
    def _create_status_display(self, status: Dict[str, Any]) -> pn.Column:
        """Create status display section"""
        try:
            status_display = pn.Column(
                pn.pane.Markdown("# 🔗 TradePulse Integration Status"),
                pn.pane.Markdown(f"**Message Bus:** {'✅ Connected' if status.get('message_bus', {}).get('connected') else '❌ Disconnected'}"),
                pn.pane.Markdown(f"**Database:** {'✅ Connected' if status.get('database', {}).get('connected') else '❌ Disconnected'}"),
                pn.pane.Markdown(f"**Models:** {status.get('models', {}).get('count', 0)} available"),
                pn.pane.Markdown(f"**AI Handlers:** {status.get('ai_handlers', {}).get('count', 0)} available"),
                pn.pane.Markdown(f"**Data Components:** {status.get('data_components', {}).get('count', 0)} available"),
                pn.pane.Markdown(f"**Portfolio Strategies:** {status.get('portfolio_strategies', {}).get('count', 0)} available"),
                pn.pane.Markdown(f"**Visualization Components:** {status.get('visualization_components', {}).get('count', 0)} available"),
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
            test_button = pn.widgets.Button(
                name='🧪 Test Integrations',
                button_type='primary',
                width=150
            )
            
            refresh_button = pn.widgets.Button(
                name='🔄 Refresh Status',
                button_type='success',
                width=150
            )
            
            # Setup button callbacks
            test_button.on_click(self.integration._test_integrations_callback)
            refresh_button.on_click(self.integration._refresh_status_callback)
            
            buttons = pn.Row(
                test_button,
                refresh_button,
                align='center'
            )
            
            return buttons
            
        except Exception as e:
            logger.error(f"Failed to create control buttons: {e}")
            return pn.Row("Error: Failed to create control buttons")
