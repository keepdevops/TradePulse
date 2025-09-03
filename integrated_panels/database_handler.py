#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Database Handler
Handles database operations
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Handles database operations"""
    
    def __init__(self, database):
        self.database = database
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute database query"""
        try:
            if self.database and hasattr(self.database, 'execute_query'):
                return self.database.execute_query(query)
            else:
                logger.warning("Database not available")
                return []
                
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            return []
    
    def store_data(self, table: str, data: Dict[str, Any]) -> bool:
        """Store data in database"""
        try:
            if self.database and hasattr(self.database, 'store_data'):
                return self.database.store_data(table, data)
            else:
                logger.warning("Database not available")
                return False
                
        except Exception as e:
            logger.error(f"Failed to store data: {e}")
            return False
