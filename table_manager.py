"""
Table Manager
Handles table operations for the database interface.
"""

import pandas as pd
from typing import Dict, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TableManager:
    """Manages table operations for the database interface."""
    
    def __init__(self, database):
        """Initialize the table manager."""
        self.database = database
    
    def create_table(self, table_name: str, schema: Dict[str, str]) -> bool:
        """
        Create a new table with specified schema.
        
        Args:
            table_name: Name of the table to create
            schema: Dictionary mapping column names to SQL types
        
        Returns:
            True if table creation was successful
        """
        try:
            # Build CREATE TABLE statement
            columns = [f"{col} {dtype}" for col, dtype in schema.items()]
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            
            # Execute creation
            self.database.execute_query(create_sql)
            logger.info(f"Table '{table_name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Table creation failed: {e}")
            return False
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists.
        
        Args:
            table_name: Name of the table to check
        
        Returns:
            True if table exists
        """
        try:
            if self.database.db_type == 'duckdb':
                result = self.database.execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=:name",
                    {'name': table_name}
                )
            elif self.database.db_type == 'postgresql':
                result = self.database.execute_query(
                    "SELECT table_name FROM information_schema.tables WHERE table_name = :name",
                    {'name': table_name}
                )
            elif self.database.db_type == 'sqlite':
                result = self.database.execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=:name",
                    {'name': table_name}
                )
            else:
                return False
            
            return len(result) > 0
            
        except Exception as e:
            logger.error(f"Table existence check failed: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> Optional[pd.DataFrame]:
        """
        Get information about a table's structure.
        
        Args:
            table_name: Name of the table
        Returns:
            DataFrame with column information or None if table doesn't exist
        """
        try:
            if not self.table_exists(table_name):
                return None
            
            if self.database.db_type == 'duckdb':
                return self.database.execute_query(f"DESCRIBE {table_name}")
            elif self.database.db_type == 'postgresql':
                return self.database.execute_query(
                    "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = :name",
                    {'name': table_name}
                )
            elif self.database.db_type == 'sqlite':
                return self.database.execute_query(f"PRAGMA table_info({table_name})")
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return None
