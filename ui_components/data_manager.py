#!/usr/bin/env python3
"""
TradePulse UI Data Manager
Enhanced data manager with upload support for all modules
"""

import logging
from typing import Dict, List, Optional, Any
import pandas as pd

from .data_manager_core import data_manager_core
from .data_manager_ops import DataManagerOps

logger = logging.getLogger(__name__)

class DataManager:
    """Enhanced data manager for the UI with upload support"""
    
    def __init__(self):
        self.core = data_manager_core
        self.ops = DataManagerOps(self.core)
        
        # Update core methods to use operations
        self.core.generate_sample_price_data = self.ops.generate_sample_price_data
        self.core.generate_sample_portfolio_data = self.ops.generate_sample_portfolio_data
        self.core.generate_sample_ml_predictions = self.ops.generate_sample_ml_predictions
    
    @property
    def uploaded_datasets(self):
        """Access uploaded datasets from global store"""
        return self.core.uploaded_datasets
    
    @property
    def symbols(self):
        """Access symbols from core"""
        return self.core.symbols
    
    def load_initial_data(self):
        """Load initial data for the system"""
        return self.core.load_initial_data()
    
    def add_uploaded_data(self, key: str, data, metadata: Optional[Dict] = None) -> str:
        """Add uploaded data to the global store for use by all modules across all instances"""
        return self.core.add_uploaded_data(key, data, metadata)
    
    def get_dataset(self, dataset_id: str):
        """Get a specific dataset by ID"""
        return self.core.get_dataset(dataset_id)
    
    def get_available_datasets(self, module: Optional[str] = None) -> List[str]:
        """Get list of available datasets, optionally filtered by module"""
        return self.core.get_available_datasets(module)
    
    def activate_dataset_for_module(self, dataset_id: str, module: str) -> bool:
        """Activate a dataset for a specific module"""
        return self.core.activate_dataset_for_module(dataset_id, module)
    
    def deactivate_dataset_for_module(self, dataset_id: str, module: str) -> bool:
        """Deactivate a dataset for a specific module"""
        return self.core.deactivate_dataset_for_module(dataset_id, module)
    
    def get_active_datasets_for_module(self, module: str) -> Dict[str, Any]:
        """Get active datasets for a specific module"""
        return self.core.get_active_datasets_for_module(module)
    
    def search_datasets(self, query: str) -> Dict[str, Dict]:
        """Search datasets by name, type, or metadata"""
        return self.core.search_datasets(query)
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        return self.core.get_dataset_statistics()
    
    def cleanup_old_datasets(self, days_old: int = 30) -> int:
        """Clean up datasets older than specified days"""
        return self.ops.cleanup_old_datasets(days_old)
    
    def export_dataset(self, dataset_id: str, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        return self.ops.export_dataset(dataset_id, format, filepath)
    
    def get_price_data(self, symbol: str = None) -> Dict[str, pd.DataFrame]:
        """Get price data for symbols"""
        return self.ops.get_price_data(symbol)
    
    def get_price_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        """Get price data for a specific symbol as DataFrame"""
        return self.ops.get_price_data_for_symbol(symbol)
    
    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get portfolio data"""
        return self.ops.get_portfolio_data()
    
    def get_ml_predictions(self) -> Dict[str, Any]:
        """Get ML predictions"""
        return self.ops.get_ml_predictions()
    
    def update_price_data(self, symbol: str, new_data):
        """Update price data for a symbol"""
        return self.ops.update_price_data(symbol, new_data)
