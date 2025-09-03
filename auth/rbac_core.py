#!/usr/bin/env python3
"""
TradePulse RBAC Core
Core role-based access control functionality
"""

import logging
import sqlite3
from typing import Dict, Set, Optional
from .rbac_permissions import Permission, Role, RoleDefinition, RBACPermissions

logger = logging.getLogger(__name__)

class RBACCore:
    """Core RBAC functionality"""
    
    def __init__(self, db_path: str = "tradepulse_auth.db"):
        """Initialize RBAC core"""
        self.db_path = db_path
        self.permissions = RBACPermissions()
    
    def init_database(self):
        """Initialize RBAC database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create user_roles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        role_name TEXT NOT NULL,
                        assigned_by INTEGER,
                        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active INTEGER DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (assigned_by) REFERENCES users (id)
                    )
                """)
                
                # Create custom_roles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS custom_roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role_name TEXT UNIQUE NOT NULL,
                        display_name TEXT NOT NULL,
                        description TEXT,
                        permissions TEXT NOT NULL,
                        parent_role TEXT,
                        created_by INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active INTEGER DEFAULT 1,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                """)
                
                # Create role_permissions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS role_permissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role_name TEXT NOT NULL,
                        permission_name TEXT NOT NULL,
                        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        granted_by INTEGER,
                        FOREIGN KEY (granted_by) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
                logger.info("RBAC database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize RBAC database: {e}")
            raise
    
    def get_user_roles(self, user_id: int) -> Set[str]:
        """Get all roles assigned to a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT role_name FROM user_roles 
                    WHERE user_id = ? AND is_active = 1
                """, (user_id,))
                
                roles = {row[0] for row in cursor.fetchall()}
                return roles
                
        except Exception as e:
            logger.error(f"Failed to get roles for user {user_id}: {e}")
            return set()
    
    def get_user_permissions(self, user_id: int) -> Set[Permission]:
        """Get all permissions for a user based on their roles"""
        try:
            user_roles = self.get_user_roles(user_id)
            all_permissions = set()
            
            for role_name in user_roles:
                role_permissions = self.permissions.get_role_permissions(role_name)
                all_permissions.update(role_permissions)
            
            return all_permissions
            
        except Exception as e:
            logger.error(f"Failed to get permissions for user {user_id}: {e}")
            return set()
    
    def list_roles(self) -> Dict[str, RoleDefinition]:
        """List all available roles"""
        return self.permissions.get_default_roles()
    
    def get_role_hierarchy(self) -> Dict[str, str]:
        """Get role hierarchy"""
        return self.permissions.get_role_hierarchy()
    
    def get_role_info(self, role_name: str) -> Optional[RoleDefinition]:
        """Get information about a specific role"""
        roles = self.permissions.get_default_roles()
        return roles.get(role_name)
