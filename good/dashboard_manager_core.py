#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Core Functionality
Core dashboard manager class with basic functionality
"""

import panel as pn
import logging
from typing import Dict, Any, Optional
from enum import Enum

from .dashboard_manager_components import DashboardManagerComponents
from .dashboard_manager_operations import DashboardManagerOperations
from .dashboard_manager_management import DashboardManagerManagement
from .dashboard_manager_layout import DashboardManagerLayout
from .dashboard_manager_callbacks import DashboardManagerCallbacks

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User role enumeration"""
    DAY_TRADER = "day_trader"
    ML_ANALYST = "ml_analyst"
    TREND_ANALYST = "trend_analyst"
    DEFAULT = "default"

class DashboardManagerCore:
    """Core dashboard manager functionality"""
    
    def __init__(self):
        self.current_role = UserRole.DEFAULT
        self.role_switcher = None
        self.dashboard_layout = None
        
        # Initialize components
        self.components = DashboardManagerComponents()
        self.operations = DashboardManagerOperations()
        self.management = DashboardManagerManagement()
        self.layout = DashboardManagerLayout()
        self.callbacks = DashboardManagerCallbacks(self)
    
    def create_role_switcher(self):
        """Create role selection component"""
        try:
            self.role_switcher = pn.widgets.Select(
                name="🎭 User Role",
                options=[
                    ("Day Trader", UserRole.DAY_TRADER),
                    ("ML AI Analyst", UserRole.ML_ANALYST),
                    ("Trend Analyst", UserRole.TREND_ANALYST),
                    ("Default", UserRole.DEFAULT)
                ],
                value=UserRole.DEFAULT,
                width=200
            )
            self.role_switcher.param.watch(self.callbacks.on_role_change, 'value')
            return self.role_switcher
        except Exception as e:
            logger.error(f"Failed to create role switcher: {e}")
            return pn.pane.Markdown("Role switcher unavailable")
    
    def set_refresh_callback(self, callback):
        """Set callback function to refresh dashboard"""
        self.callbacks.set_refresh_callback(callback)
    
    def get_current_role(self) -> UserRole:
        """Get current user role"""
        return self.current_role
    
    def create_dashboard(self, panels: Dict[str, Any]) -> pn.Column:
        """Create dashboard based on current role"""
        try:
            # Create role switcher if not exists
            if self.role_switcher is None:
                self.create_role_switcher()
            
            # Create layout based on current role
            if self.current_role == UserRole.DAY_TRADER:
                return self.management.create_day_trader_layout(panels, self.role_switcher)
            elif self.current_role == UserRole.ML_ANALYST:
                return self.management.create_ml_analyst_layout(panels, self.role_switcher)
            elif self.current_role == UserRole.TREND_ANALYST:
                return self.management.create_trend_analyst_layout(panels, self.role_switcher)
            else:
                return self.layout.create_default_layout(panels, self.role_switcher)
                
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            return pn.Column("Error: Failed to create dashboard")
    
    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get dashboard information"""
        return {
            'current_role': self.current_role.value,
            'role_switcher_created': self.role_switcher is not None,
            'dashboard_layout_created': self.dashboard_layout is not None,
            'available_roles': [role.value for role in UserRole],
            'manager_type': 'Dashboard Manager'
        }
