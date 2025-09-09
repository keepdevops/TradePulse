#!/usr/bin/env python3
"""
TradePulse Unified Data Access System
Provides unified access to both API data and uploaded data for all modules
"""

import logging
from typing import Dict, List, Optional, Any, Union
import pandas as pd

from .data_access_core import data_access_manager_core
from .data_access_file_ops import DataAccessFileOps

logger = logging.getLogger(__name__)

class DataAccessManager:
    """Unified data access manager for all modules"""
    
    def __init__(self, data_manager):
        logger.info(f"🔧 Initializing DataAccessManager with data_manager: {data_manager}")
        
        # Initialize the global instance properly
        global data_access_manager_core
        if data_access_manager_core is None:
            logger.info("🔧 Creating new data_access_manager_core instance")
            # Import here to avoid circular import
            from .data_access_core import DataAccessManager as CoreDataAccessManager
            data_access_manager_core = CoreDataAccessManager(data_manager)
        else:
            logger.info("🔧 Using existing data_access_manager_core instance")
        
        self.core = data_access_manager_core
        logger.info(f"🔧 Core data_manager: {self.core.data_manager}")
        
        # Ensure data_manager is set on the core
        if self.core.data_manager is None:
            logger.info("🔧 Setting data_manager on core")
            self.core.data_manager = data_manager
        
        self.file_ops = DataAccessFileOps(self.core)
        
        # Update API sources to use file operations
        self.core.api_sources.update({
            'mock': self.file_ops._generate_mock_data,
            'upload': self.file_ops._fetch_upload_data
        })
        
        logger.info("✅ DataAccessManager initialized successfully")
    
    def get_data(self, source: str, symbol: str, timeframe: str = '1d', 
                 start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Get data from specified source"""
        return self.core.get_data(source, symbol, timeframe, start_date, end_date)
    
    def get_uploaded_data(self, dataset_id: Optional[str] = None, 
                         module: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Get uploaded data for specific module or dataset"""
        return self.core.get_uploaded_data(dataset_id, module)
    
    def get_combined_data(self, symbols: List[str], source: str = 'yahoo', 
                         uploaded_datasets: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Get combined API and uploaded data"""
        return self.core.get_combined_data(symbols, source, uploaded_datasets)
    
    def clear_cache(self):
        """Clear the data cache"""
        return self.core.clear_cache()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.core.get_cache_stats()
    
    def get_available_data_files(self) -> Dict[str, List[str]]:
        """Get list of available data files by type"""
        return self.file_ops.get_available_data_files()
