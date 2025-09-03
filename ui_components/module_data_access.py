#!/usr/bin/env python3
"""
TradePulse Module Data Access Component
Provides unified data access for each module (under 200 lines)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ModuleDataAccess:
    """Unified data access component for individual modules"""
    
    def __init__(self, data_manager, data_access_manager, module_name: str):
        self.data_manager = data_manager
        self.data_access = data_access_manager
        self.data_access_manager = data_access_manager  # Expose the manager directly
        self.module_name = module_name
        self.active_datasets = {}
        self.data_cache = {}
        
    def get_api_data(self, symbols: List[str], source: str = 'yahoo', 
                    timeframe: str = '1d') -> Dict[str, pd.DataFrame]:
        """Get API data for specified symbols"""
        try:
            data = {}
            for symbol in symbols:
                df = self.data_access.get_data(source, symbol, timeframe)
                if not df.empty:
                    data[symbol] = df
                    logger.info(f"📊 {self.module_name}: Loaded API data for {symbol}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get API data: {e}")
            return {}
    
    def get_uploaded_data(self, dataset_ids: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Get uploaded data for this module"""
        try:
            if dataset_ids:
                # Get specific datasets
                data = {}
                for dataset_id in dataset_ids:
                    df = self.data_access.get_uploaded_data(dataset_id)
                    if not df.empty:
                        data[dataset_id] = df
                        logger.info(f"📁 {self.module_name}: Loaded uploaded data {dataset_id}")
                return data
            else:
                # Get all available datasets for this module
                return self.data_access.get_uploaded_data(module=self.module_name)
                
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get uploaded data: {e}")
            return {}
    
    def get_combined_data(self, symbols: List[str], dataset_ids: Optional[List[str]] = None,
                         source: str = 'yahoo') -> Dict[str, pd.DataFrame]:
        """Get combined API and uploaded data"""
        try:
            combined_data = {}
            
            # Get API data
            api_data = self.get_api_data(symbols, source)
            combined_data.update(api_data)
            
            # Get uploaded data
            uploaded_data = self.get_uploaded_data(dataset_ids)
            combined_data.update(uploaded_data)
            
            logger.info(f"🔄 {self.module_name}: Combined {len(combined_data)} datasets")
            return combined_data
            
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get combined data: {e}")
            return {}
    
    def activate_dataset(self, dataset_id: str) -> bool:
        """Activate a dataset for this module"""
        try:
            data = self.data_access.get_uploaded_data(dataset_id)
            if not data.empty:
                self.active_datasets[dataset_id] = data
                logger.info(f"✅ {self.module_name}: Activated dataset {dataset_id}")
                return True
            else:
                logger.warning(f"⚠️ {self.module_name}: Dataset {dataset_id} is empty")
                return False
                
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to activate dataset {dataset_id}: {e}")
            return False
    
    def deactivate_dataset(self, dataset_id: str) -> bool:
        """Deactivate a dataset for this module"""
        try:
            if dataset_id in self.active_datasets:
                del self.active_datasets[dataset_id]
                logger.info(f"✅ {self.module_name}: Deactivated dataset {dataset_id}")
                return True
            else:
                logger.warning(f"⚠️ {self.module_name}: Dataset {dataset_id} not active")
                return False
                
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to deactivate dataset {dataset_id}: {e}")
            return False
    
    def is_data_access_available(self) -> bool:
        """Check if data access manager is available"""
        return self.data_access_manager is not None
    
    def get_active_datasets(self) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for this module"""
        return self.active_datasets.copy()
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available datasets for this module"""
        try:
            return self.data_manager.get_available_datasets(self.module_name)
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get available datasets: {e}")
            return []
    
    def get_dataset_info(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific dataset"""
        try:
            if dataset_id in self.data_manager.uploaded_datasets:
                dataset_info = self.data_manager.uploaded_datasets[dataset_id]
                return {
                    'id': dataset_id,
                    'shape': dataset_info['shape'],
                    'columns': dataset_info['columns'],
                    'upload_time': dataset_info['upload_time'],
                    'memory_usage': dataset_info['memory_usage'],
                    'access_count': dataset_info['access_count']
                }
            return None
            
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get dataset info: {e}")
            return None
    
    def clear_cache(self):
        """Clear module's data cache"""
        self.data_cache.clear()
        logger.info(f"🗑️ {self.module_name}: Cache cleared")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of data available to this module"""
        try:
            summary = {
                'module': self.module_name,
                'active_datasets': len(self.active_datasets),
                'available_datasets': len(self.get_available_datasets()),
                'cache_size': len(self.data_cache),
                'active_dataset_ids': list(self.active_datasets.keys())
            }
            return summary
            
        except Exception as e:
            logger.error(f"❌ {self.module_name}: Failed to get data summary: {e}")
            return {'module': self.module_name, 'error': str(e)}
