#!/usr/bin/env python3
"""
TradePulse AI - Callbacks
Handles AI panel callback operations and event handling
"""

import logging
from typing import Dict
import pandas as pd

logger = logging.getLogger(__name__)

class AICallbacks:
    """Handles AI panel callback operations and event handling"""
    
    def __init__(self, ai_operations, ui_components):
        self.ai_operations = ai_operations
        self.ui_components = ui_components
    
    def setup_callbacks(self, components: Dict, dataset_selector):
        """Setup component callbacks"""
        components['train_button'].on_click(self.train_model)
        components['predict_button'].on_click(self.make_prediction)
        components['evaluate_button'].on_click(self.evaluate_model)
        
        # Dataset selector callback
        dataset_selector.add_dataset_change_callback(self.on_dataset_change)
    
    def train_model(self, event):
        """Train the selected ML model using the model manager"""
        try:
            model_name = event.obj.owner.components['model_selector'].value
            epochs = event.obj.owner.components['epochs_input'].value
            learning_rate = event.obj.owner.components['learning_rate'].value
            
            # Get active datasets for training
            active_datasets = event.obj.owner.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"🚀 Training {model_name} model with {len(active_datasets)} active datasets")
                
                # Create model configuration
                model_config = {
                    'name': f"{model_name} Model",
                    'type': model_name,
                    'hyperparameters': {
                        'epochs': epochs,
                        'learning_rate': learning_rate
                    },
                    'datasets': list(active_datasets.keys())
                }
                
                # Validate model configuration
                is_valid, errors = self.ai_operations.model_manager.validate_model_config(model_config)
                if not is_valid:
                    logger.error(f"❌ Invalid model configuration: {errors}")
                    return
                
                # Create model
                model_id = self.ai_operations.model_manager.create_model(model_config)
                
                # Train model
                training_success = self.ai_operations.model_manager.train_model(
                    model_id, active_datasets, model_config['hyperparameters']
                )
                
                if training_success:
                    # Update performance display
                    self.ai_operations.update_performance_display(model_name, active_datasets, event.obj.owner.components)
                    
                    # Update training progress
                    event.obj.owner.components['training_progress'].value = 100
                    
                    logger.info(f"✅ {model_name} model training completed")
                else:
                    logger.error(f"❌ {model_name} model training failed")
            else:
                logger.info("⚠️ No active datasets - using default training data")
                
        except Exception as e:
            logger.error(f"❌ Model training failed: {e}")
    
    def make_prediction(self, event):
        """Make predictions using the trained model"""
        try:
            model_name = event.obj.owner.components['model_selector'].value
            
            # Get active datasets for prediction
            active_datasets = event.obj.owner.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"🔮 Making predictions with {model_name} using {len(active_datasets)} active datasets")
                
                # Find a trained model of the selected type
                trained_models = self.ai_operations.model_manager.get_models_by_type(model_name)
                trained_models = [m for m in trained_models if m['status'] == 'trained']
                
                if trained_models:
                    # Use the most recently trained model
                    model = trained_models[-1]
                    
                    # Generate predictions for each dataset
                    predictions_data = []
                    for dataset_id, data in active_datasets.items():
                        logger.info(f"📊 Using dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                        
                        try:
                            # Make predictions using the model manager
                            prediction_result = self.ai_operations.model_manager.make_prediction(model['id'], data)
                            
                            # Create prediction records
                            for i, pred in enumerate(prediction_result['predictions']):
                                predictions_data.append({
                                    'Dataset': dataset_id,
                                    'Row': i + 1,
                                    'Prediction': pred,
                                    'Confidence': prediction_result['confidence_scores'][i],
                                    'Model': model_name
                                })
                                
                        except Exception as e:
                            logger.warning(f"Failed to make predictions on dataset {dataset_id}: {e}")
                    
                    # Update predictions table
                    if predictions_data:
                        predictions_df = pd.DataFrame(predictions_data)
                        event.obj.owner.components['predictions_table'].value = predictions_df
                        logger.info(f"✅ Predictions generated using {model_name}")
                    else:
                        logger.warning("No predictions were generated")
                else:
                    logger.warning(f"No trained {model_name} models found")
            else:
                logger.info("⚠️ No active datasets - using default prediction data")
                
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
    
    def evaluate_model(self, event):
        """Evaluate the trained model performance"""
        try:
            model_name = event.obj.owner.components['model_selector'].value
            
            # Get active datasets for evaluation
            active_datasets = event.obj.owner.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"📊 Evaluating {model_name} model with {len(active_datasets)} active datasets")
                
                # Find trained models of the selected type
                trained_models = self.ai_operations.model_manager.get_models_by_type(model_name)
                trained_models = [m for m in trained_models if m['status'] == 'trained']
                
                if trained_models:
                    # Evaluate the most recently trained model
                    model = trained_models[-1]
                    
                    # Use uploaded data for evaluation
                    for dataset_id, data in active_datasets.items():
                        logger.info(f"📊 Evaluating on dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                    
                    # Evaluate model using the model manager
                    evaluation_results = self.ai_operations.model_manager.evaluate_model(model['id'], active_datasets)
                    
                    # Update performance display
                    self.ai_operations.update_performance_display(model_name, active_datasets, event.obj.owner.components)
                    
                    logger.info(f"✅ {model_name} model evaluation completed")
                else:
                    logger.warning(f"No trained {model_name} models found")
            else:
                logger.info("⚠️ No active datasets - using default evaluation data")
                
        except Exception as e:
            logger.error(f"❌ Model evaluation failed: {e}")
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for AI/ML operations"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for AI module")
        
        if change_type == 'activated':
            # Dataset is now available for ML training
            logger.info(f"✅ Dataset {dataset_id} activated for AI/ML operations")
            
        elif change_type == 'deactivated':
            # Dataset is no longer available
            logger.info(f"❌ Dataset {dataset_id} deactivated for AI/ML operations")
