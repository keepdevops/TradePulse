#!/usr/bin/env python3
"""
TradePulse Data Upload Component
Handles file uploads for Feather, DuckDB, SQLite, CSV, JSON, and Excel formats
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Union, Any
import logging

from .data_upload.file_loader import FileLoader
from .data_upload.data_manager_integration import DataManagerIntegration

logger = logging.getLogger(__name__)

class DataUploadComponent:
    """Component for handling data file uploads in multiple formats"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.file_loader = FileLoader()
        self.data_manager_integration = DataManagerIntegration(data_manager)
        self.create_components()
    
    def create_components(self):
        """Create the upload interface components"""
        # File upload widget with explicit support for feather and duckdb
        self.file_input = pn.widgets.FileInput(
            name='📁 Upload Data File',
            accept='.feather,.duckdb,.db,.sqlite,.csv,.json,.xlsx,.xls,.parquet',
            width=300
        )
        
        # Format detection display
        self.format_display = pn.pane.Markdown("**Detected Format:** None")
        
        # Upload button
        self.upload_button = pn.widgets.Button(
            name='🚀 Process File',
            button_type='primary',
            width=150,
            disabled=True
        )
        
        # Data preview table
        self.preview_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Data Preview'
        )
        
        # Upload status
        self.status_display = pn.pane.Markdown("**Status:** Ready to upload")
        
        # Data info display
        self.data_info = pn.pane.Markdown("**Data Info:** No data loaded")
        
        # Setup callbacks
        self.file_input.param.watch(self.on_file_selected, 'value')
        self.upload_button.on_click(self.process_uploaded_file)
    
    def on_file_selected(self, event):
        """Handle file selection"""
        if event.new is not None:
            # Fix: Use the correct filename from the file input
            filename = self.file_input.filename if hasattr(self.file_input, 'filename') else "unknown"
            detected_format = self.file_loader.detect_file_format(filename)
            self.format_display.object = f"**Detected Format:** {detected_format}"
            self.upload_button.disabled = False
            self.status_display.object = f"**Status:** File selected: {filename}"
            logger.info(f"File selected: {filename}, detected format: {detected_format}")
        else:
            self.upload_button.disabled = True
            self.format_display.object = "**Detected Format:** None"
            self.status_display.object = "**Status:** Ready to upload"
    
    def process_uploaded_file(self, event):
        """Process the uploaded file based on its format"""
        try:
            if not self.file_input.value:
                self.status_display.object = "**Status:** ❌ No file selected"
                return
            
            # Get file content and filename
            file_content = self.file_input.value
            filename = self.file_input.filename
            
            logger.info(f"Processing file: {filename}, size: {len(file_content)} bytes")
            
            # Load file using file loader
            data = self.file_loader.load_file(file_content, filename)
            
            logger.info(f"File loaded successfully: {data.shape[0]} rows, {data.shape[1]} columns")
            
            # Update preview
            self.preview_table.value = data.head(10)
            
            # Update data info
            self.update_data_info(data, filename, self.file_loader.detect_file_format(filename))
            
            # Update status
            self.status_display.object = f"**Status:** ✅ Successfully loaded {filename}"
            
            # Add to data manager
            self.data_manager_integration.add_to_data_manager(data, filename)
            
            logger.info(f"File {filename} processed and added to data manager successfully")
            
        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            self.status_display.object = f"**Status:** ❌ Error: {str(e)}"
            # Show more detailed error information for debugging
            logger.error(f"File: {filename if 'filename' in locals() else 'unknown'}")
            logger.error(f"File size: {len(file_content) if 'file_content' in locals() else 'unknown'} bytes")
    
    def update_data_info(self, data: pd.DataFrame, filename: str, format_type: str):
        """Update the data information display"""
        try:
            info_text = f"""
            **Data Info for {filename}**
            - **Format:** {format_type}
            - **Shape:** {data.shape[0]} rows × {data.shape[1]} columns
            - **Columns:** {', '.join(data.columns.tolist())}
            - **Data Types:** {', '.join([f'{col}: {dtype}' for col, dtype in data.dtypes.items()])}
            - **Memory Usage:** {data.memory_usage(deep=True).sum() / 1024:.2f} KB
            - **Loaded:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            self.data_info.object = info_text
        except Exception as e:
            logger.error(f"Error updating data info: {e}")
            self.data_info.object = f"**Data Info:** Error displaying info - {str(e)}"
    
    def get_component(self):
        """Get the upload component layout"""
        return pn.Column(
            pn.pane.Markdown("### 📁 Data Upload"),
            pn.pane.Markdown("**Supported formats:** Feather (.feather), DuckDB (.duckdb), SQLite (.db/.sqlite), CSV (.csv), JSON (.json), Excel (.xlsx/.xls), Parquet (.parquet)"),
            self.file_input,
            self.format_display,
            self.upload_button,
            pn.pane.Markdown("---"),
            self.status_display,
            self.data_info,
            pn.pane.Markdown("### 📊 Data Preview"),
            self.preview_table,
            sizing_mode='stretch_width'
        )
    
    def get_uploaded_data(self) -> Dict[str, Any]:
        """Get all uploaded data"""
        return self.data_manager_integration.get_uploaded_data()
    
    def clear_uploaded_data(self):
        """Clear all uploaded data"""
        self.data_manager_integration.clear_uploaded_data()
        self.preview_table.value = pd.DataFrame()
        self.data_info.object = "**Data Info:** No data loaded"
        self.status_display.object = "**Status:** Ready to upload"
