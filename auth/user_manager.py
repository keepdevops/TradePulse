#!/usr/bin/env python3
"""
TradePulse User Manager
Main user management module - uses user_core and user_db_ops
"""

import logging
from typing import Dict, List, Optional
from .user_core import UserCore, User
from .user_db_ops import UserDatabaseOperations

logger = logging.getLogger(__name__)

class UserManager:
    """Manages user accounts and profiles"""
    
    def __init__(self, db_path: str = "./data/users.db"):
        self.db_path = db_path
        self.core = UserCore()
        self.db_ops = UserDatabaseOperations(db_path)
        self.db_ops.init_database()
    
    def init_database(self):
        """Initialize user database"""
        try:
            self.db_ops.init_database()
            logger.info("User database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize user database: {e}")
            raise
    
    def create_user(self, username: str, email: str, password: str, 
                   role: str = "user", profile_data: Dict = None, 
                   preferences: Dict = None) -> Optional[User]:
        """Create a new user account"""
        try:
            # Create user in database
            user_id = self.db_ops.create_user(username, email, password, role, profile_data, preferences)
            
            if user_id:
                # Get the created user object
                user = self.db_ops.get_user_by_id(user_id)
                if user:
                    logger.info(f"User {username} created successfully with ID {user_id}")
                    return user
                else:
                    logger.error(f"Failed to retrieve created user {username}")
                    return None
            
            return None
                
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db_ops.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db_ops.get_user_by_username(username)
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile data"""
        return self.db_ops.update_user_profile(user_id, profile_data)
    
    def update_user_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Update user preferences"""
        return self.db_ops.update_user_preferences(user_id, preferences)
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        return self.db_ops.update_last_login(user_id)
    
    def change_user_role(self, user_id: int, new_role: str) -> bool:
        """Change user role (admin only)"""
        return self.db_ops.change_user_role(user_id, new_role)
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        return self.db_ops.deactivate_user(user_id)
    
    def list_users(self, role_filter: str = None, status_filter: str = None) -> List[User]:
        """List users with optional filtering"""
        users = self.db_ops.list_users(include_inactive=(status_filter != "active"))
        if not users:
            return []
        
        # Apply filters
        if role_filter:
            users = [u for u in users if u.role == role_filter]
        if status_filter:
            users = [u for u in users if u.status == status_filter]
        
        return users
    
    def log_activity(self, user_id: int, action: str, details: Dict):
        """Log user activity for audit purposes"""
        self.db_ops.log_activity(user_id, action, details)
    
    def get_user_activity(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get user activity log"""
        activities = self.db_ops.get_user_activity(user_id)
        if activities and limit:
            return activities[:limit]
        return activities or []
