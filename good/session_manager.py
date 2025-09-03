#!/usr/bin/env python3
"""
TradePulse Session Manager
Manages user sessions with validation and security
"""

import logging
from typing import Optional, Dict, List
from .session_core import SessionCore, Session
from .session_storage import SessionStorage
from .session_validation import SessionValidation

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages user sessions"""
    
    def __init__(self, db_path: str = "tradepulse_auth.db"):
        """Initialize session manager"""
        self.db_path = db_path
        self.core = SessionCore()
        self.storage = SessionStorage(db_path)
        self.validator = SessionValidation()
    
    def init_database(self):
        """Initialize session database"""
        try:
            self.storage.init_database()
            logger.info("Session database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize session database: {e}")
            raise
    
    def create_session(self, user_id: int, ip_address: str = None, 
                      user_agent: str = None) -> Optional[str]:
        """Create a new session for a user"""
        try:
            # Check session limits
            current_sessions = self.storage.get_user_session_count(user_id)
            is_valid, message = self.validator.validate_session_limits(user_id, current_sessions)
            if not is_valid:
                logger.warning(f"Session limit exceeded for user {user_id}: {message}")
                return None
            
            # Create session object
            session = self.core.create_session_object(
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Store session in database
            session_id = self.storage.store_session(session)
            if session_id:
                logger.info(f"Session created for user {user_id}")
                return session_id
            else:
                logger.error(f"Failed to store session for user {user_id}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create session for user {user_id}: {e}")
            return None
    
    def validate_session(self, session_id: str, ip_address: str = None) -> Optional[int]:
        """Validate a session and return user ID if valid"""
        try:
            # Get session from database
            session = self.storage.get_session_from_db(session_id)
            if not session:
                return None
            
            # Validate session security
            is_valid, message = self.validator.validate_session_security(
                session, ip_address
            )
            if not is_valid:
                logger.warning(f"Session validation failed for {session_id}: {message}")
                return None
            
            # Update session activity
            self.storage.update_session_activity(session_id)
            
            return session.user_id
            
        except Exception as e:
            logger.error(f"Session validation failed for {session_id}: {e}")
            return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session"""
        try:
            success = self.storage.invalidate_session_db(session_id)
            if success:
                logger.info(f"Session {session_id} invalidated")
            return success
        except Exception as e:
            logger.error(f"Failed to invalidate session {session_id}: {e}")
            return False
    
    def extend_session(self, session_id: str, hours: int = 24) -> bool:
        """Extend session expiry time"""
        try:
            success = self.storage.update_session_expiry(session_id, hours)
            if success:
                logger.info(f"Session {session_id} extended by {hours} hours")
            return success
        except Exception as e:
            logger.error(f"Failed to extend session {session_id}: {e}")
            return False
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get session information"""
        try:
            session = self.storage.get_session_from_db(session_id)
            if not session:
                return None
            
            return {
                "session_id": session.session_id,
                "user_id": session.user_id,
                "created_at": session.created_at.isoformat() if session.created_at else None,
                "expiry_time": session.expiry_time.isoformat() if session.expiry_time else None,
                "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                "ip_address": session.ip_address,
                "user_agent": session.user_agent,
                "is_active": session.is_active
            }
        except Exception as e:
            logger.error(f"Failed to get session info for {session_id}: {e}")
            return None
    
    def get_user_sessions(self, user_id: int) -> List[Dict]:
        """Get all active sessions for a user"""
        try:
            sessions = self.storage.get_user_sessions(user_id)
            session_list = []
            
            for session in sessions:
                session_info = {
                    "session_id": session.session_id,
                    "created_at": session.created_at.isoformat() if session.created_at else None,
                    "expiry_time": session.expiry_time.isoformat() if session.expiry_time else None,
                    "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                    "ip_address": session.ip_address,
                    "user_agent": session.user_agent
                }
                session_list.append(session_info)
            
            return session_list
            
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {e}")
            return []
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        try:
            expired_sessions = self.storage.get_expired_sessions()
            cleaned_count = 0
            
            for session in expired_sessions:
                if self.storage.invalidate_session_db(session.session_id):
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} expired sessions")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
    
    def get_session_statistics(self) -> Dict:
        """Get session statistics"""
        try:
            total_sessions = self.storage.get_total_session_count()
            active_sessions = self.storage.get_active_session_count()
            expired_sessions = self.storage.get_expired_session_count()
            
            return {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "expired_sessions": expired_sessions,
                "cleanup_needed": expired_sessions > 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            return {}
