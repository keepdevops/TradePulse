#!/usr/bin/env python3
"""
TradePulse Session Query Operations
Query and retrieval operations for session management
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional, List
from .session_core import Session

logger = logging.getLogger(__name__)

class SessionQueryOperations:
    """Query and retrieval operations for session management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_session_from_db(self, session_id: str) -> Optional[Session]:
        """Retrieve session from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, user_id, created_at, expiry_time, 
                           last_activity, ip_address, user_agent, is_active
                    FROM user_sessions 
                    WHERE session_id = ?
                """, (session_id,))
                
                row = cursor.fetchone()
                if row:
                    return Session(
                        session_id=row[0],
                        user_id=row[1],
                        created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                        expiry_time=datetime.fromisoformat(row[3]) if row[3] else None,
                        last_activity=datetime.fromisoformat(row[4]) if row[4] else None,
                        ip_address=row[5],
                        user_agent=row[6],
                        is_active=bool(row[7])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve session from database: {e}")
            return None
    
    def get_user_session_count(self, user_id: int) -> int:
        """Get the number of active sessions for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE user_id = ? AND is_active = 1
                """, (user_id,))
                
                return cursor.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Failed to get session count for user {user_id}: {e}")
            return 0
    
    def get_user_sessions(self, user_id: int) -> List[Session]:
        """Get all active sessions for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, user_id, created_at, expiry_time, 
                           last_activity, ip_address, user_agent, is_active
                    FROM user_sessions 
                    WHERE user_id = ? AND is_active = 1
                """, (user_id,))
                
                sessions = []
                for row in cursor.fetchall():
                    session = Session(
                        session_id=row[0],
                        user_id=row[1],
                        created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                        expiry_time=datetime.fromisoformat(row[3]) if row[3] else None,
                        last_activity=datetime.fromisoformat(row[4]) if row[4] else None,
                        ip_address=row[5],
                        user_agent=row[6],
                        is_active=bool(row[7])
                    )
                    sessions.append(session)
                
                return sessions
                
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {e}")
            return []
    
    def get_expired_sessions(self) -> List[Session]:
        """Get all expired sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, user_id, created_at, expiry_time, 
                           last_activity, ip_address, user_agent, is_active
                    FROM user_sessions 
                    WHERE expiry_time < datetime('now') AND is_active = 1
                """)
                
                sessions = []
                for row in cursor.fetchall():
                    session = Session(
                        session_id=row[0],
                        user_id=row[1],
                        created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                        expiry_time=datetime.fromisoformat(row[3]) if row[3] else None,
                        last_activity=datetime.fromisoformat(row[4]) if row[4] else None,
                        ip_address=row[5],
                        user_agent=row[6],
                        is_active=bool(row[7])
                    )
                    sessions.append(session)
                
                return sessions
                
        except Exception as e:
            logger.error(f"Failed to get expired sessions: {e}")
            return []
