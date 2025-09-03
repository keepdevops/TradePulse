#!/usr/bin/env python3
"""
TradePulse Data Upload - Data Manager Integration
Handles integration with the data manager
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataManagerIntegration:
    """Handles integration with the data manager"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.uploaded_data = {}
    
    def add_to_data_manager(self, data: pd.DataFrame, filename: str) -> Optional[str]:
        """Add the loaded data to the data manager for use by all modules"""
        try:
            # Generate metadata for the dataset
            metadata = {
                'name': Path(filename).stem,
                'type': 'uploaded',
                'source': 'file_upload',
                'original_filename': filename,
                'upload_component': 'DataUploadComponent'
            }
            
            # Add to enhanced data manager
            if hasattr(self.data_manager, 'add_uploaded_data'):
                dataset_id = self.data_manager.add_uploaded_data(filename, data, metadata)
                logger.info(f"✅ Added uploaded data to data manager with dataset ID: {dataset_id}")
                
                # Store reference in local storage for component access
                self.uploaded_data[filename] = {
                    'data': data,
                    'dataset_id': dataset_id,
                    'format': self._detect_file_format(filename),
                    'timestamp': pd.Timestamp.now()
                }
                
                return dataset_id
            else:
                # Fallback: store in local storage
                self.uploaded_data[filename] = {
                    'data': data,
                    'dataset_id': None,
                    'format': self._detect_file_format(filename),
                    'timestamp': pd.Timestamp.now()
                }
                logger.warning("⚠️ Data manager doesn't support add_uploaded_data, using local storage")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to add data to data manager: {e}")
            raise
    
    def _detect_file_format(self, filename: str) -> str:
        """Detect file format based on extension"""
        if not filename:
            return "Unknown"
        
        file_ext = Path(filename).suffix.lower()
        supported_formats = {
            'feather': '.feather',
            'duckdb': '.duckdb',
            'sqlite': '.db',
            'csv': '.csv',
            'json': '.json',
            'excel': ['.xlsx', '.xls'],
            'parquet': '.parquet'
        }
        
        for format_name, extensions in supported_formats.items():
            if isinstance(extensions, list):
                if file_ext in extensions:
                    return format_name.upper()
            elif file_ext == extensions:
                return format_name.upper()
        
        return "Unknown"
    
    def get_uploaded_data(self) -> Dict[str, Any]:
        """Get all uploaded data"""
        return self.uploaded_data
    
    def clear_uploaded_data(self):
        """Clear all uploaded data"""
        self.uploaded_data.clear()
