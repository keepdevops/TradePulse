#!/usr/bin/env python3
"""
TradePulse Data Panel - Core Functionality
Core data panel class with basic functionality
"""

import panel as pn
import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional

from .. import BasePanel
from .data_components import DataComponents
from .data_operations import DataOperations
from .data_export import DataExport
from ui_components.module_data_access import ModuleDataAccess

logger = logging.getLogger(__name__)

class DataPanelCore(BasePanel):
    """Core data panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Data", data_manager)
        self.data_access = ModuleDataAccess(data_manager, data_access_manager, 'data')
        self.components = DataComponents()
        self.operations = DataOperations()
        self.export = DataExport()
        self.init_panel()
    
    def init_panel(self):
        """Initialize core panel components"""
        self.components.create_basic_components(self.data_manager)
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup basic callbacks"""
        self.components.fetch_button.on_click(self.fetch_data)
        self.components.symbol_selector.param.watch(self.on_symbol_change, 'value')
        self.components.export_button.on_click(self.quick_export)
        self.components.clear_button.on_click(self.clear_data)
    
    def get_panel(self):
        """Get the core panel layout"""
        fetch_controls = pn.Row(
            self.components.symbol_selector,
            self.components.timeframe_selector,
            self.components.data_source,
            self.components.fetch_button,
            align='center'
        )
        
        management_controls = pn.Row(
            self.components.export_button,
            self.components.clear_button,
            align='center'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 📊 Data Management"),
            fetch_controls,
            management_controls,
            self.components.export_dialog,
            self.components.data_table,
            self.components.data_stats,
            sizing_mode='stretch_width'
        )
    
    def fetch_data(self, event):
        """Fetch data for selected symbol"""
        symbol = self.components.symbol_selector.value
        timeframe = self.components.timeframe_selector.value
        data_source = self.components.data_source.value.lower().replace(' ', '_')
        
        logger.info(f"📥 Fetching data for {symbol} ({timeframe}) from {data_source}")
        
        try:
            api_data = self.data_access.get_api_data([symbol], data_source, timeframe)
            
            if symbol in api_data:
                new_data = api_data[symbol]
                self.components.data_table.value = new_data
                self.operations.update_statistics(new_data, symbol, timeframe, data_source)
                logger.info(f"✅ Successfully fetched {len(new_data)} records for {symbol}")
            else:
                logger.warning(f"⚠️ No data returned for {symbol}")
                self.components.data_table.value = self.operations.create_sample_data()
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch data for {symbol}: {e}")
            self.components.data_table.value = self.operations.create_sample_data()
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        symbol = event.new
        logger.info(f"🔄 Symbol changed to {symbol}")
        self.components.data_table.value = self.operations.create_sample_data()
    
    def quick_export(self, event):
        """Quick export current data"""
        current_data = self.components.data_table.value
        if current_data is None or current_data.empty:
            current_data = self.operations.create_sample_data()
        
        result = self.export.quick_export_csv(current_data)
        self.components.export_dialog.object = result
    
    def clear_data(self, event):
        """Clear current data"""
        try:
            self.components.data_table.value = pd.DataFrame()
            self.components.data_stats.object = self.operations.get_clear_statistics()
            logger.info("Data cleared successfully")
        except Exception as e:
            logger.error(f"Clear data failed: {e}")
