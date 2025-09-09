#!/usr/bin/env python3
"""
TradePulse Data Panel - Core Main
Main data panel core functionality
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
from .m3_file_browser import m3_file_browser
from ui_components.module_data_access import ModuleDataAccess
from ..file_browser_component import FileBrowserComponent

logger = logging.getLogger(__name__)

class DataPanelCore:
    """Core data panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        self.data_manager = data_manager
        self.data_access = ModuleDataAccess(data_manager, data_access_manager, 'data')
        self.components = DataComponents()
        self.operations = DataOperations()
        self.export = DataExport()
        
        # Initialize file browser component
        self.file_browser = FileBrowserComponent(data_manager)
        
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
        
        # Create tabs for different data access methods
        data_tabs = pn.Tabs()
        
        # Tab 1: Standard Data Fetching
        standard_data_tab = pn.Column(
            pn.pane.Markdown("### 📊 Standard Data Management"),
            fetch_controls,
            date_controls,
            management_controls,
            self.components.export_dialog,
            self.components.data_table,
            self.components.data_stats,
            sizing_mode='stretch_width'
        )
        
        # Tab 2: File Browser (Local PC)
        file_browser_tab = self.file_browser.get_component()
        
        # Tab 3: M3 File Browser
        m3_browser_tab = m3_file_browser.get_panel()
        
        # Tab 4: Available Files
        available_files_tab = pn.Column(
            pn.pane.Markdown("### 📁 Available Data Files"),
            self.get_available_files_section(),
            sizing_mode='stretch_width'
        )
        
        # Add tabs
        data_tabs.append(("📊 Standard Data", standard_data_tab))
        data_tabs.append(("📁 File Browser", file_browser_tab))
        data_tabs.append(("📂 M3 File Browser", m3_browser_tab))
        data_tabs.append(("📂 Available Files", available_files_tab))
        
        return pn.Column(
            pn.pane.Markdown("## 📊 Data Panel"),
            pn.pane.Markdown("Enhanced data access with M3 file browsing capabilities"),
            data_tabs,
            sizing_mode='stretch_width'
        )
    
    def fetch_data(self, event):
        """Fetch data from selected source"""
        try:
            symbol = self.components.symbol_selector.value
            timeframe = self.components.timeframe_selector.value
            source = self.components.data_source.value
            
            # Get date range from pickers
            start_date = self.components.start_date_picker.value
            end_date = self.components.end_date_picker.value
            
            if not self.data_access.is_data_access_available():
                logger.error("❌ Data access manager not available")
                return
            
            # Fetch data
            data = self.data_access.data_access_manager.get_data(
                source, symbol, timeframe, start_date, end_date
            )
            
            if not data.empty:
                # Update table
                self.components.data_table.value = data
                
                # Update statistics
                stats = self.operations.update_statistics(data, symbol, timeframe, source)
                self.components.data_stats.object = stats
                
                logger.info(f"✅ Fetched {len(data)} records for {symbol}")
            else:
                logger.warning(f"⚠️ No data returned for {symbol}")
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch data: {e}")
    
    def get_available_files_section(self):
        """Get available files section"""
        try:
            if self.data_access.is_data_access_available():
                available_files = self.data_access.data_access_manager.get_available_data_files()
                
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
    
    def get_uploaded_data(self):
        """Get data from the upload component"""
        return self.components.data_table.value
    
    def get_file_browser(self):
        """Get the file browser component"""
        return self.file_browser
    
    def on_symbol_change(self, event):
        """Handle symbol change event"""
        try:
            symbol = event.new
            logger.info(f"📊 Symbol changed to: {symbol}")
            # Update any dependent components here
        except Exception as e:
            logger.error(f"❌ Failed to handle symbol change: {e}")
    
    def on_date_range_change(self, event):
        """Handle date range change event"""
        try:
            date_range = event.new
            logger.info(f"📅 Date range changed to: {date_range}")
            # Update date pickers based on preset
            if date_range == "1M":
                # Set to last month
                pass
            elif date_range == "3M":
                # Set to last 3 months
                pass
            elif date_range == "6M":
                # Set to last 6 months
                pass
            elif date_range == "1Y":
                # Set to last year
                pass
        except Exception as e:
            logger.error(f"❌ Failed to handle date range change: {e}")
    
    def quick_export(self, event):
        """Handle quick export event"""
        try:
            data = self.components.data_table.value
            if not data.empty:
                # Export current data
                filename = f"export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                data.to_csv(filename, index=False)
                logger.info(f"✅ Exported data to {filename}")
            else:
                logger.warning("⚠️ No data to export")
        except Exception as e:
            logger.error(f"❌ Failed to export data: {e}")
    
    def clear_data(self, event):
        """Handle clear data event"""
        try:
            self.components.data_table.value = pd.DataFrame()
            self.components.data_stats.object = "No data loaded"
            logger.info("🗑️ Data cleared")
        except Exception as e:
            logger.error(f"❌ Failed to clear data: {e}")

# Global instance - will be properly initialized when used
data_panel_core_main = None

def get_data_panel_core_main(data_manager=None, data_access_manager=None):
    """Get the global data panel core main instance"""
    global data_panel_core_main
    if data_panel_core_main is None:
        data_panel_core_main = DataPanelCore(data_manager, data_access_manager)
    return data_panel_core_main
