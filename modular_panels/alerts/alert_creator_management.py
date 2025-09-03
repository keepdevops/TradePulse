#!/usr/bin/env python3
"""
TradePulse Alert Creator - Management
UI management for the alert creator
"""

import panel as pn
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AlertCreatorManagement:
    """UI management for alert creator"""
    
    @staticmethod
    def get_form_layout(components: Dict[str, Any]) -> pn.Column:
        """Get the alert creation form layout"""
        try:
            # Create form sections
            alert_type_section = pn.Column(
                pn.pane.Markdown("### 🚨 Alert Type"),
                components.get('alert_type', pn.pane.Markdown("No component")),
                sizing_mode='stretch_width'
            )
            
            condition_section = pn.Column(
                pn.pane.Markdown("### ⚙️ Alert Conditions"),
                pn.Row(
                    components.get('condition_operator', pn.pane.Markdown("No component")),
                    components.get('threshold_value', pn.pane.Markdown("No component")),
                    components.get('percentage_change', pn.pane.Markdown("No component")),
                    align='center'
                ),
                sizing_mode='stretch_width'
            )
            
            settings_section = pn.Column(
                pn.pane.Markdown("### 🔔 Alert Settings"),
                pn.Row(
                    components.get('alert_enabled', pn.pane.Markdown("No component")),
                    components.get('notification_type', pn.pane.Markdown("No component")),
                    align='center'
                ),
                sizing_mode='stretch_width'
            )
            
            actions_section = pn.Column(
                pn.pane.Markdown("### 🎯 Actions"),
                pn.Row(
                    components.get('create_alert', pn.pane.Markdown("No component")),
                    components.get('test_alert', pn.pane.Markdown("No component")),
                    align='center'
                ),
                sizing_mode='stretch_width'
            )
            
            # Create complete form layout
            form_layout = pn.Column(
                alert_type_section,
                pn.Spacer(height=20),
                condition_section,
                pn.Spacer(height=20),
                settings_section,
                pn.Spacer(height=20),
                actions_section,
                sizing_mode='stretch_width',
                margin=(10, 0)
            )
            
            return form_layout
            
        except Exception as e:
            logger.error(f"Failed to create form layout: {e}")
            return pn.Column("Error: Failed to create form layout")
    
    @staticmethod
    def create_alert_summary_display(config: Dict[str, Any]):
        """Create alert summary display"""
        try:
            summary_lines = [
                "### 📋 Alert Summary",
                f"**Type**: {config.get('alert_type', 'Unknown')}",
                f"**Condition**: {config.get('condition_operator', 'Unknown')} {config.get('threshold_value', 0)}",
                f"**Percentage Change**: {config.get('percentage_change', 0)}%",
                f"**Enabled**: {config.get('alert_enabled', False)}",
                f"**Notifications**: {', '.join(config.get('notification_type', []))}"
            ]
            
            return pn.pane.Markdown("\n".join(summary_lines))
            
        except Exception as e:
            logger.error(f"Failed to create alert summary display: {e}")
            return pn.pane.Markdown("Error: Failed to create alert summary")
    
    @staticmethod
    def create_alert_status_display(status: str, message: str = ""):
        """Create alert status display"""
        try:
            status_text = f"""
            ### 📊 Alert Status
            **Status**: {status}
            {f"**Message**: {message}" if message else ""}
            """
            
            return pn.pane.Markdown(status_text)
            
        except Exception as e:
            logger.error(f"Failed to create alert status display: {e}")
            return pn.pane.Markdown("Error: Failed to create status display")
    
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
        ### ⏳ Processing Alert...
        Please wait while we create your alert.
        """)
    
    @staticmethod
    def create_alert_preview(config: Dict[str, Any]):
        """Create alert preview panel"""
        try:
            preview_lines = [
                "### 👀 Alert Preview",
                f"**Alert Type**: {config.get('alert_type', 'Unknown')}",
                f"**Condition**: {config.get('condition_operator', 'Unknown')} {config.get('threshold_value', 0)}",
                f"**Change Threshold**: {config.get('percentage_change', 0)}%",
                f"**Status**: {'Enabled' if config.get('alert_enabled', False) else 'Disabled'}",
                f"**Notifications**: {', '.join(config.get('notification_type', []))}"
            ]
            
            return pn.pane.Markdown("\n".join(preview_lines))
            
        except Exception as e:
            logger.error(f"Failed to create alert preview: {e}")
            return pn.pane.Markdown("Error: Failed to create alert preview")



