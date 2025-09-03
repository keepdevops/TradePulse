#!/usr/bin/env python3
"""
TradePulse Session Storage
Main session storage module - coordinates session operations
"""

import logging
from typing import Optional, List
from .session_core import Session
from .session_db_ops import SessionDatabaseOperations
from .session_query_ops import SessionQueryOperations
from .session_maintenance_ops import SessionMaintenanceOperations

logger = logging.getLogger(__name__)

class SessionStorage:
    """Main session storage coordinator"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db_ops = SessionDatabaseOperations(db_path)
        self.query_ops = SessionQueryOperations(db_path)
        self.maintenance_ops = SessionMaintenanceOperations(db_path)
    
    def init_database(self):
        """Initialize session database tables"""
        self.db_ops.init_database()
    
    def store_session(self, session: Session) -> bool:
        """Store session in database"""
        return self.db_ops.store_session(session)
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity in database"""
        return self.db_ops.update_session_activity(session_id)
    
    def update_session_expiry(self, session_id: str, expires_at) -> bool:
        """Update session expiry time in database"""
        return self.db_ops.update_session_expiry(session_id, expires_at)
    
    def invalidate_session_db(self, session_id: str) -> bool:
        """Mark session as inactive in database"""
        return self.db_ops.invalidate_session_db(session_id)
    
    def get_session_from_db(self, session_id: str) -> Optional[Session]:
        """Retrieve session from database"""
        return self.query_ops.get_session_from_db(session_id)
    
    def get_user_session_count(self, user_id: int) -> int:
        """Get the number of active sessions for a user"""
        return self.query_ops.get_user_session_count(user_id)
    
    def get_user_sessions(self, user_id: int) -> List[Session]:
        """Get all active sessions for a user"""
        return self.query_ops.get_user_sessions(user_id)
    
    def get_expired_sessions(self) -> List[Session]:
        """Get all expired sessions"""
        return self.query_ops.get_expired_sessions()
    
    def get_total_session_count(self) -> int:
        """Get total number of sessions"""
        return self.maintenance_ops.get_total_session_count()
    
    def get_active_session_count(self) -> int:
        """Get number of active sessions"""
        return self.maintenance_ops.get_active_session_count()
    
    def get_expired_session_count(self) -> int:
        """Get number of expired sessions"""
        return self.maintenance_ops.get_expired_session_count()
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        return self.maintenance_ops.cleanup_expired_sessions()
    
    def get_session_statistics(self) -> dict:
        """Get comprehensive session statistics"""
        return self.maintenance_ops.get_session_statistics()
