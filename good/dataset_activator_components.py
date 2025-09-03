#!/usr/bin/env python3
"""
TradePulse Dataset Activator - Components
UI components for the dataset activator
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DatasetActivatorComponents:
    """UI components for dataset activator"""
    
    def __init__(self):
        self.activate_button = None
        self.deactivate_button = None
        self.export_button = None
        self.active_datasets_display = None
        self.status_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Activate button
        self.activate_button = pn.widgets.Button(
            name='✅ Activate for Module',
            button_type='primary',
            width=150,
            disabled=True
        )
        
        # Deactivate button
        self.deactivate_button = pn.widgets.Button(
            name='❌ Deactivate',
            button_type='warning',
            width=150,
            disabled=True
        )
        
        # Export button
        self.export_button = pn.widgets.Button(
            name='📤 Export',
            button_type='success',
            width=100,
            disabled=True
        )
        
        # Active datasets display
        self.active_datasets_display = pn.pane.Markdown("**Active Datasets:** None")
        
        # Status display
        self.status_display = pn.pane.Markdown("""
        ### 📊 Dataset Status
        - **Selected**: None
        - **Active**: 0 datasets
        - **Available**: 0 datasets
        """)
    
    def create_action_buttons_row(self):
        """Create row of action buttons"""
        return pn.Row(
            self.activate_button,
            self.deactivate_button,
            self.export_button,
            align='center'
        )
    
    def create_status_section(self):
        """Create status section"""
        return pn.Column(
            self.active_datasets_display,
            self.status_display,
            sizing_mode='stretch_width'
        )
    
    def create_control_panel(self):
        """Create control panel"""
        return pn.Column(
            pn.pane.Markdown("### 🎛️ Dataset Controls"),
            self.create_action_buttons_row(),
            self.create_status_section(),
            sizing_mode='stretch_width'
        )
    
    def update_button_states(self, has_selected_dataset: bool, selected_dataset_active: bool):
        """Update button enabled/disabled states"""
        if self.activate_button:
            self.activate_button.disabled = not has_selected_dataset or selected_dataset_active
        
        if self.deactivate_button:
            self.deactivate_button.disabled = not has_selected_dataset or not selected_dataset_active
        
        if self.export_button:
            self.export_button.disabled = not has_selected_dataset
    
    def update_active_datasets_display(self, active_datasets: set):
        """Update active datasets display"""
        if self.active_datasets_display:
            if not active_datasets:
                self.active_datasets_display.object = "**Active Datasets:** None"
            else:
                datasets_list = ", ".join(sorted(active_datasets))
                self.active_datasets_display.object = f"**Active Datasets:** {datasets_list}"
    
    def update_status_display(self, selected_dataset: str, active_count: int, available_count: int):
        """Update status display"""
        if self.status_display:
            self.status_display.object = f"""
            ### 📊 Dataset Status
            - **Selected**: {selected_dataset or 'None'}
            - **Active**: {active_count} datasets
            - **Available**: {available_count} datasets
            """

