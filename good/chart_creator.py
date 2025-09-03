#!/usr/bin/env python3
"""
TradePulse UI Panels - Chart Creator
Handles chart creation functionality
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChartCreator:
    """Handles chart creation functionality"""
    
    def __init__(self):
        pass
    
    def create_empty_chart(self):
        """Create an empty placeholder chart"""
        try:
            fig = go.Figure()
            fig.add_annotation(
                text="Select data to display chart",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            fig.update_layout(
                title="TradePulse Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create empty chart: {e}")
            return go.Figure()
    
    def create_candlestick_chart(self, data: pd.DataFrame, symbol: str = "Unknown") -> go.Figure:
        """Create a candlestick chart from OHLC data"""
        try:
            if data.empty:
                logger.warning("⚠️ No data provided for candlestick chart")
                return self.create_empty_chart()
            
            # Ensure required columns exist
            required_columns = ['open', 'high', 'low', 'close']
            if not all(col in data.columns for col in required_columns):
                logger.error(f"❌ Missing required columns for candlestick chart: {required_columns}")
                return self.create_empty_chart()
            
            fig = go.Figure(data=go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=symbol
            ))
            
            fig.update_layout(
                title=f"{symbol} - Candlestick Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                height=400,
                template="plotly_dark"
            )
            
            logger.info(f"✅ Candlestick chart created for {symbol}")
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create candlestick chart: {e}")
            return self.create_empty_chart()
    
    def create_line_chart(self, data: pd.DataFrame, symbol: str = "Unknown", column: str = "close") -> go.Figure:
        """Create a line chart from data"""
        try:
            if data.empty:
                logger.warning("⚠️ No data provided for line chart")
                return self.create_empty_chart()
            
            if column not in data.columns:
                logger.error(f"❌ Column {column} not found in data")
                return self.create_empty_chart()
            
            fig = go.Figure(data=go.Scatter(
                x=data.index,
                y=data[column],
                mode='lines',
                name=f"{symbol} - {column.title()}"
            ))
            
            fig.update_layout(
                title=f"{symbol} - {column.title()} Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                height=400,
                template="plotly_dark"
            )
            
            logger.info(f"✅ Line chart created for {symbol} - {column}")
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create line chart: {e}")
            return self.create_empty_chart()
    
    def create_bar_chart(self, data: pd.DataFrame, symbol: str = "Unknown", column: str = "volume") -> go.Figure:
        """Create a bar chart from data"""
        try:
            if data.empty:
                logger.warning("⚠️ No data provided for bar chart")
                return self.create_empty_chart()
            
            if column not in data.columns:
                logger.error(f"❌ Column {column} not found in data")
                return self.create_empty_chart()
            
            fig = go.Figure(data=go.Bar(
                x=data.index,
                y=data[column],
                name=f"{symbol} - {column.title()}"
            ))
            
            fig.update_layout(
                title=f"{symbol} - {column.title()} Chart",
                xaxis_title="Time",
                yaxis_title=column.title(),
                height=400,
                template="plotly_dark"
            )
            
            logger.info(f"✅ Bar chart created for {symbol} - {column}")
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create bar chart: {e}")
            return self.create_empty_chart()
