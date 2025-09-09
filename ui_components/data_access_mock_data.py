#!/usr/bin/env python3
"""
TradePulse Data Access - Mock Data Generation
Mock data generation functionality for testing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataAccessMockData:
    """Mock data generation functionality for data access"""
    
    def __init__(self, file_ops):
        self.file_ops = file_ops
    
    def _generate_mock_data(self, symbol: str, timeframe: str = '1d', 
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Generate mock data for testing with support for longer date ranges"""
        try:
            # Generate date range
            if start_date and end_date:
                start = pd.to_datetime(start_date)
                end = pd.to_datetime(end_date)
            else:
                end = datetime.now()
                start = end - timedelta(days=365)
            
            # Map timeframe to frequency
            freq_mapping = {
                '1m': '1min',
                '5m': '5min', 
                '15m': '15min',
                '1h': '1h',  # Fixed deprecated 'H' to 'h'
                '1d': 'D'
            }
            freq = freq_mapping.get(timeframe, 'D')
            
            # For very long ranges, use daily data and resample
            if (end - start).days > 365 * 2:  # More than 2 years
                freq = 'D'  # Use daily data for long ranges
                logger.info(f"📅 Using daily frequency for long date range: {(end - start).days} days")
            
            # Generate dates
            dates = pd.date_range(start=start, end=end, freq=freq)
            
            # Generate mock price data
            np.random.seed(hash(symbol) % 2**32)  # Consistent seed per symbol
            base_price = 100 + hash(symbol) % 900  # Base price between 100-1000
            
            data = []
            current_price = base_price
            
            for date in dates:
                # Random walk with some trend
                change = np.random.normal(0, 2) + np.sin(date.dayofyear / 365 * 2 * np.pi) * 0.5
                current_price = max(1, current_price + change)
                
                data.append({
                    'Date': date,
                    'Open': current_price * (1 + np.random.normal(0, 0.01)),
                    'High': current_price * (1 + abs(np.random.normal(0, 0.02))),
                    'Low': current_price * (1 - abs(np.random.normal(0, 0.02))),
                    'Close': current_price,
                    'Volume': int(np.random.exponential(1000000))
                })
            
            df = pd.DataFrame(data)
            df['Symbol'] = symbol
            return df
            
        except Exception as e:
            logger.error(f"❌ Mock data generation error for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_freq_mapping(self) -> Dict[str, str]:
        """Get frequency mapping for timeframes"""
        return {
            '1m': '1min',
            '5m': '5min', 
            '15m': '15min',
            '1h': '1h',
            '1d': 'D'
        }
    
    def calculate_long_range_threshold(self) -> int:
        """Calculate threshold for long date ranges"""
        return 365 * 2  # More than 2 years
