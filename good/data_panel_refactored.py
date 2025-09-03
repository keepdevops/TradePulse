#!/usr/bin/env python3
"""
TradePulse Modular Panels - Data Panel (Refactored)
Enhanced data management and fetching panel with upload support
Refactored to be under 200 lines
"""

import panel as pn
import logging
import pandas as pd

from . import BasePanel
from .data_upload_component import DataUploadComponent
from .data.data_panel_core import DataPanelCore

logger = logging.getLogger(__name__)

class DataPanel(BasePanel):
    """Enhanced data management and fetching panel with upload support"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Data", data_manager)
        self.upload_component = DataUploadComponent(data_manager)
        self.core_panel = DataPanelCore(data_manager, data_access_manager)
        self.init_panel()
    
    def init_panel(self):
        """Initialize enhanced data panel components"""
        # Add advanced export button to core components
        self.core_panel.components.advanced_export_button = pn.widgets.Button(
            name='⚙️ Advanced Export',
            button_type='success',
            width=120
        )
        self.core_panel.components.advanced_export_button.on_click(self.advanced_export)
    
    def get_panel(self):
        """Get the enhanced data panel layout"""
        # Get core panel layout
        core_layout = self.core_panel.get_panel()
        
        # Add advanced export button to management controls
        if hasattr(self.core_panel.components, 'advanced_export_button'):
            # Find the management controls row and add the advanced export button
            for child in core_layout:
                if isinstance(child, pn.Row) and len(child) > 0:
                    if hasattr(child[0], 'name') and 'Export' in str(child[0].name):
                        # This is the management controls row
                        child.append(self.core_panel.components.advanced_export_button)
                        break
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('📥 Fetch Data', core_layout),
            ('📁 Upload Data', self.upload_component.get_component()),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 📊 Enhanced Data Management"),
            pn.pane.Markdown("Fetch real-time data or upload your own files in multiple formats"),
            tabs,
            sizing_mode='stretch_width'
        )
    
    def advanced_export(self, event):
        """Advanced export with format selection"""
        try:
            current_data = self.core_panel.components.data_table.value
            if current_data is None or current_data.empty:
                current_data = self.core_panel.operations.create_sample_data()
            
            # Create export options
            export_format = pn.widgets.Select(
                name='Export Format',
                options=self.core_panel.export.get_export_formats(),
                value='CSV',
                width=150
            )
            
            export_filename = pn.widgets.TextInput(
                name='Filename',
                value=f"tradepulse_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
                width=200
            )
            
            # Status display
            export_status = pn.pane.Markdown("### 📤 Export Data\nSelect format and filename, then click Export")
            
            def do_export(evt):
                try:
                    format_type = export_format.value.lower()
                    filename = export_filename.value
                    
                    result = self.core_panel.export.export_data_advanced(
                        current_data, format_type, filename
                    )
                    export_status.object = result
                    
                except Exception as e:
                    logger.error(f"Export failed: {e}")
                    export_status.object = f"### ❌ Export Failed\nError: {str(e)}"
            
            export_button = pn.widgets.Button(
                name='💾 Export',
                button_type='primary',
                width=100
            )
            export_button.on_click(do_export)
            
            # Create export dialog content
            export_dialog_content = f"""
            ### 📤 Export Data
            
            **Format**: {export_format.value}
            **Filename**: {export_filename.value}
            
            {export_status.object}
            
            ---
            """
            
            # Display the export dialog in the main panel
            self.core_panel.components.export_dialog.object = export_dialog_content
            
        except Exception as e:
            logger.error(f"Advanced export failed: {e}")
    
    def get_uploaded_data(self):
        """Get data from the upload component"""
        return self.upload_component.get_uploaded_data()
