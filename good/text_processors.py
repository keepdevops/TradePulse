#!/usr/bin/env python3
"""
TradePulse Data Upload - Text Processors
Handles text format processing (CSV, JSON)
"""

import pandas as pd
from typing import Dict, Any, Tuple
import logging
import io
import json

logger = logging.getLogger(__name__)

class TextProcessors:
    """Handles text format processing (CSV, JSON)"""
    
    @staticmethod
    def process_csv(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process CSV format file"""
        try:
            # Try to decode content
            try:
                content_str = file_content.decode('utf-8')
            except UnicodeDecodeError:
                content_str = file_content.decode('latin-1')
            
            # Read CSV from string
            data = pd.read_csv(io.StringIO(content_str))
            
            metadata = {
                'format': 'csv',
                'filename': filename,
                'shape': data.shape,
                'columns': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'encoding': 'utf-8' if file_content.decode('utf-8', errors='ignore') == content_str else 'latin-1'
            }
            
            return data, metadata
            
        except Exception as e:
            logger.error(f"Failed to process CSV file: {e}")
            raise
    
    @staticmethod
    def process_json(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process JSON format file"""
        try:
            # Decode content
            content_str = file_content.decode('utf-8')
            
            # Parse JSON
            json_data = json.loads(content_str)
            
            # Convert to DataFrame
            if isinstance(json_data, list):
                data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # If it's a dict with nested data, try to find the main data
                if 'data' in json_data:
                    data = pd.DataFrame(json_data['data'])
                elif 'results' in json_data:
                    data = pd.DataFrame(json_data['results'])
                else:
                    # Flatten the dict
                    data = pd.json_normalize(json_data)
            else:
                raise ValueError("Unsupported JSON structure")
            
            metadata = {
                'format': 'json',
                'filename': filename,
                'shape': data.shape,
                'columns': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'json_structure': type(json_data).__name__
            }
            
            return data, metadata
            
        except Exception as e:
            logger.error(f"Failed to process JSON file: {e}")
            raise
