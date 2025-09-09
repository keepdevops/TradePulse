#!/usr/bin/env python3
"""
TradePulse Data Upload - UI Module
UI layout and management functionality for data upload
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataUploadUI:
    """UI management for data upload component"""
    
    def __init__(self, core_component):
        self.core = core_component
    
    def create_component_layout(self):
        """Create the component layout"""
        try:
            # Get upload manager components
            upload_components = self.core.upload_manager.get_components()
            
            # Create upload section
            upload_section = pn.Column(
                pn.pane.Markdown("### 📁 File Upload"),
                pn.Row(
                    upload_components['file_input'],
                    self.core.format_display,
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
                self.core.preview_table,
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
    
    def get_component_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from all components"""
        try:
            format_stats = self.core.format_detector.get_detection_statistics()
            processing_stats = self.core.file_processor.get_processing_statistics()
            upload_stats = self.core.upload_manager.get_upload_statistics()
            
            return {
                'format_detection': format_stats,
                'file_processing': processing_stats,
                'upload_management': upload_stats,
                'total_uploaded_files': len(self.core.uploaded_data)
            }
            
        except Exception as e:
            logger.error(f"Failed to get component statistics: {e}")
            return {}
    
    def clear_all_history(self) -> int:
        """Clear all history from all components"""
        try:
            format_cleared = self.core.format_detector.clear_detection_history()
            processing_cleared = self.core.file_processor.clear_processing_history()
            upload_cleared = self.core.upload_manager.clear_upload_history()
            
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
            self.core._update_preview_table(pd.DataFrame())
            
            # Clear format display
            self.core.format_display.object = "**Detected Format:** None"
            
            # Clear upload manager displays
            self.core.upload_manager.clear_upload_data()
            
            logger.info("✅ All displays refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh displays: {e}")
