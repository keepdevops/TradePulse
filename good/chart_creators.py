#!/usr/bin/env python3
"""
TradePulse Modular Panels - Chart Creators
Chart creation utilities for the charts panel
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

class ChartCreators:
    """Chart creation utilities"""
    
    @staticmethod
    def create_candlestick_chart():
        """Create sample candlestick chart"""
        dates = pd.date_range(start='2024-12-01', end='2024-12-31', freq='D')
        
        # Generate sample OHLC data
        base_price = 150
        ohlc_data = []
        
        for date in dates:
            change = np.random.normal(0, 2)
            base_price += change
            open_price = base_price
            high_price = base_price + abs(np.random.normal(0, 1))
            low_price = base_price - abs(np.random.normal(0, 1))
            close_price = base_price + np.random.normal(0, 1)
            
            ohlc_data.append([open_price, high_price, low_price, close_price])
        
        fig = go.Figure(data=[go.Candlestick(
            x=dates,
            open=[d[0] for d in ohlc_data],
            high=[d[1] for d in ohlc_data],
            low=[d[2] for d in ohlc_data],
            close=[d[3] for d in ohlc_data],
            name='AAPL'
        )])
        
        fig.update_layout(
            title='AAPL Candlestick Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_volume_chart():
        """Create volume chart"""
        dates = pd.date_range(start='2024-12-01', end='2024-12-31', freq='D')
        volumes = np.random.randint(1000000, 10000000, len(dates))
        
        fig = go.Figure(data=[go.Bar(
            x=dates,
            y=volumes,
            name='Volume'
        )])
        
        fig.update_layout(
            title='Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_dark',
            height=150
        )
        
        return fig
    
    @staticmethod
    def create_rsi_chart():
        """Create RSI chart"""
        dates = pd.date_range(start='2024-12-01', end='2024-12-31', freq='D')
        rsi_values = np.random.uniform(20, 80, len(dates))
        
        fig = go.Figure(data=[go.Scatter(
            x=dates,
            y=rsi_values,
            name='RSI',
            line=dict(color='orange')
        )])
        
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
        
        fig.update_layout(
            title='RSI Indicator',
            xaxis_title='Date',
            yaxis_title='RSI',
            template='plotly_dark',
            height=150
        )
        
        return fig
