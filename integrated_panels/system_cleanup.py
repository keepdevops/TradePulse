#!/usr/bin/env python3
"""
TradePulse Integrated Panels - System Cleanup
Handles system cleanup functionality
"""

import logging

logger = logging.getLogger(__name__)

class SystemCleanup:
    """Handles system cleanup functionality"""
    
    def __init__(self, integrated_ui):
        self.integrated_ui = integrated_ui
    
    def cleanup_system(self):
        """Cleanup the integrated system"""
        try:
            logger.info("🧹 Cleaning up integrated system")
            
            # Stop all updates
            self.integrated_ui.stop_integrated_updates()
            
            # Clear component data
            self._clear_component_data()
            
            logger.info("✅ Integrated system cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup integrated system: {e}")
    
    def _clear_component_data(self):
        """Clear component data"""
        try:
            # Clear TradePulse integration
            if hasattr(self.integrated_ui.tradepulse_integration, 'clear_component'):
                self.integrated_ui.tradepulse_integration.clear_component()
            
            # Clear UI orchestrator
            if hasattr(self.integrated_ui.ui_orchestrator, 'clear_component'):
                self.integrated_ui.ui_orchestrator.clear_component()
            
            # Clear system monitor
            if hasattr(self.integrated_ui.system_monitor, 'clear_component'):
                self.integrated_ui.system_monitor.clear_component()
            
            # Clear performance tracker
            if hasattr(self.integrated_ui.performance_tracker, 'clear_component'):
                self.integrated_ui.performance_tracker.clear_component()
                
        except Exception as e:
            logger.error(f"Failed to clear component data: {e}")
