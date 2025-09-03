#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Advanced Charts
Advanced performance chart types for the performance display
"""

import panel as pn
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PerformanceDisplayAdvancedCharts:
    """Advanced performance chart types for performance display"""
    
    @staticmethod
    def create_operations_distribution_chart(performance_metrics) -> pn.pane.Plotly:
        """Create operations distribution chart"""
        try:
            # Get recent operations
            metrics = performance_metrics.get_metrics_summary()
            recent_operations = metrics.get('last_operations', [])
            
            if not recent_operations:
                # Create empty chart
                fig = go.Figure()
                fig.add_annotation(
                    text="No operations data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
            else:
                # Create distribution chart
                df = pd.DataFrame(recent_operations)
                
                # Count operations by type
                operation_counts = df['operation'].value_counts()
                
                fig = go.Figure()
                
                # Add pie chart
                fig.add_trace(go.Pie(
                    labels=operation_counts.index,
                    values=operation_counts.values,
                    hole=0.3,
                    marker_colors=['#ff6b6b', '#4ecdc4', '#feca57', '#48dbfb', '#ff9ff3']
                ))
                
                # Update layout
                fig.update_layout(
                    title='Operations Distribution',
                    template='plotly_dark',
                    height=300
                )
            
            chart = pn.pane.Plotly(fig, sizing_mode='stretch_width')
            return chart
            
        except Exception as e:
            logger.error(f"Failed to create operations distribution chart: {e}")
            return pn.pane.Markdown("Chart Error")
    
    @staticmethod
    def create_error_rate_chart(performance_metrics) -> pn.pane.Plotly:
        """Create error rate chart"""
        try:
            # Get historical data
            history_df = performance_metrics.get_metrics_history(hours=6)
            
            if history_df.empty:
                # Create empty chart
                fig = go.Figure()
                fig.add_annotation(
                    text="No error data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
            else:
                # Calculate error rate
                history_df['error_rate'] = 100 - history_df['success_rate']
                
                # Create error rate chart
                fig = go.Figure()
                
                # Add error rate line
                fig.add_trace(go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['error_rate'],
                    mode='lines+markers',
                    name='Error Rate',
                    line=dict(color='#ff6b6b', width=2),
                    marker=dict(size=6),
                    fill='tonexty'
                ))
                
                # Add threshold line
                fig.add_hline(y=5, line_dash="dash", line_color="orange",
                             annotation_text="Warning Threshold")
                
                # Update layout
                fig.update_layout(
                    title='Error Rate Over Time',
                    xaxis_title='Time',
                    yaxis_title='Error Rate (%)',
                    template='plotly_dark',
                    height=300,
                    yaxis=dict(range=[0, 20])
                )
            
            chart = pn.pane.Plotly(fig, sizing_mode='stretch_width')
            return chart
            
        except Exception as e:
            logger.error(f"Failed to create error rate chart: {e}")
            return pn.pane.Markdown("Chart Error")



