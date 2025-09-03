#!/usr/bin/env python3
"""
TradePulse Authentication System
Complete authentication and authorization system
"""

# Core authentication classes
from .auth_service import AuthService
from .user_manager import UserManager
from .rbac import RoleBasedAccessControl, Permission, Role
from .session_manager import SessionManager

# Core data models
from .user_core import User, UserCore
from .session_core import Session, SessionCore

# Security utilities
from .security_utils import SecurityUtils
from .security_core import SecurityCore
from .security_extended import SecurityExtended

# RBAC components
from .rbac_core import RBACCore
from .rbac_manager import RBACManager
from .rbac_permissions import Permission, Role, RoleDefinition, RBACPermissions
from .rbac_permissions_core import Permission, Role, RoleDefinition
from .rbac_role_definitions import RBACRoleDefinitions

# Session management components
from .session_storage import SessionStorage
from .session_validation import SessionValidation
from .session_db_ops import SessionDatabaseOperations
from .session_query_ops import SessionQueryOperations
from .session_maintenance_ops import SessionMaintenanceOperations

# User management components
from .user_db_ops import UserDatabaseOperations
from .user_crud_ops import UserCRUDOperations
from .user_update_ops import UserUpdateOperations
from .user_activity_ops import UserActivityOperations
from .user_activity_core import UserActivityCore
from .user_activity_advanced import UserActivityAdvanced

# Authentication operation modules
from .auth_core import AuthCore
from .auth_user_ops import AuthUserOperations
from .auth_session_ops import AuthSessionOperations
from .auth_admin_ops import AuthAdminOperations
from .auth_security_ops import AuthSecurityOperations
from .auth_maintenance_ops import AuthMaintenanceOperations

# Export main classes for backward compatibility
__all__ = [
    # Main service classes
    'AuthService',
    'UserManager',
    'RoleBasedAccessControl',
    'SessionManager',
    
    # Core data models
    'User',
    'UserCore',
    'Session',
    'SessionCore',
    
    # Security
    'SecurityUtils',
    'SecurityCore',
    'SecurityExtended',
    
    # RBAC
    'Permission',
    'Role',
    'RoleDefinition',
    'RBACCore',
    'RBACManager',
    'RBACPermissions',
    
    # Session management
    'SessionStorage',
    'SessionValidation',
    'SessionDatabaseOperations',
    'SessionQueryOperations',
    'SessionMaintenanceOperations',
    
    # User management
    'UserDatabaseOperations',
    'UserCRUDOperations',
    'UserUpdateOperations',
    'UserActivityOperations',
    
    # Authentication operations
    'AuthCore',
    'AuthUserOperations',
    'AuthSessionOperations',
    'AuthAdminOperations',
    'AuthSecurityOperations',
    'AuthMaintenanceOperations',
]
