#!/usr/bin/env python3
"""
TradePulse Data Access - File Operations
File reading, scanning, and mock data generation functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import os
import glob
from pathlib import Path
import json

from .data_access_file_readers import DataAccessFileReaders
from .data_access_file_scanning import DataAccessFileScanning
from .data_access_mock_data import DataAccessMockData

logger = logging.getLogger(__name__)

class DataAccessFileOps:
    """File operations for data access"""
    
    def __init__(self, core_manager):
        self.core = core_manager
        self.readers = DataAccessFileReaders(self)
        self.scanning = DataAccessFileScanning(self)
        self.mock_data = DataAccessMockData(self)
    
    def _fetch_upload_data(self, symbol: str, timeframe: str = '1d', 
                          start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Fetch uploaded data from hard drive"""
        try:
            # Define scan directories and file patterns
            scan_directories = self.scanning.get_scan_directories()
            file_patterns_config = self.scanning.get_file_patterns()
            
            # Define file patterns and readers
            file_patterns = {
                'csv': {
                    'patterns': file_patterns_config['csv'],
                    'reader': self.readers._read_csv_file
                },
                'json': {
                    'patterns': file_patterns_config['json'],
                    'reader': self.readers._read_json_file
                },
                'feather': {
                    'patterns': file_patterns_config['feather'],
                    'reader': self.readers._read_feather_file
                },
                'parquet': {
                    'patterns': file_patterns_config['parquet'],
                    'reader': self.readers._read_parquet_file
                },
                'duckdb': {
                    'patterns': file_patterns_config['duckdb'],
                    'reader': self.readers._read_duckdb_file
                },
                'keras': {
                    'patterns': file_patterns_config['keras'],
                    'reader': self.readers._read_keras_file
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
                common_data_files = self.scanning._scan_for_data_files()
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
            combined_data = combined_data.drop_duplicates()
            
            logger.info(f"✅ Loaded {len(combined_data)} records from uploaded data for {symbol}")
            return combined_data
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch uploaded data for {symbol}: {e}")
            return pd.DataFrame()
    

    
    def get_available_data_files(self) -> Dict[str, List[str]]:
        """Get list of available data files by type"""
        return self.scanning.get_available_data_files()
    
    def _generate_mock_data(self, symbol: str, timeframe: str = '1d', 
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Generate mock data for testing with support for longer date ranges"""
        return self.mock_data._generate_mock_data(symbol, timeframe, start_date, end_date)
    
    
