#!/usr/bin/env python3
"""
TradePulse Panel UI - Base Components
Base classes and utilities for modular UI components
"""

import panel as pn
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import threading
import time
from typing import Dict, List, Optional, Callable
import logging
from abc import ABC, abstractmethod

# Setup logging
logger = logging.getLogger(__name__)

class BaseComponent(ABC):
    """Base class for all UI components"""
    
    def __init__(self, name: str):
        self.name = name
        self.components = {}
        self.callbacks = {}
    
    @abstractmethod
    def create_components(self):
        """Create the component's UI elements"""
        pass
    
    @abstractmethod
    def get_layout(self):
        """Get the component's layout"""
        pass
    
    def add_callback(self, event_name: str, callback: Callable):
        """Add a callback for an event"""
        self.callbacks[event_name] = callback
    
    def trigger_callback(self, event_name: str, *args, **kwargs):
        """Trigger a callback"""
        if event_name in self.callbacks:
            self.callbacks[event_name](*args, **kwargs)

class DataManager:
    """Manages data for the UI"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.portfolio_data = {}
        self.ml_predictions = {}
        self.alerts = []
        self.orders = []
        
        self.load_initial_data()
    
    def load_initial_data(self):
        """Load initial data for all symbols"""
        logger.info("📊 Loading initial data...")
        
        for symbol in self.symbols:
            try:
                # Generate sample data for now
                dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
                np.random.seed(hash(symbol) % 1000)
                
                base_price = 100 + np.random.randint(50, 200)
                prices = []
                
                for i in range(len(dates)):
                    change = np.random.normal(0, 2)
                    base_price += change
                    open_price = base_price
                    high_price = base_price + abs(np.random.normal(0, 1))
                    low_price = base_price - abs(np.random.normal(0, 1))
                    close_price = base_price + np.random.normal(0, 1)
                    volume = np.random.randint(1000000, 10000000)
                    prices.append([open_price, high_price, low_price, close_price, volume])
                
                df = pd.DataFrame(prices, columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=dates)
                self.price_data[symbol] = df
                
                # Generate ML predictions
                self.ml_predictions[symbol] = {
                    'adm': np.random.normal(0, 1, len(dates)),
                    'cipo': np.random.normal(0, 1, len(dates)),
                    'bicipo': np.random.normal(0, 1, len(dates))
                }
                
            except Exception as e:
                logger.error(f"❌ Error loading data for {symbol}: {e}")
        
        # Initialize portfolio data
        self.portfolio_data = {
            'total_value': 100000.0,
            'cash': 50000.0,
            'positions': {
                'AAPL': {'shares': 100, 'avg_price': 150.0, 'current_price': 155.0},
                'GOOGL': {'shares': 50, 'avg_price': 2800.0, 'current_price': 2850.0},
                'MSFT': {'shares': 75, 'avg_price': 300.0, 'current_price': 310.0}
            },
            'performance': {
                'total_return': 0.05,
                'daily_pnl': 2500.0,
                'sharpe_ratio': 1.2,
                'max_drawdown': -0.08
            }
        }
        
        logger.info("✅ Initial data loaded successfully")
    
    def get_price_data(self, symbol: str) -> pd.DataFrame:
        """Get price data for a symbol"""
        return self.price_data.get(symbol, pd.DataFrame())
    
    def get_ml_predictions(self, symbol: str) -> Dict:
        """Get ML predictions for a symbol"""
        return self.ml_predictions.get(symbol, {})
    
    def get_portfolio_data(self) -> Dict:
        """Get portfolio data"""
        return self.portfolio_data
    
    def update_price_data(self, symbol: str, new_price: float):
        """Update price data for a symbol"""
        if symbol in self.price_data:
            df = self.price_data[symbol]
            if len(df) > 0:
                df.iloc[-1, df.columns.get_loc('Close')] = new_price
                df.iloc[-1, df.columns.get_loc('High')] = max(df.iloc[-1]['High'], new_price)
                df.iloc[-1, df.columns.get_loc('Low')] = min(df.iloc[-1]['Low'], new_price)
