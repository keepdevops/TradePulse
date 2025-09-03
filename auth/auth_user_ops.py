#!/usr/bin/env python3
"""
TradePulse Auth User Operations
User-related operations for the authentication service
"""

import logging
from typing import Dict, Optional, Tuple, List
from .rbac import Permission, Role
from .security_utils import SecurityUtils

logger = logging.getLogger(__name__)

class AuthUserOperations:
    """User operations for authentication service"""
    
    def __init__(self, user_manager, rbac):
        self.user_manager = user_manager
        self.rbac = rbac
    
    def register_user(self, username: str, email: str, password: str, 
                     profile_data: Dict = None) -> Tuple[bool, str]:
        """Register a new user account"""
        try:
            # Validate password strength
            is_strong, message = SecurityUtils.validate_password_strength(password)
            if not is_strong:
                return False, message
            
            # Sanitize inputs
            username = SecurityUtils.sanitize_input(username)
            email = SecurityUtils.sanitize_input(email)
            
            # Check if username or email already exists
            if self.user_manager.get_user_by_username(username):
                return False, "Username already exists"
            
            # Create user with default role
            user = self.user_manager.create_user(
                username=username,
                email=email,
                password=password,
                role="user",
                profile_data=profile_data or {}
            )
            
            if user:
                # Assign default role
                self.rbac.assign_role_to_user(user.id, "user")
                
                logger.info(f"User {username} registered successfully")
                return True, "User registered successfully"
            else:
                return False, "Failed to create user account"
                
        except Exception as e:
            logger.error(f"Failed to register user {username}: {e}")
            return False, "Registration failed due to system error"
    
    def change_password(self, user_id: int, current_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        try:
            # Get user
            user = self.user_manager.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not self._verify_user_password(user.username, current_password):
                return False, "Current password is incorrect"
            
            # Validate new password strength
            is_strong, message = SecurityUtils.validate_password_strength(new_password)
            if not is_strong:
                return False, message
            
            # Update password in database
            if self._update_user_password(user_id, new_password):
                logger.info(f"Password changed for user {user.username}")
                return True, "Password changed successfully"
            else:
                return False, "Failed to update password"
                
        except Exception as e:
            logger.error(f"Password change failed for user {user_id}: {e}")
            return False, "Password change failed due to system error"
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> Tuple[bool, str]:
        """Update user profile data"""
        try:
            # Sanitize profile data
            sanitized_data = {}
            for key, value in profile_data.items():
                if isinstance(value, str):
                    sanitized_data[key] = SecurityUtils.sanitize_input(value)
                else:
                    sanitized_data[key] = value
            
            if self.user_manager.update_user_profile(user_id, sanitized_data):
                logger.info(f"Profile updated for user {user_id}")
                return True, "Profile updated successfully"
            else:
                return False, "Failed to update profile"
                
        except Exception as e:
            logger.error(f"Profile update failed for user {user_id}: {e}")
            return False, "Profile update failed due to system error"
    
    def check_permission(self, user_id: int, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        try:
            return self.rbac.user_has_permission(user_id, permission)
        except Exception as e:
            logger.error(f"Permission check failed for user {user_id}: {e}")
            return False
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Get all permissions for a user"""
        try:
            permissions = self.rbac.get_user_permissions(user_id)
            return [perm.value for perm in permissions]
        except Exception as e:
            logger.error(f"Failed to get permissions for user {user_id}: {e}")
            return []
    
    def _verify_user_password(self, username: str, password: str) -> bool:
        """Verify user password from database"""
        try:
            import sqlite3
            with sqlite3.connect(self.user_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT password_hash FROM users WHERE username = ?
                """, (username,))
                
                row = cursor.fetchone()
                if row:
                    stored_hash = row[0]
                    return SecurityUtils.verify_password(password, stored_hash)
                return False
                
        except Exception as e:
            logger.error(f"Password verification failed for {username}: {e}")
            return False
    
    def _update_user_password(self, user_id: int, new_password: str) -> bool:
        """Update user password in database"""
        try:
            import sqlite3
            new_hash = SecurityUtils.hash_password(new_password)
            
            with sqlite3.connect(self.user_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET password_hash = ? WHERE id = ?
                """, (new_hash, user_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Password update failed for user {user_id}: {e}")
            return False
