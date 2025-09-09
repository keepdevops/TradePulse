#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Callbacks Manager
Callback management for the dashboard manager
"""

import logging

logger = logging.getLogger(__name__)

class DashboardManagerCallbacks:
    """Callback management for dashboard manager"""
    
    def __init__(self, core_manager):
        self.core_manager = core_manager
        self.refresh_callback = None
    
    def on_role_change(self, event):
        """Handle role change events"""
        try:
            # Handle tuple format from Select widget
            if isinstance(event.new, tuple):
                self.core_manager.current_role = event.new[1]  # Get the UserRole object from tuple
            else:
                self.core_manager.current_role = event.new
            
            logger.info(f"🔄 User role changed to: {self.core_manager.current_role.value}")
            # Trigger dashboard refresh
            if self.refresh_callback:
                self.refresh_callback()
        except Exception as e:
            logger.error(f"Failed to handle role change: {e}")
    
    def set_refresh_callback(self, callback):
        """Set callback function to refresh dashboard"""
        self.refresh_callback = callback
        logger.info("✅ Refresh callback set")
    
    def on_search_input(self, event):
        """Handle search input events"""
        try:
            search_term = event.new
            logger.info(f"🔍 Search term entered: {search_term}")
            
            # Here you would implement search functionality
            # For now, just log the search term
            
        except Exception as e:
            logger.error(f"Failed to handle search input: {e}")
    
    def on_panel_error(self, panel_name: str, error: str):
        """Handle panel loading errors"""
        try:
            logger.error(f"❌ Panel error for {panel_name}: {error}")
            
            # Here you would implement error handling
            # For now, just log the error
            
        except Exception as e:
            logger.error(f"Failed to handle panel error: {e}")
    
    def on_layout_change(self, layout_type: str):
        """Handle layout change events"""
        try:
            logger.info(f"🎨 Layout changed to: {layout_type}")
            
            # Here you would implement layout change handling
            # For now, just log the change
            
        except Exception as e:
            logger.error(f"Failed to handle layout change: {e}")
    
    def on_dashboard_refresh(self):
        """Handle dashboard refresh events"""
        try:
            logger.info("🔄 Dashboard refresh triggered")
            
            # Here you would implement dashboard refresh logic
            # For now, just log the refresh
            
        except Exception as e:
            logger.error(f"Failed to handle dashboard refresh: {e}")
    
    def on_role_validation(self, role: str) -> bool:
        """Validate role changes"""
        try:
            valid_roles = ['day_trader', 'ml_analyst', 'trend_analyst', 'default']
            is_valid = role in valid_roles
            
            if is_valid:
                logger.info(f"✅ Role validation passed: {role}")
            else:
                logger.warning(f"⚠️ Invalid role attempted: {role}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Failed to validate role: {e}")
            return False

