#!/usr/bin/env python3
"""
TradePulse Dataset Selector Operations
Operations for dataset selection and management
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DatasetSelectorOperations:
    """Operations for dataset selection and management"""
    
    def __init__(self, data_manager, module_name: Optional[str] = None):
        self.data_manager = data_manager
        self.module_name = module_name
        self.selection_history = []
        self.active_selections = {}
        
        # UI component references (will be set by main component)
        self.dataset_info = None
        self.preview_table = None
        self.active_datasets_display = None
        self.export_button = None
        
        logger.info(f"🔧 Dataset Selector Operations initialized for module: {module_name}")
    
    def refresh_datasets(self, datasets_list, active_datasets_display):
        """Refresh the list of available datasets"""
        try:
            # Get available datasets for this module
            available_datasets = self.data_manager.get_available_datasets(self.module_name)
            
            # Get all datasets if no module-specific filtering
            if not available_datasets:
                available_datasets = self.data_manager.get_available_datasets()
            
            # Create options list
            options = []
            for dataset_id, info in available_datasets.items():
                if hasattr(self.data_manager, 'uploaded_datasets') and dataset_id in self.data_manager.uploaded_datasets:
                    dataset_info = self.data_manager.uploaded_datasets[dataset_id]
                    display_name = f"{info.get('name', dataset_id)} ({dataset_info['shape'][0]} rows × {dataset_info['shape'][1]} cols)"
                    options.append((display_name, dataset_id))
                else:
                    display_name = f"{info.get('name', dataset_id)}"
                    options.append((display_name, dataset_id))
            
            datasets_list.options = options
            
            # Update active datasets display
            self.update_active_datasets_display(active_datasets_display)
            
        except Exception as e:
            logger.error(f"Failed to refresh datasets: {e}")
    
    def update_active_datasets_display(self, active_datasets_display):
        """Update the active datasets display"""
        try:
            active_datasets = self.get_active_datasets(self.module_name)
            if active_datasets:
                display_text = "**Active Datasets:**\n\n"
                for dataset_id, info in active_datasets.items():
                    display_text += f"- **{dataset_id}** (selected at {info['selected_at'].strftime('%H:%M:%S')})\n"
                active_datasets_display.object = display_text
            else:
                active_datasets_display.object = "**Active Datasets:** None"
        except Exception as e:
            logger.error(f"Failed to update active datasets display: {e}")
            active_datasets_display.object = "**Active Datasets:** Error loading"
    
    def get_available_datasets(self, module: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of available datasets"""
        try:
            if self.data_manager is None:
                return []
            
            available_datasets = self.data_manager.get_available_datasets(module)
            dataset_list = []
            
            for dataset_id in available_datasets:
                try:
                    dataset_data = self.data_manager.get_dataset(dataset_id)
                    if dataset_data is not None and not dataset_data.empty:
                        dataset_list.append({
                            'id': dataset_id,
                            'name': dataset_id,
                            'rows': len(dataset_data),
                            'columns': len(dataset_data.columns),
                            'columns_list': dataset_data.columns.tolist(),
                            'type': 'uploaded',
                            'last_accessed': datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.warning(f"⚠️ Error processing dataset {dataset_id}: {e}")
            
            return dataset_list
            
        except Exception as e:
            logger.error(f"❌ Error getting available datasets: {e}")
            return []
    
    def select_dataset(self, dataset_id: str, module: str) -> Dict[str, Any]:
        """Select a dataset for a specific module"""
        try:
            if self.data_manager is None:
                return {
                    'success': False,
                    'error': 'Data manager not available'
                }
            
            # Check if dataset exists
            dataset_data = self.data_manager.get_dataset(dataset_id)
            if dataset_data is None or dataset_data.empty:
                return {
                    'success': False,
                    'error': f'Dataset {dataset_id} not found or empty'
                }
            
            # Record selection
            selection_record = {
                'dataset_id': dataset_id,
                'module': module,
                'selection_time': datetime.now(),
                'rows': len(dataset_data),
                'columns': len(dataset_data.columns)
            }
            
            self.selection_history.append(selection_record)
            
            # Update active selections
            if module not in self.active_selections:
                self.active_selections[module] = {}
            
            self.active_selections[module][dataset_id] = {
                'selected_at': datetime.now(),
                'rows': len(dataset_data),
                'columns': len(dataset_data.columns)
            }
            
            logger.info(f"✅ Dataset {dataset_id} selected for module {module}")
            
            return {
                'success': True,
                'dataset_id': dataset_id,
                'module': module,
                'rows': len(dataset_data),
                'columns': len(dataset_data.columns),
                'columns_list': dataset_data.columns.tolist()
            }
            
        except Exception as e:
            logger.error(f"❌ Error selecting dataset {dataset_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def deselect_dataset(self, dataset_id: str, module: str) -> Dict[str, Any]:
        """Deselect a dataset for a specific module"""
        try:
            if module in self.active_selections and dataset_id in self.active_selections[module]:
                del self.active_selections[module][dataset_id]
                logger.info(f"✅ Dataset {dataset_id} deselected for module {module}")
                return {
                    'success': True,
                    'dataset_id': dataset_id,
                    'module': module
                }
            else:
                return {
                    'success': False,
                    'error': f'Dataset {dataset_id} not active for module {module}'
                }
                
        except Exception as e:
            logger.error(f"❌ Error deselecting dataset {dataset_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_active_datasets(self, module: Optional[str] = None) -> Dict[str, Any]:
        """Get currently active datasets"""
        try:
            if module:
                return self.active_selections.get(module, {})
            else:
                return self.active_selections.copy()
                
        except Exception as e:
            logger.error(f"❌ Error getting active datasets: {e}")
            return {}
    
    def get_selection_history(self) -> List[Dict[str, Any]]:
        """Get selection history"""
        return self.selection_history.copy()
    
    def clear_selection_history(self) -> int:
        """Clear selection history and return count"""
        count = len(self.selection_history)
        self.selection_history.clear()
        logger.info(f"🗑️ Cleared {count} selection records")
        return count
    
    def get_selection_stats(self) -> Dict[str, Any]:
        """Get selection statistics"""
        if not self.selection_history:
            return {
                'total_selections': 0,
                'active_modules': [],
                'most_selected_datasets': [],
                'recent_selections': []
            }
        
        # Count selections by dataset
        dataset_counts = {}
        for record in self.selection_history:
            dataset_id = record['dataset_id']
            dataset_counts[dataset_id] = dataset_counts.get(dataset_id, 0) + 1
        
        # Get most selected datasets
        most_selected = sorted(
            dataset_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Get recent selections
        recent_selections = sorted(
            self.selection_history, 
            key=lambda x: x['selection_time'], 
            reverse=True
        )[:10]
        
        return {
            'total_selections': len(self.selection_history),
            'active_modules': list(self.active_selections.keys()),
            'most_selected_datasets': most_selected,
            'recent_selections': recent_selections
        }
