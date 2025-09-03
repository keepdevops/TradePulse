#!/usr/bin/env python3
"""
TradePulse Data Upload - File Loader
Handles file loading for various formats
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import logging

from .database_loaders import DatabaseLoaders
from .file_loaders import FileLoaders
from .text_loaders import TextLoaders

logger = logging.getLogger(__name__)

class FileLoader:
    """Handles file loading for various formats"""
    
    def __init__(self):
        self.supported_formats = {
            'feather': '.feather',
            'duckdb': '.duckdb',
            'sqlite': '.db',
            'csv': '.csv',
            'json': '.json',
            'excel': ['.xlsx', '.xls'],
            'parquet': '.parquet'
        }
        self.database_loaders = DatabaseLoaders()
        self.file_loaders = FileLoaders()
        self.text_loaders = TextLoaders()
    
    def detect_file_format(self, filename: str) -> str:
        """Detect file format based on extension"""
        if not filename:
            return "Unknown"
        
        file_ext = Path(filename).suffix.lower()
        
        for format_name, extensions in self.supported_formats.items():
            if isinstance(extensions, list):
                if file_ext in extensions:
                    return format_name.upper()
            elif file_ext == extensions:
                return format_name.upper()
        
        return "Unknown"
    
    def load_feather_file(self, file_content: bytes) -> pd.DataFrame:
        """Load Feather format file"""
        return self.file_loaders.load_feather_file(file_content)
    
    def load_duckdb_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """Load DuckDB format file"""
        return self.database_loaders.load_duckdb_file(file_content, filename)
    
    def load_sqlite_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """Load SQLite format file"""
        return self.database_loaders.load_sqlite_file(file_content, filename)
    
    def load_csv_file(self, file_content: bytes) -> pd.DataFrame:
        """Load CSV format file"""
        return self.text_loaders.load_csv_file(file_content)
    
    def load_json_file(self, file_content: bytes) -> pd.DataFrame:
        """Load JSON format file"""
        return self.text_loaders.load_json_file(file_content)
    
    def load_excel_file(self, file_content: bytes) -> pd.DataFrame:
        """Load Excel format file"""
        return self.file_loaders.load_excel_file(file_content)
    
    def load_parquet_file(self, file_content: bytes) -> pd.DataFrame:
        """Load Parquet format file"""
        return self.file_loaders.load_parquet_file(file_content)
    
    def load_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """Load file based on detected format"""
        detected_format = self.detect_file_format(filename)
        
        if detected_format == 'FEATHER':
            return self.load_feather_file(file_content)
        elif detected_format == 'DUCKDB':
            return self.load_duckdb_file(file_content, filename)
        elif detected_format == 'SQLITE':
            return self.load_sqlite_file(file_content, filename)
        elif detected_format == 'CSV':
            return self.load_csv_file(file_content)
        elif detected_format == 'JSON':
            return self.load_json_file(file_content)
        elif detected_format == 'EXCEL':
            return self.load_excel_file(file_content)
        elif detected_format == 'PARQUET':
            return self.load_parquet_file(file_content)
        else:
            raise Exception(f"Unsupported format: {detected_format}")
