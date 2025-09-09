#!/usr/bin/env python3
"""
TradePulse Data Access - File Readers
File reading functionality for various data formats
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
import json

logger = logging.getLogger(__name__)

class DataAccessFileReaders:
    """File reading functionality for data access"""
    
    def __init__(self, file_ops):
        self.file_ops = file_ops
    
    def _read_csv_file(self, file_path: str) -> pd.DataFrame:
        """Read CSV file"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"❌ Failed to read CSV file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_json_file(self, file_path: str) -> pd.DataFrame:
        """Read JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"❌ Failed to read JSON file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_feather_file(self, file_path: str) -> pd.DataFrame:
        """Read Feather file"""
        try:
            return pd.read_feather(file_path)
        except Exception as e:
            logger.error(f"❌ Failed to read Feather file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_parquet_file(self, file_path: str) -> pd.DataFrame:
        """Read Parquet file"""
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            logger.error(f"❌ Failed to read Parquet file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_duckdb_file(self, file_path: str, symbol: str) -> pd.DataFrame:
        """Read DuckDB file"""
        try:
            import duckdb
            conn = duckdb.connect(file_path)
            query = f"SELECT * FROM data WHERE Symbol = '{symbol}'"
            return conn.execute(query).df()
        except Exception as e:
            logger.error(f"❌ Failed to read DuckDB file {file_path}: {e}")
            return pd.DataFrame()
    
    def _read_keras_file(self, file_path: str, symbol: str) -> pd.DataFrame:
        """Read Keras HDF5 file"""
        try:
            import h5py
            with h5py.File(file_path, 'r') as f:
                # Extract data from HDF5 file
                data = {}
                for key in f.keys():
                    data[key] = f[key][:]
                return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"❌ Failed to read Keras file {file_path}: {e}")
            return pd.DataFrame()
    
    def get_file_reader(self, format_name: str):
        """Get the appropriate file reader for a format"""
        readers = {
            'csv': self._read_csv_file,
            'json': self._read_json_file,
            'feather': self._read_feather_file,
            'parquet': self._read_parquet_file,
            'duckdb': self._read_duckdb_file,
            'keras': self._read_keras_file
        }
        return readers.get(format_name)
