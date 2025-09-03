#!/usr/bin/env python3
"""
TradePulse Data Upload - File Loaders
Handles file format loading (Feather, Parquet, Excel, CSV)
"""

import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
from typing import Dict, Any
import logging
import tempfile
import os
import io

logger = logging.getLogger(__name__)

class FileLoaders:
    """Handles file format loading (Feather, Parquet, Excel)"""
    
    @staticmethod
    def load_feather_file(file_content: bytes) -> pd.DataFrame:
        """Load Feather format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.feather', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Read with pandas (feather.read_feather returns DataFrame directly)
                df = pd.read_feather(tmp_file.name)
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return df
        except Exception as e:
            raise Exception(f"Failed to load Feather file: {e}")
    
    @staticmethod
    def load_parquet_file(file_content: bytes) -> pd.DataFrame:
        """Load Parquet format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Read with pandas
                df = pd.read_parquet(tmp_file.name)
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return df
        except Exception as e:
            raise Exception(f"Failed to load Parquet file: {e}")
    
    @staticmethod
    def load_excel_file(file_content: bytes) -> pd.DataFrame:
        """Load Excel format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Read Excel file
                excel_file = pd.ExcelFile(tmp_file.name)
                
                # Read first sheet (you could add UI to select specific sheet)
                sheet_name = excel_file.sheet_names[0]
                df = pd.read_excel(tmp_file.name, sheet_name=sheet_name)
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return df
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {e}")
    
    @staticmethod
    def load_csv_file(file_content: bytes) -> pd.DataFrame:
        """Load CSV format file"""
        try:
            # Try to decode and parse CSV
            content_str = file_content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content_str))
            return df
        except Exception as e:
            raise Exception(f"Failed to load CSV file: {e}")
