#!/usr/bin/env python3
"""
TradePulse Data Manager - Core Functionality
Core data manager class with basic functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json

from ..global_data_store import get_global_data_store
from .data_operations import DataOperations
from .data_registry import DataRegistry
from .data_export import DataExport

logger = logging.getLogger(__name__)

class DataManagerCore:
    """Core data manager functionality"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.portfolio_data = {}
        self.ml_predictions = {}
        self.alerts = []
        self.orders = []
        
        # Use global data store for uploaded datasets
        self.global_store = get_global_data_store()
        
        # Initialize components
        self.operations = DataOperations()
        self.registry = DataRegistry()
        self.export = DataExport()
        
        # Module-specific data access
        self.module_data_access = {
            'portfolio': ['price_data', 'uploaded_datasets'],
            'models': ['price_data', 'uploaded_datasets'],
            'ai': ['price_data', 'uploaded_datasets', 'ml_predictions'],
            'charts': ['price_data', 'uploaded_datasets'],
            'alerts': ['price_data', 'uploaded_datasets', 'alerts'],
            'system': ['uploaded_datasets', 'system_metrics']
        }
        
        self.load_initial_data()
        logger.info("📊 Enhanced DataManager initialized with upload support")
    
    @property
    def uploaded_datasets(self):
        """Access uploaded datasets from global store"""
        return self.global_store.uploaded_datasets
    
    def load_initial_data(self):
        """Load initial data for the system"""
        logger.info("📊 Loading initial data...")
        
        # Generate sample price data
        for symbol in self.symbols:
            self.price_data[symbol] = self.operations.generate_sample_price_data(symbol)
        
        # Generate sample portfolio data
        self.portfolio_data = self.operations.generate_sample_portfolio_data()
        
        # Generate sample ML predictions
        self.ml_predictions = self.operations.generate_sample_ml_predictions()
        
        logger.info("✅ Initial data loaded successfully")
    
    def add_uploaded_data(self, key: str, data: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """Add uploaded data to the global store"""
        return self.registry.add_uploaded_data(key, data, metadata, self.global_store)
    
    def get_dataset(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset by ID from global store"""
        return self.registry.get_dataset(dataset_id, self.global_store)
    
    def get_available_datasets(self, module_name: str = None) -> Dict[str, Any]:
        """Get available datasets for a specific module or all modules"""
        return self.registry.get_available_datasets(module_name, self.global_store)
    
    def activate_dataset_for_module(self, dataset_id: str, module_name: str) -> bool:
        """Activate a dataset for use by a specific module"""
        return self.registry.activate_dataset_for_module(dataset_id, module_name, self.global_store)
    
    def get_active_datasets_for_module(self, module_name: str) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for a specific module"""
        return self.registry.get_active_datasets_for_module(module_name, self.global_store)
    
    def get_data_for_module(self, module_name: str, data_type: str = 'all') -> Dict[str, Any]:
        """Get all relevant data for a specific module"""
        return self.registry.get_data_for_module(module_name, data_type, self.module_data_access, self)
    
    def search_datasets(self, query: str, module_name: str = None) -> Dict[str, Any]:
        """Search datasets by name, columns, or content"""
        return self.registry.search_datasets(query, module_name, self.global_store)
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        return self.registry.get_dataset_statistics(self.global_store, self.module_data_access)
    
    def cleanup_old_datasets(self, days_old: int = 30) -> int:
        """Clean up datasets older than specified days"""
        return self.registry.cleanup_old_datasets(days_old, self.uploaded_datasets)
    
    def export_dataset(self, dataset_id: str, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        return self.export.export_dataset(dataset_id, self.uploaded_datasets, format, filepath)
    
    # Backward compatibility methods
    def get_price_data(self, symbol: str = None) -> Dict[str, pd.DataFrame]:
        """Get price data for symbols"""
        if symbol:
            return {symbol: self.price_data.get(symbol, pd.DataFrame())}
        return self.price_data
    
    def get_price_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        """Get price data for a specific symbol as DataFrame"""
        return self.price_data.get(symbol, pd.DataFrame())
    
    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get portfolio data"""
        return self.portfolio_data
    
    def get_ml_predictions(self) -> Dict[str, Any]:
        """Get ML predictions"""
        return self.ml_predictions
    
    def update_price_data(self, symbol: str, new_data: pd.DataFrame):
        """Update price data for a symbol"""
        self.price_data[symbol] = new_data
        logger.info(f"📊 Price data updated for {symbol}")
