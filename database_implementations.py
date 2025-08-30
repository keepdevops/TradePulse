"""
Database Implementations
Contains the implementation logic for different database types.
"""

import pandas as pd
from typing import Any, Dict, Optional, Union
from sqlalchemy.engine import Engine

from utils.logger import LoggerMixin


class DatabaseImplementations(LoggerMixin):
    """
    Implementation class for different database types.
    
    This class contains all the database-specific logic that was moved
    from the main Database class to keep files under 400 lines.
    """
    
    def __init__(self, config):
        """Initialize the database implementations."""
        super().__init__()
        self.config = config
        self.log_info("Database Implementations initialized")
    
    def execute_duckdb_query(self, conn, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute query on DuckDB."""
        try:
            if params:
                # Handle parameter substitution for DuckDB
                for key, value in params.items():
                    if isinstance(value, str):
                        query = query.replace(f":{key}", f"'{value}'")
                    else:
                        query = query.replace(f":{key}", str(value))
            
            result = conn.execute(query)
            return result.df()
            
        except Exception as e:
            self.log_error(f"Error executing DuckDB query: {e}")
            raise
    
    def execute_postgresql_query(self, engine: Engine, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute query on PostgreSQL."""
        try:
            from sqlalchemy import text
            
            with engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                
                return pd.DataFrame(result.fetchall(), columns=result.keys())
                
        except Exception as e:
            self.log_error(f"Error executing PostgreSQL query: {e}")
            raise
    
    def execute_sqlite_query(self, conn, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute query on SQLite."""
        try:
            if params:
                result = pd.read_sql_query(query, conn, params=params)
            else:
                result = pd.read_sql_query(query, conn)
            
            return result
            
        except Exception as e:
            self.log_error(f"Error executing SQLite query: {e}")
            raise
    
    def insert_duckdb_data(self, conn, table_name: str, data: pd.DataFrame, if_exists: str) -> bool:
        """Insert data into DuckDB table."""
        try:
            if if_exists == 'replace':
                conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data")
            return True
            
        except Exception as e:
            self.log_error(f"Error inserting data into DuckDB: {e}")
            return False
    
    def insert_postgresql_data(self, engine: Engine, table_name: str, data: pd.DataFrame, if_exists: str) -> bool:
        """Insert data into PostgreSQL table."""
        try:
            data.to_sql(
                table_name, 
                engine, 
                if_exists=if_exists, 
                index=False,
                method='multi'
            )
            return True
            
        except Exception as e:
            self.log_error(f"Error inserting data into PostgreSQL: {e}")
            return False
    
    def insert_sqlite_data(self, conn, table_name: str, data: pd.DataFrame, if_exists: str) -> bool:
        """Insert data into SQLite table."""
        try:
            data.to_sql(
                table_name, 
                conn, 
                if_exists=if_exists, 
                index=False
            )
            return True
            
        except Exception as e:
            self.log_error(f"Error inserting data into SQLite: {e}")
            return False
