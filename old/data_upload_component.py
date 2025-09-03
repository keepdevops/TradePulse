#!/usr/bin/env python3
"""
TradePulse Data Upload - Main Component
Refactored data upload component using focused components
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
            
            try:
                # Process the file
                data, metadata = self.file_processor.process_file(file_content, filename, detected_format)
                
                # Store the processed data
                self.uploaded_data[filename] = {
                    'data': data,
                    'metadata': metadata,
                    'upload_time': pd.Timestamp.now()
                }
                
                # Add to data manager
                dataset_id = self.data_manager.add_uploaded_data(filename, data, metadata)
                
                # Update UI displays
                self._update_preview_table(data)
                self.upload_manager.update_data_info(data, metadata)
                
                # Update status
                self.upload_manager.status_display.object = f"**Status:** File {filename} processed successfully! Dataset ID: {dataset_id}"
                
                # Record successful upload
                self.upload_manager._record_upload_attempt(filename, len(file_content), True)
                
                # Clear file input
                self.upload_manager.file_input.value = None
                self.upload_manager.upload_button.disabled = True
                
                logger.info(f"✅ File {filename} processed successfully and added as dataset {dataset_id}")
                
            except Exception as e:
                # Record failed upload
                self.upload_manager._record_upload_attempt(filename, len(file_content), False, str(e))
                
                # Update status with error
                self.upload_manager.status_display.object = f"**Status:** Error processing file - {str(e)}"
                self.upload_manager.upload_button.disabled = False
                
                logger.error(f"❌ File processing failed: {e}")
                
        except Exception as e:
            logger.error(f"❌ Upload processing failed: {e}")
            self.upload_manager.status_display.object = f"**Status:** Error processing file - {str(e)}"
            self.upload_manager.upload_button.disabled = False
    
    def _update_preview_table(self, data: pd.DataFrame):
        """Update the preview table with processed data"""
        try:
            if data is None or data.empty:
                self.preview_table.value = pd.DataFrame()
                self.preview_table.name = 'Data Preview'
                return
            
            # Show first 10 rows for preview
            preview_data = data.head(10)
            self.preview_table.value = preview_data
            
            # Update table name with row count
            if len(data) > 10:
                self.preview_table.name = f'Data Preview (showing first 10 of {len(data)} rows)'
            else:
                self.preview_table.name = f'Data Preview ({len(data)} rows)'
                
        except Exception as e:
            logger.error(f"Failed to update preview table: {e}")
            self.preview_table.value = pd.DataFrame()
    
    def get_component(self):
        """Get the main data upload component layout"""
        try:
            # Get components from upload manager
            upload_components = self.upload_manager.get_components()
            
            # Create the main layout
            upload_section = pn.Column(
                pn.pane.Markdown("### 📁 File Upload"),
                pn.Row(
                    upload_components['file_input'],
                    self.format_display,
                    align='center'
                ),
                pn.Row(
                    upload_components['upload_button'],
                    align='center'
                ),
                upload_components['status_display'],
                sizing_mode='stretch_width'
            )
            
            preview_section = pn.Column(
                pn.pane.Markdown("### 📊 Data Preview"),
                self.preview_table,
                sizing_mode='stretch_width'
            )
            
            info_section = pn.Column(
                pn.pane.Markdown("### ℹ️ Data Information"),
                upload_components['data_info'],
                sizing_mode='stretch_width'
            )
            
            # Main layout with tabs
            tabs = pn.Tabs(
                ('📁 Upload', upload_section),
                ('📊 Preview', preview_section),
                ('ℹ️ Info', info_section),
                sizing_mode='stretch_width'
            )
            
            return pn.Column(
                pn.pane.Markdown("### 📁 Enhanced Data Upload System"),
                pn.pane.Markdown("Upload and process data files in multiple formats"),
                tabs,
                sizing_mode='stretch_width'
            )
            
        except Exception as e:
            logger.error(f"Failed to create component layout: {e}")
            return pn.pane.Markdown("**Error:** Failed to create data upload component")
    
    def get_uploaded_data(self) -> Dict:
        """Get all uploaded data"""
        return self.uploaded_data.copy()
    
    def get_component_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from all components"""
        try:
            format_stats = self.format_detector.get_detection_statistics()
            processing_stats = self.file_processor.get_processing_statistics()
            upload_stats = self.upload_manager.get_upload_statistics()
            
            return {
                'format_detection': format_stats,
                'file_processing': processing_stats,
                'upload_management': upload_stats,
                'total_uploaded_files': len(self.uploaded_data)
            }
            
        except Exception as e:
            logger.error(f"Failed to get component statistics: {e}")
            return {}
    
    def clear_all_history(self) -> int:
        """Clear all history from all components"""
        try:
            format_cleared = self.format_detector.clear_detection_history()
            processing_cleared = self.file_processor.clear_processing_history()
            upload_cleared = self.upload_manager.clear_upload_history()
            
            total_cleared = format_cleared + processing_cleared + upload_cleared
            
            logger.info(f"🗑️ Cleared {total_cleared} total history records")
            return total_cleared
            
        except Exception as e:
            logger.error(f"Failed to clear all history: {e}")
            return 0
    
    def refresh_displays(self):
        """Refresh all UI displays"""
        try:
            # Clear preview table
            self._update_preview_table(pd.DataFrame())
            
            # Clear format display
            self.format_display.object = "**Detected Format:** None"
            
            # Clear upload manager displays
            self.upload_manager.clear_upload_data()
            
            logger.info("✅ All displays refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh displays: {e}")
