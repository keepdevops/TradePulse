#!/usr/bin/env python3
"""
TradePulse Dataset Activator - Operations
Dataset-related operations for the dataset activator
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any, Set
from datetime import datetime

logger = logging.getLogger(__name__)

class DatasetActivatorOperations:
    """Dataset-related operations for dataset activator"""
    
    def activate_dataset(self, selected_dataset: Optional[str], active_datasets: Set[str], 
                        activation_history: List[Dict], module_name: str, callbacks):
        """Activate a dataset for the current module"""
        try:
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for activation")
                return
            
            if selected_dataset in active_datasets:
                logger.info(f"📊 Dataset {selected_dataset} is already active for {module_name}")
                return
            
            # Activate dataset
            active_datasets.add(selected_dataset)
            
            # Record activation
            self._record_activation(activation_history, selected_dataset, 'activated', module_name)
            
            # Notify callbacks
            callbacks.notify_dataset_change('activated', selected_dataset)
            
            logger.info(f"✅ Dataset {selected_dataset} activated for {module_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to activate dataset: {e}")
    
    def deactivate_dataset(self, selected_dataset: Optional[str], active_datasets: Set[str], 
                          activation_history: List[Dict], module_name: str, callbacks):
        """Deactivate a dataset for the current module"""
        try:
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for deactivation")
                return
            
            if selected_dataset not in active_datasets:
                logger.info(f"📊 Dataset {selected_dataset} is not active for {module_name}")
                return
            
            # Deactivate dataset
            active_datasets.remove(selected_dataset)
            
            # Record deactivation
            self._record_activation(activation_history, selected_dataset, 'deactivated', module_name)
            
            # Notify callbacks
            callbacks.notify_dataset_change('deactivated', selected_dataset)
            
            logger.info(f"✅ Dataset {selected_dataset} deactivated for {module_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to deactivate dataset: {e}")
    
    def export_dataset(self, selected_dataset: Optional[str], data_manager, module_name: str, 
                      active_datasets_display):
        """Export the currently selected dataset"""
        try:
            if not selected_dataset:
                logger.warning("⚠️ No dataset selected for export")
                return
            
            # Get dataset data
            dataset_data = data_manager.get_dataset(selected_dataset)
            
            if dataset_data is not None:
                # Create export filename
                export_filename = f"{selected_dataset}_{module_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                # Export to CSV
                dataset_data.to_csv(export_filename, index=False)
                
                logger.info(f"📤 Dataset {selected_dataset} exported to {export_filename}")
                
                # Show success message
                self._show_export_success(active_datasets_display, export_filename)
            else:
                logger.warning(f"⚠️ Could not retrieve dataset {selected_dataset} for export")
                
        except Exception as e:
            logger.error(f"❌ Failed to export dataset: {e}")
    
    def _record_activation(self, activation_history: List[Dict], dataset_id: str, action: str, module_name: str):
        """Record dataset activation/deactivation"""
        try:
            activation_record = {
                'timestamp': pd.Timestamp.now(),
                'dataset_id': dataset_id,
                'action': action,
                'module': module_name
            }
            activation_history.append(activation_record)
            
        except Exception as e:
            logger.error(f"Failed to record activation: {e}")
    
    def _show_export_success(self, active_datasets_display, filename: str):
        """Show export success message"""
        try:
            # Update the display to show export success
            current_text = active_datasets_display.object
            success_message = f"\n\n**📤 Export Successful:** {filename}"
            active_datasets_display.object = current_text + success_message
            
            # Clear success message after a few seconds
            import threading
            import time
            
            def clear_success_message():
                time.sleep(3)
                # Restore original display
                if "Export Successful" in active_datasets_display.object:
                    active_datasets_display.object = current_text
            
            threading.Thread(target=clear_success_message, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to show export success: {e}")
    
    def get_activator_statistics(self, activation_history: List[Dict], active_datasets: Set[str], callbacks) -> Dict:
        """Get activator statistics"""
        try:
            return {
                'total_activations': len([r for r in activation_history if r['action'] == 'activated']),
                'total_deactivations': len([r for r in activation_history if r['action'] == 'deactivated']),
                'currently_active': len(active_datasets),
                'callbacks_registered': len(callbacks.get_callbacks()),
                'last_activation': next((r['timestamp'] for r in reversed(activation_history) if r['action'] == 'activated'), None),
                'last_deactivation': next((r['timestamp'] for r in reversed(activation_history) if r['action'] == 'deactivated'), None)
            }
        except Exception as e:
            logger.error(f"Failed to get activator statistics: {e}")
            return {}
    
    def clear_activation_history(self, activation_history: List[Dict]) -> int:
        """Clear activation history and return count"""
        try:
            count = len(activation_history)
            activation_history.clear()
            logger.info(f"🗑️ Cleared {count} activation records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear activation history: {e}")
            return 0
    
    def validate_dataset_id(self, dataset_id: str) -> bool:
        """Validate dataset ID format"""
        if not dataset_id or not isinstance(dataset_id, str):
            return False
        
        # Add any specific validation rules here
        return len(dataset_id.strip()) > 0
    
    def get_activation_summary(self, activation_history: List[Dict], active_datasets: Set[str]) -> str:
        """Get activation summary"""
        if not activation_history:
            return "No activation history available"
        
        stats = self.get_activator_statistics(activation_history, active_datasets, None)
        
        summary_lines = [
            f"**Total Activations**: {stats['total_activations']}",
            f"**Total Deactivations**: {stats['total_deactivations']}",
            f"**Currently Active**: {stats['currently_active']}",
            f"**Active Datasets**: {', '.join(sorted(active_datasets)) if active_datasets else 'None'}"
        ]
        
        return "\n".join(summary_lines)

