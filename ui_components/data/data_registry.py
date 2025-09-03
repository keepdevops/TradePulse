#!/usr/bin/env python3
"""
TradePulse Data Manager - Registry
Dataset registry and management functionality
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DataRegistry:
    """Dataset registry and management functionality"""
    
    def __init__(self):
        self.dataset_registry = {}   # Registry of available datasets
        self.active_datasets = {}    # Currently active datasets for each module
    
    def add_uploaded_data(self, key: str, data: pd.DataFrame, metadata: Optional[Dict], global_store) -> str:
        """Add uploaded data to the global store"""
        try:
            # Generate unique dataset ID
            dataset_id = f"dataset_{key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Prepare metadata with enhanced information
            enhanced_metadata = {
                **(metadata or {}),
                'upload_time': datetime.now(),
                'shape': data.shape,
                'columns': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum(),
                'access_count': 0,
                'last_accessed': datetime.now()
            }
            
            # Add to global store
            success = global_store.add_uploaded_data(dataset_id, data, enhanced_metadata)
            
            if success:
                # Add to local dataset registry
                self.dataset_registry[dataset_id] = {
                    'name': key,
                    'type': 'uploaded',
                    'available': True,
                    'modules': ['portfolio', 'models', 'ai', 'charts', 'alerts', 'system']
                }
                
                logger.info(f"✅ Uploaded data added: {dataset_id} ({data.shape[0]} rows, {data.shape[1]} cols)")
                return dataset_id
            else:
                raise Exception("Failed to add data to global store")
            
        except Exception as e:
            logger.error(f"❌ Failed to add uploaded data: {e}")
            raise
    
    def get_dataset(self, dataset_id: str, global_store) -> Optional[pd.DataFrame]:
        """Get a specific dataset by ID from global store"""
        datasets = global_store.get_uploaded_data(dataset_id)
        if dataset_id in datasets:
            return datasets[dataset_id]
        return None
    
    def get_available_datasets(self, module_name: str, global_store) -> Dict[str, Any]:
        """Get available datasets for a specific module or all modules"""
        return global_store.get_available_datasets(module_name)
    
    def activate_dataset_for_module(self, dataset_id: str, module_name: str, global_store) -> bool:
        """Activate a dataset for use by a specific module"""
        try:
            datasets = global_store.get_uploaded_data(dataset_id)
            if dataset_id in datasets:
                if module_name not in self.active_datasets:
                    self.active_datasets[module_name] = {}
                
                data = datasets[dataset_id]
                self.active_datasets[module_name][dataset_id] = {
                    'activated_time': datetime.now(),
                    'data_shape': data.shape
                }
                
                logger.info(f"✅ Dataset {dataset_id} activated for {module_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to activate dataset {dataset_id} for {module_name}: {e}")
            return False
    
    def get_active_datasets_for_module(self, module_name: str, global_store) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for a specific module"""
        active_data = {}
        if module_name in self.active_datasets:
            for dataset_id in self.active_datasets[module_name]:
                datasets = global_store.get_uploaded_data(dataset_id)
                if dataset_id in datasets:
                    active_data[dataset_id] = datasets[dataset_id].copy()
        return active_data
    
    def get_data_for_module(self, module_name: str, data_type: str, module_data_access: Dict, data_manager) -> Dict[str, Any]:
        """Get all relevant data for a specific module"""
        module_data = {}
        
        if module_name in module_data_access:
            allowed_data_types = module_data_access[module_name]
            
            for data_type_name in allowed_data_types:
                if data_type == 'all' or data_type == data_type_name:
                    if data_type_name == 'price_data':
                        module_data['price_data'] = data_manager.price_data
                    elif data_type_name == 'uploaded_datasets':
                        module_data['uploaded_datasets'] = self.get_active_datasets_for_module(module_name, data_manager.global_store)
                    elif data_type_name == 'ml_predictions':
                        module_data['ml_predictions'] = data_manager.ml_predictions
                    elif data_type_name == 'alerts':
                        module_data['alerts'] = data_manager.alerts
                    elif data_type_name == 'portfolio_data':
                        module_data['portfolio_data'] = data_manager.portfolio_data
        
        return module_data
    
    def search_datasets(self, query: str, module_name: str, global_store) -> Dict[str, Any]:
        """Search datasets by name, columns, or content"""
        results = {}
        query_lower = query.lower()
        
        available_datasets = global_store.get_available_datasets(module_name)
        
        for dataset_id, metadata in available_datasets.items():
            # Check if dataset is available for the module
            if module_name and dataset_id in self.dataset_registry:
                if module_name not in self.dataset_registry[dataset_id]['modules']:
                    continue
            
            # Search in dataset name
            if query_lower in metadata.get('name', '').lower():
                results[dataset_id] = metadata
                continue
            
            # Search in column names
            if 'columns' in metadata and any(query_lower in col.lower() for col in metadata['columns']):
                results[dataset_id] = metadata
                continue
            
            # Search in metadata
            if query_lower in str(metadata).lower():
                results[dataset_id] = metadata
                continue
        
        return results
    
    def get_dataset_statistics(self, global_store, module_data_access: Dict) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        available_datasets = global_store.get_available_datasets()
        uploaded_data = global_store.get_uploaded_data()
        
        stats = {
            'total_datasets': len(available_datasets),
            'total_rows': sum(data.shape[0] for data in uploaded_data.values()),
            'total_columns': sum(data.shape[1] for data in uploaded_data.values()),
            'total_memory': sum(metadata.get('memory_usage', 0) for metadata in available_datasets.values()),
            'dataset_types': {},
            'module_usage': {module: len(self.active_datasets.get(module, {})) for module in module_data_access.keys()}
        }
        
        # Count dataset types
        for metadata in available_datasets.values():
            dataset_type = metadata.get('type', 'unknown')
            stats['dataset_types'][dataset_type] = stats['dataset_types'].get(dataset_type, 0) + 1
        
        return stats
    
    def cleanup_old_datasets(self, days_old: int, uploaded_datasets: Dict) -> int:
        """Clean up datasets older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        datasets_to_remove = []
        
        for dataset_id, info in uploaded_datasets.items():
            if info['upload_time'] < cutoff_date:
                datasets_to_remove.append(dataset_id)
        
        # Remove old datasets
        for dataset_id in datasets_to_remove:
            if dataset_id in uploaded_datasets:
                del uploaded_datasets[dataset_id]
            if dataset_id in self.dataset_registry:
                del self.dataset_registry[dataset_id]
            
            # Remove from active datasets
            for module_name in self.active_datasets:
                if dataset_id in self.active_datasets[module_name]:
                    del self.active_datasets[module_name][dataset_id]
        
        logger.info(f"🧹 Cleaned up {len(datasets_to_remove)} old datasets")
        return len(datasets_to_remove)

