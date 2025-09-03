#!/usr/bin/env python3
"""
TradePulse User Activity Advanced Operations
Advanced user activity operations like summaries and cleanup
"""

import logging
import sqlite3
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UserActivityAdvanced:
    """Advanced user activity operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_activity_summary(self, user_id: int, days: int = 30) -> Optional[Dict]:
        """Get activity summary for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get activity count by type
                cursor.execute("""
                    SELECT activity_type, COUNT(*) as count
                    FROM user_activity_logs
                    WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                    GROUP BY activity_type
                """.format(days), (user_id,))
                
                activity_counts = dict(cursor.fetchall())
                
                # Get recent activity
                cursor.execute("""
                    SELECT activity_type, timestamp
                    FROM user_activity_logs
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """, (user_id,))
                
                recent_activity = [
                    {"type": row[0], "timestamp": row[1]}
                    for row in cursor.fetchall()
                ]
                
                # Get login activity
                cursor.execute("""
                    SELECT COUNT(*) as login_count
                    FROM user_activity_logs
                    WHERE user_id = ? AND activity_type = 'login'
                    AND timestamp >= datetime('now', '-{} days')
                """.format(days), (user_id,))
                
                login_count = cursor.fetchone()[0]
                
                return {
                    "activity_counts": activity_counts,
                    "recent_activity": recent_activity,
                    "login_count": login_count,
                    "period_days": days
                }
                
        except Exception as e:
            logger.error(f"Failed to get activity summary for user {user_id}: {e}")
            return None
    
    def cleanup_old_activity_logs(self, days_to_keep: int = 90) -> int:
        """Clean up old activity logs and return count of cleaned logs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM user_activity_logs
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days_to_keep))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    logger.info(f"Cleaned up {deleted_count} old activity logs")
                
                return deleted_count
                
        except Exception as e:
            logger.error(f"Failed to cleanup old activity logs: {e}")
            return 0
    
    def get_system_activity_summary(self, days: int = 7) -> Optional[Dict]:
        """Get system-wide activity summary"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total users with activity
                cursor.execute("""
                    SELECT COUNT(DISTINCT user_id) as active_users
                    FROM user_activity_logs
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                
                active_users = cursor.fetchone()[0]
                
                # Activity by type
                cursor.execute("""
                    SELECT activity_type, COUNT(*) as count
                    FROM user_activity_logs
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY activity_type
                    ORDER BY count DESC
                """.format(days))
                
                activity_by_type = dict(cursor.fetchall())
                
                # Most active users
                cursor.execute("""
                    SELECT user_id, COUNT(*) as activity_count
                    FROM user_activity_logs
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY user_id
                    ORDER BY activity_count DESC
                    LIMIT 10
                """.format(days))
                
                most_active_users = [
                    {"user_id": row[0], "activity_count": row[1]}
                    for row in cursor.fetchall()
                ]
                
                return {
                    "active_users": active_users,
                    "activity_by_type": activity_by_type,
                    "most_active_users": most_active_users,
                    "period_days": days
                }
                
        except Exception as e:
            logger.error(f"Failed to get system activity summary: {e}")
            return None
