#!/usr/bin/env python3
"""
TradePulse M3 File Browser - Callbacks
Callback functionality for M3 file browser
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class M3FileBrowserCallbacks:
    """Callback functionality for M3 file browser"""
    
    def __init__(self, core_browser):
        self.core = core_browser
    
    def _setup_callbacks(self):
        """Setup component callbacks"""
        self.core.browse_button.on_click(self._on_browse_click)
        self.core.search_button.on_click(self._on_search_click)
        self.core.back_button.on_click(self._on_back_click)
        self.core.refresh_button.on_click(self._on_refresh_click)
        self.core.copy_button.on_click(self._on_copy_click)
        self.core.path_input.param.watch(self._on_path_change, 'value')
        self.core.file_type_selector.param.watch(self._on_file_type_change, 'value')
    
    def _on_browse_click(self, event):
        """Handle browse button click"""
        try:
            path = self.core.path_input.value.strip()
            if path:
                self.core._browse_directory(path)
            else:
                self.core._browse_directory(self.core.current_path)
        except Exception as e:
            logger.error(f"❌ Browse error: {e}")
            self.core.ui._update_status(f"❌ Browse error: {e}")
    
    def _on_search_click(self, event):
        """Handle search button click"""
        try:
            path = self.core.path_input.value.strip()
            pattern = self.core.search_input.value.strip()
            
            if not path or not pattern:
                self.core.ui._update_status("⚠️ Please enter both path and search pattern")
                return
            
            self.core._search_files(path, pattern)
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            self.core.ui._update_status(f"❌ Search error: {e}")
    
    def _on_back_click(self, event):
        """Handle back button click"""
        try:
            current_path = Path(self.core.path_input.value)
            parent_path = str(current_path.parent)
            
            if parent_path != current_path:
                self.core.path_input.value = parent_path
                self.core._browse_directory(parent_path)
        except Exception as e:
            logger.error(f"❌ Back navigation error: {e}")
            self.core.ui._update_status(f"❌ Back navigation error: {e}")
    
    def _on_refresh_click(self, event):
        """Handle refresh button click"""
        try:
            self.core.ui._load_m3_status()
            self.core._browse_directory(self.core.path_input.value)
        except Exception as e:
            logger.error(f"❌ Refresh error: {e}")
            self.core.ui._update_status(f"❌ Refresh error: {e}")
    
    def _on_copy_click(self, event):
        """Handle copy button click"""
        try:
            if not self.core.selected_file:
                self.core.ui._update_status("⚠️ Please select a file to copy")
                return
            
            from m3_file_manager import m3_file_manager
            result = m3_file_manager.copy_file_to_tradepulse(self.core.selected_file)
            
            if result.get('success'):
                self.core.ui._update_status(f"✅ Copied {result['filename']} to TradePulse")
                self.core.ui._update_file_details(result)
            else:
                self.core.ui._update_status(f"❌ Copy failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            logger.error(f"❌ Copy error: {e}")
            self.core.ui._update_status(f"❌ Copy error: {e}")
    
    def _on_path_change(self, event):
        """Handle path input change"""
        self.core.current_path = event.new
    
    def _on_file_type_change(self, event):
        """Handle file type filter change"""
        self.core.file_types_filter = event.new
