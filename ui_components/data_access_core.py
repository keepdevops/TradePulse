#!/usr/bin/env python3
"""
TradePulse Data Access - Core
Core data access functionality for unified data management
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json
import os

logger = logging.getLogger(__name__)

class DataAccessManager:
    """Unified data access manager for all modules"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.api_sources = {
            'yahoo': self._fetch_yahoo_data,
            'alpha_vantage': self._fetch_alpha_vantage_data,
            'iex': self._fetch_iex_data,
            'mock': self._generate_mock_data,
            'upload': self._fetch_upload_data
        }
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Initialize file operations for mock data and upload data
        from .data_access_file_ops import DataAccessFileOps
        self.file_ops = DataAccessFileOps(self)
        
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
                        combined_data[f"upload_{dataset_id}"] = data
            
            logger.info(f"✅ Combined data for {len(combined_data)} sources")
            return combined_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get combined data: {e}")
            return {}
    
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
                logger.warning(f"⚠️ No data returned from Yahoo Finance for {symbol}")
                return pd.DataFrame()
            
            # Reset index to make Date a column
            data = data.reset_index()
            
            # Rename columns to match expected format
            data = data.rename(columns={
                'Date': 'Date',
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Close': 'Close',
                'Volume': 'Volume'
            })
            
            # Add symbol column
            data['Symbol'] = symbol
            
            logger.info(f"✅ Fetched {len(data)} records from Yahoo Finance for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch Yahoo Finance data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _fetch_alpha_vantage_data(self, symbol: str, timeframe: str = '1d', 
                                 start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from Alpha Vantage (placeholder)"""
        try:
            # Placeholder for Alpha Vantage API
            logger.info(f"📊 Alpha Vantage data fetch for {symbol} (placeholder)")
            return self._generate_mock_data(symbol, timeframe, start_date, end_date)
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch Alpha Vantage data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _fetch_iex_data(self, symbol: str, timeframe: str = '1d', 
                       start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from IEX Cloud (placeholder)"""
        try:
            # Placeholder for IEX Cloud API
            logger.info(f"📊 IEX Cloud data fetch for {symbol} (placeholder)")
            return self._generate_mock_data(symbol, timeframe, start_date, end_date)
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch IEX Cloud data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _generate_mock_data(self, symbol: str, timeframe: str = '1d', 
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Generate mock data for testing"""
        return self.file_ops._generate_mock_data(symbol, timeframe, start_date, end_date)
    
    def _fetch_upload_data(self, symbol: str, timeframe: str = '1d', 
                          start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch uploaded data from hard drive"""
        return self.file_ops._fetch_upload_data(symbol, timeframe, start_date, end_date)
    
    def get_available_data_files(self) -> Dict[str, List[str]]:
        """Get list of available data files by type"""
        return self.file_ops.get_available_data_files()

# Global instance - will be properly initialized when DataAccessManager is created
data_access_manager_core = None
