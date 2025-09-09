#!/usr/bin/env python3
"""
TradePulse Data Upload - Core Component
Core data upload component functionality
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import logging

from .format_detector import FormatDetector
from .file_processor import FileProcessor
from .upload_manager import UploadManager

logger = logging.getLogger(__name__)

class DataUploadComponent:
    """Refactored data upload component using focused components"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.uploaded_data = {}
        
        # Initialize focused components
        self.format_detector = FormatDetector()
        self.file_processor = FileProcessor()
        self.upload_manager = UploadManager(data_manager)
        
        # Create additional UI components
        self.format_display = pn.pane.Markdown("**Detected Format:** None")
        self.preview_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Data Preview'
        )
        
        # Connect components
        self._connect_components()
        
        logger.info("✅ DataUploadComponent initialized with focused components")
    
    def _connect_components(self):
        """Connect the focused components together"""
        try:
            # Override upload manager's process method to use our processing pipeline
            self.upload_manager.process_uploaded_file = self._process_uploaded_file
            
            # Connect format detection to file selection
            self.upload_manager.file_input.param.watch(self._on_file_selected, 'value')
            
            logger.info("✅ Data upload components connected successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect components: {e}")
    
    def _on_file_selected(self, event):
        """Handle file selection and detect format"""
        try:
            if event.new is not None:
                filename = event.old if event.old else "unknown"
                
                # Detect file format
                detected_format = self.format_detector.detect_file_format(filename)
                self.format_display.object = f"**Detected Format:** {detected_format}"
                
                # Update upload manager status
                self.upload_manager.status_display.object = f"**Status:** File selected: {filename} ({detected_format})"
                self.upload_manager.upload_button.disabled = False
                
                logger.info(f"📁 File selected: {filename} (format: {detected_format})")
            else:
                self.format_display.object = "**Detected Format:** None"
                self.upload_manager.status_display.object = "**Status:** Ready to upload"
                self.upload_manager.upload_button.disabled = True
                
        except Exception as e:
            logger.error(f"❌ File selection handling failed: {e}")
            self.format_display.object = "**Detected Format:** Error"
    
    def _process_uploaded_file(self, event):
        """Process the uploaded file using the processing pipeline"""
        try:
            if self.upload_manager.file_input.value is None:
                logger.warning("⚠️ No file selected for processing")
                return
            
            # Get file content and name
            file_content = self.upload_manager.file_input.value
            filename = self.upload_manager.file_input.filename or "unknown"
            
            # Detect format
            detected_format = self.format_detector.detect_file_format(filename)
            
            logger.info(f"🚀 Processing uploaded file: {filename} (format: {detected_format})")
            
            # Update status
            self.upload_manager.status_display.object = f"**Status:** Processing {filename}..."
            self.upload_manager.upload_button.disabled = True
            
            # Process file
            processed_data = self.file_processor.process_file(file_content, detected_format)
            
            if processed_data is not None and not processed_data.empty:
                # Store processed data
                self.uploaded_data[filename] = processed_data
                
                # Update preview table
                self._update_preview_table(processed_data)
                
                # Update data info
                self._update_data_info(processed_data, filename)
                
                # Update status
                self.upload_manager.status_display.object = f"**Status:** ✅ Successfully processed {filename} ({len(processed_data)} rows)"
                self.upload_manager.upload_button.disabled = False
                
                logger.info(f"✅ Successfully processed {filename} ({len(processed_data)} rows)")
            else:
                # Handle processing failure
                self.upload_manager.status_display.object = f"**Status:** ❌ Failed to process {filename}"
                self.upload_manager.upload_button.disabled = False
                
                logger.error(f"❌ Failed to process {filename}")
                
        except Exception as e:
            logger.error(f"❌ File processing failed: {e}")
            self.upload_manager.status_display.object = f"**Status:** ❌ Error processing file: {str(e)}"
            self.upload_manager.upload_button.disabled = False
    
    def _update_preview_table(self, data: pd.DataFrame):
        """Update the preview table with processed data"""
        try:
            if data is not None and not data.empty:
                # Show first 10 rows for preview
                preview_data = data.head(10)
                self.preview_table.value = preview_data
            else:
                self.preview_table.value = pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Failed to update preview table: {e}")
            self.preview_table.value = pd.DataFrame()
    
    def _update_data_info(self, data: pd.DataFrame, filename: str):
        """Update data information display"""
        try:
            if data is not None and not data.empty:
                info_text = f"""
                **File:** {filename}
                **Rows:** {len(data):,}
                **Columns:** {len(data.columns)}
                **Memory Usage:** {data.memory_usage(deep=True).sum() / 1024:.2f} KB
                **Data Types:** {', '.join(data.dtypes.astype(str).unique())}
                """
                self.upload_manager.data_info.object = info_text
            else:
                self.upload_manager.data_info.object = "**No data available**"
                
        except Exception as e:
            logger.error(f"❌ Failed to update data info: {e}")
            self.upload_manager.data_info.object = "**Error updating data info**"
    
    def get_uploaded_data(self) -> Dict:
        """Get all uploaded data"""
        return self.uploaded_data.copy()

# Global instance
data_upload_component_core = DataUploadComponent(None)
