"""
Data Fetcher Component
Handles fetching historical data from Redline utility and live data from APIs.
"""

import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from utils.logger import LoggerMixin
from utils.database import Database
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from .data_sources import DataSources
from .data_exporter import DataExporter
from .data_operations import DataOperations


class DataFetcher(LoggerMixin):
    """
    Data fetcher for TradePulse.
    
    Handles:
    - Historical data from Redline utility (DuckDB/SQLite/JSON)
    - Live feed data from configured APIs
    - Data validation and caching
    """
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """
        Initialize the data fetcher.
        
        Args:
            config: Configuration loader instance
            message_bus: Message Bus client for communication
        """
        super().__init__()
        self.config = config
        self.message_bus = message_bus
        self.database = Database(config)
        
        # Data cache
        self.cache: Dict[str, pd.DataFrame] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.cache_duration = 300  # 5 minutes
        
        # Redline configuration
        self.redline_path = config.get('redline.data_path', './data/redline_data.duckdb')
        self.redline_format = config.get('redline.output_format', 'duckdb')
        
        # Data sources, exporter, and operations
        self.data_sources = DataSources(config, self.database)
        self.data_exporter = DataExporter(message_bus)
        self.data_operations = DataOperations(self, message_bus, config)
        
        self.log_info("Data Fetcher initialized")
    
    def fetch_historical_data(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
        
        Returns:
            Historical data as DataFrame or None if failed
        """
        try:
            # Check cache first
            cache_key = f"{ticker}_{start_date}_{end_date}"
            if self._is_cache_valid(cache_key):
                self.log_info(f"Returning cached data for {ticker}")
                return self.cache[cache_key]
            
            # Fetch from Redline utility using data sources
            data = self.data_sources.fetch_from_redline(ticker, start_date, end_date)
            
            if data is not None and not data.empty:
                # Cache the data
                self._cache_data(cache_key, data)
                
                # Publish data update message
                self.message_bus.publish("data_updated", {
                    'ticker': ticker,
                    'data_type': 'historical',
                    'rows': len(data),
                    'start_date': start_date,
                    'end_date': end_date
                })
                
                self.log_info(f"Fetched {len(data)} rows of historical data for {ticker}")
                return data
            else:
                self.log_warning(f"No historical data found for {ticker}")
                return None
                
        except Exception as e:
            self.log_error(f"Error fetching historical data for {ticker}: {e}")
            return None
    
    def fetch_live_data(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch live data for multiple tickers."""
        return self.data_operations.fetch_live_data(tickers)
    
    def fetch_multiple_tickers(
        self,
        tickers: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple tickers."""
        return self.data_operations.fetch_multiple_tickers(tickers, start_date, end_date)
    
    def get_available_tickers(self) -> List[str]:
        """Get list of available tickers from Redline data."""
        try:
            return self.data_sources.get_available_tickers()
        except Exception as e:
            self.log_error(f"Error getting available tickers: {e}")
            return []
    
    def export_data(self, ticker: str, format: str = 'csv', filepath: Optional[str] = None) -> bool:
        """
        Export data for a ticker to file.
        
        Args:
            ticker: Ticker symbol
            format: Export format ('csv', 'excel', 'json')
            filepath: Output file path (optional)
        
        Returns:
            True if export was successful
        """
        try:
            # Fetch data
            data = self.fetch_historical_data(ticker)
            if data is None or data.empty:
                self.log_warning(f"No data to export for {ticker}")
                return False
            
            # Use data exporter
            return self.data_exporter.export_data(data, ticker, format, filepath)
            
        except Exception as e:
            self.log_error(f"Error exporting data for {ticker}: {e}")
            return False
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self.cache_timestamps:
            return False
        
        age = time.time() - self.cache_timestamps[cache_key]
        return age < self.cache_duration
    
    def _cache_data(self, cache_key: str, data: pd.DataFrame) -> None:
        """Cache data with timestamp."""
        self.cache[cache_key] = data
        self.cache_timestamps[cache_key] = time.time()
        
        # Clean up old cache entries
        self._cleanup_cache()
    
    def _cleanup_cache(self) -> None:
        """Remove expired cache entries."""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.cache_timestamps.items()
            if current_time - timestamp > self.cache_duration
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.cache_timestamps[key]
        
        if expired_keys:
            self.log_debug(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def close(self) -> None:
        """Clean up resources."""
        try:
            self.database.close()
            self.log_info("Data Fetcher closed")
        except Exception as e:
            self.log_error(f"Error closing Data Fetcher: {e}")
