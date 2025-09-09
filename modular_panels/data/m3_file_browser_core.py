#!/usr/bin/env python3
"""
TradePulse M3 File Browser - Core
Core UI functionality for M3 file browsing
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from m3_file_manager import m3_file_manager
from .m3_file_browser_ui import M3FileBrowserUI
from .m3_file_browser_callbacks import M3FileBrowserCallbacks

logger = logging.getLogger(__name__)

class M3FileBrowserCore:
    """Core M3 file browser component for Panel UI"""
    
    def __init__(self):
        self.current_path = "/Users/moose"
        self.file_types_filter = []
        self.search_pattern = ""
        
        # UI Components
        self.path_input = pn.widgets.TextInput(
            name="📍 Current Path",
            value=self.current_path,
            width=400
        )
        
        self.file_type_selector = pn.widgets.MultiChoice(
            name="📄 File Types",
            options=['csv', 'json', 'feather', 'parquet', 'duckdb', 'keras', 'excel', 'text'],
            value=[],
            width=200
        )
        
        self.search_input = pn.widgets.TextInput(
            name="🔍 Search Pattern",
            placeholder="Enter filename pattern...",
            width=300
        )
        
        self.browse_button = pn.widgets.Button(
            name="📂 Browse Directory",
            button_type='primary',
            width=150
        )
        
        self.search_button = pn.widgets.Button(
            name="🔍 Search Files",
            button_type='success',
            width=150
        )
        
        self.back_button = pn.widgets.Button(
            name="⬅️ Back",
            button_type='light',
            width=100
        )
        
        self.refresh_button = pn.widgets.Button(
            name="🔄 Refresh",
            button_type='light',
            width=100
        )
        
        self.copy_button = pn.widgets.Button(
            name="📥 Copy to TradePulse",
            button_type='warning',
            width=150
        )
        
        # Display areas
        self.status_display = pn.pane.Markdown("## 📊 M3 File Browser Status")
        self.directory_display = pn.pane.Markdown("## 📁 Directory Contents")
        self.file_details_display = pn.pane.Markdown("## 📄 File Details")
        
        # Data storage
        self.current_directory_data = {}
        self.selected_file = None
        
        # Initialize UI operations and callbacks
        self.ui = M3FileBrowserUI(self)
        self.callbacks = M3FileBrowserCallbacks(self)
        
        # Setup callbacks
        self.callbacks._setup_callbacks()
        
        # Initial load
        self.ui._load_m3_status()
    

    
    def _load_m3_status(self):
        """Load M3 drive status"""
        try:
            status = m3_file_manager.get_m3_status()
            
            status_text = f"""
            ## 📊 M3 Drive Status
            
            **Accessible Paths:** {len(status.get('accessible_paths', []))}
            **Total Files Found:** {status.get('total_files_found', 0):,}
            **Total Size:** {self._format_size(status.get('total_size', 0))}
            **Scan Time:** {status.get('scan_time', 'Unknown')}
            
            ### 📁 Accessible Directories:
            """
            
            for path in status.get('accessible_paths', []):
                file_count = status.get('file_types_found', {}).get('.csv', 0) + \
                           status.get('file_types_found', {}).get('.json', 0) + \
                           status.get('file_types_found', {}).get('.feather', 0)
                status_text += f"- **{path}** ({file_count} data files)\n"
            
            self.status_display.object = status_text
            
        except Exception as e:
            logger.error(f"❌ Failed to load M3 status: {e}")
            self.status_display.object = f"❌ Failed to load M3 status: {e}"
    
    def _browse_directory(self, directory_path: str):
        """Browse specific directory"""
        try:
            # Update current path
            self.current_path = directory_path
            self.path_input.value = directory_path
            
            # Get file types filter
            file_types = self.file_types_filter if self.file_types_filter else None
            
            # Browse directory
            result = m3_file_manager.browse_directory(directory_path, file_types)
            
            if not result:
                self.ui._update_status(f"❌ Could not browse directory: {directory_path}")
                return
            
            self.current_directory_data = result
            self.ui._update_directory_display(result)
            
        except Exception as e:
            logger.error(f"❌ Browse directory error: {e}")
            self.ui._update_status(f"❌ Browse directory error: {e}")
    
    def _search_files(self, search_path: str, pattern: str):
        """Search for files"""
        try:
            file_types = self.file_types_filter if self.file_types_filter else None
            results = m3_file_manager.search_files(search_path, pattern, file_types)
            
            if not results:
                self.ui._update_status(f"🔍 No files found matching '{pattern}' in {search_path}")
                return
            
            # Create search results display using UI module
            search_text = self.ui._create_search_results_display(results, pattern, search_path)
            self.directory_display.object = search_text
            
        except Exception as e:
            logger.error(f"❌ Search files error: {e}")
            self.ui._update_status(f"❌ Search files error: {e}")
    


# Global instance
m3_file_browser_core = M3FileBrowserCore()
