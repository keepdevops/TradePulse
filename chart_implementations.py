"""
Chart Implementations
Contains the implementation logic for different chart types.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from .chart_utilities import ChartUtilities
from .candlestick_chart_creator import CandlestickChartCreator


class ChartImplementations(LoggerMixin):
    """
    Implementation class for different chart types.
    
    This class contains all the chart-specific logic that was moved
    from the main DataVisualizer to keep files under 400 lines.
    """
    
    def __init__(self):
        """Initialize the chart implementations."""
        super().__init__()
        self.chart_utils = ChartUtilities()
        self.candlestick_creator = CandlestickChartCreator()
        self.log_info("Chart Implementations initialized")
    
    def create_interactive_candlestick(
        self, 
        data: pd.DataFrame, 
        ticker: str, 
        title: Optional[str] = None,
        theme: str = 'plotly_white'
    ) -> go.Figure:
        """Create interactive candlestick chart using plotly."""
        return self.candlestick_creator.create_interactive_candlestick(data, ticker, title, theme)
    
    def create_static_candlestick(
        self, 
        data: pd.DataFrame, 
        ticker: str, 
        title: Optional[str] = None
    ) -> plt.Figure:
        """Create static candlestick chart using matplotlib."""
        return self.candlestick_creator.create_static_candlestick(data, ticker, title)
    
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
            # Use chart utilities for line chart
            return self.chart_utils.create_price_line_chart(data, ticker, price_column, title, theme)
            
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
            # Use chart utilities for volume chart
            return self.chart_utils.create_volume_chart(data, ticker, title, theme)
            
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
            # Use chart utilities for data table
            return self.chart_utils.create_data_table(data, ticker, max_rows)
            
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
        try:
            # Use chart utilities for dashboard
            return self.chart_utils.create_summary_dashboard(data, ticker, theme)
            
        except Exception as e:
            self.log_error(f"Error creating summary dashboard for {ticker}: {e}")
            raise
    
    def export_chart(
        self, 
        chart: Any, 
        ticker: str, 
        chart_type: str,
        format: str = 'html',
        filepath: Optional[str] = None,
        message_bus: Optional[Any] = None
    ) -> Optional[str]:
        """Export a chart to file."""
        try:
            # Use chart utilities for export
            return self.chart_utils.export_chart(chart, ticker, chart_type, format, filepath, message_bus)
            
        except Exception as e:
            self.log_error(f"Error exporting chart for {ticker}: {e}")
            return None
