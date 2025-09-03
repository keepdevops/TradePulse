#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Charts
Chart creation implementations for the performance display
"""

import panel as pn
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PerformanceDisplayCharts:
    """Chart creation implementations for performance display"""
    
    def create_response_time_chart(self, performance_metrics) -> pn.pane.Plotly:
        """Create response time chart"""
        try:
            # Get recent history
            history_df = performance_metrics.get_metrics_history(hours=1)
            
            if history_df.empty:
                # Create empty chart
                fig = go.Figure()
                fig.add_annotation(
                    text="No data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
            else:
                # Create response time chart
                fig = go.Figure()
                
                # Add response time line
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['duration'],
                    mode='lines+markers',
                    name='Response Time',
                    line=dict(color='#00ff88', width=2),
                    marker=dict(size=6)
                ))
                
                # Update layout
                fig.update_layout(
                    title='Response Time Over Time',
                    xaxis_title='Time',
                    yaxis_title='Response Time (seconds)',
                    template='plotly_dark',
                    height=300
                )
            
            chart = pn.pane.Plotly(fig, sizing_mode='stretch_width')
            return chart
            
        except Exception as e:
            logger.error(f"Failed to create response time chart: {e}")
            return pn.pane.Markdown("Chart Error")
    
    def create_system_usage_chart(self, performance_metrics) -> pn.pane.Plotly:
        """Create system usage chart"""
        try:
            # Get metrics summary
            metrics = performance_metrics.get_metrics_summary()
            current_metrics = metrics.get('current_metrics', {})
            
            # Create system usage chart
            fig = go.Figure()
            
            # Add memory and CPU bars
            fig.add_trace(go.Bar(
                x=['Memory Usage', 'CPU Usage'],
                y=[current_metrics.get('memory_usage', 0), current_metrics.get('cpu_usage', 0)],
                name='System Usage',
                marker_color=['#ff6b6b', '#4ecdc4']
            ))
            
            # Add threshold lines
            thresholds = performance_metrics.thresholds
            fig.add_hline(y=thresholds.get('memory_warning_threshold', 80), 
                         line_dash="dash", line_color="red",
                         annotation_text="Memory Warning")
            fig.add_hline(y=thresholds.get('cpu_warning_threshold', 70), 
                         line_dash="dash", line_color="orange",
                         annotation_text="CPU Warning")
            
            # Update layout
            fig.update_layout(
                title='System Resource Usage',
                yaxis_title='Usage (%)',
                template='plotly_dark',
                height=300,
                yaxis=dict(range=[0, 100])
            )
            
            chart = pn.pane.Plotly(fig, sizing_mode='stretch_width')
            return chart
            
        except Exception as e:
            logger.error(f"Failed to create system usage chart: {e}")
            return pn.pane.Markdown("Chart Error")
    
    def create_performance_trend_chart(self, performance_metrics) -> pn.pane.Plotly:
        """Create performance trend chart"""
        try:
            # Get historical data
            history_df = performance_metrics.get_metrics_history(hours=24)
            
            if history_df.empty:
                # Create empty chart
                fig = go.Figure()
                fig.add_annotation(
                    text="No historical data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
            else:
                # Create trend chart
                fig = go.Figure()
                
                # Add success rate line
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['success_rate'],
                    mode='lines+markers',
                    name='Success Rate',
                    line=dict(color='#00ff88', width=2),
                    marker=dict(size=4)
                ))
                
                # Add response time line (secondary y-axis)
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['duration'],
                    mode='lines+markers',
                    name='Response Time',
                    line=dict(color='#ff6b6b', width=2),
                    marker=dict(size=4),
                    yaxis='y2'
                ))
                
                # Update layout with dual y-axes
                fig.update_layout(
                    title='Performance Trends',
                    xaxis_title='Time',
                    yaxis=dict(title='Success Rate (%)', side='left'),
                    yaxis2=dict(title='Response Time (s)', side='right', overlaying='y'),
                    template='plotly_dark',
                    height=300
                )
            
            chart = pn.pane.Plotly(fig, sizing_mode='stretch_width')
            return chart
            
        except Exception as e:
            logger.error(f"Failed to create performance trend chart: {e}")
            return pn.pane.Markdown("Chart Error")
    
    def create_operations_distribution_chart(self, performance_metrics) -> pn.pane.Plotly:
        """Create operations distribution chart"""
        from .performance_display_advanced_charts import PerformanceDisplayAdvancedCharts
        return PerformanceDisplayAdvancedCharts.create_operations_distribution_chart(performance_metrics)
    
    def create_error_rate_chart(self, performance_metrics) -> pn.pane.Plotly:
        """Create error rate chart"""
        from .performance_display_advanced_charts import PerformanceDisplayAdvancedCharts
        return PerformanceDisplayAdvancedCharts.create_error_rate_chart(performance_metrics)
