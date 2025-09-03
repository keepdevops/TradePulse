#!/usr/bin/env python3
"""
TradePulse Session Core
Core session functionality and data model
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Session:
    """Session data model"""
    session_id: str
    user_id: int
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool
    last_activity: datetime

class SessionCore:
    """Core session functionality"""
    
    def __init__(self):
        self.session_timeout_hours = 24
        self.max_sessions_per_user = 5
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return secrets.token_urlsafe(32)
    
    def calculate_expiry_time(self) -> datetime:
        """Calculate session expiration time"""
        return datetime.now() + timedelta(hours=self.session_timeout_hours)
    
    def is_session_expired(self, session: Session) -> bool:
        """Check if a session is expired"""
        return datetime.now() > session.expires_at
    
    def extend_session(self, session: Session) -> Session:
        """Extend session expiration time"""
        session.expires_at = self.calculate_expiry_time()
        session.last_activity = datetime.now()
        return session
    
    def create_session_object(self, user_id: int, ip_address: str = None, 
                            user_agent: str = None) -> Session:
        """Create a new session object"""
        return Session(
            session_id=self.generate_session_id(),
            user_id=user_id,
            created_at=datetime.now(),
            expires_at=self.calculate_expiry_time(),
            ip_address=ip_address or "unknown",
            user_agent=user_agent or "unknown",
            is_active=True,
            last_activity=datetime.now()
        )
    
    def validate_session_basic(self, session: Session) -> bool:
        """Basic session validation"""
        if not session.is_active:
            return False
        
        if self.is_session_expired(session):
            return False
        
        return True
    
    def update_session_activity(self, session: Session) -> Session:
        """Update session last activity"""
        session.last_activity = datetime.now()
        return session
