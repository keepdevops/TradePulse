#!/usr/bin/env python3
"""
TradePulse Data Upload - Text Loaders
Handles text format loading (CSV, JSON)
"""

import pandas as pd
from typing import Dict, Any
import logging
import io
import json

logger = logging.getLogger(__name__)

class TextLoaders:
    """Handles text format loading (CSV, JSON)"""
    
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
    
    @staticmethod
    def load_json_file(file_content: bytes) -> pd.DataFrame:
        """Load JSON format file"""
        try:
            # Try to decode and parse JSON
            content_str = file_content.decode('utf-8')
            data = pd.read_json(content_str)
            
            # Handle different JSON structures
            if isinstance(data, pd.DataFrame):
                return data
            elif isinstance(data, dict):
                # Try to find DataFrame-like data
                for key, value in data.items():
                    if isinstance(value, pd.DataFrame):
                        return value
                    elif isinstance(value, list) and len(value) > 0:
                        return pd.DataFrame(value)
                
                # If no DataFrame found, convert the whole dict
                return pd.DataFrame([data])
            else:
                return pd.DataFrame(data)
        except Exception as e:
            raise Exception(f"Failed to load JSON file: {e}")
