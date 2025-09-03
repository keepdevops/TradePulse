#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Components
UI components for the performance display
"""

import panel as pn
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PerformanceDisplayComponents:
    """UI components for performance display"""
    
    def create_metrics_summary(self, performance_metrics) -> pn.Column:
        """Create metrics summary display"""
        try:
            metrics = performance_metrics.get_metrics_summary()
            current_metrics = metrics.get('current_metrics', {})
            
            summary = pn.Column(
                pn.pane.Markdown("### 📊 Performance Metrics Summary"),
                pn.pane.Markdown(f"**Total Operations:** {current_metrics.get('total_operations', 0)}"),
                pn.pane.Markdown(f"**Average Response Time:** {current_metrics.get('average_response_time', 0):.3f}s"),
                pn.pane.Markdown(f"**Success Rate:** {current_metrics.get('success_rate', 100):.1f}%"),
                pn.pane.Markdown(f"**Memory Usage:** {current_metrics.get('memory_usage', 0):.1f}%"),
                pn.pane.Markdown(f"**CPU Usage:** {current_metrics.get('cpu_usage', 0):.1f}%"),
                pn.pane.Markdown(f"**Active Connections:** {current_metrics.get('active_connections', 0)}"),
                pn.pane.Markdown(f"**Queue Size:** {current_metrics.get('queue_size', 0)}"),
                sizing_mode='stretch_width',
                background='#2d2d2d',
                margin=(10, 0)
            )
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to create metrics summary: {e}")
            return pn.Column("Metrics Summary Error")
    
    def create_alerts_display(self, performance_metrics) -> pn.Column:
        """Create performance alerts display"""
        try:
            alerts = performance_metrics.get_performance_alerts()
            
            if not alerts:
                alerts_content = pn.pane.Markdown("✅ No performance alerts")
            else:
                alerts_content = pn.Column()
                for alert in alerts:
                    alert_color = 'orange' if alert['type'] == 'warning' else 'red'
                    alert_text = f"⚠️ **{alert['metric'].title()}:** {alert['message']}"
                    alerts_content.append(pn.pane.Markdown(alert_text, style={'color': alert_color}))
            
            alerts_display = pn.Column(
                pn.pane.Markdown("### 🚨 Performance Alerts"),
                alerts_content,
                sizing_mode='stretch_width',
                background='#3d3d3d',
                margin=(10, 0)
            )
            
            return alerts_display
            
        except Exception as e:
            logger.error(f"Failed to create alerts display: {e}")
            return pn.Column("Alerts Error")
    
    def create_operations_table(self, performance_metrics) -> pn.widgets.Tabulator:
        """Create operations history table"""
        try:
            # Get recent operations
            metrics = performance_metrics.get_metrics_summary()
            recent_operations = metrics.get('last_operations', [])
            
            if not recent_operations:
                # Create empty DataFrame
                df = pd.DataFrame(columns=['Operation', 'Duration', 'Success', 'Timestamp'])
            else:
                # Convert to DataFrame
                df = pd.DataFrame(recent_operations)
                df['Timestamp'] = df['timestamp'].dt.strftime('%H:%M:%S')
                df = df[['operation', 'duration', 'success', 'Timestamp']]
                df.columns = ['Operation', 'Duration (s)', 'Success', 'Timestamp']
            
            table = pn.widgets.Tabulator(
                df,
                height=200,
                name='Recent Operations',
                sizing_mode='stretch_width'
            )
            
            return table
            
        except Exception as e:
            logger.error(f"Failed to create operations table: {e}")
            return pn.pane.Markdown("Table Error")
    
    def create_control_buttons(self, display_core) -> pn.Row:
        """Create control buttons"""
        try:
            refresh_button = pn.widgets.Button(
                name='🔄 Refresh',
                button_type='primary',
                width=120
            )
            
            export_button = pn.widgets.Button(
                name='📤 Export',
                button_type='success',
                width=120
            )
            
            reset_button = pn.widgets.Button(
                name='🔄 Reset',
                button_type='warning',
                width=120
            )
            
            # Setup callbacks
            refresh_button.on_click(display_core.refresh_display)
            export_button.on_click(display_core.export_data)
            reset_button.on_click(display_core.reset_metrics)
            
            buttons = pn.Row(
                refresh_button,
                export_button,
                reset_button,
                align='center'
            )
            
            return buttons
            
        except Exception as e:
            logger.error(f"Failed to create control buttons: {e}")
            return pn.pane.Markdown("Buttons Error")
    
    def create_performance_panel(self, display_core):
        """Create complete performance panel"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Performance Display"),
            display_core.get_display_layout(),
            sizing_mode='stretch_width'
        )
    
    def update_metrics_display(self, metrics_summary, current_metrics: dict):
        """Update metrics display"""
        try:
            if metrics_summary:
                # Update the metrics summary content
                summary_content = f"""
                ### 📊 Performance Metrics Summary
                
                **Total Operations:** {current_metrics.get('total_operations', 0)}  
                **Average Response Time:** {current_metrics.get('average_response_time', 0):.3f}s  
                **Success Rate:** {current_metrics.get('success_rate', 100):.1f}%  
                **Memory Usage:** {current_metrics.get('memory_usage', 0):.1f}%  
                **CPU Usage:** {current_metrics.get('cpu_usage', 0):.1f}%  
                **Active Connections:** {current_metrics.get('active_connections', 0)}  
                **Queue Size:** {current_metrics.get('queue_size', 0)}
                """
                metrics_summary.object = summary_content
                
        except Exception as e:
            logger.error(f"Failed to update metrics display: {e}")
    
    def update_alerts_display(self, alerts_display, alerts: list):
        """Update alerts display"""
        try:
            if alerts_display:
                if not alerts:
                    alerts_display.object = "✅ No performance alerts"
                else:
                    alerts_text = "### 🚨 Performance Alerts\n\n"
                    for alert in alerts:
                        alert_color = 'orange' if alert['type'] == 'warning' else 'red'
                        alerts_text += f"⚠️ **{alert['metric'].title()}:** {alert['message']}\n"
                    alerts_display.object = alerts_text
                    
        except Exception as e:
            logger.error(f"Failed to update alerts display: {e}")
    
    def update_operations_table(self, operations_table, recent_operations: list):
        """Update operations table"""
        try:
            if operations_table:
                if not recent_operations:
                    df = pd.DataFrame(columns=['Operation', 'Duration', 'Success', 'Timestamp'])
                else:
                    df = pd.DataFrame(recent_operations)
                    df['Timestamp'] = df['timestamp'].dt.strftime('%H:%M:%S')
                    df = df[['operation', 'duration', 'success', 'Timestamp']]
                    df.columns = ['Operation', 'Duration (s)', 'Success', 'Timestamp']
                
                operations_table.value = df
                
        except Exception as e:
            logger.error(f"Failed to update operations table: {e}")



