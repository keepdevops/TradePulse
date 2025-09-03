#!/usr/bin/env python3
"""
TradePulse RBAC Permissions
Main RBAC permissions coordinator
"""

from .rbac_permissions_core import Permission, Role, RoleDefinition
from .rbac_role_definitions import RBACRoleDefinitions

class RBACPermissions:
    """RBAC permissions management coordinator"""
    
    @staticmethod
    def get_role_hierarchy() -> dict:
        """Get role hierarchy (parent -> child relationships)"""
        return RBACRoleDefinitions.get_role_hierarchy()
    
    @staticmethod
    def get_default_roles() -> dict:
        """Get default system roles with their permissions"""
        return RBACRoleDefinitions.get_default_roles()
    
    @staticmethod
    def get_role_permissions(role_name: str) -> set:
        """Get permissions for a specific role"""
        return RBACRoleDefinitions.get_role_permissions(role_name)
