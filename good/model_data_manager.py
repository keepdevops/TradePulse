#!/usr/bin/env python3
"""
TradePulse Model Data Manager Module
Handles data management and prediction functionality for the Models Panel
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelDataManager:
    """Manages data operations for the Models Panel"""
    
    def __init__(self, data_access, data_manager):
        self.data_access = data_access
        self.data_manager = data_manager
    
    def get_training_data_info(self, uploaded_data):
        """Get training data information for uploaded datasets"""
        try:
            if uploaded_data:
                dataset_names = list(uploaded_data.keys())
                total_rows = sum(data.shape[0] for data in uploaded_data.values())
                
                return {
                    'datasets_used': len(uploaded_data),
                    'total_records': total_rows,
                    'dataset_names': dataset_names,
                    'data_shapes': {name: data.shape for name, data in uploaded_data.items()}
                }
            else:
                return {
                    'data_source': 'API',
                    'symbols': ['AAPL', 'GOOGL'],
                    'data_type': 'market_data'
                }
        except Exception as e:
            logger.error(f"❌ Error getting training data info: {e}")
            return {}
    
    def get_prediction_data_info(self, uploaded_data):
        """Get prediction data information"""
        try:
            if uploaded_data:
                # Use uploaded data for prediction
                dataset_id = list(uploaded_data.keys())[0]  # Use first dataset
                data = uploaded_data[dataset_id]
                logger.info(f"📊 Making prediction using dataset {dataset_id}: {data.shape}")
                
                return {
                    'dataset_id': dataset_id,
                    'data_shape': data.shape,
                    'data_source': 'uploaded'
                }
            else:
                # Fallback to API data
                symbol = self.data_manager.symbols[0] if self.data_manager.symbols else 'AAPL'
                logger.info(f"📊 Making prediction using API data for {symbol}")
                
                return {
                    'symbol': symbol,
                    'data_source': 'API'
                }
        except Exception as e:
            logger.error(f"❌ Error getting prediction data info: {e}")
            return {}
    
    def prepare_hyperparameters(self, epochs, learning_rate, batch_size, hidden_layers):
        """Prepare hyperparameters dictionary"""
        return {
            'epochs': epochs,
            'learning_rate': learning_rate,
            'batch_size': batch_size,
            'hidden_layers': hidden_layers
        }
    
    def validate_training_data(self, uploaded_data, api_data):
        """Validate that training data is available"""
        if not uploaded_data and not api_data:
            logger.error("❌ No data available for training")
            return False
        return True
