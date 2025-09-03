#!/usr/bin/env python3
"""
TradePulse Data Upload - File Processor
Handles file processing for various data formats
"""

import pandas as pd
from typing import Dict, List, Optional, Union, Any, Tuple
import logging

from .format_processors import FormatProcessors
from .processing_history import ProcessingHistory

logger = logging.getLogger(__name__)

class FileProcessor:
    """Handles file processing for various data formats"""
    
    def __init__(self):
        self.processing_history = ProcessingHistory()
        self.format_processors = FormatProcessors()
        self.supported_formats = {
            'feather': '.feather',
            'duckdb': '.duckdb',
            'sqlite': '.db',
            'csv': '.csv',
            'json': '.json',
            'excel': ['.xlsx', '.xls'],
            'parquet': '.parquet'
        }
    
    def process_file(self, file_content: bytes, filename: str, format_type: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Process file content based on detected format
        
        Args:
            file_content: Raw file content
            filename: Original filename
            format_type: Detected format type
            
        Returns:
            Tuple: (DataFrame, metadata)
        """
        try:
            logger.info(f"🔄 Processing file: {filename} (format: {format_type})")
            
            # Process based on format
            if format_type.upper() == 'FEATHER':
                data, metadata = self.format_processors.process_feather(file_content, filename)
            elif format_type.upper() == 'DUCKDB':
                data, metadata = self.format_processors.process_duckdb(file_content, filename)
            elif format_type.upper() == 'SQLITE':
                data, metadata = self.format_processors.process_sqlite(file_content, filename)
            elif format_type.upper() == 'CSV':
                data, metadata = self.format_processors.process_csv(file_content, filename)
            elif format_type.upper() == 'JSON':
                data, metadata = self.format_processors.process_json(file_content, filename)
            elif format_type.upper() == 'EXCEL':
                data, metadata = self.format_processors.process_excel(file_content, filename)
            elif format_type.upper() == 'PARQUET':
                data, metadata = self.format_processors.process_parquet(file_content, filename)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            # Record processing
            self.processing_history.record_processing(filename, format_type, data.shape, True)
            
            logger.info(f"✅ File processed successfully: {data.shape[0]} rows, {data.shape[1]} columns")
            return data, metadata
            
        except Exception as e:
            logger.error(f"❌ File processing failed: {e}")
            self.processing_history.record_processing(filename, format_type, (0, 0), False, str(e))
            raise
    
    def get_processing_history(self) -> List[Dict]:
        """Get file processing history"""
        return self.processing_history.get_processing_history()
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get file processing statistics"""
        return self.processing_history.get_processing_statistics()
    
    def clear_processing_history(self) -> int:
        """Clear processing history and return count"""
        return self.processing_history.clear_processing_history()
