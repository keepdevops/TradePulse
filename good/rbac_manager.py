#!/usr/bin/env python3
"""
TradePulse RBAC Manager
Manages user role assignments and permission checking
"""

import logging
from typing import Dict, List, Set, Optional
from .rbac_core import RBACCore, Permission, Role

logger = logging.getLogger(__name__)

class RBACManager:
    """Manages user role assignments and permission checking"""
    
    def __init__(self, db_path: str = "tradepulse_auth.db"):
        self.core = RBACCore(db_path)
        self.user_roles = {}  # user_id -> role
        self.user_permissions = {}  # user_id -> set of permissions
    
    def init_database(self):
        """Initialize RBAC database"""
        try:
            self.core.init_database()
            logger.info("RBAC database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RBAC database: {e}")
            raise
    
    def assign_role_to_user(self, user_id: int, role: str) -> bool:
        """Assign a role to a user"""
        try:
            # Get available roles from core
            available_roles = self.core.list_roles()
            if role not in available_roles:
                logger.error(f"Invalid role: {role}")
                return False
            
            self.user_roles[user_id] = role
            self.user_permissions[user_id] = self._get_user_permissions(user_id)
            
            logger.info(f"Role {role} assigned to user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to assign role {role} to user {user_id}: {e}")
            return False
    
    def remove_user_role(self, user_id: int) -> bool:
        """Remove role from user"""
        try:
            if user_id in self.user_roles:
                del self.user_roles[user_id]
            
            if user_id in self.user_permissions:
                del self.user_permissions[user_id]
            
            logger.info(f"Role removed from user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove role from user {user_id}: {e}")
            return False
    
    def _get_user_permissions(self, user_id: int) -> Set[Permission]:
        """Get all permissions for a user including inherited ones"""
        if user_id not in self.user_roles:
            return set()
        
        role_name = self.user_roles[user_id]
        permissions = set()
        
        # Get permissions from current role and inherited roles
        current_role = role_name
        while current_role:
            role_permissions = self.core.get_user_permissions(user_id)
            if role_permissions:
                permissions.update(role_permissions)
            break  # For now, just get direct permissions
        
        return permissions
    
    def user_has_permission(self, user_id: int, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        try:
            if user_id not in self.user_permissions:
                return False
            
            return permission in self.user_permissions[user_id]
            
        except Exception as e:
            logger.error(f"Failed to check permission for user {user_id}: {e}")
            return False
    
    def user_has_any_permission(self, user_id: int, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions"""
        try:
            if user_id not in self.user_permissions:
                return False
            
            user_perms = self.user_permissions[user_id]
            return any(perm in user_perms for perm in permissions)
            
        except Exception as e:
            logger.error(f"Failed to check permissions for user {user_id}: {e}")
            return False
    
    def user_has_all_permissions(self, user_id: int, permissions: List[Permission]) -> bool:
        """Check if user has all of the specified permissions"""
        try:
            if user_id not in self.user_permissions:
                return False
            
            user_perms = self.user_permissions[user_id]
            return all(perm in user_perms for perm in permissions)
            
        except Exception as e:
            logger.error(f"Failed to check permissions for user {user_id}: {e}")
            return False
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Get the role assigned to a user"""
        return self.user_roles.get(user_id)
    
    def get_user_permissions(self, user_id: int) -> Set[Permission]:
        """Get all permissions for a user"""
        if user_id not in self.user_permissions:
            return set()
        return self.user_permissions[user_id].copy()
    
    def get_users_with_role(self, role_name: str) -> List[int]:
        """Get list of user IDs with a specific role"""
        return [user_id for user_id, role in self.user_roles.items() if role == role_name]
    
    def create_custom_role(self, name: str, description: str, 
                          permissions: List[Permission], 
                          inherits_from: str = None) -> bool:
        """Create a custom role (admin only)"""
        try:
            if name in self.core.roles:
                logger.warning(f"Role {name} already exists")
                return False
            
            # Validate inherited role
            if inherits_from and inherits_from not in self.core.roles:
                logger.error(f"Invalid inherited role: {inherits_from}")
                return False
            
            # Create custom role
            from .rbac_core import RoleDefinition
            self.core.roles[name] = RoleDefinition(
                name=name,
                description=description,
                permissions=set(permissions),
                inherits_from=inherits_from
            )
            
            logger.info(f"Custom role {name} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create custom role {name}: {e}")
            return False
    
    def delete_custom_role(self, name: str) -> bool:
        """Delete a custom role (admin only)"""
        try:
            if name not in self.core.roles:
                logger.warning(f"Role {name} does not exist")
                return False
            
            # Check if role is assigned to any users
            if name in self.user_roles.values():
                logger.error(f"Cannot delete role {name} - assigned to users")
                return False
            
            # Only allow deletion of custom roles
            if name in [role.value for role in Role]:
                logger.error(f"Cannot delete system role: {name}")
                return False
            
            del self.core.roles[name]
            logger.info(f"Custom role {name} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete custom role {name}: {e}")
            return False
    
    # Delegate core RBAC methods
    def get_role_permissions(self, role_name: str) -> Set[Permission]:
        return self.core.get_role_permissions(role_name)
    
    def list_roles(self) -> list:
        return self.core.list_roles()
    
    def get_role_hierarchy(self) -> Dict[str, list]:
        return self.core.get_role_hierarchy()
