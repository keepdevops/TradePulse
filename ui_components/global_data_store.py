#!/usr/bin/env python3
"""
TradePulse Global Data Store
Provides shared data storage across all DataManager instances to solve data persistence issues
"""

import pandas as pd
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import threading

logger = logging.getLogger(__name__)

class GlobalDataStore:
    """Singleton global data store for sharing data across all DataManager instances"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GlobalDataStore, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the global data store"""
        self.uploaded_datasets = {}
        self.dataset_metadata = {}
        self.access_counts = {}
        self.initialized = True
        logger.info("🌐 Global Data Store initialized")
    
    def add_uploaded_data(self, dataset_id: str, data: pd.DataFrame, metadata: Dict[str, Any]) -> bool:
        """Add uploaded data to the global store"""
        try:
            with self._lock:
                self.uploaded_datasets[dataset_id] = data.copy()
                self.dataset_metadata[dataset_id] = metadata.copy()
                self.access_counts[dataset_id] = 0
                
                logger.info(f"🌐 Global Store: Added dataset {dataset_id} ({data.shape})")
                return True
                
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to add dataset {dataset_id}: {e}")
            return False
    
    def get_uploaded_data(self, dataset_id: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """Get uploaded data from the global store"""
        try:
            with self._lock:
                if dataset_id:
                    if dataset_id in self.uploaded_datasets:
                        self.access_counts[dataset_id] += 1
                        return {dataset_id: self.uploaded_datasets[dataset_id].copy()}
                    else:
                        return {}
                else:
                    # Return all datasets
                    result = {}
                    for ds_id, data in self.uploaded_datasets.items():
                        self.access_counts[ds_id] += 1
                        result[ds_id] = data.copy()
                    return result
                    
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to get dataset {dataset_id}: {e}")
            return {}
    
    def get_dataset_metadata(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific dataset"""
        try:
            with self._lock:
                return self.dataset_metadata.get(dataset_id, {}).copy()
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to get metadata for {dataset_id}: {e}")
            return None
    
    def get_available_datasets(self, module: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get available datasets (optionally filtered by module)"""
        try:
            with self._lock:
                result = {}
                for dataset_id, metadata in self.dataset_metadata.items():
                    # For now, all datasets are available to all modules
                    # Future enhancement: module-specific filtering
                    result[dataset_id] = metadata.copy()
                return result
                
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to get available datasets: {e}")
            return {}
    
    def remove_dataset(self, dataset_id: str) -> bool:
        """Remove a dataset from the global store"""
        try:
            with self._lock:
                if dataset_id in self.uploaded_datasets:
                    del self.uploaded_datasets[dataset_id]
                    del self.dataset_metadata[dataset_id]
                    del self.access_counts[dataset_id]
                    logger.info(f"🗑️ Global Store: Removed dataset {dataset_id}")
                    return True
                else:
                    logger.warning(f"⚠️ Global Store: Dataset {dataset_id} not found")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to remove dataset {dataset_id}: {e}")
            return False
    
    def clear_all_data(self) -> bool:
        """Clear all data from the global store"""
        try:
            with self._lock:
                count = len(self.uploaded_datasets)
                self.uploaded_datasets.clear()
                self.dataset_metadata.clear()
                self.access_counts.clear()
                logger.info(f"🗑️ Global Store: Cleared {count} datasets")
                return True
                
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to clear data: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the global data store"""
        try:
            with self._lock:
                total_datasets = len(self.uploaded_datasets)
                total_memory = sum(
                    data.memory_usage(deep=True).sum() 
                    for data in self.uploaded_datasets.values()
                )
                total_records = sum(
                    data.shape[0] 
                    for data in self.uploaded_datasets.values()
                )
                
                return {
                    'total_datasets': total_datasets,
                    'total_memory_bytes': total_memory,
                    'total_records': total_records,
                    'dataset_ids': list(self.uploaded_datasets.keys()),
                    'access_counts': self.access_counts.copy()
                }
                
        except Exception as e:
            logger.error(f"❌ Global Store: Failed to get stats: {e}")
            return {}

# Global instance
_global_data_store = None

def get_global_data_store() -> GlobalDataStore:
    """Get the global data store instance"""
    global _global_data_store
    if _global_data_store is None:
        _global_data_store = GlobalDataStore()
    return _global_data_store
