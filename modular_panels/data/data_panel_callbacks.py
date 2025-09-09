#!/usr/bin/env python3
"""
TradePulse Data Panel - Callbacks
Data panel callback functionality
"""

import panel as pn
import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class DataPanelCallbacks:
    """Data panel callback functionality"""
    
    def __init__(self, core_panel):
        self.core = core_panel
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        try:
            symbol = event.new
            logger.info(f"🔄 Symbol changed to {symbol}")
            
            # Create sample data safely
            sample_data = self.core.operations.create_sample_data()
            
            # Update table value safely
            if hasattr(self.core.components, 'data_table') and self.core.components.data_table is not None:
                self.core.components.data_table.value = sample_data
            else:
                logger.warning("⚠️ Data table component not available")
                
        except Exception as e:
            logger.error(f"❌ Failed to handle symbol change: {e}")
    
    def on_date_range_change(self, event):
        """Handle date range preset change"""
        try:
            preset = event.new
            logger.info(f"📅 Date range preset changed to: {preset}")
            
            # Calculate date range based on preset
            now = pd.Timestamp.now()
            
            if preset == 'Last 7 Days':
                start_date = now - pd.Timedelta(days=7)
            elif preset == 'Last 30 Days':
                start_date = now - pd.Timedelta(days=30)
            elif preset == 'Last 90 Days':
                start_date = now - pd.Timedelta(days=90)
            elif preset == 'Last 6 Months':
                start_date = now - pd.Timedelta(days=180)
            elif preset == 'Last 1 Year':
                start_date = now - pd.Timedelta(days=365)
            elif preset == 'Last 2 Years':
                start_date = now - pd.Timedelta(days=730)
            elif preset == 'Last 5 Years':
                start_date = now - pd.Timedelta(days=1825)
            elif preset == 'Last 10 Years':
                start_date = now - pd.Timedelta(days=3650)
            elif preset == 'All Available Data':
                start_date = pd.Timestamp('2010-01-01')  # Default to 2010
            else:  # Custom Range
                # Keep current values
                return
            
            # Update date pickers
            self.core.components.start_date_picker.value = start_date
            self.core.components.end_date_picker.value = now
            
            logger.info(f"📅 Updated date range: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to handle date range change: {e}")
    
    def quick_export(self, event):
        """Quick export current data"""
        current_data = self.core.components.data_table.value
        if current_data is None or current_data.empty:
            current_data = self.core.operations.create_sample_data()
        
        result = self.core.export.quick_export_csv(current_data)
        self.core.components.export_dialog.object = result
    
    def clear_data(self, event):
        """Clear current data"""
        try:
            self.core.components.data_table.value = pd.DataFrame()
            self.core.components.data_stats.object = self.core.operations.get_clear_statistics()
            logger.info("Data cleared successfully")
        except Exception as e:
            logger.error(f"Clear data failed: {e}")
