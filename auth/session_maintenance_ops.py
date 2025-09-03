#!/usr/bin/env python3
"""
TradePulse Session Maintenance Operations
Maintenance and statistics operations for session management
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)

class SessionMaintenanceOperations:
    """Maintenance and statistics operations for session management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_total_session_count(self) -> int:
        """Get total number of sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM user_sessions")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get total session count: {e}")
            return 0
    
    def get_active_session_count(self) -> int:
        """Get number of active sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE is_active = 1")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get active session count: {e}")
            return 0
    
    def get_expired_session_count(self) -> int:
        """Get number of expired sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE expiry_time < datetime('now') AND is_active = 1
                """)
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get expired session count: {e}")
            return 0
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_sessions 
                    SET is_active = 0 
                    WHERE expiry_time < datetime('now') AND is_active = 1
                """)
                
                cleaned_count = cursor.rowcount
                conn.commit()
                
                if cleaned_count > 0:
                    logger.info(f"Cleaned up {cleaned_count} expired sessions")
                
                return cleaned_count
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
    
    def get_session_statistics(self) -> dict:
        """Get comprehensive session statistics"""
        try:
            total = self.get_total_session_count()
            active = self.get_active_session_count()
            expired = self.get_expired_session_count()
            
            return {
                "total_sessions": total,
                "active_sessions": active,
                "expired_sessions": expired,
                "inactive_sessions": total - active
            }
            
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            return {}
