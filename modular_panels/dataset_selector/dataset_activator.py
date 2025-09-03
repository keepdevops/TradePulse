#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Activator
Handles dataset activation, deactivation, and management
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)

class DatasetActivator:
    """Handles dataset activation, deactivation, and management"""
    
    def __init__(self, data_manager, module_name: str):
        self.data_manager = data_manager
        self.module_name = module_name
        self.active_datasets = set()
        self.activation_history = []
        self.on_dataset_change_callbacks = []
        
        # Create UI components
        self.activate_button = pn.widgets.Button(
            name='✅ Activate for Module',
            button_type='primary',
            width=150,
            disabled=True
        )
        
        self.deactivate_button = pn.widgets.Button(
            name='❌ Deactivate',
            button_type='warning',
            width=150,
            disabled=True
        )
        
        self.export_button = pn.widgets.Button(
            name='📤 Export',
            button_type='success',
            width=100,
            disabled=True
        )
        
        self.active_datasets_display = pn.pane.Markdown("**Active Datasets:** None")
        
        # Setup callbacks
        self.activate_button.on_click(self.activate_dataset)
        self.deactivate_button.on_click(self.deactivate_dataset)
        self.export_button.on_click(self.export_dataset)
    
    def add_dataset_change_callback(self, callback: Callable):
        """Add callback for dataset change events"""
        if callback not in self.on_dataset_change_callbacks:
            self.on_dataset_change_callbacks.append(callback)
            logger.info(f"✅ Added dataset change callback for {self.module_name}")
    
    def remove_dataset_change_callback(self, callback: Callable):
        """Remove dataset change callback"""
        if callback in self.on_dataset_change_callbacks:
            self.on_dataset_change_callbacks.remove(callback)
            logger.info(f"✅ Removed dataset change callback for {self.module_name}")
    
    def activate_dataset(self, event):
        """Activate a dataset for the current module"""
        try:
            # Get currently selected dataset from browser
            selected_dataset = self._get_selected_dataset()
            
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for activation")
                return
            
            if selected_dataset in self.active_datasets:
                logger.info(f"📊 Dataset {selected_dataset} is already active for {self.module_name}")
                return
            
            # Activate dataset
            self.active_datasets.add(selected_dataset)
            
            # Record activation
            self._record_activation(selected_dataset, 'activated')
            
            # Update UI
            self._update_active_datasets_display()
            self._update_button_states()
            
            # Notify callbacks
            self._notify_dataset_change('activated', selected_dataset)
            
            logger.info(f"✅ Dataset {selected_dataset} activated for {self.module_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to activate dataset: {e}")
    
    def deactivate_dataset(self, event):
        """Deactivate a dataset for the current module"""
        try:
            # Get currently selected dataset from browser
            selected_dataset = self._get_selected_dataset()
            
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for deactivation")
                return
            
            if selected_dataset not in self.active_datasets:
                logger.info(f"📊 Dataset {selected_dataset} is not active for {self.module_name}")
                return
            
            # Deactivate dataset
            self.active_datasets.remove(selected_dataset)
            
            # Record deactivation
            self._record_activation(selected_dataset, 'deactivated')
            
            # Update UI
            self._update_active_datasets_display()
            self._update_button_states()
            
            # Notify callbacks
            self._notify_dataset_change('deactivated', selected_dataset)
            
            logger.info(f"✅ Dataset {selected_dataset} deactivated for {self.module_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to deactivate dataset: {e}")
    
    def export_dataset(self, event):
        """Export the currently selected dataset"""
        try:
            selected_dataset = self._get_selected_dataset()
            
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for export")
                return
            
            # Get dataset data
            dataset_data = self.data_manager.get_dataset(selected_dataset)
            
            if dataset_data is not None:
                # Create export filename
                export_filename = f"{selected_dataset}_{self.module_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                # Export to CSV
                dataset_data.to_csv(export_filename, index=False)
                
                logger.info(f"📤 Dataset {selected_dataset} exported to {export_filename}")
                
                # Show success message
                self._show_export_success(export_filename)
            else:
                logger.warning(f"⚠️ Could not retrieve dataset {selected_dataset} for export")
                
        except Exception as e:
            logger.error(f"❌ Failed to export dataset: {e}")
    
    def _get_selected_dataset(self) -> Optional[str]:
        """Get the currently selected dataset ID"""
        # This method should be implemented to get the selected dataset from the browser
        # For now, return None - will be connected by the main component
        return None
    
    def _record_activation(self, dataset_id: str, action: str):
        """Record dataset activation/deactivation"""
        try:
            activation_record = {
                'timestamp': pd.Timestamp.now(),
                'dataset_id': dataset_id,
                'action': action,
                'module': self.module_name
            }
            self.activation_history.append(activation_record)
            
        except Exception as e:
            logger.error(f"Failed to record activation: {e}")
    
    def _update_active_datasets_display(self):
        """Update the active datasets display"""
        try:
            if not self.active_datasets:
                self.active_datasets_display.object = "**Active Datasets:** None"
            else:
                datasets_list = ", ".join(sorted(self.active_datasets))
                self.active_datasets_display.object = f"**Active Datasets:** {datasets_list}"
                
        except Exception as e:
            logger.error(f"Failed to update active datasets display: {e}")
    
    def _update_button_states(self):
        """Update button enabled/disabled states"""
        try:
            has_active_datasets = len(self.active_datasets) > 0
            has_selected_dataset = self._get_selected_dataset() is not None
            
            # Activate button: enabled when dataset is selected and not active
            self.activate_button.disabled = not has_selected_dataset or self._get_selected_dataset() in self.active_datasets
            
            # Deactivate button: enabled when dataset is selected and active
            self.deactivate_button.disabled = not has_selected_dataset or self._get_selected_dataset() not in self.active_datasets
            
            # Export button: enabled when dataset is selected
            self.export_button.disabled = not has_selected_dataset
            
        except Exception as e:
            logger.error(f"Failed to update button states: {e}")
    
    def _notify_dataset_change(self, change_type: str, dataset_id: str):
        """Notify all callbacks of dataset changes"""
        try:
            for callback in self.on_dataset_change_callbacks:
                try:
                    callback(change_type, dataset_id)
                except Exception as e:
                    logger.error(f"Callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify dataset change: {e}")
    
    def _show_export_success(self, filename: str):
        """Show export success message"""
        try:
            # Update the display to show export success
            current_text = self.active_datasets_display.object
            success_message = f"\n\n**📤 Export Successful:** {filename}"
            self.active_datasets_display.object = current_text + success_message
            
            # Clear success message after a few seconds
            import threading
            import time
            
            def clear_success_message():
                time.sleep(3)
                self._update_active_datasets_display()
            
            threading.Thread(target=clear_success_message, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to show export success: {e}")
    
    def get_active_datasets(self) -> set:
        """Get set of active dataset IDs"""
        return self.active_datasets.copy()
    
    def is_dataset_active(self, dataset_id: str) -> bool:
        """Check if a dataset is active"""
        return dataset_id in self.active_datasets
    
    def get_activation_history(self) -> List[Dict]:
        """Get activation/deactivation history"""
        return self.activation_history.copy()
    
    def get_activator_statistics(self) -> Dict:
        """Get activator statistics"""
        try:
            return {
                'total_activations': len([r for r in self.activation_history if r['action'] == 'activated']),
                'total_deactivations': len([r for r in self.activation_history if r['action'] == 'deactivated']),
                'currently_active': len(self.active_datasets),
                'callbacks_registered': len(self.on_dataset_change_callbacks),
                'last_activation': next((r['timestamp'] for r in reversed(self.activation_history) if r['action'] == 'activated'), None),
                'last_deactivation': next((r['timestamp'] for r in reversed(self.activation_history) if r['action'] == 'deactivated'), None)
            }
        except Exception as e:
            logger.error(f"Failed to get activator statistics: {e}")
            return {}
    
    def clear_activation_history(self) -> int:
        """Clear activation history and return count"""
        try:
            count = len(self.activation_history)
            self.activation_history.clear()
            logger.info(f"🗑️ Cleared {count} activation records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear activation history: {e}")
            return 0
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'activate_button': self.activate_button,
            'deactivate_button': self.deactivate_button,
            'export_button': self.export_button,
            'active_datasets_display': self.active_datasets_display
        }
    
    def get_component(self, component_name: str = None):
        """Get a specific component by name or the entire layout if no name provided"""
        if component_name is None:
            # Return the entire layout
            return self.create_component_layout()
        else:
            # Return specific component
            components = self.get_components()
            return components.get(component_name)
    
    def create_component_layout(self):
        """Create the dataset activator component layout"""
        import panel as pn
        
        # Create the layout with all components
        return pn.Column(
            pn.pane.Markdown(f"### 📁 Dataset Activator - {self.module_name}"),
            pn.Row(
                self.activate_button,
                self.deactivate_button,
                self.export_button,
                align='center'
            ),
            self.active_datasets_display,
            sizing_mode='stretch_width'
        )
