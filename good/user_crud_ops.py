#!/usr/bin/env python3
"""
TradePulse User CRUD Operations
Basic CRUD operations for user management
"""

import logging
import sqlite3
from typing import Dict, List, Optional
from .user_core import UserCore, User

logger = logging.getLogger(__name__)

class UserCRUDOperations:
    """Basic CRUD operations for user management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.core = UserCore()
    
    def create_user(self, username: str, email: str, password: str, 
                    role: str = "user", profile_data: Dict = None, 
                    preferences: Dict = None) -> Optional[int]:
        """Create a new user"""
        try:
            # Hash password
            password_hash = self.core.hash_password(password)
            
            # Serialize profile and preferences
            profile_json = self.core.serialize_profile_data(profile_data) if profile_data else None
            preferences_json = self.core.serialize_profile_data(preferences) if preferences else None
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (
                        username, email, password_hash, salt, role,
                        profile_data, preferences
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    username, email, password_hash, "", role,
                    profile_json, preferences_json
                ))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"User {username} created successfully")
                return user_id
                
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, email, password_hash, salt, role,
                           status, profile_data, preferences, created_at,
                           updated_at, last_login, failed_login_attempts,
                           account_locked_until
                    FROM users WHERE id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return self.core.create_user_from_row(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by ID {user_id}: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, email, password_hash, salt, role,
                           status, profile_data, preferences, created_at,
                           updated_at, last_login, failed_login_attempts,
                           account_locked_until
                    FROM users WHERE username = ?
                """, (username,))
                
                row = cursor.fetchone()
                if row:
                    return self.core.create_user_from_row(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by username {username}: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, email, password_hash, salt, role,
                           status, profile_data, preferences, created_at,
                           updated_at, last_login, failed_login_attempts,
                           account_locked_until
                    FROM users WHERE email = ?
                """, (email,))
                
                row = cursor.fetchone()
                if row:
                    return self.core.create_user_from_row(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by email {email}: {e}")
            return None
    
    def list_users(self, include_inactive: bool = False) -> Optional[List[User]]:
        """List all users"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT id, username, email, password_hash, salt, role, status,
                           profile_data, preferences, created_at, updated_at, last_login,
                           failed_login_attempts, account_locked_until
                    FROM users
                """
                
                if not include_inactive:
                    query += " WHERE status = 'active'"
                
                query += " ORDER BY created_at DESC"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                users = []
                for row in rows:
                    try:
                        user = self.core.create_user_from_row(row)
                        users.append(user)
                    except Exception as e:
                        logger.error(f"Failed to create user object from row: {e}")
                        continue
                
                return users
                
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return None
