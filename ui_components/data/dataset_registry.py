#!/usr/bin/env python3
"""
TradePulse Data - Dataset Registry
Manages dataset metadata and availability
"""

import pandas as pd
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatasetRegistry:
    """Manages dataset metadata and availability"""
    
    def __init__(self):
        self.datasets = {}
        self.module_access = {
            'portfolio': ['price_data', 'uploaded_datasets'],
            'models': ['price_data', 'uploaded_datasets'],
            'ai': ['price_data', 'uploaded_datasets', 'ml_predictions'],
            'charts': ['price_data', 'uploaded_datasets'],
            'alerts': ['price_data', 'uploaded_datasets', 'alerts'],
            'system': ['uploaded_datasets', 'system_metrics']
        }
    
    def register_dataset(self, dataset_id: str, name: str, data_type: str = 'uploaded',
                        modules: Optional[List[str]] = None) -> bool:
        """Register a new dataset"""
        try:
            if dataset_id in self.datasets:
                logger.warning(f"Dataset {dataset_id} already registered")
                return False
            
            self.datasets[dataset_id] = {
                'id': dataset_id,
                'name': name,
                'type': data_type,
                'available': True,
                'modules': modules or list(self.module_access.keys()),
                'registered_at': datetime.now(),
                'last_updated': datetime.now(),
                'metadata': {}
            }
            
            logger.info(f"✅ Dataset registered: {dataset_id} ({name})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register dataset: {e}")
            return False
    
    def unregister_dataset(self, dataset_id: str) -> bool:
        """Unregister a dataset"""
        try:
            if dataset_id in self.datasets:
                del self.datasets[dataset_id]
                logger.info(f"✅ Dataset unregistered: {dataset_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unregister dataset: {e}")
            return False
    
    def get_dataset_info(self, dataset_id: str) -> Optional[Dict]:
        """Get dataset information"""
        return self.datasets.get(dataset_id)
    
    def get_all_datasets(self) -> List[Dict]:
        """Get all registered datasets"""
        return list(self.datasets.values())
    
    def get_datasets_by_type(self, data_type: str) -> List[Dict]:
        """Get datasets by type"""
        return [ds for ds in self.datasets.values() if ds['type'] == data_type]
    
    def get_datasets_for_module(self, module: str) -> List[Dict]:
        """Get datasets available for a specific module"""
        if module not in self.module_access:
            return []
        
        available_types = self.module_access[module]
        return [ds for ds in self.datasets.values() 
                if ds['available'] and any(t in ds['modules'] for t in available_types)]
    
    def update_dataset_metadata(self, dataset_id: str, metadata: Dict) -> bool:
        """Update dataset metadata"""
        try:
            if dataset_id in self.datasets:
                self.datasets[dataset_id]['metadata'].update(metadata)
                self.datasets[dataset_id]['last_updated'] = datetime.now()
                logger.info(f"✅ Dataset metadata updated: {dataset_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update dataset metadata: {e}")
            return False
    
    def set_dataset_availability(self, dataset_id: str, available: bool) -> bool:
        """Set dataset availability"""
        try:
            if dataset_id in self.datasets:
                self.datasets[dataset_id]['available'] = available
                self.datasets[dataset_id]['last_updated'] = datetime.now()
                logger.info(f"✅ Dataset availability set: {dataset_id} = {available}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to set dataset availability: {e}")
            return False
    
    def get_registry_statistics(self) -> Dict:
        """Get registry statistics"""
        try:
            total_datasets = len(self.datasets)
            type_counts = {}
            module_counts = {}
            
            for dataset in self.datasets.values():
                # Count by type
                ds_type = dataset['type']
                type_counts[ds_type] = type_counts.get(ds_type, 0) + 1
                
                # Count by module availability
                for module in dataset['modules']:
                    module_counts[module] = module_counts.get(module, 0) + 1
            
            return {
                'total_datasets': total_datasets,
                'type_distribution': type_counts,
                'module_distribution': module_counts,
                'available_datasets': sum(1 for ds in self.datasets.values() if ds['available'])
            }
            
        except Exception as e:
            logger.error(f"Failed to get registry statistics: {e}")
            return {}
    
    def validate_dataset_access(self, dataset_id: str, module: str) -> bool:
        """Validate if a module can access a dataset"""
        try:
            if dataset_id not in self.datasets:
                return False
            
            dataset = self.datasets[dataset_id]
            if not dataset['available']:
                return False
            
            if module not in self.module_access:
                return False
            
            # Check if module has access to dataset types
            module_types = self.module_access[module]
            return any(t in dataset['modules'] for t in module_types)
            
        except Exception as e:
            logger.error(f"Failed to validate dataset access: {e}")
            return False
    
    def search_datasets(self, query: str, search_fields: List[str] = None) -> List[Dict]:
        """Search datasets by query"""
        try:
            if not search_fields:
                search_fields = ['name', 'type']
            
            results = []
            query_lower = query.lower()
            
            for dataset in self.datasets.values():
                for field in search_fields:
                    if field in dataset and query_lower in str(dataset[field]).lower():
                        results.append(dataset)
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search datasets: {e}")
            return []
    
    def clear_registry(self) -> int:
        """Clear all datasets and return count"""
        try:
            count = len(self.datasets)
            self.datasets.clear()
            logger.info(f"🗑️ Cleared {count} datasets from registry")
            return count
        except Exception as e:
            logger.error(f"Failed to clear registry: {e}")
            return 0
