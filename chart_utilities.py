"""
Chart Utilities
Contains utility methods for chart creation and export functionality.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from .chart_creators import ChartCreators


class ChartUtilities(LoggerMixin):
    """
    Utility class for chart creation and export functionality.
    
    This class contains the chart utility methods that were extracted
    from ChartImplementations to keep files under 250 lines.
    """
    
    def __init__(self):
        """Initialize the chart utilities."""
        super().__init__()
        self.chart_creators = ChartCreators()
        self.log_info("Chart Utilities initialized")
    
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
            return self.chart_creators.create_price_line_chart(data, ticker, price_column, title, theme)
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
            return self.chart_creators.create_volume_chart(data, ticker, title, theme)
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
            return self.chart_creators.create_data_table(data, ticker, max_rows)
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
            return self.chart_creators.create_summary_dashboard(data, ticker, theme)
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
            # Determine filepath
            if filepath is None:
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{ticker}_{chart_type}_{timestamp}.{format}"
                filepath = f"./exports/charts/{filename}"
            
            # Ensure export directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Export based on format and chart type
            if hasattr(chart, 'write_html') and format == 'html':
                chart.write_html(filepath)
            elif hasattr(chart, 'write_image') and format in ['png', 'pdf']:
                chart.write_image(filepath)
            elif hasattr(chart, 'savefig'):
                chart.savefig(filepath, dpi=300, bbox_inches='tight')
            else:
                self.log_error(f"Unsupported export format {format} for chart type")
                return None
            
            self.log_info(f"Exported {chart_type} chart for {ticker} to {filepath}")
            
            # Publish export message if message bus is available
            if message_bus:
                message_bus.publish("chart_exported", {
                    'ticker': ticker,
                    'chart_type': chart_type,
                    'format': format,
                    'filepath': filepath
                })
            
            return filepath
            
        except Exception as e:
            self.log_error(f"Error exporting chart for {ticker}: {e}")
            return None
