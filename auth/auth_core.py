#!/usr/bin/env python3
"""
TradePulse Auth Core
Core authentication functionality
"""

import logging
import sqlite3
from typing import Dict, Optional, Tuple
from .security_utils import SecurityUtils

logger = logging.getLogger(__name__)

class AuthCore:
    """Core authentication functionality"""
    
    def __init__(self):
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 30
        self.failed_login_attempts = {}  # username -> (count, lockout_until)
    
    def verify_user_password(self, db_path: str, username: str, password: str) -> bool:
        """Verify user password from database"""
        try:
            with sqlite3.connect(db_path) as conn:
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
    
    def update_user_password(self, db_path: str, user_id: int, new_password: str) -> bool:
        """Update user password in database"""
        try:
            new_hash = SecurityUtils.hash_password(new_password)
            
            with sqlite3.connect(db_path) as conn:
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
    
    def is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to too many failed login attempts"""
        if username not in self.failed_login_attempts:
            return False
        
        count, lockout_until = self.failed_login_attempts[username]
        
        if lockout_until and datetime.now() < lockout_until:
            return True
        
        # Clear expired lockout
        if lockout_until and datetime.now() >= lockout_until:
            del self.failed_login_attempts[username]
        
        return False
    
    def record_failed_login(self, username: str):
        """Record a failed login attempt"""
        from datetime import datetime, timedelta
        
        if username not in self.failed_login_attempts:
            self.failed_login_attempts[username] = (1, None)
        else:
            count, lockout_until = self.failed_login_attempts[username]
            count += 1
            
            # Lock account if too many failed attempts
            if count >= self.max_login_attempts:
                lockout_until = datetime.now() + timedelta(minutes=self.lockout_duration_minutes)
                self.failed_login_attempts[username] = (count, lockout_until)
                logger.warning(f"Account {username} locked due to {count} failed login attempts")
            else:
                self.failed_login_attempts[username] = (count, None)
    
    def clear_failed_login_attempts(self, username: str):
        """Clear failed login attempts for a user"""
        if username in self.failed_login_attempts:
            del self.failed_login_attempts[username]
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        return SecurityUtils.validate_password_strength(password)
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input"""
        return SecurityUtils.sanitize_input(input_string)
