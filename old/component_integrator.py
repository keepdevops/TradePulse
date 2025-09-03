#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Component Integrator
Handles setup of component integration
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ComponentIntegrator:
    """Handles setup of component integration"""
    
    def __init__(self, integrated_ui):
        self.integrated_ui = integrated_ui
    
    def setup_integration(self):
        """Setup integration between components"""
        try:
            logger.info("🔧 Setting up component integration")
            
            # Setup TradePulse integration callbacks
            self._setup_tradepulse_callbacks()
            
            # Setup UI orchestrator callbacks
            self._setup_ui_orchestrator_callbacks()
            
            # Setup system monitor callbacks
            self._setup_system_monitor_callbacks()
            
            # Setup performance tracker callbacks
            self._setup_performance_tracker_callbacks()
            
            logger.info("✅ Component integration setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup component integration: {e}")
    
    def _setup_tradepulse_callbacks(self):
        """Setup TradePulse integration callbacks"""
        try:
            if hasattr(self.integrated_ui.tradepulse_integration, 'message_bus'):
                self.integrated_ui.tradepulse_integration.message_bus.subscribe('system_alert', self._handle_system_alert)
                self.integrated_ui.tradepulse_integration.message_bus.subscribe('performance_update', self._handle_performance_update)
                
        except Exception as e:
            logger.error(f"Failed to setup TradePulse callbacks: {e}")
    
    def _setup_ui_orchestrator_callbacks(self):
        """Setup UI orchestrator callbacks"""
        try:
            if hasattr(self.integrated_ui.ui_orchestrator, 'add_callback'):
                self.integrated_ui.ui_orchestrator.add_callback('refresh', self._handle_ui_refresh)
                self.integrated_ui.ui_orchestrator.add_callback('export', self._handle_ui_export)
                
        except Exception as e:
            logger.error(f"Failed to setup UI orchestrator callbacks: {e}")
    
    def _setup_system_monitor_callbacks(self):
        """Setup system monitor callbacks"""
        try:
            if hasattr(self.integrated_ui.system_monitor, 'add_callback'):
                self.integrated_ui.system_monitor.add_callback('alert', self._handle_monitor_alert)
                
        except Exception as e:
            logger.error(f"Failed to setup system monitor callbacks: {e}")
    
    def _setup_performance_tracker_callbacks(self):
        """Setup performance tracker callbacks"""
        try:
            if hasattr(self.integrated_ui.performance_tracker, 'add_callback'):
                self.integrated_ui.performance_tracker.add_callback('optimization_suggestion', self._handle_optimization_suggestion)
                
        except Exception as e:
            logger.error(f"Failed to setup performance tracker callbacks: {e}")
    
    def _handle_system_alert(self, alert_data):
        """Handle system alerts from TradePulse integration"""
        try:
            logger.warning(f"⚠️ System alert received: {alert_data}")
            
            # Forward alert to system monitor
            if hasattr(self.integrated_ui.system_monitor, 'add_system_alert'):
                self.integrated_ui.system_monitor.add_system_alert(alert_data)
            
        except Exception as e:
            logger.error(f"Failed to handle system alert: {e}")
    
    def _handle_performance_update(self, performance_data):
        """Handle performance updates from TradePulse integration"""
        try:
            logger.debug(f"📊 Performance update received: {performance_data}")
            
            # Update performance tracker if needed
            if hasattr(self.integrated_ui.performance_tracker, 'update_performance_data'):
                self.integrated_ui.performance_tracker.update_performance_data(performance_data)
            
        except Exception as e:
            logger.error(f"Failed to handle performance update: {e}")
    
    def _handle_ui_refresh(self):
        """Handle UI refresh requests"""
        try:
            logger.info("🔄 UI refresh requested")
            
            # Refresh all components
            self._refresh_all_components()
            
        except Exception as e:
            logger.error(f"Failed to handle UI refresh: {e}")
    
    def _handle_ui_export(self):
        """Handle UI export requests"""
        try:
            logger.info("📤 UI export requested")
            
            # Export all component data
            export_data = self._export_all_component_data()
            
            logger.info(f"📊 Export completed: {len(export_data)} components exported")
            
        except Exception as e:
            logger.error(f"Failed to handle UI export: {e}")
    
    def _handle_monitor_alert(self, alert_data):
        """Handle alerts from system monitor"""
        try:
            logger.warning(f"⚠️ Monitor alert: {alert_data}")
            
            # Send alert to TradePulse message bus
            if hasattr(self.integrated_ui.tradepulse_integration, 'message_bus'):
                self.integrated_ui.tradepulse_integration.message_bus.send_message('monitor_alert', alert_data)
            
        except Exception as e:
            logger.error(f"Failed to handle monitor alert: {e}")
    
    def _handle_optimization_suggestion(self, suggestion_data):
        """Handle optimization suggestions from performance tracker"""
        try:
            logger.info(f"💡 Optimization suggestion: {suggestion_data}")
            
            # Send suggestion to TradePulse message bus
            if hasattr(self.integrated_ui.tradepulse_integration, 'message_bus'):
                self.integrated_ui.tradepulse_integration.message_bus.send_message('optimization_suggestion', suggestion_data)
            
        except Exception as e:
            logger.error(f"Failed to handle optimization suggestion: {e}")
    
    def _refresh_all_components(self):
        """Refresh all integrated components"""
        try:
            logger.info("🔄 Refreshing all components")
            
            # Refresh TradePulse integration
            if hasattr(self.integrated_ui.tradepulse_integration, 'refresh_components'):
                self.integrated_ui.tradepulse_integration.refresh_components()
            
            # Refresh UI orchestrator
            if hasattr(self.integrated_ui.ui_orchestrator, 'refresh_component'):
                self.integrated_ui.ui_orchestrator.refresh_component()
            
            # Refresh system monitor
            if hasattr(self.integrated_ui.system_monitor, 'refresh_component'):
                self.integrated_ui.system_monitor.refresh_component()
            
            # Refresh performance tracker
            if hasattr(self.integrated_ui.performance_tracker, 'refresh_component'):
                self.integrated_ui.performance_tracker.refresh_component()
            
            logger.info("✅ All components refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh all components: {e}")
    
    def _export_all_component_data(self) -> Dict[str, Any]:
        """Export data from all components"""
        try:
            export_data = {}
            
            # Export TradePulse integration data
            if hasattr(self.integrated_ui.tradepulse_integration, 'export_integration_state'):
                export_data['tradepulse_integration'] = self.integrated_ui.tradepulse_integration.export_integration_state()
            
            # Export UI orchestrator data
            if hasattr(self.integrated_ui.ui_orchestrator, 'export_component_data'):
                export_data['ui_orchestrator'] = self.integrated_ui.ui_orchestrator.export_component_data()
            
            # Export system monitor data
            if hasattr(self.integrated_ui.system_monitor, 'export_monitoring_data'):
                export_data['system_monitor'] = self.integrated_ui.system_monitor.export_monitoring_data()
            
            # Export performance tracker data
            if hasattr(self.integrated_ui.performance_tracker, 'export_performance_data'):
                export_data['performance_tracker'] = self.integrated_ui.performance_tracker.export_performance_data()
            
            # Add export metadata
            from datetime import datetime
            export_data['export_metadata'] = {
                'export_timestamp': datetime.now().isoformat(),
                'component_count': len(export_data),
                'export_version': '1.0'
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export all component data: {e}")
            return {}
