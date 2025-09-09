#!/usr/bin/env python3
"""
Dashboard Manager for Role-Based Dashboard Layouts
Implements the dashboard customization system from SSD V10.11
REFACTORED: Now uses modular components to stay under 200 lines
"""

import panel as pn
import logging
from typing import Dict, Any, Optional
from enum import Enum

from .dashboard_manager_refactored import DashboardManager as RefactoredDashboardManager

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User role enumeration"""
    DAY_TRADER = "day_trader"
    ML_ANALYST = "ml_analyst"
    TREND_ANALYST = "trend_analyst"
    DEFAULT = "default"

class DashboardManager:
    """Manages role-based dashboard layouts"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_manager = RefactoredDashboardManager()
        
    def create_role_switcher(self):
        """Create role selection component"""
        # Delegate to refactored implementation
        return self._refactored_manager.create_role_switcher()
    
    def on_role_change(self, event):
        """Handle role change events"""
        # Delegate to refactored implementation
        self._refactored_manager.on_role_change(event)
    
    def set_refresh_callback(self, callback):
        """Set callback function to refresh dashboard"""
        # Delegate to refactored implementation
        self._refactored_manager.set_refresh_callback(callback)
    
    def get_current_role(self) -> UserRole:
        """Get current user role"""
        # Delegate to refactored implementation
        return self._refactored_manager.get_current_role()
    
    def create_dashboard(self, panels: Dict[str, Any]) -> pn.Column:
        """Create dashboard based on current role"""
        # Delegate to refactored implementation
        return self._refactored_manager.create_dashboard(panels)
