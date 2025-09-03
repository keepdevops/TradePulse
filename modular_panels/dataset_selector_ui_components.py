#!/usr/bin/env python3
"""
TradePulse Dataset Selector - UI Components
Handles dataset selector UI component creation
"""

import panel as pn
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DatasetSelectorUIComponents:
    """Handles dataset selector UI component creation"""
    
    def create_search_input(self):
        """Create dataset search input"""
        return pn.widgets.TextInput(
            name='🔍 Search Datasets',
            placeholder='Search by name, columns, or content...',
            width=250
        )
    
    def create_type_filter(self):
        """Create dataset type filter"""
        return pn.widgets.Select(
            name='📁 Type Filter',
            options=['All Types', 'Uploaded', 'Price Data', 'ML Predictions'],
            value='All Types',
            width=150
        )
    
    def create_datasets_list(self):
        """Create available datasets list"""
        return pn.widgets.Select(
            name='📊 Available Datasets',
            options=[],
            size=8,
            width=300
        )
    
    def create_dataset_info(self):
        """Create dataset info display"""
        return pn.pane.Markdown("**Dataset Info:** Select a dataset to view details")
    
    def create_preview_table(self):
        """Create dataset preview table"""
        return pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Dataset Preview'
        )
    
    def create_activate_button(self):
        """Create activate button"""
        return pn.widgets.Button(
            name='✅ Activate for Module',
            button_type='primary',
            width=150,
            disabled=True
        )
    
    def create_deactivate_button(self):
        """Create deactivate button"""
        return pn.widgets.Button(
            name='❌ Deactivate',
            button_type='warning',
            width=150,
            disabled=True
        )
    
    def create_export_button(self):
        """Create export button"""
        return pn.widgets.Button(
            name='📤 Export',
            button_type='success',
            width=100,
            disabled=True
        )
    
    def create_active_datasets_display(self):
        """Create active datasets display"""
        return pn.pane.Markdown("**Active Datasets:** None")
    
    def create_component_layout(self, module_name, search_input, type_filter, datasets_list, 
                               dataset_info, preview_table, activate_button, deactivate_button, 
                               export_button, active_datasets_display):
        """Create the dataset selector component layout"""
        return pn.Column(
            pn.pane.Markdown(f"### 📊 Dataset Selector - {module_name.title()} Module"),
            pn.pane.Markdown("Browse, select, and activate datasets for use in this module"),
            
            # Search and filter controls
            pn.Row(
                search_input,
                type_filter,
                align='center'
            ),
            
            pn.pane.Markdown("---"),
            
            # Dataset selection and info
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("**Available Datasets:**"),
                    datasets_list,
                    sizing_mode='stretch_width'
                ),
                pn.Column(
                    dataset_info,
                    sizing_mode='stretch_width'
                ),
                sizing_mode='stretch_width'
            ),
            
            # Preview table
            pn.pane.Markdown("**Dataset Preview:**"),
            preview_table,
            
            # Action buttons
            pn.Row(
                activate_button,
                deactivate_button,
                export_button,
                align='center'
            ),
            
            pn.pane.Markdown("---"),
            
            # Active datasets
            active_datasets_display,
            
            sizing_mode='stretch_width'
        )
