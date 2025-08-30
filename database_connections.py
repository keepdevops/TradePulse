"""
Database Connections
Contains methods for managing database connections.
"""

import sqlite3
import duckdb
import psycopg2
from pathlib import Path
from typing import Any, Dict
from sqlalchemy import create_engine
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader

logger = setup_logger(__name__)


class DatabaseConnections:
    """
    Class for managing database connections.
    
    This class contains the connection management methods that were extracted
    from Database to keep files under 250 lines.
    """
    
    def __init__(self, config: ConfigLoader):
        """Initialize the database connections manager."""
        self.config = config
    
    def init_connections(self, db_type: str) -> Dict[str, Any]:
        """
        Initialize database connections based on type.
        
        Args:
            db_type: Type of database to initialize
        
        Returns:
            Dictionary of database connections
        """
        connections = {}
        
        try:
            if db_type == 'duckdb':
                # Try DuckDB with retry mechanism
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        connections['duckdb'] = self._init_duckdb()
                        break
                    except Exception as duckdb_error:
                        if attempt < max_retries - 1:
                            logger.warning(f"DuckDB attempt {attempt + 1} failed: {duckdb_error}. Retrying...")
                            self.force_close_duckdb()
                            import time
                            time.sleep(1)  # Wait before retry
                        else:
                            logger.error(f"All DuckDB attempts failed: {duckdb_error}")
                            raise
            elif db_type == 'postgresql':
                connections['postgresql'] = self._init_postgresql()
            elif db_type == 'sqlite':
                connections['sqlite'] = self._init_sqlite()
            else:
                logger.warning(f"Unsupported database type: {db_type}")
                connections['duckdb'] = self._init_duckdb()  # Fallback to DuckDB
                
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            # Fallback to SQLite
            connections['sqlite'] = self._init_sqlite()
        
        return connections
    
    def _init_duckdb(self) -> Any:
        """Initialize DuckDB connection for Redline data."""
        try:
            db_path = self.config.get('database.path', './data/redline_data.duckdb')
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Force close any existing connections and clean up lock files
            self.force_close_duckdb()
            
            connection = duckdb.connect(db_path)
            logger.info(f"DuckDB connection established: {db_path}")
            return connection
            
        except Exception as e:
            logger.error(f"Failed to initialize DuckDB: {e}")
            # Try to clean up any remaining lock files
            try:
                db_path = self.config.get('database.path', './data/redline_data.duckdb')
                lock_files = [f"{db_path}.lock", f"{db_path}.wal", f"{db_path}.shm"]
                for lock_file in lock_files:
                    if Path(lock_file).exists():
                        Path(lock_file).unlink()
                        logger.info(f"Cleaned up lock file after error: {lock_file}")
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up lock files after error: {cleanup_error}")
            raise
    
    def _init_postgresql(self) -> Any:
        """Initialize PostgreSQL connection."""
        try:
            pg_config = self.config.get('database.postgresql', {})
            
            connection_string = (
                f"postgresql://{pg_config.get('username', 'tradepulse_user')}:"
                f"{pg_config.get('password', '')}@"
                f"{pg_config.get('host', 'localhost')}:"
                f"{pg_config.get('port', 5432)}/"
                f"{pg_config.get('database', 'tradepulse')}"
            )
            
            # Test connection
            conn = psycopg2.connect(connection_string)
            conn.close()
            
            # Create SQLAlchemy engine
            engine = create_engine(connection_string)
            logger.info("PostgreSQL connection established")
            return engine
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            raise
    
    def _init_sqlite(self) -> Any:
        """Initialize SQLite connection."""
        try:
            db_path = self.config.get('database.sqlite_path', './data/stock_data.db')
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            
            connection = sqlite3.connect(db_path)
            logger.info(f"SQLite connection established: {db_path}")
            return connection
            
        except Exception as e:
            logger.error(f"Failed to initialize SQLite: {e}")
            raise
    
    def close_connections(self, connections: Dict[str, Any]) -> None:
        """
        Close all database connections.
        
        Args:
            connections: Dictionary of database connections to close
        """
        try:
            for db_type, connection in connections.items():
                if hasattr(connection, 'close'):
                    connection.close()
                elif hasattr(connection, 'dispose'):
                    connection.dispose()
            
            logger.info("Database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    def force_close_duckdb(self) -> None:
        """Force close any existing DuckDB connections and clean up lock files."""
        try:
            import duckdb
            # Force close any existing connections
            duckdb.connect(':memory:').close()
            
            # Clean up lock files
            db_path = self.config.get('database.path', './data/redline_data.duckdb')
            lock_files = [f"{db_path}.lock", f"{db_path}.wal", f"{db_path}.shm"]
            for lock_file in lock_files:
                if Path(lock_file).exists():
                    try:
                        Path(lock_file).unlink()
                        logger.info(f"Force cleaned up lock file: {lock_file}")
                    except Exception as cleanup_error:
                        logger.warning(f"Could not force clean up lock file {lock_file}: {cleanup_error}")
                        
        except Exception as e:
            logger.warning(f"Error in force close DuckDB: {e}")
