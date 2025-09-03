#!/usr/bin/env python3
"""
TradePulse Auth Maintenance Operations
System maintenance and statistics operations for the authentication service
"""

import logging
from typing import Dict, List
from .security_utils import SecurityUtils

logger = logging.getLogger(__name__)

class AuthMaintenanceOperations:
    """System maintenance and statistics operations for authentication service"""
    
    def __init__(self, user_manager, session_manager, security_ops):
        self.user_manager = user_manager
        self.session_manager = session_manager
        self.security_ops = security_ops
    
    def get_system_statistics(self) -> Dict:
        """Get authentication system statistics"""
        try:
            total_users = len(self.user_manager.list_users())
            active_users = len(self.user_manager.list_users(status_filter="active"))
            session_stats = self.session_manager.get_session_statistics()
            
            # Count users by role
            users_by_role = {}
            for user in self.user_manager.list_users():
                role = user.role
                users_by_role[role] = users_by_role.get(role, 0) + 1
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users,
                "users_by_role": users_by_role,
                "session_statistics": session_stats,
                "failed_login_attempts": self.security_ops.get_failed_login_count()
            }
            
        except Exception as e:
            logger.error(f"Failed to get system statistics: {e}")
            return {}
    
    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Validate password strength requirements"""
        return SecurityUtils.validate_password_strength(password)
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input"""
        return SecurityUtils.sanitize_input(input_string)
    
    def sanitize_profile_data(self, profile_data: Dict) -> Dict:
        """Sanitize profile data"""
        sanitized_data = {}
        for key, value in profile_data.items():
            if isinstance(value, str):
                sanitized_data[key] = self.sanitize_input(value)
            else:
                sanitized_data[key] = value
        return sanitized_data
    
    def prepare_user_info(self, user, session_id: str = None, permissions: List = None) -> Dict:
        """Prepare user information dictionary"""
        user_info = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_data": user.profile_data,
            "preferences": user.preferences
        }
        
        if session_id:
            user_info["session_id"] = session_id
        
        if permissions:
            user_info["permissions"] = [perm.value for perm in permissions]
        
        return user_info
    
    def prepare_user_list_info(self, users: List) -> List[Dict]:
        """Prepare user list information for admin views"""
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
        return user_list
