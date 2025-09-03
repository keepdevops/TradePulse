#!/usr/bin/env python3
"""
TradePulse RBAC Permissions Core
Core permission and role enums for role-based access control
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Set

class Permission(Enum):
    """System permissions"""
    # User management
    VIEW_USERS = "view_users"
    CREATE_USERS = "create_users"
    EDIT_USERS = "edit_users"
    DELETE_USERS = "delete_users"
    MANAGE_USERS = "manage_users"
    
    # Session management
    VIEW_SESSIONS = "view_sessions"
    MANAGE_SESSIONS = "manage_sessions"
    
    # System access
    ACCESS_SYSTEM = "access_system"
    VIEW_LOGS = "view_logs"
    MANAGE_SYSTEM = "manage_system"
    
    # Trading operations
    VIEW_TRADES = "view_trades"
    EXECUTE_TRADES = "execute_trades"
    MANAGE_TRADES = "manage_trades"
    
    # Portfolio management
    VIEW_PORTFOLIO = "view_portfolio"
    MANAGE_PORTFOLIO = "manage_portfolio"
    
    # Data access
    VIEW_DATA = "view_data"
    MANAGE_DATA = "manage_data"
    
    # AI/ML operations
    VIEW_AI_MODELS = "view_ai_models"
    TRAIN_AI_MODELS = "train_ai_models"
    MANAGE_AI_MODELS = "manage_ai_models"
    
    # Alerts and notifications
    VIEW_ALERTS = "view_alerts"
    MANAGE_ALERTS = "manage_alerts"
    
    # Reports and analytics
    VIEW_REPORTS = "view_reports"
    GENERATE_REPORTS = "generate_reports"
    MANAGE_REPORTS = "manage_reports"

class Role(Enum):
    """System roles"""
    GUEST = "guest"
    USER = "user"
    TRADER = "trader"
    ANALYST = "analyst"
    MANAGER = "manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

@dataclass
class RoleDefinition:
    """Role definition with permissions and hierarchy"""
    name: str
    display_name: str
    description: str
    permissions: Set[Permission]
    parent_role: str = None
    is_system_role: bool = True
