#!/usr/bin/env python3
"""
TradePulse UI Chart Component
Component for creating and managing charts
"""

import panel as pn
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .base_component import BaseComponent
from .data_manager import DataManager

class ChartComponent(BaseComponent):
    """Component for creating and managing charts"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("ChartComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create chart components"""
        self.components['candlestick'] = pn.pane.Plotly(
            self.create_candlestick_chart(),
            height=400
        )
        
        self.components['volume'] = pn.pane.Plotly(
            self.create_volume_chart(),
            height=200
        )
        
        self.components['indicators'] = pn.pane.Plotly(
            self.create_indicators_chart(),
            height=300
        )
        
        self.components['ml_predictions'] = pn.pane.Plotly(
            self.create_ml_predictions_chart(),
            height=300
        )
    
    def get_layout(self):
        """Get the chart layout"""
        return pn.Column(
            pn.pane.Markdown("### 📈 Price Charts"),
            self.components['candlestick'],
            self.components['volume'],
            pn.pane.Markdown("### 📊 Technical Indicators"),
            self.components['indicators'],
            pn.pane.Markdown("### 🤖 ML Predictions"),
            self.components['ml_predictions']
        )
    
    def create_candlestick_chart(self, symbol: str = "AAPL") -> go.Figure:
        """Create candlestick chart"""
        df = self.data_manager.get_price_data_for_symbol(symbol)
        if df.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        )])
        
        fig.update_layout(
            title=f'{symbol} Candlestick Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    def create_volume_chart(self, symbol: str = "AAPL") -> go.Figure:
        """Create volume chart"""
        df = self.data_manager.get_price_data_for_symbol(symbol)
        if df.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='Volume'
        )])
        
        fig.update_layout(
            title='Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_dark',
            height=200
        )
        
        return fig
    
    def create_indicators_chart(self, symbol: str = "AAPL") -> go.Figure:
        """Create technical indicators chart"""
        df = self.data_manager.get_price_data_for_symbol(symbol)
        if df.empty:
            return go.Figure()
        
        close_prices = df['Close']
        
        # Calculate indicators
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        sma_20 = close_prices.rolling(window=20).mean()
        ema_12 = close_prices.ewm(span=12).mean()
        ema_26 = close_prices.ewm(span=26).mean()
        macd = ema_12 - ema_26
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=rsi,
            name='RSI',
            line=dict(color='orange')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=macd,
            name='MACD',
            line=dict(color='blue'),
            yaxis='y2'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=sma_20,
            name='SMA 20',
            line=dict(color='green'),
            yaxis='y3'
        ))
        
        fig.update_layout(
            title='Technical Indicators',
            xaxis_title='Date',
            yaxis=dict(title='RSI', side='left'),
            yaxis2=dict(title='MACD', side='right', overlaying='y'),
            yaxis3=dict(title='SMA', side='right', overlaying='y', position=0.95),
            template='plotly_dark',
            height=300
        )
        
        return fig
    
    def create_ml_predictions_chart(self, symbol: str = "AAPL") -> go.Figure:
        """Create ML predictions chart"""
        df = self.data_manager.get_price_data_for_symbol(symbol)
        predictions = self.data_manager.get_ml_predictions()
        
        if df.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Actual prices
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            name='Actual',
            line=dict(color='blue')
        ))
        
        # Model predictions
        colors = ['red', 'green', 'orange']
        models = ['adm', 'cipo', 'bicipo']
        
        for i, model in enumerate(models):
            if model in predictions:
                pred_values = df['Close'].iloc[0] + np.cumsum(predictions[model])
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=pred_values,
                    name=f'{model.upper()} Prediction',
                    line=dict(color=colors[i], dash='dash')
                ))
        
        fig.update_layout(
            title='ML Model Predictions',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            height=300
        )
        
        return fig
    
    def update_charts(self, symbol: str):
        """Update all charts for a symbol"""
        self.components['candlestick'].object = self.create_candlestick_chart(symbol)
        self.components['volume'].object = self.create_volume_chart(symbol)
        self.components['indicators'].object = self.create_indicators_chart(symbol)
        self.components['ml_predictions'].object = self.create_ml_predictions_chart(symbol)
