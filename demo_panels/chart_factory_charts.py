#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Charts
Chart creation implementations for the chart factory
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class ChartFactoryCharts:
    """Chart creation implementations for chart factory"""
    
    def create_candlestick_chart(self, data_generator, chart_configs: Dict) -> go.Figure:
        """Create candlestick chart"""
        try:
            # Generate sample data
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            data = data_generator.generate_candlestick_data(len(dates))
            
            fig = go.Figure()
            
            # Add candlestick trace
            fig.add_trace(go.Candlestick(
                x=dates,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='OHLC'
            ))
            
            # Update layout
            fig.update_layout(
                title='Candlestick Chart',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template=chart_configs['candlestick']['template'],
                height=chart_configs['candlestick']['height']
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create candlestick chart: {e}")
            return self._create_error_chart("Candlestick Chart Error")
    
    def create_volume_chart(self, data_generator, chart_configs: Dict) -> go.Figure:
        """Create volume chart"""
        try:
            # Generate sample data
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            data = data_generator.generate_volume_data(len(dates))
            
            fig = go.Figure()
            
            # Add volume bars
            colors = ['green' if close > open else 'red' 
                     for close, open in zip(data['close'], data['open'])]
            
            fig.add_trace(go.Bar(
                x=dates,
                y=data['volume'],
                name='Volume',
                marker_color=colors
            ))
            
            # Update layout
            fig.update_layout(
                title='Volume Chart',
                xaxis_title='Date',
                yaxis_title='Volume',
                template=chart_configs['volume']['template'],
                height=chart_configs['volume']['height']
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create volume chart: {e}")
            return self._create_error_chart("Volume Chart Error")
    
    def create_line_chart(self, data_generator, chart_configs: Dict) -> go.Figure:
        """Create line chart"""
        try:
            # Generate sample data
            dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
            data = data_generator.generate_line_data(len(dates))
            
            fig = go.Figure()
            
            # Add price line
            fig.add_trace(go.Scatter(
                x=dates,
                y=data['price'],
                mode='lines',
                name='Price',
                line=dict(color='#00ff88', width=2)
            ))
            
            # Add moving averages if configured
            if chart_configs['line']['show_ma']:
                for period in chart_configs['line']['ma_periods']:
                    ma_data = data['price'].rolling(window=period).mean()
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=ma_data,
                        mode='lines',
                        name=f'MA {period}',
                        line=dict(dash='dash', width=1)
                    ))
            
            # Update layout
            fig.update_layout(
                title='Line Chart',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template=chart_configs['line']['template'],
                height=chart_configs['line']['height']
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create line chart: {e}")
            return self._create_error_chart("Line Chart Error")
    
    def create_bar_chart(self, data_generator, chart_configs: Dict) -> go.Figure:
        """Create bar chart"""
        try:
            # Generate sample data
            categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
            data = data_generator.generate_bar_data(len(categories))
            
            fig = go.Figure()
            
            # Add bar trace
            fig.add_trace(go.Bar(
                x=categories,
                y=data['values'],
                name='Values',
                marker_color='#4ecdc4'
            ))
            
            # Update layout
            fig.update_layout(
                title='Bar Chart',
                xaxis_title='Categories',
                yaxis_title='Values',
                template=chart_configs['bar']['template'],
                height=chart_configs['bar']['height']
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create bar chart: {e}")
            return self._create_error_chart("Bar Chart Error")
    
    def create_portfolio_performance_chart(self, data_generator) -> go.Figure:
        """Create portfolio performance chart"""
        from .chart_factory_advanced_charts import ChartFactoryAdvancedCharts
        return ChartFactoryAdvancedCharts.create_portfolio_performance_chart(data_generator)
    
    def create_trading_activity_chart(self, data_generator) -> go.Figure:
        """Create trading activity chart"""
        from .chart_factory_advanced_charts import ChartFactoryAdvancedCharts
        return ChartFactoryAdvancedCharts.create_trading_activity_chart(data_generator)
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """Create error chart when chart creation fails"""
        from .chart_factory_advanced_charts import ChartFactoryAdvancedCharts
        return ChartFactoryAdvancedCharts._create_error_chart(error_message)
