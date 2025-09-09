#!/usr/bin/env python3
"""
TradePulse Data Upload - Format Detector
Detects file formats and provides format-specific information
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class FormatDetector:
    """Detects file formats and provides format-specific information"""
    
    def __init__(self):
        self.supported_formats = {
            'csv': {
                'extensions': ['.csv'],
                'mime_types': ['text/csv', 'application/csv'],
                'description': 'Comma-separated values',
                'readable': True,
                'writable': True
            },
            'json': {
                'extensions': ['.json'],
                'mime_types': ['application/json'],
                'description': 'JavaScript Object Notation',
                'readable': True,
                'writable': True
            },
            'feather': {
                'extensions': ['.feather'],
                'mime_types': ['application/octet-stream'],
                'description': 'Feather format for fast data storage',
                'readable': True,
                'writable': True
            },
            'parquet': {
                'extensions': ['.parquet', '.parq'],
                'mime_types': ['application/octet-stream'],
                'description': 'Columnar storage format',
                'readable': True,
                'writable': True
            },
            'excel': {
                'extensions': ['.xlsx', '.xls'],
                'mime_types': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
                'description': 'Microsoft Excel format',
                'readable': True,
                'writable': True
            },
            'duckdb': {
                'extensions': ['.duckdb', '.db'],
                'mime_types': ['application/octet-stream'],
                'description': 'DuckDB database format',
                'readable': True,
                'writable': True
            },
            'keras': {
                'extensions': ['.h5', '.hdf5'],
                'mime_types': ['application/octet-stream'],
                'description': 'Keras HDF5 model format',
                'readable': True,
                'writable': True
            }
        }
    
    def detect_format(self, file_path: str) -> Optional[str]:
        """Detect the format of a file based on its extension"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ File does not exist: {file_path}")
                return None
            
            file_extension = Path(file_path).suffix.lower()
            
            for format_name, format_info in self.supported_formats.items():
                if file_extension in format_info['extensions']:
                    logger.info(f"✅ Detected format: {format_name} for {file_path}")
                    return format_name
            
            logger.warning(f"⚠️ Unknown format for file: {file_path}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error detecting format for {file_path}: {e}")
            return None
    
    def get_format_info(self, format_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific format"""
        return self.supported_formats.get(format_name)
    
    def is_supported(self, file_path: str) -> bool:
        """Check if a file format is supported"""
        format_name = self.detect_format(file_path)
        return format_name is not None
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions"""
        extensions = []
        for format_info in self.supported_formats.values():
            extensions.extend(format_info['extensions'])
        return extensions
    
    def get_supported_formats(self) -> Dict[str, Dict[str, Any]]:
        """Get all supported formats"""
        return self.supported_formats.copy()
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a file and return validation results"""
        try:
            if not os.path.exists(file_path):
                return {
                    'valid': False,
                    'error': 'File does not exist',
                    'format': None
                }
            
            format_name = self.detect_format(file_path)
            if format_name is None:
                return {
                    'valid': False,
                    'error': 'Unsupported file format',
                    'format': None
                }
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return {
                    'valid': False,
                    'error': 'File is empty',
                    'format': format_name
                }
            
            return {
                'valid': True,
                'error': None,
                'format': format_name,
                'size': file_size,
                'size_human': self._format_size(file_size)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'format': None
            }
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
