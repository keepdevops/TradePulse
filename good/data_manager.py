#!/usr/bin/env python3
"""
TradePulse Panel UI - Data Manager
Handles data generation and updates
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataManager:
    """Handles data generation and updates"""
    
    def __init__(self):
        pass
    
    def generate_simulated_data(self, symbol: str) -> Dict:
        """Generate simulated market data for testing"""
        try:
            # Simulate realistic market data
            base_price = 100.0 + hash(symbol) % 1000  # Vary by symbol
            change = (np.random.random() - 0.5) * 10  # Random change
            price = base_price + change
            change_percent = (change / base_price) * 100
            
            return {
                'price': price,
                'change': change,
                'change_percent': change_percent,
                'volume': int(np.random.random() * 1000000),
                'market_cap': price * np.random.random() * 1000000000,
                'high_24h': price * (1 + np.random.random() * 0.1),
                'low_24h': price * (1 - np.random.random() * 0.1),
                'avg_volume': int(np.random.random() * 500000),
                'high_52w': price * (1 + np.random.random() * 0.5),
                'low_52w': price * (1 - np.random.random() * 0.3),
                'pe_ratio': 10 + np.random.random() * 30
            }
            
        except Exception as e:
            logger.error(f"Failed to generate simulated data: {e}")
            return {}
    
    def generate_simulated_chart_data(self, symbol: str) -> pd.DataFrame:
        """Generate simulated chart data for testing"""
        try:
            # Create time index
            dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
            
            # Generate OHLC data
            base_price = 100.0 + hash(symbol) % 1000
            prices = []
            
            for i in range(100):
                # Random walk with trend
                if i == 0:
                    price = base_price
                else:
                    change = np.random.normal(0, 0.02)  # 2% daily volatility
                    price = prices[-1] * (1 + change)
                
                prices.append(price)
            
            # Create OHLC data
            data = pd.DataFrame({
                'open': prices,
                'high': [p * (1 + np.random.random() * 0.02) for p in prices],
                'low': [p * (1 - np.random.random() * 0.02) for p in prices],
                'close': prices,
                'volume': [int(np.random.random() * 1000000) for _ in prices]
            }, index=dates)
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to generate simulated chart data: {e}")
            return pd.DataFrame()
    
    def generate_system_metrics(self) -> Dict[str, float]:
        """Generate simulated system metrics"""
        try:
            return {
                'cpu_usage': np.random.random() * 100,
                'memory_usage': np.random.random() * 100,
                'network_usage': np.random.random() * 100
            }
        except Exception as e:
            logger.error(f"Failed to generate system metrics: {e}")
            return {'cpu_usage': 0.0, 'memory_usage': 0.0, 'network_usage': 0.0}
