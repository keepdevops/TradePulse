#!/usr/bin/env python3
"""
TradePulse RBAC Role Definitions
Role definitions with permissions and hierarchy
"""

from typing import Dict, Set
from .rbac_permissions_core import Permission, RoleDefinition

class RBACRoleDefinitions:
    """RBAC role definitions management"""
    
    @staticmethod
    def get_role_hierarchy() -> Dict[str, str]:
        """Get role hierarchy (parent -> child relationships)"""
        return {
            "guest": None,
            "user": "guest",
            "trader": "user",
            "analyst": "user",
            "manager": "trader",
            "admin": "manager",
            "super_admin": "admin"
        }
    
    @staticmethod
    def get_default_roles() -> Dict[str, RoleDefinition]:
        """Get default system roles with their permissions"""
        return {
            "guest": RoleDefinition(
                name="guest",
                display_name="Guest",
                description="Limited read-only access to public information",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA
                }
            ),
            "user": RoleDefinition(
                name="user",
                display_name="User",
                description="Basic user with limited trading capabilities",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA,
                    Permission.VIEW_TRADES,
                    Permission.VIEW_PORTFOLIO,
                    Permission.VIEW_ALERTS,
                    Permission.VIEW_REPORTS
                },
                parent_role="guest"
            ),
            "trader": RoleDefinition(
                name="trader",
                display_name="Trader",
                description="Active trader with full trading capabilities",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA,
                    Permission.VIEW_TRADES,
                    Permission.EXECUTE_TRADES,
                    Permission.VIEW_PORTFOLIO,
                    Permission.MANAGE_PORTFOLIO,
                    Permission.VIEW_ALERTS,
                    Permission.MANAGE_ALERTS,
                    Permission.VIEW_REPORTS,
                    Permission.GENERATE_REPORTS
                },
                parent_role="user"
            ),
            "analyst": RoleDefinition(
                name="analyst",
                display_name="Analyst",
                description="Data analyst with advanced analysis capabilities",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA,
                    Permission.MANAGE_DATA,
                    Permission.VIEW_TRADES,
                    Permission.VIEW_PORTFOLIO,
                    Permission.VIEW_AI_MODELS,
                    Permission.TRAIN_AI_MODELS,
                    Permission.VIEW_ALERTS,
                    Permission.VIEW_REPORTS,
                    Permission.GENERATE_REPORTS
                },
                parent_role="user"
            ),
            "manager": RoleDefinition(
                name="manager",
                display_name="Manager",
                description="Team manager with oversight capabilities",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA,
                    Permission.MANAGE_DATA,
                    Permission.VIEW_TRADES,
                    Permission.MANAGE_TRADES,
                    Permission.VIEW_PORTFOLIO,
                    Permission.MANAGE_PORTFOLIO,
                    Permission.VIEW_AI_MODELS,
                    Permission.MANAGE_AI_MODELS,
                    Permission.VIEW_ALERTS,
                    Permission.MANAGE_ALERTS,
                    Permission.VIEW_REPORTS,
                    Permission.MANAGE_REPORTS,
                    Permission.VIEW_USERS,
                    Permission.VIEW_SESSIONS
                },
                parent_role="trader"
            ),
            "admin": RoleDefinition(
                name="admin",
                display_name="Administrator",
                description="System administrator with full system access",
                permissions={
                    Permission.ACCESS_SYSTEM,
                    Permission.VIEW_DATA,
                    Permission.MANAGE_DATA,
                    Permission.VIEW_TRADES,
                    Permission.MANAGE_TRADES,
                    Permission.VIEW_PORTFOLIO,
                    Permission.MANAGE_PORTFOLIO,
                    Permission.VIEW_AI_MODELS,
                    Permission.MANAGE_AI_MODELS,
                    Permission.VIEW_ALERTS,
                    Permission.MANAGE_ALERTS,
                    Permission.VIEW_REPORTS,
                    Permission.MANAGE_REPORTS,
                    Permission.VIEW_USERS,
                    Permission.CREATE_USERS,
                    Permission.EDIT_USERS,
                    Permission.MANAGE_USERS,
                    Permission.VIEW_SESSIONS,
                    Permission.MANAGE_SESSIONS,
                    Permission.VIEW_LOGS,
                    Permission.MANAGE_SYSTEM
                },
                parent_role="manager"
            ),
            "super_admin": RoleDefinition(
                name="super_admin",
                display_name="Super Administrator",
                description="Super administrator with all permissions",
                permissions=set(Permission),  # All permissions
                parent_role="admin"
            )
        }
    
    @staticmethod
    def get_role_permissions(role_name: str) -> Set[Permission]:
        """Get permissions for a specific role"""
        roles = RBACRoleDefinitions.get_default_roles()
        if role_name not in roles:
            return set()
        
        role = roles[role_name]
        permissions = role.permissions.copy()
        
        # Add inherited permissions from parent roles
        current_role = role
        while current_role.parent_role:
            parent_role = roles.get(current_role.parent_role)
            if parent_role:
                permissions.update(parent_role.permissions)
                current_role = parent_role
            else:
                break
        
        return permissions
