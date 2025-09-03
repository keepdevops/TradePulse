#!/usr/bin/env python3
"""
TradePulse User Activity Core Operations
Core user activity logging and retrieval operations
"""

import logging
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UserActivityCore:
    """Core user activity operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def log_activity(self, user_id: int, activity_type: str, 
                     description: str = None, metadata: Dict = None, 
                     ip_address: str = None, user_agent: str = None) -> bool:
        """Log user activity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO user_activity_logs (
                        user_id, activity_type, description, metadata,
                        ip_address, user_agent, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    activity_type,
                    description,
                    str(metadata) if metadata else None,
                    ip_address,
                    user_agent,
                    datetime.now()
                ))
                
                conn.commit()
                logger.debug(f"Activity logged for user {user_id}: {activity_type}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to log activity for user {user_id}: {e}")
            return False
    
    def get_user_activity(self, user_id: int, limit: int = 100, 
                          activity_type: str = None, 
                          start_date: datetime = None, 
                          end_date: datetime = None) -> Optional[List[Dict]]:
        """Get user activity logs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT id, activity_type, description, metadata,
                           ip_address, user_agent, timestamp
                    FROM user_activity_logs
                    WHERE user_id = ?
                """
                params = [user_id]
                
                if activity_type:
                    query += " AND activity_type = ?"
                    params.append(activity_type)
                
                if start_date:
                    query += " AND timestamp >= ?"
                    params.append(start_date)
                
                if end_date:
                    query += " AND timestamp <= ?"
                    params.append(end_date)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                activities = []
                for row in rows:
                    activity = {
                        "id": row[0],
                        "activity_type": row[1],
                        "description": row[2],
                        "metadata": row[3],
                        "ip_address": row[4],
                        "user_agent": row[5],
                        "timestamp": row[6]
                    }
                    activities.append(activity)
                
                return activities
                
        except Exception as e:
            logger.error(f"Failed to get activity for user {user_id}: {e}")
            return None
