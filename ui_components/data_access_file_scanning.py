#!/usr/bin/env python3
"""
TradePulse Data Access - File Scanning
File scanning and discovery functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
import os
import glob
from pathlib import Path

logger = logging.getLogger(__name__)

class DataAccessFileScanning:
    """File scanning functionality for data access"""
    
    def __init__(self, file_ops):
        self.file_ops = file_ops
    
    def _scan_for_data_files(self) -> List[str]:
        """Scan for data files in common locations"""
        try:
            data_files = []
            
            # Common locations to scan
            common_locations = [
                str(Path.home() / "Downloads"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop"),
                str(Path.home() / "Data"),
                str(Path.home() / "Trading"),
                str(Path.home() / "Stocks"),
                "/Users/*/Downloads",
                "/Users/*/Documents",
                "/Users/*/Desktop",
            ]
            
            # Common data file extensions
            extensions = ["*.csv", "*.json", "*.feather", "*.parquet", "*.duckdb", "*.h5", "*.hdf5"]
            
            for location in common_locations:
                if os.path.exists(location):
                    for ext in extensions:
                        try:
                            pattern = os.path.join(location, ext)
                            files = glob.glob(pattern)
                            data_files.extend(files)
                        except Exception as e:
                            logger.debug(f"⚠️ Error scanning {location} for {ext}: {e}")
                            continue
            
            # Remove duplicates and limit results
            data_files = list(set(data_files))[:20]  # Limit to 20 files
            
            logger.info(f"🔍 Found {len(data_files)} potential data files")
            return data_files
            
        except Exception as e:
            logger.error(f"❌ Failed to scan for data files: {e}")
            return []
    
    def get_available_data_files(self) -> Dict[str, List[str]]:
        """Get list of available data files by type"""
        try:
            file_types = {
                'csv': [],
                'json': [],
                'feather': [],
                'parquet': [],
                'duckdb': [],
                'keras': []
            }
            
            # Scan directories
            scan_directories = [
                "uploads/",
                "upload_data/",
                "redline_data/",
                "data/",
                "model_training_data/",
                str(Path.home() / "Downloads"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop"),
            ]
            
            for directory in scan_directories:
                if not os.path.exists(directory):
                    continue
                    
                for file_type, extensions in {
                    'csv': ['*.csv'],
                    'json': ['*.json'],
                    'feather': ['*.feather'],
                    'parquet': ['*.parquet'],
                    'duckdb': ['*.duckdb'],
                    'keras': ['*.h5', '*.hdf5']
                }.items():
                    for ext in extensions:
                        pattern = os.path.join(directory, ext)
                        files = glob.glob(pattern)
                        file_types[file_type].extend(files)
            
            # Remove duplicates
            for file_type in file_types:
                file_types[file_type] = list(set(file_types[file_type]))
            
            logger.info(f"📁 Found data files: {sum(len(files) for files in file_types.values())} total")
            return file_types
            
        except Exception as e:
            logger.error(f"❌ Failed to get available data files: {e}")
            return {}
    
    def get_scan_directories(self) -> List[str]:
        """Get list of directories to scan for data files"""
        return [
            "uploads/",
            "upload_data/",
            "redline_data/",
            "data/",
            "model_training_data/",
            str(Path.home() / "Downloads"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Desktop"),
        ]
    
    def get_file_patterns(self) -> Dict[str, List[str]]:
        """Get file patterns for different formats"""
        return {
            'csv': ["*.csv", "*_data.csv", "data_*.csv"],
            'json': ["*.json", "*_data.json", "data_*.json"],
            'feather': ["*.feather", "*_data.feather"],
            'parquet': ["*.parquet", "*_data.parquet"],
            'duckdb': ["*.duckdb", "*_data.duckdb"],
            'keras': ["*.h5", "*_data.h5", "*.hdf5"]
        }
