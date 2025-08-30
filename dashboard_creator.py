"""
Dashboard Creator
Contains methods for creating comprehensive dashboard charts.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin


class DashboardCreator(LoggerMixin):
    """
    Class for creating comprehensive dashboard charts.
    
    This class contains the dashboard creation method that was extracted
    from ChartCreators to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the dashboard creator."""
        super().__init__()
        self.log_info("Dashboard Creator initialized")
    
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
        try:
            # Create subplots
            fig = make_subplots(
                rows=3, 
                cols=1,
                subplot_titles=(
                    f'{ticker} Price Chart',
                    f'{ticker} Volume',
                    f'{ticker} Price Statistics'
                ),
                vertical_spacing=0.08,
                row_width=[0.5, 0.25, 0.25]
            )
            
            # Prepare data
            chart_data = data.copy()
            if 'date' in chart_data.columns:
                chart_data['date'] = pd.to_datetime(chart_data['date'])
                chart_data = chart_data.sort_values('date')
            
            # Price chart
            fig.add_trace(
                go.Scatter(
                    x=chart_data['date'],
                    y=chart_data['close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='#2196F3', width=2)
                ),
                row=1, col=1
            )
            
            # Volume chart
            colors = ['#26A69A' if close >= open else '#EF5350' 
                     for close, open in zip(chart_data['close'], chart_data['open'])]
            
            fig.add_trace(
                go.Bar(
                    x=chart_data['date'],
                    y=chart_data['volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # Statistics table
            stats_data = [
                ['Metric', 'Value'],
                ['Current Price', f"${chart_data['close'].iloc[-1]:.2f}"],
                ['Price Change', f"${chart_data['close'].iloc[-1] - chart_data['close'].iloc[0]:.2f}"],
                ['Price Change %', f"{((chart_data['close'].iloc[-1] / chart_data['close'].iloc[0]) - 1) * 100:.2f}%"],
                ['High', f"${chart_data['high'].max():.2f}"],
                ['Low', f"${chart_data['low'].min():.2f}"],
                ['Avg Volume', f"{chart_data['volume'].mean():.0f}"]
            ]
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=['Metric', 'Value'],
                        fill_color='paleturquoise',
                        align='left',
                        font=dict(size=12)
                    ),
                    cells=dict(
                        values=[row[0] for row in stats_data[1:]], 
                        values2=[row[1] for row in stats_data[1:]],
                        fill_color='lavender',
                        align='left',
                        font=dict(size=11)
                    )
                ),
                row=3, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Stock Dashboard',
                template=theme,
                height=800,
                showlegend=False
            )
            
            # Update axes
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            
            self.log_info(f"Created summary dashboard for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating summary dashboard for {ticker}: {e}")
            raise
