#!/usr/bin/env python3
"""
TradePulse M3 File Browser Component
Enhanced file browsing interface for M3 hard drive access
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .m3_file_browser_core import m3_file_browser_core

logger = logging.getLogger(__name__)

class M3FileBrowser:
    """Enhanced M3 file browser component for Panel UI"""
    
    def __init__(self):
        self.core = m3_file_browser_core
    

    
    def get_panel(self) -> pn.Column:
        """Get the M3 file browser panel"""
        try:
            # Create control panel
            controls = pn.Row(
                pn.Column(
                    pn.pane.Markdown("### 🎛️ Controls"),
                    self.core.path_input,
                    self.core.file_type_selector,
                    self.core.search_input,
                    width=300
                ),
                pn.Column(
                    pn.pane.Markdown("### 🔘 Actions"),
                    self.core.browse_button,
                    self.core.search_button,
                    self.core.back_button,
                    self.core.refresh_button,
                    self.core.copy_button,
                    width=200
                ),
                sizing_mode='stretch_width'
            )
            
            # Create main panel
            main_panel = pn.Column(
                pn.pane.Markdown("# 📁 M3 File Browser"),
                pn.pane.Markdown("Enhanced file browsing for M3 hard drive access"),
                controls,
                self.core.status_display,
                self.core.directory_display,
                self.core.file_details_display,
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ M3 File Browser panel created")
            return main_panel
            
        except Exception as e:
            logger.error(f"❌ Failed to create M3 File Browser panel: {e}")
            return pn.Column(f"❌ Error creating M3 File Browser: {e}")

# Global instance
m3_file_browser = M3FileBrowser()
