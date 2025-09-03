#!/usr/bin/env python3
"""
TradePulse Modular Panels - System Operations
System operations and data management
"""

import pandas as pd
import logging
import threading
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemOperations:
    """System operations and data management"""
    
    @staticmethod
    def create_system_metrics():
        """Create system metrics data"""
        return pd.DataFrame({
            'Component': ['Message Bus', 'Database', 'ML Models', 'Data Feed', 'Web Server'],
            'Status': ['✅ Online', '✅ Online', '✅ Online', '✅ Online', '✅ Online'],
            'Uptime': ['2h 15m', '2h 15m', '2h 15m', '2h 15m', '2h 15m'],
            'CPU %': [12.5, 8.3, 15.7, 6.2, 4.1],
            'Memory %': [45.2, 32.1, 28.9, 18.5, 12.3],
            'Last Update': ['14:35:12', '14:35:10', '14:35:08', '14:35:05', '14:35:02']
        })
    
    @staticmethod
    def update_system_logs(current_logs, new_entry):
        """Update system logs with new entry"""
        updated_logs = new_entry + "\n" + current_logs.split('\n', 1)[1]
        return updated_logs
    
    @staticmethod
    def start_all_services(components):
        """Start all system services"""
        logger.info("🚀 Starting all system services")
        
        # Update status indicators
        for indicator in [components['message_bus_status'], 
                         components['database_status'],
                         components['ml_models_status'],
                         components['data_feed_status']]:
            indicator.value = 1
        
        return f"- **{datetime.now().strftime('%H:%M:%S')}**: All services started successfully"
    
    @staticmethod
    def stop_all_services(components):
        """Stop all system services"""
        logger.info("⏹️ Stopping all system services")
        
        # Update status indicators
        for indicator in [components['message_bus_status'], 
                         components['database_status'],
                         components['ml_models_status'],
                         components['data_feed_status']]:
            indicator.value = 0
        
        return f"- **{datetime.now().strftime('%H:%M:%S')}**: All services stopped"
    
    @staticmethod
    def restart_system(components):
        """Restart the entire system"""
        logger.info("🔄 Restarting system")
        
        def restart_sequence():
            # Stop services
            for indicator in [components['message_bus_status'], 
                             components['database_status'],
                             components['ml_models_status'],
                             components['data_feed_status']]:
                indicator.value = 0
            
            time.sleep(2)  # Simulate restart time
            
            # Start services
            for indicator in [components['message_bus_status'], 
                             components['database_status'],
                             components['ml_models_status'],
                             components['data_feed_status']]:
                indicator.value = 1
        
        threading.Thread(target=restart_sequence, daemon=True).start()
        
        return f"- **{datetime.now().strftime('%H:%M:%S')}**: System restart initiated"
