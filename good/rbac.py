#!/usr/bin/env python3
"""
TradePulse Role-Based Access Control (RBAC)
Main RBAC module - imports from rbac_core and rbac_manager
"""

from .rbac_core import Permission, Role, RoleDefinition, RBACCore
from .rbac_manager import RBACManager

# Re-export all RBAC classes for backward compatibility
class RoleBasedAccessControl(RBACManager):
    """Main RBAC class - extends RBACManager for backward compatibility"""
    
    def __init__(self, db_path: str = "tradepulse_auth.db"):
        super().__init__(db_path)
    
    # Additional methods can be added here if needed
