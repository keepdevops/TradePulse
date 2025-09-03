#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Main Integrated Panel UI
Main orchestrator for the integrated TradePulse panel system
"""

import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
import json
import threading
import time
from typing import Dict, List, Optional, Any
import logging

# Import integrated panel components
from .tradepulse_integration import TradePulseIntegration
from .ui_orchestrator import UIOrchestrator
from .system_monitor import SystemMonitor
from .performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class TradePulseIntegratedUI:
    """Fully integrated TradePulse Panel UI orchestrator"""
    
    def __init__(self):
        # Configure Panel
        pn.extension('plotly', 'tabulator', sizing_mode='stretch_width')
        pn.config.theme = 'dark'
        
        # Initialize TradePulse components
        self.tradepulse_integration = TradePulseIntegration()
        self.ui_orchestrator = UIOrchestrator()
        self.system_monitor = SystemMonitor()
        self.performance_tracker = PerformanceTracker()
        
        # Initialize UI
        self.init_integrated_ui()
        self.start_integrated_updates()
    
    def init_integrated_ui(self):
        """Initialize the integrated UI system"""
        try:
            logger.info("🔧 Initializing integrated TradePulse UI")
            
            # Create main layout
            self.main_layout = self._create_main_layout()
            
            # Setup component integration
            self._setup_component_integration()
            
            # Setup monitoring and tracking
            self._setup_monitoring_and_tracking()
            
            logger.info("✅ Integrated TradePulse UI initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize integrated UI: {e}")
    
    def _create_main_layout(self) -> pn.Column:
        """Create the main integrated UI layout"""
        try:
            from .integration_status_tab import IntegrationStatusTab
            
            # Create integration status tab
            status_tab = IntegrationStatusTab(self)
            
            # Create tabbed interface
            tabs = pn.Tabs(
                ('Main Trading', self.ui_orchestrator.get_layout()),
                ('System Monitor', self.system_monitor.create_monitoring_dashboard()),
                ('Performance', self.performance_tracker.create_performance_dashboard()),
                ('Integration Status', status_tab.create_status_tab()),
                sizing_mode='stretch_width'
            )
            
            # Create main layout
            main_layout = pn.Column(
                pn.pane.Markdown('# TradePulse Integrated Panel System', style={'color': 'white', 'text-align': 'center'}),
                pn.Spacer(height=20),
                tabs,
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return main_layout
            
        except Exception as e:
            logger.error(f"Failed to create main layout: {e}")
            return pn.Column("Error: Failed to create main layout")
    
    def _setup_component_integration(self):
        """Setup integration between components"""
        try:
            from .component_integrator import ComponentIntegrator
            integrator = ComponentIntegrator(self)
            integrator.setup_integration()
            
        except Exception as e:
            logger.error(f"Failed to setup component integration: {e}")
    
    def _setup_monitoring_and_tracking(self):
        """Setup monitoring and tracking systems"""
        try:
            from .monitoring_setup import MonitoringSetup
            setup = MonitoringSetup(self)
            setup.setup_monitoring()
            
        except Exception as e:
            logger.error(f"Failed to setup monitoring and tracking: {e}")
    
    def start_integrated_updates(self):
        """Start the integrated update system"""
        try:
            logger.info("🔄 Starting integrated update system")
            
            # Start UI updates
            self.ui_orchestrator.start_updates()
            
            logger.info("✅ Integrated update system started")
            
        except Exception as e:
            logger.error(f"Failed to start integrated updates: {e}")
    
    def stop_integrated_updates(self):
        """Stop the integrated update system"""
        try:
            logger.info("🛑 Stopping integrated update system")
            
            # Stop UI updates
            self.ui_orchestrator.stop_updates()
            
            # Stop monitoring
            self.system_monitor.stop_monitoring()
            
            # Stop tracking
            self.performance_tracker.stop_tracking()
            
            logger.info("✅ Integrated update system stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop integrated updates: {e}")
    
    def get_layout(self) -> pn.Column:
        """Get the complete integrated UI layout"""
        try:
            return self.main_layout
        except Exception as e:
            logger.error(f"Failed to get layout: {e}")
            return pn.Column("Error: Failed to get integrated UI layout")
    
    def get_integrated_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the integrated system"""
        try:
            return {
                'tradepulse_integration': self.tradepulse_integration.get_component_status(),
                'ui_orchestrator': self.ui_orchestrator.get_orchestrator_status(),
                'system_monitor': self.system_monitor.get_monitor_status(),
                'performance_tracker': self.performance_tracker.get_tracker_status(),
                'integration_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get integrated status: {e}")
            return {}
    
    def test_integrated_system(self) -> Dict[str, bool]:
        """Test the integrated system functionality"""
        try:
            from .system_tester import SystemTester
            tester = SystemTester(self)
            return tester.test_system()
            
        except Exception as e:
            logger.error(f"Failed to test integrated system: {e}")
            return {'overall': False}
    
    def cleanup_integrated_system(self):
        """Cleanup the integrated system"""
        try:
            from .system_cleanup import SystemCleanup
            cleanup = SystemCleanup(self)
            cleanup.cleanup_system()
            
        except Exception as e:
            logger.error(f"Failed to cleanup integrated system: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.cleanup_integrated_system()
        except Exception:
            pass
