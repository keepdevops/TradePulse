"""
Chart Creators
Contains methods for creating various types of charts.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from .dashboard_creator import DashboardCreator


class ChartCreators(LoggerMixin):
    """
    Class for creating various types of charts.
    
    This class contains the chart creation methods that were extracted
    from ChartUtilities to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the chart creators."""
        super().__init__()
        self.dashboard_creator = DashboardCreator()
        self.log_info("Chart Creators initialized")
    
    def create_price_line_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        price_column: str = 'close',
        title: Optional[str] = None,
        theme: str = 'plotly_white'
    ) -> go.Figure:
        """Create a simple line chart for price data."""
        try:
            # Prepare data
            chart_data = data[['date', price_column]].copy()
            chart_data['date'] = pd.to_datetime(chart_data['date'])
            chart_data = chart_data.sort_values('date')
            
            # Create line chart
            fig = px.line(
                chart_data,
                x='date',
                y=price_column,
                title=title or f'{ticker} {price_column.title()} Price',
                template=theme
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=f"Price ($)",
                height=400,
                showlegend=False
            )
            
            # Add hover information
            fig.update_traces(
                hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
            )
            
            self.log_info(f"Created price line chart for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating price line chart for {ticker}: {e}")
            raise
    
    def create_volume_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        title: Optional[str] = None,
        theme: str = 'plotly_white'
    ) -> go.Figure:
        """Create a volume chart."""
        try:
            # Prepare data
            chart_data = data[['date', 'volume', 'close', 'open']].copy()
            chart_data['date'] = pd.to_datetime(chart_data['date'])
            chart_data = chart_data.sort_values('date')
            
            # Color bars based on price movement
            colors = ['#26A69A' if close >= open else '#EF5350' 
                     for close, open in zip(chart_data['close'], chart_data['open'])]
            
            # Create volume chart
            fig = go.Figure()
            
            fig.add_trace(
                go.Bar(
                    x=chart_data['date'],
                    y=chart_data['volume'],
                    marker_color=colors,
                    name='Volume',
                    opacity=0.7
                )
            )
            
            # Update layout
            fig.update_layout(
                title=title or f'{ticker} Trading Volume',
                xaxis_title="Date",
                yaxis_title="Volume",
                template=theme,
                height=400,
                showlegend=False
            )
            
            self.log_info(f"Created volume chart for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating volume chart for {ticker}: {e}")
            raise
    
    def create_data_table(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        max_rows: int = 100
    ) -> go.Figure:
        """Create an interactive data table."""
        try:
            # Prepare data
            table_data = data.copy()
            if 'date' in table_data.columns:
                table_data['date'] = pd.to_datetime(table_data['date']).dt.strftime('%Y-%m-%d')
            
            # Limit rows
            if len(table_data) > max_rows:
                table_data = table_data.tail(max_rows)
                self.log_info(f"Limited table to last {max_rows} rows for {ticker}")
            
            # Create table
            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=list(table_data.columns),
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=12)
                ),
                cells=dict(
                    values=[table_data[col] for col in table_data.columns],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=11)
                )
            )])
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Data Table',
                height=400
            )
            
            self.log_info(f"Created data table for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating data table for {ticker}: {e}")
            raise
    
    def create_summary_dashboard(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        theme: str = 'plotly_white'
    ) -> go.Figure:
        """
        Create a comprehensive dashboard with multiple charts.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            theme: Plotly theme to use
        
        Returns:
            Plotly figure object with subplots
        """
        return self.dashboard_creator.create_summary_dashboard(data, ticker, theme)
