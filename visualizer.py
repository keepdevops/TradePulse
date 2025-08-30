"""
Data Visualizer Component
Renders interactive candlestick charts and data visualizations.
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

# Suppress matplotlib warnings
warnings.filterwarnings('ignore')

from utils.logger import LoggerMixin
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from .chart_implementations import ChartImplementations
from .chart_manager import ChartManager


class DataVisualizer(LoggerMixin):
    """
    Data visualizer for TradePulse.
    
    Handles:
    - Interactive candlestick charts using mplfinance and plotly
    - Data table visualizations
    - Export of charts and visualizations
    """
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """
        Initialize the data visualizer.
        
        Args:
            config: Configuration loader instance
            message_bus: Message Bus client for communication
        """
        super().__init__()
        self.config = config
        self.message_bus = message_bus
        
        # Visualization settings
        self.theme = config.get('visualization.theme', 'plotly_white')
        self.candlestick_enabled = config.get('visualization.candlestick_charts', True)
        self.interactive_enabled = config.get('visualization.interactive', True)
        self.export_formats = config.get('visualization.export_formats', ['png', 'html'])
        
        # Chart cache
        self.chart_cache: Dict[str, Any] = {}
        
        # Chart implementations and manager
        self.chart_impl = ChartImplementations()
        self.chart_manager = ChartManager(self.chart_impl, self.theme, self.interactive_enabled)
        
        self.log_info("Data Visualizer initialized")
    
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
        return self.chart_manager.create_candlestick_chart(data, ticker, title, interactive)
    
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
        return self.chart_manager.create_price_line_chart(data, ticker, price_column, title)
    
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
        return self.chart_manager.create_volume_chart(data, ticker, title)
    
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
        return self.chart_manager.create_data_table(data, ticker, max_rows)
    
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
        return self.chart_manager.create_summary_dashboard(data, ticker)
    
    def export_chart(
        self, 
        chart: Any, 
        ticker: str, 
        chart_type: str,
        format: str = 'html',
        filepath: Optional[str] = None
    ) -> Optional[str]:
        """
        Export a chart to file.
        
        Args:
            chart: Chart object to export
            ticker: Stock ticker symbol
            chart_type: Type of chart (e.g., 'candlestick', 'line')
            format: Export format ('html', 'png', 'pdf')
            filepath: Output file path (optional)
        
        Returns:
            Path to exported file or None if failed
        """
        return self.chart_manager.export_chart(chart, ticker, chart_type, format, filepath, self.message_bus)
    
    def get_cached_chart(self, cache_key: str) -> Optional[Any]:
        """Get a cached chart by key."""
        return self.chart_cache.get(cache_key)
    
    def clear_cache(self) -> None:
        """Clear the chart cache."""
        self.chart_cache.clear()
        self.log_info("Chart cache cleared")
    
    def close(self) -> None:
        """Clean up resources."""
        try:
            self.clear_cache()
            plt.close('all')  # Close all matplotlib figures
            self.log_info("Data Visualizer closed")
        except Exception as e:
            self.log_error(f"Error closing Data Visualizer: {e}")
