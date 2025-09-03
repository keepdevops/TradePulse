#!/usr/bin/env python3
"""
TradePulse User Database Operations
Database operations for user management
"""

import logging
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
from .user_core import UserCore, User
from .user_activity_ops import UserActivityOperations
from .user_crud_ops import UserCRUDOperations
from .user_update_ops import UserUpdateOperations

logger = logging.getLogger(__name__)

class UserDatabaseOperations:
    """Database operations for user management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.core = UserCore()
        self.activity_ops = UserActivityOperations(db_path)
        self.crud_ops = UserCRUDOperations(db_path)
        self.update_ops = UserUpdateOperations(db_path)
    
    def init_database(self):
        """Initialize user database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'user',
                        status TEXT NOT NULL DEFAULT 'active',
                        profile_data TEXT,
                        preferences TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        failed_login_attempts INTEGER DEFAULT 0,
                        account_locked_until TIMESTAMP
                    )
                """)
                
                # Create user_activity_logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_activity_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        activity_type TEXT NOT NULL,
                        description TEXT,
                        metadata TEXT,
                        ip_address TEXT,
                        user_agent TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
                logger.info("User database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize user database: {e}")
            raise
    
    def create_user(self, username: str, email: str, password: str, 
                    role: str = "user", profile_data: Dict = None, 
                    preferences: Dict = None) -> Optional[int]:
        """Create a new user"""
        try:
            user_id = self.crud_ops.create_user(username, email, password, role, profile_data, preferences)
            
            if user_id:
                # Log user creation
                self.activity_ops.log_activity(
                    user_id, "user_created", 
                    f"User account created with role: {role}"
                )
            
            return user_id
                
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.crud_ops.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.crud_ops.get_user_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.crud_ops.get_user_by_email(email)
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile data"""
        success = self.update_ops.update_user_profile(user_id, profile_data)
        if success:
            # Log profile update
            self.activity_ops.log_activity(
                user_id, "profile_updated", 
                "User profile updated"
            )
        return success
    
    def update_user_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Update user preferences"""
        success = self.update_ops.update_user_preferences(user_id, preferences)
        if success:
            # Log preferences update
            self.activity_ops.log_activity(
                user_id, "preferences_updated", 
                "User preferences updated"
            )
        return success
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login time"""
        success = self.update_ops.update_last_login(user_id)
        if success:
            # Log login
            self.activity_ops.log_activity(
                user_id, "login", 
                "User logged in"
            )
        return success
    
    def change_user_role(self, user_id: int, new_role: str) -> bool:
        """Change user's role"""
        success = self.update_ops.change_user_role(user_id, new_role)
        if success:
            # Log role change
            self.activity_ops.log_activity(
                user_id, "role_changed", 
                f"User role changed to: {new_role}"
            )
        return success
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        success = self.update_ops.deactivate_user(user_id)
        if success:
            # Log deactivation
            self.activity_ops.log_activity(
                user_id, "account_deactivated", 
                "User account deactivated"
            )
        return success
    
    def list_users(self, include_inactive: bool = False) -> Optional[List[User]]:
        """List all users"""
        return self.crud_ops.list_users(include_inactive)
    
    def get_user_activity(self, user_id: int) -> Optional[List[Dict]]:
        """Get user activity logs"""
        return self.activity_ops.get_user_activity(user_id)
    
    def log_activity(self, user_id: int, activity_type: str, 
                     description: str = None, metadata: Dict = None, 
                     ip_address: str = None, user_agent: str = None) -> bool:
        """Log user activity"""
        return self.activity_ops.log_activity(
            user_id, activity_type, description, metadata, ip_address, user_agent
        )
