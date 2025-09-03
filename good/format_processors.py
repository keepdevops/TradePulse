#!/usr/bin/env python3
"""
TradePulse Data Upload - Format Processors
Handles specific format processing for various data types
"""

import pandas as pd
from typing import Dict, Any, Tuple
import logging

from .database_processors import DatabaseProcessors
from .file_processors import FileProcessors
from .text_processors import TextProcessors

logger = logging.getLogger(__name__)

class FormatProcessors:
    """Handles specific format processing for various data types"""
    
    def __init__(self):
        self.database_processors = DatabaseProcessors()
        self.file_processors = FileProcessors()
        self.text_processors = TextProcessors()
    
    def process_feather(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Feather format file"""
        return self.file_processors.process_feather(file_content, filename)
    
    def process_duckdb(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process DuckDB format file"""
        return self.database_processors.process_duckdb(file_content, filename)
    
    def process_sqlite(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process SQLite format file"""
        return self.database_processors.process_sqlite(file_content, filename)
    
    def process_csv(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process CSV format file"""
        return self.text_processors.process_csv(file_content, filename)
    
    def process_json(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process JSON format file"""
        return self.text_processors.process_json(file_content, filename)
    
    def process_excel(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Excel format file"""
        return self.file_processors.process_excel(file_content, filename)
    
    def process_parquet(self, file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Parquet format file"""
        return self.file_processors.process_parquet(file_content, filename)
