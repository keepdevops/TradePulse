#!/usr/bin/env python3
"""
TradePulse Session Validation
Session validation and security checks
"""

import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta
from .session_core import Session

logger = logging.getLogger(__name__)

class SessionValidation:
    """Session validation and security checks"""
    
    def __init__(self, max_sessions_per_user: int = 5, 
                 session_timeout_hours: int = 24,
                 max_failed_attempts: int = 5):
        self.max_sessions_per_user = max_sessions_per_user
        self.session_timeout_hours = session_timeout_hours
        self.max_failed_attempts = max_failed_attempts
    
    def validate_session_security(self, session: Session, 
                                 ip_address: str = None, 
                                 user_agent: str = None) -> Tuple[bool, str]:
        """Validate session security parameters"""
        try:
            # Check if session is expired
            if self._is_session_expired(session):
                return False, "Session has expired"
            
            # Check IP address if provided
            if ip_address and session.ip_address and session.ip_address != ip_address:
                logger.warning(f"IP address mismatch for session {session.session_id}")
                return False, "Session security validation failed"
            
            # Check user agent if provided
            if user_agent and session.user_agent and session.user_agent != user_agent:
                logger.warning(f"User agent mismatch for session {session.session_id}")
                return False, "Session security validation failed"
            
            # Check if session is still active
            if not session.is_active:
                return False, "Session is not active"
            
            return True, "Session is valid"
            
        except Exception as e:
            logger.error(f"Session security validation failed: {e}")
            return False, "Session validation error"
    
    def _is_session_expired(self, session: Session) -> bool:
        """Check if session has expired"""
        if not session.expiry_time:
            return True
        
        return datetime.now() > session.expiry_time
    
    def validate_session_limits(self, user_id: int, current_sessions: int) -> Tuple[bool, str]:
        """Validate session limits for a user"""
        try:
            if current_sessions >= self.max_sessions_per_user:
                return False, f"Maximum sessions ({self.max_sessions_per_user}) reached for user"
            
            return True, "Session limit validation passed"
            
        except Exception as e:
            logger.error(f"Session limit validation failed: {e}")
            return False, "Session limit validation error"
    
    def check_session_activity(self, session: Session, 
                              max_inactivity_hours: int = 2) -> Tuple[bool, str]:
        """Check if session has been inactive for too long"""
        try:
            if not session.last_activity:
                return False, "Session has no activity record"
            
            inactivity_threshold = datetime.now() - timedelta(hours=max_inactivity_hours)
            if session.last_activity < inactivity_threshold:
                return False, f"Session inactive for more than {max_inactivity_hours} hours"
            
            return True, "Session activity is within limits"
            
        except Exception as e:
            logger.error(f"Session activity check failed: {e}")
            return False, "Session activity check error"
    
    def validate_session_permissions(self, session: Session, 
                                   required_permissions: list = None) -> Tuple[bool, str]:
        """Validate if session has required permissions"""
        try:
            if not required_permissions:
                return True, "No permissions required"
            
            # This would typically check against user permissions
            # For now, we'll assume all sessions have basic permissions
            return True, "Session permissions validated"
            
        except Exception as e:
            logger.error(f"Session permission validation failed: {e}")
            return False, "Session permission validation error"
    
    def get_session_risk_score(self, session: Session, 
                              ip_address: str = None, 
                              user_agent: str = None) -> int:
        """Calculate session risk score (0-100, higher = more risky)"""
        try:
            risk_score = 0
            
            # IP address mismatch
            if ip_address and session.ip_address and session.ip_address != ip_address:
                risk_score += 30
            
            # User agent mismatch
            if user_agent and session.user_agent and session.user_agent != user_agent:
                risk_score += 20
            
            # Session age
            if session.created_at:
                age_hours = (datetime.now() - session.created_at).total_seconds() / 3600
                if age_hours > 12:
                    risk_score += 15
                if age_hours > 24:
                    risk_score += 25
            
            # Inactivity
            if session.last_activity:
                inactivity_hours = (datetime.now() - session.last_activity).total_seconds() / 3600
                if inactivity_hours > 1:
                    risk_score += 10
                if inactivity_hours > 4:
                    risk_score += 20
            
            return min(risk_score, 100)
            
        except Exception as e:
            logger.error(f"Failed to calculate session risk score: {e}")
            return 50  # Default medium risk
