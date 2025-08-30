"""
Chart Manager
Contains methods for managing chart creation and validation.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Any, Optional
from utils.logger import LoggerMixin
from .chart_exporter import ChartExporter
from .simple_chart_creator import SimpleChartCreator


class ChartManager(LoggerMixin):
    """
    Class for managing chart creation and validation.
    
    This class contains the chart management methods that were extracted
    from DataVisualizer to keep files under 250 lines.
    """
    
    def __init__(self, chart_impl, theme: str, interactive_enabled: bool):
        """Initialize the chart manager."""
        super().__init__()
        self.chart_impl = chart_impl
        self.theme = theme
        self.interactive_enabled = interactive_enabled
        self.chart_exporter = ChartExporter()
        self.simple_chart_creator = SimpleChartCreator(chart_impl, theme)
    
    def create_candlestick_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        title: Optional[str] = None,
        interactive: bool = True
    ) -> Optional[Any]:
        """
        Create a candlestick chart for stock data.
        
        Args:
            data: Stock data DataFrame with OHLCV columns
            ticker: Stock ticker symbol
            title: Chart title (optional)
            interactive: Whether to create interactive plotly chart
        
        Returns:
            Chart object (matplotlib figure or plotly figure)
        """
        try:
            if data is None or data.empty:
                self.log_warning(f"No data provided for {ticker} candlestick chart")
                return None
            
            # Ensure required columns exist
            required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                self.log_error(f"Missing required columns for {ticker}: {missing_columns}")
                return None
            
            # Prepare data
            chart_data = data[required_columns].copy()
            chart_data['date'] = pd.to_datetime(chart_data['date'])
            chart_data = chart_data.set_index('date').sort_index()
            
            if interactive and self.interactive_enabled:
                return self.chart_impl.create_interactive_candlestick(chart_data, ticker, title, self.theme)
            else:
                return self.chart_impl.create_static_candlestick(chart_data, ticker, title)
                
        except Exception as e:
            self.log_error(f"Error creating candlestick chart for {ticker}: {e}")
            return None
    
    def create_price_line_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        price_column: str = 'close',
        title: Optional[str] = None
    ) -> go.Figure:
        """Create a simple line chart for price data."""
        return self.simple_chart_creator.create_price_line_chart(data, ticker, price_column, title)
    
    def create_volume_chart(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        title: Optional[str] = None
    ) -> go.Figure:
        """Create a volume chart."""
        return self.simple_chart_creator.create_volume_chart(data, ticker, title)
    
    def create_data_table(
        self, 
        data: pd.DataFrame, 
        ticker: str,
        max_rows: int = 100
    ) -> go.Figure:
        """Create an interactive data table."""
        return self.simple_chart_creator.create_data_table(data, ticker, max_rows)
    
    def create_summary_dashboard(
        self, 
        data: pd.DataFrame, 
        ticker: str
    ) -> go.Figure:
        """Create a comprehensive dashboard with multiple charts."""
        return self.simple_chart_creator.create_summary_dashboard(data, ticker)
    
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
        return self.chart_exporter.export_chart(chart, ticker, chart_type, format, filepath, message_bus)
