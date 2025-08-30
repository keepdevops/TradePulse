"""
Database Interface
Provides a unified interface for database interactions.
"""

import sqlite3
import duckdb
import psycopg2
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
from .database_implementations import DatabaseImplementations
from .database_connections import DatabaseConnections
from .table_manager import TableManager

logger = setup_logger(__name__)


class Database:
    """
    Database interface for TradePulse.
    
    Supports multiple database types:
    - SQLite: Local storage
    - PostgreSQL: Remote storage
    - DuckDB: Redline historical data
    """
    
    def __init__(self, config: Optional[ConfigLoader] = None):
        """
        Initialize the database interface.
        
        Args:
            config: Configuration loader instance
        """
        if config is None:
            config = ConfigLoader()
        
        self.config = config
        self.db_type = config.get('database.type', 'duckdb')
        self.connections: Dict[str, Any] = {}
        
        # Database implementations and connections
        self.implementations = DatabaseImplementations(config)
        self.connection_manager = DatabaseConnections(config)
        self.table_manager = TableManager(self)
        
        # Initialize database connections
        self._init_connections()
    
    def _init_connections(self) -> None:
        """Initialize database connections based on configuration."""
        try:
            self.connections = self.connection_manager.init_connections(self.db_type)
            logger.info(f"Database connections initialized for {self.db_type}")
                
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            # Fallback to SQLite
            self.db_type = 'sqlite'
            self.connections = self.connection_manager.init_connections('sqlite')
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a DataFrame.
        
        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
        
        Returns:
            Query results as pandas DataFrame
        """
        try:
            if self.db_type == 'duckdb':
                return self.implementations.execute_duckdb_query(self.connections['duckdb'], query, params)
            elif self.db_type == 'postgresql':
                return self.implementations.execute_postgresql_query(self.connections['postgresql'], query, params)
            elif self.db_type == 'sqlite':
                return self.implementations.execute_sqlite_query(self.connections['sqlite'], query, params)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def insert_data(self, table_name: str, data: pd.DataFrame, if_exists: str = 'append') -> bool:
        """
        Insert data into a table.
        
        Args:
            table_name: Target table name
            data: Data to insert
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
        
        Returns:
            True if insertion was successful
        """
        try:
            if self.db_type == 'duckdb':
                return self.implementations.insert_duckdb_data(self.connections['duckdb'], table_name, data, if_exists)
            elif self.db_type == 'postgresql':
                return self.implementations.insert_postgresql_data(self.connections['postgresql'], table_name, data, if_exists)
            elif self.db_type == 'sqlite':
                return self.implementations.insert_sqlite_data(self.connections['sqlite'], table_name, data, if_exists)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                
        except Exception as e:
            logger.error(f"Data insertion failed: {e}")
            return False
    
    def create_table(self, table_name: str, schema: Dict[str, str]) -> bool:
        """Create a new table with specified schema."""
        return self.table_manager.create_table(table_name, schema)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        return self.table_manager.table_exists(table_name)
    
    def get_table_info(self, table_name: str) -> Optional[pd.DataFrame]:
        """Get information about a table's structure."""
        return self.table_manager.get_table_info(table_name)
    
    def close(self) -> None:
        """Close all database connections."""
        try:
            self.connection_manager.close_connections(self.connections)
            self.connections.clear()
            logger.info("Database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience functions for quick database operations
def quick_query(query: str, db_type: str = 'duckdb', **kwargs) -> pd.DataFrame:
    """
    Quick function to execute a database query.
    
    Args:
        query: SQL query string
        db_type: Database type to use
        **kwargs: Additional database configuration
    
    Returns:
        Query results as pandas DataFrame
    """
    with Database() as db:
        return db.execute_query(query)


def quick_insert(table_name: str, data: pd.DataFrame, db_type: str = 'duckdb', **kwargs) -> bool:
    """
    Quick function to insert data into a table.
    
    Args:
        table_name: Target table name
        data: Data to insert
        db_type: Database type to use
        **kwargs: Additional database configuration
    
    Returns:
        True if insertion was successful
    """
    with Database() as db:
        return db.insert_data(table_name, data)
