#!/usr/bin/env python3
"""
TradePulse Auth Admin Operations
Admin operations for the authentication service
"""

import logging
from typing import Dict, List, Optional, Tuple
from .rbac import Permission, Role

logger = logging.getLogger(__name__)

class AuthAdminOperations:
    """Admin operations for authentication service"""
    
    def __init__(self, user_manager, rbac):
        self.user_manager = user_manager
        self.rbac = rbac
    
    def create_user(self, username: str, email: str, password: str, 
                    role: str = "user", profile_data: Dict = None, 
                    preferences: Dict = None, auth_core = None) -> Tuple[bool, str, Optional[int]]:
        """Create a new user"""
        try:
            # Validate input
            if auth_core:
                if not auth_core.validate_password_strength(password):
                    return False, "Password does not meet security requirements", None
                
                username = auth_core.sanitize_input(username)
                email = auth_core.sanitize_input(email)
            
            # Check if username already exists
            existing_user = self.user_manager.get_user_by_username(username)
            if existing_user:
                return False, "Username already exists", None
            
            # Check if email already exists
            existing_email = self.user_manager.get_user_by_email(email)
            if existing_email:
                return False, "Email already exists", None
            
            # Validate role
            if role not in [r.value for r in Role]:
                return False, "Invalid role specified", None
            
            # Create user
            user_id = self.user_manager.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                profile_data=profile_data,
                preferences=preferences
            )
            
            if user_id:
                logger.info(f"User {username} created successfully with role {role}")
                return True, "User created successfully", user_id
            else:
                return False, "Failed to create user", None
                
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            return False, "Failed to create user due to system error", None
    
    def update_user_role(self, user_id: int, new_role: str, 
                         admin_user_id: int = None) -> Tuple[bool, str]:
        """Update a user's role"""
        try:
            # Check if admin has permission
            if admin_user_id:
                if not self.rbac.user_has_permission(admin_user_id, Permission.MANAGE_USERS):
                    return False, "Insufficient permissions to manage users"
            
            # Validate role
            if new_role not in [r.value for r in Role]:
                return False, "Invalid role specified"
            
            # Update role
            success = self.user_manager.change_user_role(user_id, new_role)
            if success:
                logger.info(f"User {user_id} role updated to {new_role}")
                return True, "User role updated successfully"
            else:
                return False, "Failed to update user role"
                
        except Exception as e:
            logger.error(f"Failed to update user {user_id} role: {e}")
            return False, "Failed to update user role due to system error"
    
    def deactivate_user(self, user_id: int, admin_user_id: int = None) -> Tuple[bool, str]:
        """Deactivate a user account"""
        try:
            # Check if admin has permission
            if admin_user_id:
                if not self.rbac.user_has_permission(admin_user_id, Permission.MANAGE_USERS):
                    return False, "Insufficient permissions to manage users"
            
            # Deactivate user
            success = self.user_manager.deactivate_user(user_id)
            if success:
                logger.info(f"User {user_id} deactivated")
                return True, "User deactivated successfully"
            else:
                return False, "Failed to deactivate user"
                
        except Exception as e:
            logger.error(f"Failed to deactivate user {user_id}: {e}")
            return False, "Failed to deactivate user due to system error"
    
    def list_users(self, admin_user_id: int, role_filter: str = None, 
                   status_filter: str = None) -> Tuple[bool, str, Optional[List[Dict]]]:
        """List users with optional filtering"""
        try:
            # Check if admin has permission
            if not self.rbac.user_has_permission(admin_user_id, Permission.MANAGE_USERS):
                return False, "Insufficient permissions to view users", None
            
            # Get users with filters
            users = self.user_manager.list_users(role_filter, status_filter)
            
            # Convert User objects to dictionaries for admin view
            user_list = []
            for user in users:
                user_info = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "status": user.status,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "profile_data": user.profile_data
                }
                user_list.append(user_info)
            
            return True, "Users retrieved successfully", user_list
                
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return False, "Failed to retrieve users due to system error", None
    
    def get_user_activity(self, user_id: int, admin_user_id: int = None) -> Tuple[bool, str, Optional[List[Dict]]]:
        """Get user activity logs"""
        try:
            # Check if admin has permission
            if admin_user_id:
                if not self.rbac.user_has_permission(admin_user_id, Permission.VIEW_USERS):
                    return False, "Insufficient permissions to view user activity", None
            
            # Get activity
            activity = self.user_manager.get_user_activity(user_id)
            if activity is not None:
                return True, "User activity retrieved successfully", activity
            else:
                return False, "Failed to retrieve user activity", None
                
        except Exception as e:
            logger.error(f"Failed to get user activity for {user_id}: {e}")
            return False, "Failed to retrieve user activity due to system error", None
