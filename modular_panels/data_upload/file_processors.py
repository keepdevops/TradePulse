#!/usr/bin/env python3
"""
TradePulse Data Upload - File Processors
Handles file format processing (Feather, Parquet, Excel)
"""

import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
from typing import Dict, Any, Tuple
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

class FileProcessors:
    """Handles file format processing (Feather, Parquet, Excel)"""
    
    @staticmethod
    def process_feather(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Feather format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.feather', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Read Feather file with pandas
                data = pd.read_feather(temp_file_path)
                
                metadata = {
                    'format': 'feather',
                    'filename': filename,
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.to_dict()
                }
                
                return data, metadata
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to process Feather file: {e}")
            raise
    
    @staticmethod
    def process_parquet(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Parquet format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Read Parquet file with pandas
                data = pd.read_parquet(temp_file_path)
                
                metadata = {
                    'format': 'parquet',
                    'filename': filename,
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.to_dict()
                }
                
                return data, metadata
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to process Parquet file: {e}")
            raise
    
    @staticmethod
    def process_excel(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process Excel format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Read Excel file
                excel_file = pd.ExcelFile(temp_file_path)
                
                # Read first sheet
                sheet_name = excel_file.sheet_names[0]
                data = pd.read_excel(temp_file_path, sheet_name=sheet_name)
                
                metadata = {
                    'format': 'excel',
                    'filename': filename,
                    'sheet_name': sheet_name,
                    'sheets': excel_file.sheet_names,
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.to_dict()
                }
                
                return data, metadata
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to process Excel file: {e}")
            raise
