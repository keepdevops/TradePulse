#!/usr/bin/env python3
"""
TradePulse Unified Data Access System
Provides unified access to both API data and uploaded data for all modules
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json

logger = logging.getLogger(__name__)

class DataAccessManager:
    """Unified data access manager for all modules"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.api_sources = {
            'yahoo': self._fetch_yahoo_data,
            'alpha_vantage': self._fetch_alpha_vantage_data,
            'iex': self._fetch_iex_data,
            'mock': self._generate_mock_data
        }
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
    def get_data(self, source: str, symbol: str, timeframe: str = '1d', 
                 start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Get data from specified source"""
        try:
            cache_key = f"{source}_{symbol}_{timeframe}_{start_date}_{end_date}"
            
            # Check cache first
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_ttl:
                    logger.info(f"📋 Using cached data for {symbol}")
                    return cached_data.copy()
            
            # Fetch fresh data
            if source in self.api_sources:
                data = self.api_sources[source](symbol, timeframe, start_date, end_date)
            else:
                raise ValueError(f"Unknown data source: {source}")
            
            # Cache the result
            self.cache[cache_key] = (data, datetime.now())
            
            logger.info(f"✅ Fetched {len(data)} records for {symbol} from {source}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch data for {symbol} from {source}: {e}")
            return pd.DataFrame()
    
    def get_uploaded_data(self, dataset_id: Optional[str] = None, 
                         module: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Get uploaded data for specific module or dataset"""
        try:
            if dataset_id:
                # Return specific dataset
                return self.data_manager.get_dataset(dataset_id)
            elif module:
                # Return all datasets available for module
                available_datasets = self.data_manager.get_available_datasets(module)
                return {ds_id: self.data_manager.get_dataset(ds_id) 
                       for ds_id in available_datasets}
            else:
                # Return all uploaded datasets
                return {ds_id: self.data_manager.get_dataset(ds_id) 
                       for ds_id in self.data_manager.uploaded_datasets.keys()}
                
        except Exception as e:
            logger.error(f"❌ Failed to get uploaded data: {e}")
            return pd.DataFrame() if dataset_id else {}
    
    def get_combined_data(self, symbols: List[str], source: str = 'yahoo', 
                         uploaded_datasets: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Get combined API and uploaded data"""
        try:
            combined_data = {}
            
            # Get API data for symbols
            for symbol in symbols:
                data = self.get_data(source, symbol)
                if not data.empty:
                    combined_data[f"api_{symbol}"] = data
            
            # Get uploaded datasets
            if uploaded_datasets:
                for dataset_id in uploaded_datasets:
                    data = self.get_uploaded_data(dataset_id)
                    if not data.empty:
                        combined_data[f"uploaded_{dataset_id}"] = data
            
            logger.info(f"✅ Combined {len(combined_data)} datasets")
            return combined_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get combined data: {e}")
            return {}
    
    def _fetch_yahoo_data(self, symbol: str, timeframe: str = '1d', 
                         start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            
            if start_date and end_date:
                data = ticker.history(start=start_date, end=end_date, interval=timeframe)
            else:
                data = ticker.history(period="1y", interval=timeframe)
            
            if data.empty:
                logger.warning(f"⚠️ No data returned for {symbol}")
                return pd.DataFrame()
            
            # Reset index to make date a column
            data.reset_index(inplace=True)
            return data
            
        except Exception as e:
            logger.error(f"❌ Yahoo Finance error for {symbol}: {e}")
            return pd.DataFrame()
    
    def _fetch_alpha_vantage_data(self, symbol: str, timeframe: str = '1d', 
                                 start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from Alpha Vantage (mock implementation)"""
        try:
            # Mock Alpha Vantage implementation
            # In production, you would use actual Alpha Vantage API
            logger.info(f"📡 Mock Alpha Vantage data for {symbol}")
            return self._generate_mock_data(symbol, timeframe, start_date, end_date)
            
        except Exception as e:
            logger.error(f"❌ Alpha Vantage error for {symbol}: {e}")
            return pd.DataFrame()
    
    def _fetch_iex_data(self, symbol: str, timeframe: str = '1d', 
                       start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from IEX Cloud (mock implementation)"""
        try:
            # Mock IEX implementation
            # In production, you would use actual IEX Cloud API
            logger.info(f"📡 Mock IEX data for {symbol}")
            return self._generate_mock_data(symbol, timeframe, start_date, end_date)
            
        except Exception as e:
            logger.error(f"❌ IEX error for {symbol}: {e}")
            return pd.DataFrame()
    
    def _generate_mock_data(self, symbol: str, timeframe: str = '1d', 
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Generate mock data for testing"""
        try:
            # Generate date range
            if start_date and end_date:
                start = pd.to_datetime(start_date)
                end = pd.to_datetime(end_date)
            else:
                end = datetime.now()
                start = end - timedelta(days=365)
            
            # Generate dates
            dates = pd.date_range(start=start, end=end, freq='D')
            
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
    
    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()
        logger.info("🗑️ Data cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'cache_ttl': self.cache_ttl,
            'cached_keys': list(self.cache.keys())
        }
