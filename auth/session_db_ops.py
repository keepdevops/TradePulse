#!/usr/bin/env python3
"""
TradePulse Session Database Operations
Core database operations for session management
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional
from .session_core import Session

logger = logging.getLogger(__name__)

class SessionDatabaseOperations:
    """Core database operations for session management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def init_database(self):
        """Initialize session database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create user_sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        session_id TEXT PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expiry_time TIMESTAMP NOT NULL,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        user_agent TEXT,
                        is_active INTEGER DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
                logger.info("Session database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize session database: {e}")
            raise
    
    def store_session(self, session: Session) -> bool:
        """Store session in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_sessions 
                    (session_id, user_id, created_at, expiry_time, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    session.user_id,
                    session.created_at.isoformat(),
                    session.expires_at.isoformat(),
                    session.ip_address,
                    session.user_agent
                ))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to store session in database: {e}")
            return False
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_sessions 
                    SET last_activity = ? 
                    WHERE session_id = ?
                """, (datetime.now().isoformat(), session_id))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to update session activity in database: {e}")
            return False
    
    def update_session_expiry(self, session_id: str, expires_at: datetime) -> bool:
        """Update session expiry time in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_sessions 
                    SET expiry_time = ? 
                    WHERE session_id = ?
                """, (expires_at.isoformat(), session_id))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to update session expiry in database: {e}")
            return False
    
    def invalidate_session_db(self, session_id: str) -> bool:
        """Mark session as inactive in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_sessions 
                    SET is_active = 0 
                    WHERE session_id = ?
                """, (session_id,))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to invalidate session in database: {e}")
            return False
