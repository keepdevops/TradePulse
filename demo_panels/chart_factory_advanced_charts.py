#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Advanced Charts
Advanced chart types for the chart factory
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class ChartFactoryAdvancedCharts:
    """Advanced chart types for chart factory"""
    
    @staticmethod
    def create_portfolio_performance_chart(data_generator) -> go.Figure:
        """Create portfolio performance chart"""
        try:
            # Generate sample data
            dates = pd.date_range(start='2024-01-01', periods=365, freq='D')
            data = data_generator.generate_portfolio_data(len(dates))
            
            fig = go.Figure()
            
            # Add portfolio value line
            fig.add_trace(go.Scatter(
                x=dates,
                y=data['portfolio_value'],
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#ff6b6b', width=2)
            ))
            
            # Add benchmark line
            fig.add_trace(go.Scatter(
                x=dates,
                y=data['benchmark'],
                mode='lines',
                name='Benchmark',
                line=dict(color='#4ecdc4', width=2, dash='dash')
            ))
            
            # Update layout
            fig.update_layout(
                title='Portfolio Performance',
                xaxis_title='Date',
                yaxis_title='Value ($)',
                template='plotly_dark',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create portfolio performance chart: {e}")
            return ChartFactoryAdvancedCharts._create_error_chart("Portfolio Performance Chart Error")
    
    @staticmethod
    def create_trading_activity_chart(data_generator) -> go.Figure:
        """Create trading activity chart"""
        try:
            # Generate sample data
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            data = data_generator.generate_trading_data(len(dates))
            
            fig = go.Figure()
            
            # Add trading volume bars
            fig.add_trace(go.Bar(
                x=dates,
                y=data['trading_volume'],
                name='Trading Volume',
                marker_color='#feca57'
            ))
            
            # Update layout
            fig.update_layout(
                title='Trading Activity',
                xaxis_title='Date',
                yaxis_title='Volume',
                template='plotly_dark',
                height=300
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create trading activity chart: {e}")
            return ChartFactoryAdvancedCharts._create_error_chart("Trading Activity Chart Error")
    
    @staticmethod
    def _create_error_chart(error_message: str) -> go.Figure:
        """Create error chart when chart creation fails"""
        try:
            fig = go.Figure()
            fig.add_annotation(
                text=error_message,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(
                title='Chart Error',
                template='plotly_dark',
                height=300
            )
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create error chart: {e}")
            # Return minimal figure
            return go.Figure()



