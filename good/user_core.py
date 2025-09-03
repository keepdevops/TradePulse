#!/usr/bin/env python3
"""
TradePulse User Core
Core user functionality and data model
"""

import logging
import json
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from .security_utils import SecurityUtils

logger = logging.getLogger(__name__)

@dataclass
class User:
    """User data model"""
    id: int
    username: str
    email: str
    password_hash: str
    salt: str
    role: str
    status: str
    profile_data: Dict
    preferences: Dict
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    failed_login_attempts: int
    account_locked_until: Optional[datetime]

class UserCore:
    """Core user functionality"""
    
    def __init__(self):
        pass
    
    def create_user_object(self, user_id: int, username: str, email: str, 
                          role: str, profile_data: Dict = None, 
                          preferences: Dict = None) -> User:
        """Create a new user object"""
        return User(
            id=user_id,
            username=username,
            email=email,
            role=role,
            status="active",
            created_at=datetime.now(),
            last_login=None,
            profile_data=profile_data or {},
            preferences=preferences or {}
        )
    
    def hash_password(self, password: str) -> str:
        """Hash a password for storage"""
        return SecurityUtils.hash_password(password)
    
    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Validate password strength"""
        return SecurityUtils.validate_password_strength(password)
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input"""
        return SecurityUtils.sanitize_input(input_string)
    
    def serialize_profile_data(self, profile_data: Dict) -> str:
        """Serialize profile data to JSON"""
        return json.dumps(profile_data)
    
    def deserialize_profile_data(self, profile_json: str) -> Dict:
        """Deserialize profile data from JSON"""
        try:
            return json.loads(profile_json) if profile_json else {}
        except json.JSONDecodeError:
            logger.error(f"Failed to deserialize profile data: {profile_json}")
            return {}
    
    def serialize_preferences(self, preferences: Dict) -> str:
        """Serialize preferences to JSON"""
        return json.dumps(preferences)
    
    def deserialize_preferences(self, preferences_json: str) -> Dict:
        """Deserialize preferences from JSON"""
        try:
            return json.loads(preferences_json) if preferences_json else {}
        except json.JSONDecodeError:
            logger.error(f"Failed to deserialize preferences: {preferences_json}")
            return {}
    
    def create_user_from_row(self, row: tuple) -> User:
        """Create user object from database row"""
        try:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                salt=row[4],
                role=row[5],
                status=row[6],
                profile_data=self.deserialize_profile_data(row[7]),
                preferences=self.deserialize_preferences(row[8]),
                created_at=datetime.fromisoformat(row[9]) if row[9] else datetime.now(),
                updated_at=datetime.fromisoformat(row[10]) if row[10] else datetime.now(),
                last_login=datetime.fromisoformat(row[11]) if row[11] else None,
                failed_login_attempts=row[12] if row[12] else 0,
                account_locked_until=datetime.fromisoformat(row[13]) if row[13] else None
            )
        except Exception as e:
            logger.error(f"Failed to create user from row: {e}, row: {row}")
            raise
    
    def update_user_timestamp(self, user_id: int, field: str) -> str:
        """Generate SQL for updating user timestamp fields"""
        return f"UPDATE users SET {field} = CURRENT_TIMESTAMP WHERE id = ?"
    
    def update_user_json_field(self, user_id: int, field: str, data: Dict) -> tuple[str, tuple]:
        """Generate SQL for updating user JSON fields"""
        sql = f"UPDATE users SET {field} = ? WHERE id = ?"
        params = (self.serialize_profile_data(data), user_id)
        return sql, params
