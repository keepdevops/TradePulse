#!/usr/bin/env python3
"""
TradePulse Authentication Service
Main authentication service that coordinates all authentication operations
"""

import logging
from typing import Dict, Optional, Tuple, List
from .user_manager import UserManager, User
from .rbac import RoleBasedAccessControl, Permission, Role
from .session_manager import SessionManager
from .auth_user_ops import AuthUserOperations
from .auth_session_ops import AuthSessionOperations
from .auth_admin_ops import AuthAdminOperations
from .auth_security_ops import AuthSecurityOperations
from .auth_maintenance_ops import AuthMaintenanceOperations

logger = logging.getLogger(__name__)

class AuthService:
    """Main authentication service for TradePulse"""
    
    def __init__(self, db_path: str = "./data/users.db"):
        self.user_manager = UserManager(db_path)
        self.rbac = RoleBasedAccessControl(db_path)
        self.session_manager = SessionManager(db_path)
        
        # Initialize operational modules
        self.security_ops = AuthSecurityOperations(self.user_manager)
        self.user_ops = AuthUserOperations(self.user_manager, self.rbac)
        self.session_ops = AuthSessionOperations(self.user_manager, self.rbac, self.session_manager, self.security_ops)
        self.admin_ops = AuthAdminOperations(self.user_manager, self.rbac)
        self.maintenance_ops = AuthMaintenanceOperations(self.user_manager, self.session_manager, self.security_ops)
        
        # Initialize databases
        self.rbac.init_database()
        self.session_manager.init_database()
        
        # Initialize default admin user if none exists
        self._ensure_admin_user_exists()
    
    def _ensure_admin_user_exists(self):
        """Ensure at least one admin user exists in the system"""
        try:
            admin_users = self.user_manager.list_users(role_filter="admin")
            if not admin_users:
                # Create default admin user
                admin_user = self.user_manager.create_user(
                    username="admin",
                    email="admin@tradepulse.com",
                    password="Admin123!",
                    role="admin",
                    profile_data={
                        "first_name": "System",
                        "last_name": "Administrator",
                        "created_by": "system"
                    }
                )
                
                if admin_user:
                    self.rbac.assign_role_to_user(admin_user.id, "admin")
                    logger.info("Default admin user created: admin/Admin123!")
                else:
                    logger.error("Failed to create default admin user")
                    
        except Exception as e:
            logger.error(f"Failed to ensure admin user exists: {e}")
    
    def register_user(self, username: str, email: str, password: str, 
                     profile_data: Dict = None) -> Tuple[bool, str]:
        """Register a new user account"""
        return self.user_ops.register_user(username, email, password, profile_data)
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: str = None, user_agent: str = None) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate a user and create a session"""
        return self.session_ops.authenticate_user(username, password, ip_address, user_agent)
    
    def validate_session(self, session_id: str, ip_address: str = None) -> Tuple[bool, Optional[Dict]]:
        """Validate a session and return user information"""
        return self.session_ops.validate_session(session_id, ip_address)
    
    def logout_user(self, session_id: str) -> bool:
        """Logout a user by invalidating their session"""
        return self.session_ops.logout_user(session_id)
    
    def change_password(self, user_id: int, current_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        return self.user_ops.change_password(user_id, current_password, new_password)
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> Tuple[bool, str]:
        """Update user profile data"""
        return self.user_ops.update_user_profile(user_id, profile_data)
    
    def check_permission(self, user_id: int, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        return self.user_ops.check_permission(user_id, permission)
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Get all permissions for a user"""
        return self.user_ops.get_user_permissions(user_id)
    
    def assign_role_to_user(self, admin_user_id: int, target_user_id: int, 
                           new_role: str) -> Tuple[bool, str]:
        """Assign a role to a user (admin only)"""
        return self.admin_ops.assign_role_to_user(admin_user_id, target_user_id, new_role)
    
    def list_users(self, admin_user_id: int, role_filter: str = None, 
                   status_filter: str = None) -> Tuple[bool, str, Optional[List[Dict]]]:
        """List users (admin only)"""
        return self.admin_ops.list_users(admin_user_id, role_filter, status_filter)
    
    def get_user_activity(self, user_id: int, target_user_id: int = None) -> Tuple[bool, str, Optional[List[Dict]]]:
        """Get user activity log"""
        return self.admin_ops.get_user_activity(user_id, target_user_id)
    
    def get_system_statistics(self) -> Dict:
        """Get authentication system statistics"""
        return self.maintenance_ops.get_system_statistics()
