#!/usr/bin/env python3
"""
TradePulse Panel UI - Chart Creation Logic
Chart creation utilities and methods
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict
import logging

from .base import DataManager

logger = logging.getLogger(__name__)

class CandlestickChartCreator:
    """Handles candlestick chart creation"""
    
    @staticmethod
    def create_chart(data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create candlestick chart"""
        df = data_manager.get_price_data(symbol)
        if df.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
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

class VolumeChartCreator:
    """Handles volume chart creation"""
    
    @staticmethod
    def create_chart(data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create volume chart"""
        df = data_manager.get_price_data(symbol)
        if df.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Bar(
            x=df.index,
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

class TechnicalIndicatorsCreator:
    """Handles technical indicators chart creation"""
    
    @staticmethod
    def calculate_rsi(close_prices: pd.Series) -> pd.Series:
        """Calculate RSI indicator"""
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def calculate_macd(close_prices: pd.Series) -> pd.Series:
        """Calculate MACD indicator"""
        ema_12 = close_prices.ewm(span=12).mean()
        ema_26 = close_prices.ewm(span=26).mean()
        return ema_12 - ema_26
    
    @staticmethod
    def create_chart(data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create technical indicators chart"""
        df = data_manager.get_price_data(symbol)
        if df.empty:
            return go.Figure()
        
        close_prices = df['Close']
        
        # Calculate indicators
        rsi = TechnicalIndicatorsCreator.calculate_rsi(close_prices)
        sma_20 = close_prices.rolling(window=20).mean()
        macd = TechnicalIndicatorsCreator.calculate_macd(close_prices)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=rsi,
            name='RSI',
            line=dict(color='orange')
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=macd,
            name='MACD',
            line=dict(color='blue'),
            yaxis='y2'
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
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

class MLPredictionsCreator:
    """Handles ML predictions chart creation"""
    
    @staticmethod
    def create_chart(data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create ML predictions chart"""
        df = data_manager.get_price_data(symbol)
        predictions = data_manager.get_ml_predictions(symbol)
        
        if df.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Actual prices
        fig.add_trace(go.Scatter(
            x=df.index,
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
                    x=df.index,
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

class ChartCreator:
    """Main chart creator that coordinates all chart types"""
    
    def __init__(self):
        self.candlestick_creator = CandlestickChartCreator()
        self.volume_creator = VolumeChartCreator()
        self.indicators_creator = TechnicalIndicatorsCreator()
        self.ml_creator = MLPredictionsCreator()
    
    def create_candlestick_chart(self, data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create candlestick chart"""
        return self.candlestick_creator.create_chart(data_manager, symbol)
    
    def create_volume_chart(self, data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create volume chart"""
        return self.volume_creator.create_chart(data_manager, symbol)
    
    def create_indicators_chart(self, data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create technical indicators chart"""
        return self.indicators_creator.create_chart(data_manager, symbol)
    
    def create_ml_predictions_chart(self, data_manager: DataManager, symbol: str = "AAPL") -> go.Figure:
        """Create ML predictions chart"""
        return self.ml_creator.create_chart(data_manager, symbol)
