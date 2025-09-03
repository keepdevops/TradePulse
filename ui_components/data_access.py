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
    
    def _fetch_upload_data(self, symbol: str, timeframe: str = '1d', 
                          start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from uploaded files and hard drive (supports duckdb, feather, keras, json, csv formats)"""
        try:
            import glob
            import os
            from pathlib import Path
            
            # Define directories to scan for data files
            scan_directories = [
                "uploads/",
                "upload_data/",
                "redline_data/",
                "data/",
                "model_training_data/",
                str(Path.home() / "Downloads"),  # User's Downloads folder
                str(Path.home() / "Documents"),  # User's Documents folder
                str(Path.home() / "Desktop"),    # User's Desktop folder
            ]
            
            # Define supported file patterns and their readers
            file_patterns = {
                'csv': {
                    'patterns': ["*.csv", "*_data.csv", "*_stock.csv", "*_trading.csv"],
                    'reader': lambda f: pd.read_csv(f)
                },
                'json': {
                    'patterns': ["*.json", "*_data.json", "*_stock.json"],
                    'reader': lambda f: pd.read_json(f)
                },
                'feather': {
                    'patterns': ["*.feather", "*_data.feather"],
                    'reader': lambda f: pd.read_feather(f)
                },
                'parquet': {
                    'patterns': ["*.parquet", "*_data.parquet"],
                    'reader': lambda f: pd.read_parquet(f)
                },
                'duckdb': {
                    'patterns': ["*.duckdb", "*_data.duckdb"],
                    'reader': self._read_duckdb_file
                },
                'keras': {
                    'patterns': ["*.h5", "*_data.h5", "*.hdf5"],
                    'reader': self._read_keras_file
                }
            }
            
            all_data = []
            files_found = False
            
            # Scan all directories for data files
            for directory in scan_directories:
                if not os.path.exists(directory):
                    logger.debug(f"📁 Directory not found: {directory}")
                    continue
                    
                logger.info(f"🔍 Scanning directory: {directory}")
                
                # Try each file format in this directory
                for format_name, config in file_patterns.items():
                    try:
                        for pattern in config['patterns']:
                            search_pattern = os.path.join(directory, pattern)
                            files = glob.glob(search_pattern)
                            
                            if files:
                                files_found = True
                                logger.info(f"📁 Found {len(files)} {format_name} files in {directory}")
                                
                                for file_path in files:
                                    try:
                                        if format_name == 'duckdb':
                                            df = config['reader'](file_path, symbol)
                                        elif format_name == 'keras':
                                            df = config['reader'](file_path, symbol)
                                        else:
                                            df = config['reader'](file_path)
                                        
                                        if not df.empty:
                                            # Add symbol column if not present
                                            if 'Symbol' not in df.columns:
                                                df['Symbol'] = symbol
                                            all_data.append(df)
                                            logger.info(f"✅ Loaded {format_name} data from {file_path}")
                                            
                                    except Exception as e:
                                        logger.warning(f"⚠️ Failed to read {file_path} ({format_name}): {e}")
                                        continue
                                        
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to process {format_name} files in {directory}: {e}")
                        continue
            
            if not files_found:
                logger.warning(f"⚠️ No uploaded data files found in any supported format")
                # Try to scan for any data files in common locations
                logger.info("🔍 Scanning for data files in common locations...")
                common_data_files = self._scan_for_data_files()
                if common_data_files:
                    logger.info(f"📁 Found {len(common_data_files)} potential data files")
                    for file_path in common_data_files[:5]:  # Limit to first 5 files
                        try:
                            # Try to read as CSV first
                            df = pd.read_csv(file_path)
                            if not df.empty:
                                if 'Symbol' not in df.columns:
                                    df['Symbol'] = symbol
                                all_data.append(df)
                                logger.info(f"✅ Loaded data from {file_path}")
                        except Exception as e:
                            logger.debug(f"⚠️ Could not read {file_path}: {e}")
                            continue
                
                if not all_data:
                    logger.warning(f"⚠️ No data files found on hard drive")
                    return pd.DataFrame()
            
            if not all_data:
                logger.warning(f"⚠️ No valid uploaded data found for {symbol}")
                return pd.DataFrame()
            
            # Combine all data
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Convert Date column to datetime if it exists
            if 'Date' in combined_data.columns:
                combined_data['Date'] = pd.to_datetime(combined_data['Date'])
                
                # Sort by date
                combined_data = combined_data.sort_values('Date')
                
                # Filter by date range if specified
                if start_date and end_date:
                    start_dt = pd.to_datetime(start_date)
                    end_dt = pd.to_datetime(end_date)
                    combined_data = combined_data[
                        (combined_data['Date'] >= start_dt) & 
                        (combined_data['Date'] <= end_dt)
                    ]
            
            # Remove duplicates
            combined_data = combined_data.drop_duplicates(subset=['Date', 'Symbol'] if 'Date' in combined_data.columns else ['Symbol'])
            
            logger.info(f"✅ Fetched {len(combined_data)} records from uploaded files for {symbol}")
            return combined_data
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch uploaded data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _read_duckdb_file(self, file_path: str, symbol: str) -> pd.DataFrame:
        """Read data from DuckDB file"""
        try:
            import duckdb
            
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ DuckDB file not found: {file_path}")
                return pd.DataFrame()
            
            conn = duckdb.connect(file_path)
            
            # Try to get table names
            tables = conn.execute("SHOW TABLES").fetchdf()
            if tables.empty:
                logger.warning(f"⚠️ No tables found in DuckDB file: {file_path}")
                conn.close()
                return pd.DataFrame()
            
            # Try to read from first table or specific table
            table_name = tables.iloc[0]['name'] if len(tables) > 0 else 'uploaded_data'
            
            try:
                # Try to query the table
                query = f"SELECT * FROM {table_name} LIMIT 1000"
                data = conn.execute(query).fetchdf()
                conn.close()
                
                if not data.empty:
                    # Add symbol column if not present
                    if 'Symbol' not in data.columns:
                        data['Symbol'] = symbol
                    return data
                else:
                    logger.warning(f"⚠️ No data found in table {table_name}")
                    return pd.DataFrame()
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to query table {table_name}: {e}")
                conn.close()
                return pd.DataFrame()
                
        except ImportError:
            logger.error("❌ DuckDB not available for uploaded data access")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"❌ Failed to read DuckDB file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_keras_file(self, file_path: str, symbol: str) -> pd.DataFrame:
        """Read data from Keras HDF5 file"""
        try:
            import h5py
            
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ Keras file not found: {file_path}")
                return pd.DataFrame()
            
            data = []
            with h5py.File(file_path, 'r') as f:
                # Try to extract data from Keras file
                if 'data' in f:
                    keras_data = f['data'][:]
                    # Convert Keras data to DataFrame format
                    # This is a simplified conversion - adjust based on your Keras data structure
                    if len(keras_data.shape) >= 2:
                        data = pd.DataFrame(keras_data, columns=[f'feature_{i}' for i in range(keras_data.shape[1])])
                        data['Symbol'] = symbol
                        return data
                
                logger.warning(f"⚠️ No compatible data found in Keras file: {file_path}")
                return pd.DataFrame()
                
        except ImportError:
            logger.error("❌ h5py not available for Keras file access")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"❌ Failed to read Keras file {file_path}: {e}")
            return pd.DataFrame()
    
    def _scan_for_data_files(self) -> List[str]:
        """Scan for data files in common locations"""
        try:
            import glob
            from pathlib import Path
            
            data_files = []
            common_locations = [
                str(Path.home() / "Downloads"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop"),
                str(Path.home() / "Data"),
                str(Path.home() / "Trading"),
                str(Path.home() / "Stocks"),
                "/Users/*/Downloads",
                "/Users/*/Documents",
                "/Users/*/Desktop",
            ]
            
            # Common data file extensions
            extensions = ["*.csv", "*.json", "*.feather", "*.parquet", "*.duckdb", "*.h5", "*.hdf5"]
            
            for location in common_locations:
                if os.path.exists(location):
                    for ext in extensions:
                        try:
                            pattern = os.path.join(location, ext)
                            files = glob.glob(pattern)
                            data_files.extend(files)
                        except Exception as e:
                            logger.debug(f"⚠️ Error scanning {location} for {ext}: {e}")
                            continue
            
            # Remove duplicates and limit results
            data_files = list(set(data_files))[:20]  # Limit to 20 files
            
            logger.info(f"🔍 Found {len(data_files)} potential data files")
            return data_files
            
        except Exception as e:
            logger.error(f"❌ Failed to scan for data files: {e}")
            return []
    
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
    
    def get_available_data_files(self) -> Dict[str, List[str]]:
        """Get list of available data files by type"""
        try:
            import glob
            from pathlib import Path
            
            file_types = {
                'csv': [],
                'json': [],
                'feather': [],
                'parquet': [],
                'duckdb': [],
                'keras': []
            }
            
            # Scan directories
            scan_directories = [
                "uploads/",
                "upload_data/",
                "redline_data/",
                "data/",
                "model_training_data/",
                str(Path.home() / "Downloads"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop"),
            ]
            
            for directory in scan_directories:
                if not os.path.exists(directory):
                    continue
                    
                for file_type, extensions in {
                    'csv': ['*.csv'],
                    'json': ['*.json'],
                    'feather': ['*.feather'],
                    'parquet': ['*.parquet'],
                    'duckdb': ['*.duckdb'],
                    'keras': ['*.h5', '*.hdf5']
                }.items():
                    for ext in extensions:
                        pattern = os.path.join(directory, ext)
                        files = glob.glob(pattern)
                        file_types[file_type].extend(files)
            
            # Remove duplicates
            for file_type in file_types:
                file_types[file_type] = list(set(file_types[file_type]))
            
            logger.info(f"📁 Found data files: {sum(len(files) for files in file_types.values())} total")
            return file_types
            
        except Exception as e:
            logger.error(f"❌ Failed to get available data files: {e}")
            return {}
