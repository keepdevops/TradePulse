#!/usr/bin/env python3
"""
TradePulse Data Manager - Core
Core data management functionality for the UI
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json
from .global_data_store import get_global_data_store

logger = logging.getLogger(__name__)

class DataManager:
    """Enhanced data manager for the UI with upload support"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.portfolio_data = {}
        self.ml_predictions = {}
        self.alerts = []
        self.orders = []
        
        # Use global data store for uploaded datasets to ensure persistence across instances
        self.global_store = get_global_data_store()
        
        # Local references to global data for backward compatibility
        self._uploaded_datasets = None  # Will be replaced by property
        self.dataset_registry = {}   # Registry of available datasets
        self.active_datasets = {}    # Currently active datasets for each module
        
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
            self.price_data[symbol] = self.generate_sample_price_data(symbol)
        
        # Generate sample portfolio data
        self.portfolio_data = self.generate_sample_portfolio_data()
        
        # Generate sample ML predictions
        self.ml_predictions = self.generate_sample_ml_predictions()
        
        logger.info("✅ Initial data loaded successfully")
    
    def generate_sample_price_data(self, symbol: str) -> pd.DataFrame:
        """Generate sample price data for a symbol"""
        try:
            # Generate 1 year of daily data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Generate mock price data
            np.random.seed(hash(symbol) % 2**32)
            base_price = 100 + hash(symbol) % 900
            
            data = []
            current_price = base_price
            
            for date in dates:
                change = np.random.normal(0, 2)
                current_price = max(1, current_price + change)
                
                data.append({
                    'Date': date,
                    'Open': current_price * (1 + np.random.normal(0, 0.01)),
                    'High': current_price * (1 + abs(np.random.normal(0, 0.02))),
                    'Low': current_price * (1 - abs(np.random.normal(0, 0.02))),
                    'Close': current_price,
                    'Volume': int(np.random.exponential(1000000))
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"❌ Failed to generate sample price data for {symbol}: {e}")
            return pd.DataFrame()
    
    def generate_sample_portfolio_data(self) -> Dict[str, Any]:
        """Generate sample portfolio data"""
        try:
            return {
                'total_value': 100000,
                'cash': 25000,
                'positions': {
                    'AAPL': {'shares': 100, 'avg_price': 150.0, 'current_price': 155.0},
                    'GOOGL': {'shares': 50, 'avg_price': 2800.0, 'current_price': 2850.0},
                    'MSFT': {'shares': 75, 'avg_price': 300.0, 'current_price': 310.0}
                },
                'performance': {
                    'daily_return': 0.02,
                    'weekly_return': 0.08,
                    'monthly_return': 0.15,
                    'yearly_return': 0.25
                }
            }
        except Exception as e:
            logger.error(f"❌ Failed to generate sample portfolio data: {e}")
            return {}
    
    def generate_sample_ml_predictions(self) -> Dict[str, Any]:
        """Generate sample ML predictions"""
        try:
            return {
                'AAPL': {'prediction': 155.0, 'confidence': 0.85},
                'GOOGL': {'prediction': 2850.0, 'confidence': 0.78},
                'MSFT': {'prediction': 310.0, 'confidence': 0.92}
            }
        except Exception as e:
            logger.error(f"❌ Failed to generate sample ML predictions: {e}")
            return {}
    
    def add_uploaded_data(self, key: str, data: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """Add uploaded data to the global store for use by all modules across all instances"""
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
            
            # Add to global store (this will be shared across all DataManager instances)
            success = self.global_store.add_uploaded_data(dataset_id, data, enhanced_metadata)
            
            if success:
                # Add to local dataset registry for this instance
                self.dataset_registry[dataset_id] = {
                    'name': key,
                    'type': 'uploaded',
                    'available': True,
                    'modules': list(self.module_data_access.keys())
                }
                
                logger.info(f"✅ Uploaded data added: {dataset_id} ({data.shape[0]} rows, {data.shape[1]} columns)")
                return dataset_id
            else:
                logger.error(f"❌ Failed to add uploaded data to global store")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to add uploaded data: {e}")
            return None
    
    def get_dataset(self, dataset_id: str) -> pd.DataFrame:
        """Get a specific dataset by ID"""
        try:
            # Get from global store
            data = self.global_store.get_uploaded_data(dataset_id)
            if data is not None:
                # Update access statistics
                self.global_store.update_dataset_access(dataset_id)
                return data
            else:
                logger.warning(f"⚠️ Dataset {dataset_id} not found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Failed to get dataset {dataset_id}: {e}")
            return pd.DataFrame()
    
    def get_available_datasets(self, module: Optional[str] = None) -> List[str]:
        """Get list of available datasets, optionally filtered by module"""
        try:
            available_datasets = self.global_store.get_available_datasets()
            
            if module:
                # Filter by module access
                module_datasets = []
                for dataset_id, metadata in available_datasets.items():
                    if module in metadata.get('modules', []):
                        module_datasets.append(dataset_id)
                return module_datasets
            else:
                return list(available_datasets.keys())
                
        except Exception as e:
            logger.error(f"❌ Failed to get available datasets: {e}")
            return []
    
    def activate_dataset_for_module(self, dataset_id: str, module: str) -> bool:
        """Activate a dataset for a specific module"""
        try:
            if dataset_id not in self.uploaded_datasets:
                logger.warning(f"⚠️ Dataset {dataset_id} not found")
                return False
            
            if module not in self.module_data_access:
                logger.warning(f"⚠️ Module {module} not found")
                return False
            
            if module not in self.active_datasets:
                self.active_datasets[module] = {}
            
            self.active_datasets[module][dataset_id] = {
                'activated_at': datetime.now(),
                'access_count': 0
            }
            
            logger.info(f"✅ Dataset {dataset_id} activated for module {module}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to activate dataset {dataset_id} for module {module}: {e}")
            return False
    
    def deactivate_dataset_for_module(self, dataset_id: str, module: str) -> bool:
        """Deactivate a dataset for a specific module"""
        try:
            if module in self.active_datasets and dataset_id in self.active_datasets[module]:
                del self.active_datasets[module][dataset_id]
                logger.info(f"✅ Dataset {dataset_id} deactivated for module {module}")
                return True
            else:
                logger.warning(f"⚠️ Dataset {dataset_id} not active for module {module}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to deactivate dataset {dataset_id} for module {module}: {e}")
            return False
    
    def get_active_datasets_for_module(self, module: str) -> Dict[str, Any]:
        """Get active datasets for a specific module"""
        return self.active_datasets.get(module, {})
    
    def search_datasets(self, query: str) -> Dict[str, Dict]:
        """Search datasets by name, type, or metadata"""
        try:
            results = {}
            available_datasets = self.global_store.get_available_datasets()
            
            query_lower = query.lower()
            for dataset_id, metadata in available_datasets.items():
                # Search in name, type, and metadata
                if (query_lower in dataset_id.lower() or
                    query_lower in metadata.get('name', '').lower() or
                    query_lower in metadata.get('type', '').lower()):
                    results[dataset_id] = metadata
            
            logger.info(f"🔍 Found {len(results)} datasets matching '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to search datasets: {e}")
            return {}
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        try:
            available_datasets = self.global_store.get_available_datasets()
            
            total_datasets = len(available_datasets)
            total_rows = sum(metadata.get('shape', [0, 0])[0] for metadata in available_datasets.values())
            total_columns = sum(metadata.get('shape', [0, 0])[1] for metadata in available_datasets.values())
            
            # Calculate memory usage
            total_memory = sum(metadata.get('memory_usage', 0) for metadata in available_datasets.values())
            
            # Get most accessed datasets
            access_counts = [(ds_id, metadata.get('access_count', 0)) 
                           for ds_id, metadata in available_datasets.items()]
            access_counts.sort(key=lambda x: x[1], reverse=True)
            
            return {
                'total_datasets': total_datasets,
                'total_rows': total_rows,
                'total_columns': total_columns,
                'total_memory_mb': total_memory / (1024 * 1024),
                'most_accessed': access_counts[:5],
                'active_modules': list(self.active_datasets.keys()),
                'total_active': sum(len(datasets) for datasets in self.active_datasets.values())
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get dataset statistics: {e}")
            return {}

# Global instance
data_manager_core = DataManager()
