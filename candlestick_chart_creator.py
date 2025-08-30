"""
Candlestick Chart Creator
Contains the implementation logic for candlestick charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional
from utils.logger import LoggerMixin


class CandlestickChartCreator(LoggerMixin):
    """Handles creation of candlestick charts."""
    
    def create_interactive_candlestick(
        self, 
        data: pd.DataFrame, 
        ticker: str, 
        title: Optional[str] = None,
        theme: str = 'plotly_white'
    ) -> go.Figure:
        """
        Create interactive candlestick chart using plotly.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            title: Chart title
            theme: Plotly theme
        
        Returns:
            Plotly figure object
        """
        try:
            # Create subplot with secondary y-axis for volume
            fig = make_subplots(
                rows=2, 
                cols=1, 
                shared_xaxes=True,
                vertical_spacing=0.03,
                subplot_titles=(f'{ticker} Price Chart', 'Volume'),
                row_width=[0.7, 0.3]
            )
            
            # Add candlestick trace
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name=f'{ticker} OHLC',
                    increasing_line_color='#26A69A',
                    decreasing_line_color='#EF5350'
                ),
                row=1, col=1
            )
            
            # Add volume bars
            colors = ['#26A69A' if close >= open else '#EF5350' 
                     for close, open in zip(data['close'], data['open'])]
            
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # Update layout
            chart_title = title or f'{ticker} Stock Price Chart'
            fig.update_layout(
                title=chart_title,
                yaxis_title='Price ($)',
                yaxis2_title='Volume',
                xaxis_rangeslider_visible=False,
                template=theme,
                height=600,
                showlegend=False
            )
            
            # Update axes
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            
            self.log_info(f"Created interactive candlestick chart for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating interactive candlestick chart: {e}")
            raise
    
    def create_static_candlestick(
        self, 
        data: pd.DataFrame, 
        ticker: str, 
        title: Optional[str] = None
    ) -> plt.Figure:
        """
        Create static candlestick chart using matplotlib.
        
        Args:
            data: Stock data DataFrame
            ticker: Stock ticker symbol
            title: Chart title
        
        Returns:
            Matplotlib figure object
        """
        try:
            import mplfinance as mpf
            
            # Prepare data for mplfinance
            ohlc_data = data[['open', 'high', 'low', 'close', 'volume']].copy()
            
            # Create the chart
            fig, axes = mpf.plot(
                ohlc_data,
                type='candle',
                volume=True,
                title=title or f'{ticker} Stock Price Chart',
                style='charles',
                figsize=(12, 8),
                returnfig=True
            )
            
            # Customize the chart
            axes[0].set_ylabel('Price ($)')
            axes[2].set_ylabel('Volume')
            axes[2].set_xlabel('Date')
            
            self.log_info(f"Created static candlestick chart for {ticker}")
            return fig
            
        except Exception as e:
            self.log_error(f"Error creating static candlestick chart: {e}")
            raise
