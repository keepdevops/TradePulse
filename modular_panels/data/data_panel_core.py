#!/usr/bin/env python3
"""
TradePulse Data Panel - Core Functionality
Core data panel class with basic functionality
"""

import panel as pn
import pandas as pd
import numpy as np
import logging
import os
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
        self.components.date_range_preset.param.watch(self.on_date_range_change, 'value')
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
        
        date_controls = pn.Row(
            self.components.date_range_preset,
            self.components.start_date_picker,
            self.components.end_date_picker,
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
            date_controls,
            management_controls,
            self.components.export_dialog,
            self.components.data_table,
            self.components.data_stats,
            self.get_available_files_section(),
            sizing_mode='stretch_width'
        )
    
    def fetch_data(self, event):
        """Fetch data for selected symbol with date range"""
        symbol = self.components.symbol_selector.value
        timeframe = self.components.timeframe_selector.value
        start_date = self.components.start_date_picker.value
        end_date = self.components.end_date_picker.value
        
        # Map display names to internal source names
        source_mapping = {
            'Yahoo Finance': 'yahoo',
            'Alpha Vantage': 'alpha_vantage', 
            'IEX Cloud': 'iex',
            'Mock Data': 'mock',
            'Upload Data': 'upload'
        }
        data_source = source_mapping.get(self.components.data_source.value, 'mock')
        
        # Convert dates to string format
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None
        
        logger.info(f"📥 Fetching data for {symbol} ({timeframe}) from {data_source}")
        logger.info(f"📅 Date range: {start_date_str} to {end_date_str}")
        
        try:
            # Use the enhanced data access with date range
            if self.data_access.is_data_access_available():
                # Use the unified data access manager
                data = self.data_access.data_access_manager.get_data(
                    data_source, symbol, timeframe, start_date_str, end_date_str
                )
                
                if not data.empty:
                    self.components.data_table.value = data
                    self.operations.update_statistics(data, symbol, timeframe, data_source)
                    logger.info(f"✅ Successfully fetched {len(data)} records for {symbol}")
                else:
                    logger.warning(f"⚠️ No data returned for {symbol}")
                    self.components.data_table.value = self.operations.create_sample_data()
            else:
                # Fallback to original method
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
    
    def get_available_files_section(self):
        """Show available data files on hard drive"""
        try:
            if self.data_access.is_data_access_available():
                available_files = self.data_access.data_access_manager.get_available_data_files()
                
                if not available_files:
                    return pn.pane.Markdown("### 📁 Available Data Files\nNo data files found on hard drive.")
                
                file_sections = []
                for file_type, files in available_files.items():
                    if files:
                        file_list = "\n".join([f"- `{os.path.basename(f)}`" for f in files[:5]])  # Show first 5 files
                        if len(files) > 5:
                            file_list += f"\n- ... and {len(files) - 5} more files"
                        
                        file_sections.append(f"**{file_type.upper()} Files ({len(files)}):**\n{file_list}")
                
                if file_sections:
                    content = "### 📁 Available Data Files\n" + "\n\n".join(file_sections)
                    return pn.pane.Markdown(content)
                else:
                    return pn.pane.Markdown("### 📁 Available Data Files\nNo data files found on hard drive.")
            else:
                return pn.pane.Markdown("### 📁 Available Data Files\nData access manager not available.")
                
        except Exception as e:
            logger.error(f"❌ Failed to get available files section: {e}")
            return pn.pane.Markdown("### 📁 Available Data Files\nError loading file list.")
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        try:
            symbol = event.new
            logger.info(f"🔄 Symbol changed to {symbol}")
            
            # Create sample data safely
            sample_data = self.operations.create_sample_data()
            
            # Update table value safely
            if hasattr(self.components, 'data_table') and self.components.data_table is not None:
                self.components.data_table.value = sample_data
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
            self.components.start_date_picker.value = start_date
            self.components.end_date_picker.value = now
            
            logger.info(f"📅 Updated date range: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to handle date range change: {e}")
    
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
    
    def get_uploaded_data(self):
        """Get data from the upload component"""
        return self.components.data_table.value
