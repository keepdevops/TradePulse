#!/usr/bin/env python3
"""
TradePulse User Update Operations
User update operations for profile, preferences, and status
"""

import logging
import sqlite3
from typing import Dict
from .user_core import UserCore

logger = logging.getLogger(__name__)

class UserUpdateOperations:
    """User update operations for profile, preferences, and status"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.core = UserCore()
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile data"""
        try:
            profile_json = self.core.serialize_profile_data(profile_data)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET profile_data = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (profile_json, user_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Profile updated for user {user_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to update profile for user {user_id}: {e}")
            return False
    
    def update_user_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Update user preferences"""
        try:
            preferences_json = self.core.serialize_profile_data(preferences)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET preferences = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (preferences_json, user_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Preferences updated for user {user_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to update preferences for user {user_id}: {e}")
            return False
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login time"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to update last login for user {user_id}: {e}")
            return False
    
    def change_user_role(self, user_id: int, new_role: str) -> bool:
        """Change user's role"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET role = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (new_role, user_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Role changed to {new_role} for user {user_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to change role for user {user_id}: {e}")
            return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET status = 'inactive', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"User {user_id} deactivated")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to deactivate user {user_id}: {e}")
            return False
