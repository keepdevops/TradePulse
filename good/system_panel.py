#!/usr/bin/env python3
"""
TradePulse Modular Panels - System Panel
System status and configuration panel
"""

import panel as pn
import logging
from . import BasePanel
from .system_operations import SystemOperations

logger = logging.getLogger(__name__)

class SystemPanel(BasePanel):
    """System status and configuration panel"""
    
    def __init__(self):
        super().__init__("System")
    
    def init_panel(self):
        """Initialize system panel components"""
        # System status indicators
        self.components['message_bus_status'] = pn.indicators.Number(
            name='Message Bus',
            value=1,
            format='{value}',
            width=100
        )
        
        self.components['database_status'] = pn.indicators.Number(
            name='Database',
            value=1,
            format='{value}',
            width=100
        )
        
        self.components['ml_models_status'] = pn.indicators.Number(
            name='ML Models',
            value=1,
            format='{value}',
            width=100
        )
        
        self.components['data_feed_status'] = pn.indicators.Number(
            name='Data Feed',
            value=1,
            format='{value}',
            width=100
        )
        
        # System controls
        self.components['start_all_button'] = pn.widgets.Button(
            name='🚀 Start All Services',
            button_type='success',
            width=140
        )
        
        self.components['stop_all_button'] = pn.widgets.Button(
            name='⏹️ Stop All Services',
            button_type='danger',
            width=140
        )
        
        self.components['restart_button'] = pn.widgets.Button(
            name='🔄 Restart System',
            button_type='warning',
            width=120
        )
        
        # System metrics table
        self.components['system_metrics'] = pn.widgets.Tabulator(
            SystemOperations.create_system_metrics(),
            height=200
        )
        
        # System logs
        self.components['system_logs'] = pn.pane.Markdown("""
        ### 📋 System Logs
        - **14:35:12**: System startup completed
        - **14:34:58**: Database connection established
        - **14:34:45**: Message bus initialized
        - **14:34:30**: ML models loaded successfully
        - **14:34:15**: Data feed connected
        """)
        
        # Configuration settings
        self.components['config_settings'] = pn.pane.Markdown("""
        ### ⚙️ System Configuration
        - **Environment**: Production
        - **Log Level**: INFO
        - **Auto-restart**: Enabled
        - **Backup**: Daily at 02:00
        - **Monitoring**: Enabled
        """)
        
        # Setup callbacks
        self.components['start_all_button'].on_click(self.start_all_services)
        self.components['stop_all_button'].on_click(self.stop_all_services)
        self.components['restart_button'].on_click(self.restart_system)
    
    def get_panel(self):
        """Get the system panel layout"""
        status_indicators = pn.Row(
            self.components['message_bus_status'],
            self.components['database_status'],
            self.components['ml_models_status'],
            self.components['data_feed_status'],
            align='center'
        )
        
        controls = pn.Row(
            self.components['start_all_button'],
            self.components['stop_all_button'],
            self.components['restart_button'],
            align='center'
        )
        
        return pn.Column(
            pn.pane.Markdown("### ⚙️ System Status & Configuration"),
            status_indicators,
            controls,
            pn.pane.Markdown("#### System Metrics"),
            self.components['system_metrics'],
            self.components['system_logs'],
            self.components['config_settings'],
            sizing_mode='stretch_width'
        )
    
    def start_all_services(self, event):
        """Start all system services"""
        new_entry = SystemOperations.start_all_services(self.components)
        self.components['system_logs'].object = SystemOperations.update_system_logs(
            self.components['system_logs'].object, new_entry
        )
    
    def stop_all_services(self, event):
        """Stop all system services"""
        new_entry = SystemOperations.stop_all_services(self.components)
        self.components['system_logs'].object = SystemOperations.update_system_logs(
            self.components['system_logs'].object, new_entry
        )
    
    def restart_system(self, event):
        """Restart the entire system"""
        new_entry = SystemOperations.restart_system(self.components)
        self.components['system_logs'].object = SystemOperations.update_system_logs(
            self.components['system_logs'].object, new_entry
        )
