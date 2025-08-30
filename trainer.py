#!/usr/bin/env python3
"""
Model Trainer for Models Grid
Consolidates training functionality for all models.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from utils.logger import setup_logger
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader

# Import model implementations
from models_grid.adm import ADMModel
from models_grid.cipo import CIPOModel
from models_grid.bicipo import BICIPOModel

logger = setup_logger(__name__)


class ModelTrainer:
    """Consolidated model trainer for all model types."""
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """Initialize the model trainer."""
        self.config = config
        self.message_bus = message_bus
        self.models = {}
        self.logger = setup_logger(__name__)
        
    def train_model(self, model_type: str, data: pd.DataFrame, 
                   target_column: str, **kwargs) -> Dict[str, Any]:
        """
        Train a specific model type.
        
        Args:
            model_type: Type of model to train ('adm', 'cipo', 'bicipo')
            data: Training data
            target_column: Target variable column name
            **kwargs: Additional training parameters
            
        Returns:
            Training results and model information
        """
        try:
            if model_type == 'adm':
                model = ADMModel()
                results = model.train(data, target_column, **kwargs)
            elif model_type == 'cipo':
                model = CIPOModel()
                results = model.train(data, target_column, **kwargs)
            elif model_type == 'bicipo':
                model = BICIPOModel()
                results = model.train(data, target_column, **kwargs)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            self.models[model_type] = model
            self.logger.info(f"Successfully trained {model_type} model")
            return results
            
        except Exception as e:
            self.logger.error(f"Error training {model_type} model: {e}")
            raise
    
    def train_all_models(self, data: pd.DataFrame, target_column: str, 
                        **kwargs) -> Dict[str, Any]:
        """
        Train all available model types.
        
        Args:
            data: Training data
            target_column: Target variable column name
            **kwargs: Additional training parameters
            
        Returns:
            Results from all trained models
        """
        results = {}
        model_types = ['adm', 'cipo', 'bicipo']
        
        for model_type in model_types:
            try:
                results[model_type] = self.train_model(
                    model_type, data, target_column, **kwargs
                )
            except Exception as e:
                self.logger.error(f"Failed to train {model_type}: {e}")
                results[model_type] = {'error': str(e)}
        
        return results
    
    def get_model(self, model_type: str) -> Optional[Any]:
        """Get a trained model by type."""
        return self.models.get(model_type)
    
    def save_model(self, model_type: str, filepath: str) -> bool:
        """Save a trained model to disk."""
        try:
            model = self.models.get(model_type)
            if model and hasattr(model, 'save'):
                model.save(filepath)
                self.logger.info(f"Saved {model_type} model to {filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error saving {model_type} model: {e}")
            return False
    
    def load_model(self, model_type: str, filepath: str) -> bool:
        """Load a model from disk."""
        try:
            if model_type == 'adm':
                model = ADMModel()
            elif model_type == 'cipo':
                model = CIPOModel()
            elif model_type == 'bicipo':
                model = BICIPOModel()
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            if hasattr(model, 'load'):
                model.load(filepath)
                self.models[model_type] = model
                self.logger.info(f"Loaded {model_type} model from {filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error loading {model_type} model: {e}")
            return False
