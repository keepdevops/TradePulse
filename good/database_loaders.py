#!/usr/bin/env python3
"""
TradePulse Data Upload - Database Loaders
Handles database file loading (DuckDB, SQLite)
"""

import pandas as pd
import sqlite3
import duckdb
from typing import Dict, Any
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

class DatabaseLoaders:
    """Handles database file loading (DuckDB, SQLite)"""
    
    @staticmethod
    def load_duckdb_file(file_content: bytes, filename: str) -> pd.DataFrame:
        """Load DuckDB format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Connect to DuckDB and read
                con = duckdb.connect(tmp_file.name)
                
                # Get table names
                tables = con.execute("SHOW TABLES").fetchall()
                if not tables:
                    raise Exception("No tables found in DuckDB file")
                
                # Read first table (you could add UI to select specific table)
                table_name = tables[0][0]
                df = con.execute(f"SELECT * FROM {table_name}").fetchdf()
                
                con.close()
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return df
        except Exception as e:
            raise Exception(f"Failed to load DuckDB file: {e}")
    
    @staticmethod
    def load_sqlite_file(file_content: bytes, filename: str) -> pd.DataFrame:
        """Load SQLite format file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Connect to SQLite and read
                con = sqlite3.connect(tmp_file.name)
                
                # Get table names
                cursor = con.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                if not tables:
                    raise Exception("No tables found in SQLite file")
                
                # Read first table (you could add UI to select specific table)
                table_name = tables[0][0]
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)
                
                con.close()
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return df
        except Exception as e:
            raise Exception(f"Failed to load SQLite file: {e}")
