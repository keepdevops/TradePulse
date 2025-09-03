#!/usr/bin/env python3
"""
TradePulse Dataset Activator - Management
UI management for the dataset activator
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DatasetActivatorManagement:
    """UI management for dataset activator"""
    
    @staticmethod
    def update_active_datasets_display(active_datasets_display, active_datasets: set):
        """Update the active datasets display"""
        try:
            if not active_datasets:
                active_datasets_display.object = "**Active Datasets:** None"
            else:
                datasets_list = ", ".join(sorted(active_datasets))
                active_datasets_display.object = f"**Active Datasets:** {datasets_list}"
                
        except Exception as e:
            logger.error(f"Failed to update active datasets display: {e}")
    
    @staticmethod
    def update_button_states(activate_button, deactivate_button, export_button, 
                            has_selected_dataset: bool, selected_dataset_active: bool):
        """Update button enabled/disabled states"""
        try:
            # Activate button: enabled when dataset is selected and not active
            if activate_button:
                activate_button.disabled = not has_selected_dataset or selected_dataset_active
            
            # Deactivate button: enabled when dataset is selected and active
            if deactivate_button:
                deactivate_button.disabled = not has_selected_dataset or not selected_dataset_active
            
            # Export button: enabled when dataset is selected
            if export_button:
                export_button.disabled = not has_selected_dataset
            
        except Exception as e:
            logger.error(f"Failed to update button states: {e}")
    
    @staticmethod
    def create_activator_layout(activate_button, deactivate_button, export_button, 
                              active_datasets_display):
        """Create the activator layout"""
        try:
            # Action buttons row
            action_buttons = pn.Row(
                activate_button,
                deactivate_button,
                export_button,
                align='center'
            )
            
            # Status section
            status_section = pn.Column(
                pn.pane.Markdown("### 📊 Dataset Status"),
                active_datasets_display,
                sizing_mode='stretch_width'
            )
            
            # Main layout
            layout = pn.Column(
                pn.pane.Markdown("### 🎛️ Dataset Controls"),
                action_buttons,
                pn.Spacer(height=10),
                status_section,
                sizing_mode='stretch_width'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create activator layout: {e}")
            return pn.Column("Error: Failed to create activator layout")
    
    @staticmethod
    def create_activation_history_display(activation_history: list):
        """Create activation history display"""
        try:
            if not activation_history:
                return pn.pane.Markdown("**No activation history available**")
            
            # Create history text
            history_lines = ["### 📋 Activation History"]
            for record in activation_history[-10:]:  # Show last 10 records
                timestamp = record.get('timestamp', 'Unknown')
                dataset_id = record.get('dataset_id', 'Unknown')
                action = record.get('action', 'Unknown')
                module = record.get('module', 'Unknown')
                
                history_lines.append(f"- **{timestamp}**: {dataset_id} {action} for {module}")
            
            return pn.pane.Markdown("\n".join(history_lines))
            
        except Exception as e:
            logger.error(f"Failed to create activation history display: {e}")
            return pn.pane.Markdown("Error: Failed to create activation history display")
    
    @staticmethod
    def create_statistics_display(statistics: dict):
        """Create statistics display"""
        try:
            stats_lines = [
                "### 📊 Activator Statistics",
                f"- **Total Activations**: {statistics.get('total_activations', 0)}",
                f"- **Total Deactivations**: {statistics.get('total_deactivations', 0)}",
                f"- **Currently Active**: {statistics.get('currently_active', 0)}",
                f"- **Callbacks Registered**: {statistics.get('callbacks_registered', 0)}",
                f"- **Last Activation**: {statistics.get('last_activation', 'Never')}",
                f"- **Last Deactivation**: {statistics.get('last_deactivation', 'Never')}"
            ]
            
            return pn.pane.Markdown("\n".join(stats_lines))
            
        except Exception as e:
            logger.error(f"Failed to create statistics display: {e}")
            return pn.pane.Markdown("Error: Failed to create statistics display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)

