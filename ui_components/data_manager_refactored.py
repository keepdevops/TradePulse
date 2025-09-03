#!/usr/bin/env python3
"""
TradePulse UI Data Manager (Refactored)
Enhanced data manager with upload support for all modules
Refactored to be under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json

from .global_data_store import get_global_data_store
from .data.data_manager_core import DataManagerCore

logger = logging.getLogger(__name__)

class DataManager:
    """Enhanced data manager for the UI with upload support"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_manager = DataManagerCore()
        
        # Expose core attributes for backward compatibility
        self.symbols = self._refactored_manager.symbols
        self.price_data = self._refactored_manager.price_data
        self.portfolio_data = self._refactored_manager.portfolio_data
        self.ml_predictions = self._refactored_manager.ml_predictions
        self.alerts = self._refactored_manager.alerts
        self.orders = self._refactored_manager.orders
        self.global_store = self._refactored_manager.global_store
        self._uploaded_datasets = None
        self.dataset_registry = self._refactored_manager.registry.dataset_registry
        self.active_datasets = self._refactored_manager.registry.active_datasets
        self.module_data_access = self._refactored_manager.module_data_access
    
    @property
    def uploaded_datasets(self):
        """Access uploaded datasets from global store"""
        return self._refactored_manager.uploaded_datasets
    
    def load_initial_data(self):
        """Load initial data for the system"""
        self._refactored_manager.load_initial_data()
    
    def add_uploaded_data(self, key: str, data: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """Add uploaded data to the global store for use by all modules across all instances"""
        return self._refactored_manager.add_uploaded_data(key, data, metadata)
    
    def get_dataset(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset by ID from global store"""
        return self._refactored_manager.get_dataset(dataset_id)
    
    def get_available_datasets(self, module_name: str = None) -> Dict[str, Any]:
        """Get available datasets for a specific module or all modules from global store"""
        return self._refactored_manager.get_available_datasets(module_name)
    
    def activate_dataset_for_module(self, dataset_id: str, module_name: str) -> bool:
        """Activate a dataset for use by a specific module"""
        return self._refactored_manager.activate_dataset_for_module(dataset_id, module_name)
    
    def get_active_datasets_for_module(self, module_name: str) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for a specific module"""
        return self._refactored_manager.get_active_datasets_for_module(module_name)
    
    def get_data_for_module(self, module_name: str, data_type: str = 'all') -> Dict[str, Any]:
        """Get all relevant data for a specific module"""
        return self._refactored_manager.get_data_for_module(module_name, data_type)
    
    def search_datasets(self, query: str, module_name: str = None) -> Dict[str, Any]:
        """Search datasets by name, columns, or content"""
        return self._refactored_manager.search_datasets(query, module_name)
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        return self._refactored_manager.get_dataset_statistics()
    
    def cleanup_old_datasets(self, days_old: int = 30) -> int:
        """Clean up datasets older than specified days"""
        return self._refactored_manager.cleanup_old_datasets(days_old)
    
    def export_dataset(self, dataset_id: str, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        return self._refactored_manager.export_dataset(dataset_id, format, filepath)
    
    # Backward compatibility methods
    def get_price_data(self, symbol: str = None) -> Dict[str, pd.DataFrame]:
        """Get price data for symbols"""
        return self._refactored_manager.get_price_data(symbol)
    
    def get_price_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        """Get price data for a specific symbol as DataFrame"""
        return self._refactored_manager.get_price_data_for_symbol(symbol)
    
    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get portfolio data"""
        return self._refactored_manager.get_portfolio_data()
    
    def get_ml_predictions(self) -> Dict[str, Any]:
        """Get ML predictions"""
        return self._refactored_manager.get_ml_predictions()
    
    def update_price_data(self, symbol: str, new_data: pd.DataFrame):
        """Update price data for a symbol"""
        self._refactored_manager.update_price_data(symbol, new_data)

