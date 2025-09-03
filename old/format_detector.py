#!/usr/bin/env python3
"""
TradePulse Data Upload - Format Detector
Handles file format detection and validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import logging

logger = logging.getLogger(__name__)

class FormatDetector:
    """Handles file format detection and validation"""
    
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
        
        self.format_mime_types = {
            'feather': 'application/octet-stream',
            'duckdb': 'application/octet-stream',
            'sqlite': 'application/x-sqlite3',
            'csv': 'text/csv',
            'json': 'application/json',
            'excel': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
            'parquet': 'application/octet-stream'
        }
        
        self.detection_history = []
    
    def detect_file_format(self, filename: str) -> str:
        """Detect file format based on extension"""
        try:
            if not filename:
                return "Unknown"
            
            file_ext = Path(filename).suffix.lower()
            
            for format_name, extensions in self.supported_formats.items():
                if isinstance(extensions, list):
                    if file_ext in extensions:
                        self._record_detection(filename, format_name, file_ext)
                        return format_name.upper()
                else:
                    if file_ext == extensions:
                        self._record_detection(filename, format_name, file_ext)
                        return format_name.upper()
            
            # Unknown format
            self._record_detection(filename, "Unknown", file_ext)
            return "Unknown"
            
        except Exception as e:
            logger.error(f"Failed to detect file format: {e}")
            return "Unknown"
    
    def detect_format_from_content(self, file_content: bytes, filename: str = "") -> str:
        """Detect format from file content (magic bytes)"""
        try:
            if not file_content:
                return "Unknown"
            
            # Check for common file signatures
            if file_content.startswith(b'PK\x03\x04'):
                # ZIP file (Excel, some other formats)
                if filename.lower().endswith(('.xlsx', '.xls')):
                    return "EXCEL"
                return "ZIP"
            
            elif file_content.startswith(b'SQLite format 3'):
                return "SQLITE"
            
            elif file_content.startswith(b'PAR1'):
                return "PARQUET"
            
            elif file_content.startswith(b'{"') or file_content.startswith(b'['):
                return "JSON"
            
            elif file_content.startswith(b'PK\x05\x06'):
                # ZIP file (end of file)
                return "ZIP"
            
            # Try to detect CSV by checking first few lines
            try:
                first_lines = file_content[:1000].decode('utf-8', errors='ignore')
                if ',' in first_lines and '\n' in first_lines:
                    # Simple heuristic: if it has commas and newlines, likely CSV
                    return "CSV"
            except:
                pass
            
            # Default to extension-based detection
            return self.detect_file_format(filename)
            
        except Exception as e:
            logger.error(f"Failed to detect format from content: {e}")
            return "Unknown"
    
    def validate_format(self, filename: str, expected_format: str) -> bool:
        """Validate if file format matches expected format"""
        try:
            detected_format = self.detect_file_format(filename)
            is_valid = detected_format.upper() == expected_format.upper()
            
            logger.info(f"Format validation: {filename} - Expected: {expected_format}, Detected: {detected_format}, Valid: {is_valid}")
            return is_valid
            
        except Exception as e:
            logger.error(f"Failed to validate format: {e}")
            return False
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions"""
        try:
            extensions = []
            for ext in self.supported_formats.values():
                if isinstance(ext, list):
                    extensions.extend(ext)
                else:
                    extensions.append(ext)
            return extensions
            
        except Exception as e:
            logger.error(f"Failed to get supported extensions: {e}")
            return []
    
    def get_format_info(self, format_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific format"""
        try:
            if format_name.lower() not in self.supported_formats:
                return {}
            
            format_info = {
                'name': format_name,
                'extensions': self.supported_formats[format_name.lower()],
                'mime_types': self.format_mime_types.get(format_name.lower(), []),
                'description': self._get_format_description(format_name.lower())
            }
            
            return format_info
            
        except Exception as e:
            logger.error(f"Failed to get format info: {e}")
            return {}
    
    def _get_format_description(self, format_name: str) -> str:
        """Get description for a specific format"""
        descriptions = {
            'feather': 'Apache Arrow Feather format - fast, language-agnostic data frame storage',
            'duckdb': 'DuckDB database file - embedded analytical database',
            'sqlite': 'SQLite database file - embedded relational database',
            'csv': 'Comma-separated values - simple tabular data format',
            'json': 'JavaScript Object Notation - structured data format',
            'excel': 'Microsoft Excel spreadsheet format',
            'parquet': 'Apache Parquet - columnar storage format for analytics'
        }
        
        return descriptions.get(format_name, 'Unknown format')
    
    def _record_detection(self, filename: str, format_name: str, extension: str):
        """Record format detection operation"""
        try:
            detection_record = {
                'timestamp': pd.Timestamp.now(),
                'filename': filename,
                'detected_format': format_name,
                'extension': extension,
                'success': format_name != "Unknown"
            }
            
            self.detection_history.append(detection_record)
            
        except Exception as e:
            logger.error(f"Failed to record detection: {e}")
    
    def get_detection_history(self) -> List[Dict]:
        """Get format detection history"""
        return self.detection_history.copy()
    
    def get_detection_statistics(self) -> Dict[str, Any]:
        """Get format detection statistics"""
        try:
            if not self.detection_history:
                return {'total_detections': 0}
            
            total_detections = len(self.detection_history)
            successful_detections = sum(1 for d in self.detection_history if d['success'])
            failed_detections = total_detections - successful_detections
            
            # Count by format
            format_counts = {}
            for detection in self.detection_history:
                format_name = detection['detected_format']
                format_counts[format_name] = format_counts.get(format_name, 0) + 1
            
            # Count by extension
            extension_counts = {}
            for detection in self.detection_history:
                ext = detection['extension']
                extension_counts[ext] = extension_counts.get(ext, 0) + 1
            
            return {
                'total_detections': total_detections,
                'successful_detections': successful_detections,
                'failed_detections': failed_detections,
                'success_rate': (successful_detections / total_detections * 100) if total_detections > 0 else 0,
                'format_distribution': format_counts,
                'extension_distribution': extension_counts,
                'last_detection': self.detection_history[-1]['timestamp'] if self.detection_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get detection statistics: {e}")
            return {}
    
    def clear_detection_history(self) -> int:
        """Clear detection history and return count"""
        try:
            count = len(self.detection_history)
            self.detection_history.clear()
            logger.info(f"🗑️ Cleared {count} detection records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear detection history: {e}")
            return 0
