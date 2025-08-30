"""
Simple Chart Creator
Contains methods for creating simple charts like line, volume, data table, and dashboard.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Optional
from utils.logger import LoggerMixin


class SimpleChartCreator(LoggerMixin):
    """Handles creation of simple charts."""
    
    def __init__(self, chart_impl, theme: str):
        """Initialize the simple chart creator."""
        super().__init__()
        self.chart_impl = chart_impl
        self.theme = theme
    
    def create_price_line_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        price_column: str = 'close',
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Create a simple line chart for price data.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            price_column: Column to use for price (default: 'close')
            title: Chart title (optional)
        
        Returns:
            Plotly figure object
        """
        try:
            if data is None or data.empty:
                self.log_warning(f"No data provided for {ticker} line chart")
                return None
            
            # Use chart implementations for line chart
            return self.chart_impl.create_price_line_chart(data, ticker, price_column, title, self.theme)
            
        except Exception as e:
            self.log_error(f"Error creating price line chart for {ticker}: {e}")
            return None
    
    def create_volume_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Create a volume chart.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            title: Chart title (optional)
        
        Returns:
            Plotly figure object
        """
        try:
            if data is None or data.empty:
                self.log_warning(f"No data provided for {ticker} volume chart")
                return None
            
            # Use chart implementations for volume chart
            return self.chart_impl.create_volume_chart(data, ticker, title, self.theme)
            
        except Exception as e:
            self.log_error(f"Error creating volume chart for {ticker}: {e}")
            return None
    
    def create_data_table(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        max_rows: int = 100
    ) -> go.Figure:
        """
        Create an interactive data table.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            max_rows: Maximum number of rows to display
        
        Returns:
            Plotly figure object
        """
        try:
            if data is None or data.empty:
                self.log_warning(f"No data provided for {ticker} data table")
                return None
            
            # Use chart implementations for data table
            return self.chart_impl.create_data_table(data, ticker, max_rows)
            
        except Exception as e:
            self.log_error(f"Error creating data table for {ticker}: {e}")
            return None
    
    def create_summary_dashboard(
        self, 
        data: pd.DataFrame, 
        ticker: str
    ) -> go.Figure:
        """
        Create a comprehensive dashboard with multiple charts.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
        
        Returns:
            Plotly figure object with subplots
        """
        try:
            if data is None or data.empty:
                self.log_warning(f"No data provided for {ticker} dashboard")
                return None
            
            # Use chart implementations for dashboard
            return self.chart_impl.create_summary_dashboard(data, ticker, self.theme)
            
        except Exception as e:
            self.log_error(f"Error creating summary dashboard for {ticker}: {e}")
            return None
