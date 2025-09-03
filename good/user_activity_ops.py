#!/usr/bin/env python3
"""
TradePulse User Activity Operations
Main user activity operations coordinator
"""

import logging
from typing import Dict, List, Optional
from .user_activity_core import UserActivityCore
from .user_activity_advanced import UserActivityAdvanced

logger = logging.getLogger(__name__)

class UserActivityOperations:
    """Main user activity operations coordinator"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.core = UserActivityCore(db_path)
        self.advanced = UserActivityAdvanced(db_path)
    
    def log_activity(self, user_id: int, activity_type: str, 
                     description: str = None, metadata: Dict = None, 
                     ip_address: str = None, user_agent: str = None) -> bool:
        """Log user activity"""
        return self.core.log_activity(user_id, activity_type, description, metadata, ip_address, user_agent)
    
    def get_user_activity(self, user_id: int, limit: int = 100, 
                          activity_type: str = None, 
                          start_date = None, 
                          end_date = None) -> Optional[List[Dict]]:
        """Get user activity logs"""
        return self.core.get_user_activity(user_id, limit, activity_type, start_date, end_date)
    
    def get_activity_summary(self, user_id: int, days: int = 30) -> Optional[Dict]:
        """Get activity summary for a user"""
        return self.advanced.get_activity_summary(user_id, days)
    
    def cleanup_old_activity_logs(self, days_to_keep: int = 90) -> int:
        """Clean up old activity logs and return count of cleaned logs"""
        return self.advanced.cleanup_old_activity_logs(days_to_keep)
    
    def get_system_activity_summary(self, days: int = 7) -> Optional[Dict]:
        """Get system-wide activity summary"""
        return self.advanced.get_system_activity_summary(days)
