#!/usr/bin/env python3
"""
TradePulse Auth Session Operations
Session-related operations for the authentication service
"""

import logging
from typing import Dict, Optional, Tuple
from .rbac import Permission

logger = logging.getLogger(__name__)

class AuthSessionOperations:
    """Session operations for authentication service"""
    
    def __init__(self, user_manager, rbac, session_manager, security_ops):
        self.user_manager = user_manager
        self.rbac = rbac
        self.session_manager = session_manager
        self.security_ops = security_ops
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: str = None, user_agent: str = None) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate a user and create a session"""
        try:
            # Check if account is locked
            if self.security_ops.is_account_locked(username):
                return False, "Account is temporarily locked due to too many failed attempts", None
            
            # Get user by username
            user = self.user_manager.get_user_by_username(username)
            if not user:
                self.security_ops.record_failed_login(username)
                return False, "Invalid username or password", None
            
            # Check if user is active
            if user.status != "active":
                return False, "Account is not active", None
            
            # Verify password
            if not self.security_ops.verify_user_password(username, password):
                self.security_ops.record_failed_login(username)
                return False, "Invalid username or password", None
            
            # Clear failed login attempts on successful login
            self.security_ops.clear_failed_login_attempts(username)
            
            # Update last login time
            self.user_manager.update_last_login(user.id)
            
            # Create session
            session_id = self.session_manager.create_session(
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            if not session_id:
                return False, "Failed to create session", None
            
            # Get user permissions
            permissions = self.rbac.get_user_permissions(user.id)
            
            # Prepare user info
            user_info = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "session_id": session_id,
                "permissions": [perm.value for perm in permissions],
                "profile_data": user.profile_data,
                "preferences": user.preferences
            }
            
            logger.info(f"User {username} authenticated successfully")
            return True, "Authentication successful", user_info
            
        except Exception as e:
            logger.error(f"Authentication failed for {username}: {e}")
            return False, "Authentication failed due to system error", None
    
    def validate_session(self, session_id: str, ip_address: str = None) -> Tuple[bool, Optional[Dict]]:
        """Validate a session and return user information"""
        try:
            # Validate session
            user_id = self.session_manager.validate_session(session_id, ip_address)
            if not user_id:
                return False, None
            
            # Get user information
            user = self.user_manager.get_user_by_id(user_id)
            if not user or user.status != "active":
                return False, None
            
            # Get user permissions
            permissions = self.rbac.get_user_permissions(user_id)
            
            # Prepare user info
            user_info = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "session_id": session_id,
                "permissions": [perm.value for perm in permissions],
                "profile_data": user.profile_data,
                "preferences": user.preferences
            }
            
            return True, user_info
            
        except Exception as e:
            logger.error(f"Session validation failed for {session_id}: {e}")
            return False, None
    
    def logout_user(self, session_id: str) -> bool:
        """Logout a user by invalidating their session"""
        try:
            return self.session_manager.invalidate_session(session_id)
        except Exception as e:
            logger.error(f"Logout failed for session {session_id}: {e}")
            return False
