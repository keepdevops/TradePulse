#!/usr/bin/env python3
"""
TradePulse Alerts Panel - Management
Panel layout and management for the alerts panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class AlertsManagement:
    """Panel layout and management for alerts panel"""
    
    @staticmethod
    def create_panel_layout(dataset_selector, alert_creator, components):
        """Create the complete panel layout"""
        try:
            # Create main sections
            dataset_section = dataset_selector.get_component()
            
            alert_creation_section = pn.Column(
                pn.pane.Markdown("## 🚨 Create New Alert"),
                alert_creator.get_form_layout()
            )
            
            alerts_management_section = pn.Column(
                pn.pane.Markdown("## 📊 Active Alerts"),
                pn.Row(
                    components.clear_alerts,
                    align='center'
                ),
                components.alerts_table,
                sizing_mode='stretch_width',
                margin=(10, 0)
            )
            
            history_section = pn.Column(
                components.alert_history,
                sizing_mode='stretch_width',
                margin=(10, 0)
            )
            
            # Create complete layout
            layout = pn.Column(
                dataset_section,
                pn.Spacer(height=20),
                alert_creation_section,
                pn.Spacer(height=20),
                alerts_management_section,
                pn.Spacer(height=20),
                history_section,
                sizing_mode='stretch_width'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create panel layout: {e}")
            return pn.Column("Error: Failed to create panel layout")
    
    @staticmethod
    def create_alert_summary_section(alerts_count: int, history_count: int):
        """Create alert summary section"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Alert Summary"),
            pn.pane.Markdown(f"""
            - **Active Alerts**: {alerts_count}
            - **Alert History**: {history_count} entries
            """),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_alert_filters_section():
        """Create alert filters section"""
        return pn.Column(
            pn.pane.Markdown("### 🔍 Alert Filters"),
            pn.Row(
                pn.widgets.Select(
                    name='Filter by Type',
                    options=['All', 'Price Alert', 'Volume Alert', 'Technical Indicator', 'Custom'],
                    value='All',
                    width=150
                ),
                pn.widgets.Select(
                    name='Filter by Status',
                    options=['All', 'Active', 'Inactive', 'Triggered'],
                    value='All',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_alert_actions_section():
        """Create alert actions section"""
        return pn.Column(
            pn.pane.Markdown("### ⚡ Quick Actions"),
            pn.Row(
                pn.widgets.Button(
                    name='🚨 Test All Alerts',
                    button_type='warning',
                    width=150
                ),
                pn.widgets.Button(
                    name='📊 Export Alerts',
                    button_type='light',
                    width=150
                ),
                align='center'
            ),
            sizing_mode='stretch_width'
        )

