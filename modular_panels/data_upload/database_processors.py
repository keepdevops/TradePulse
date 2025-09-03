#!/usr/bin/env python3
"""
TradePulse Data Upload - Database Processors
Handles database format processing (DuckDB, SQLite)
"""

import pandas as pd
import sqlite3
import duckdb
from typing import Dict, Any, Tuple
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

class DatabaseProcessors:
    """Handles database format processing (DuckDB, SQLite)"""
    
    @staticmethod
    def process_duckdb(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process DuckDB format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Connect to DuckDB and read data
                con = duckdb.connect(temp_file_path)
                
                # Get table names
                tables = con.execute("SHOW TABLES").fetchall()
                if not tables:
                    raise ValueError("No tables found in DuckDB file")
                
                # Read first table
                table_name = tables[0][0]
                data = con.execute(f"SELECT * FROM {table_name}").fetchdf()
                
                metadata = {
                    'format': 'duckdb',
                    'filename': filename,
                    'table_name': table_name,
                    'tables': [t[0] for t in tables],
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.to_dict()
                }
                
                con.close()
                return data, metadata
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to process DuckDB file: {e}")
            raise
    
    @staticmethod
    def process_sqlite(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process SQLite format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Connect to SQLite and read data
                con = sqlite3.connect(temp_file_path)
                
                # Get table names
                cursor = con.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                if not tables:
                    raise ValueError("No tables found in SQLite file")
                
                # Read first table
                table_name = tables[0][0]
                data = pd.read_sql_query(f"SELECT * FROM {table_name}", con)
                
                metadata = {
                    'format': 'sqlite',
                    'filename': filename,
                    'table_name': table_name,
                    'tables': [t[0] for t in tables],
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.to_dict()
                }
                
                con.close()
                return data, metadata
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Failed to process SQLite file: {e}")
            raise
