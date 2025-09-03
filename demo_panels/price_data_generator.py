#!/usr/bin/env python3
"""
TradePulse Demo Panels - Price Data Generator
Handles generation of demo price data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class PriceDataGenerator:
    """Handles generation of demo price data"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.init_demo_data()
    
    def init_demo_data(self):
        """Initialize demo price data"""
        try:
            logger.info("🔧 Initializing demo price data")
            
            # Generate sample price data
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            np.random.seed(42)  # For reproducible results
            
            for symbol in self.symbols:
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
                
                df = pd.DataFrame(
                    prices, 
                    columns=['Open', 'High', 'Low', 'Close', 'Volume'], 
                    index=dates
                )
                self.price_data[symbol] = df
            
            logger.info(f"✅ Demo price data initialized for {len(self.symbols)} symbols")
            
        except Exception as e:
            logger.error(f"Failed to initialize demo price data: {e}")
    
    def get_price_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get price data for a specific symbol"""
        try:
            return self.price_data.get(symbol)
        except Exception as e:
            logger.error(f"Failed to get price data for {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a specific symbol"""
        try:
            if symbol in self.price_data:
                return self.price_data[symbol]['Close'].iloc[-1]
            return None
        except Exception as e:
            logger.error(f"Failed to get current price for {symbol}: {e}")
            return None
    
    def get_price_change(self, symbol: str, days: int = 1) -> Optional[Dict[str, float]]:
        """Get price change for a specific symbol over specified days"""
        try:
            if symbol in self.price_data:
                df = self.price_data[symbol]
                if len(df) >= days + 1:
                    current_price = df['Close'].iloc[-1]
                    previous_price = df['Close'].iloc[-days-1]
                    
                    change = current_price - previous_price
                    change_pct = (change / previous_price) * 100
                    
                    return {
                        'change': change,
                        'change_pct': change_pct,
                        'current_price': current_price,
                        'previous_price': previous_price
                    }
            return None
        except Exception as e:
            logger.error(f"Failed to get price change for {symbol}: {e}")
            return None
    
    def get_volume_data(self, symbol: str) -> Optional[pd.Series]:
        """Get volume data for a specific symbol"""
        try:
            if symbol in self.price_data:
                return self.price_data[symbol]['Volume']
            return None
        except Exception as e:
            logger.error(f"Failed to get volume data for {symbol}: {e}")
            return None
    
    def reset_price_data(self):
        """Reset price data to initial state"""
        try:
            logger.info("🔄 Resetting price data")
            self.init_demo_data()
            logger.info("✅ Price data reset completed")
        except Exception as e:
            logger.error(f"Failed to reset price data: {e}")
    
    def export_price_data(self) -> Dict[str, Any]:
        """Export price data for external use"""
        try:
            export_data = {
                'price_data': {symbol: df.to_dict() for symbol, df in self.price_data.items()},
                'export_timestamp': datetime.now().isoformat()
            }
            logger.info("📤 Price data exported")
            return export_data
        except Exception as e:
            logger.error(f"Failed to export price data: {e}")
            return {}
    
    def import_price_data(self, price_data: Dict[str, Any]):
        """Import price data from external source"""
        try:
            if 'price_data' in price_data:
                self.price_data = {symbol: pd.DataFrame(data) for symbol, data in price_data['price_data'].items()}
            logger.info("📥 Price data imported")
        except Exception as e:
            logger.error(f"Failed to import price data: {e}")
