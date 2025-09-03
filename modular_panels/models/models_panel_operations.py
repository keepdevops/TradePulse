#!/usr/bin/env python3
"""
TradePulse Models Panel - Operations
Model-related operations for the models panel
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelsPanelOperations:
    """Model-related operations for models panel"""
    
    def train_model(self, components, callbacks, data_access, data_manager_helper, 
                   model_trainer, ui_components):
        """Train the selected model using uploaded data"""
        model = components['model_selector'].value
        hyperparameters = data_manager_helper.prepare_hyperparameters(
            components['epochs'].value,
            components['learning_rate'].value,
            components['batch_size'].value,
            components['hidden_layers'].value
        )
        
        logger.info(f"📈 Training {model} model with hyperparameters: {hyperparameters}")
        
        # Get uploaded datasets for training
        try:
            uploaded_data = data_access.get_uploaded_data()
            api_data = data_access.get_api_data(['AAPL', 'GOOGL'], 'yahoo', '1d')
            
            if not data_manager_helper.validate_training_data(uploaded_data, api_data):
                return
            
            if uploaded_data:
                logger.info(f"📊 Using {len(uploaded_data)} uploaded datasets for training")
                # Update model status to show training with uploaded data
                components['model_status'].object = ui_components.create_training_progress_message(
                    model, uploaded_data, hyperparameters
                )
            else:
                logger.warning("⚠️ No uploaded datasets available for training")
                logger.info(f"📊 Using API data for training: {len(api_data)} symbols")
            
            # Get training data info
            data_info = data_manager_helper.get_training_data_info(uploaded_data)
            
            # Safety check: ensure we have valid callbacks
            callbacks_to_use = callbacks if callbacks is not None else None
            if callbacks_to_use is None:
                logger.error("❌ No callbacks available, cannot start training")
                components['model_status'].object = """
                ### 🤖 Model Status
                ❌ **Training Failed**: Callbacks not available
                """
                return
            
            logger.info(f"✅ Using callbacks: {callbacks_to_use is not None}")
            
            # Start training using the ModelTrainer
            model_trainer.train_model(
                model_name=model,
                hyperparameters=hyperparameters,
                data_info=data_info,
                update_callback=callbacks_to_use.update_performance_callback,
                status_callback=callbacks_to_use.update_status_callback,
                progress_callback=callbacks_to_use.update_progress_callback
            )
            
        except Exception as e:
            logger.error(f"❌ Error during training: {e}")
            components['model_status'].object = f"""
            ### 🤖 Model Status
            ❌ **Training Error**: {str(e)}
            """
            return
    
    def make_prediction(self, components, callbacks, data_access, data_manager_helper, 
                       model_trainer, ui_components):
        """Make prediction with selected model using uploaded data"""
        model = components['model_selector'].value
        
        logger.info(f"🔮 Making prediction with {model} model")
        
        # Get data for prediction
        try:
            uploaded_data = data_access.get_uploaded_data()
            data_info = data_manager_helper.get_prediction_data_info(uploaded_data)
            
            # Safety check: ensure we have valid callbacks
            callbacks_to_use = callbacks if callbacks is not None else None
            if callbacks_to_use is None:
                logger.error("❌ No callbacks available, cannot make prediction")
                components['model_status'].object = """
                ### 🤖 Model Status
                ❌ **Prediction Failed**: Callbacks not available
                """
                return
            
            logger.info(f"✅ Using callbacks for prediction: {callbacks_to_use is not None}")
            
            # Make prediction using the ModelTrainer
            result = model_trainer.make_prediction(model, data_info)
            
            if result.get('error'):
                components['model_status'].object = f"""
                ### 🤖 Model Status
                ❌ **Error making prediction**: {result['error']}
                """
            else:
                # Update status with prediction result using UI components
                components['model_status'].object = ui_components.create_prediction_status_message(
                    model, result, data_info
                )
                
        except Exception as e:
            logger.error(f"❌ Error making prediction: {e}")
            components['model_status'].object = f"""
            ### 🤖 Model Status
            ❌ **Error making prediction**: {e}
            """
    
    def validate_model_config(self, config: Dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate model configuration"""
        errors = []
        
        # Check required fields
        required_fields = ['model_type', 'hyperparameters']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate model type
        if 'model_type' in config:
            model_type = config['model_type']
            valid_types = ['LSTM', 'GRU', 'Transformer', 'CNN', 'RNN']
            if model_type not in valid_types:
                errors.append(f"Invalid model type: {model_type}. Must be one of {valid_types}")
        
        # Validate hyperparameters
        if 'hyperparameters' in config:
            hyperparams = config['hyperparameters']
            if not isinstance(hyperparams, dict):
                errors.append("Hyperparameters must be a dictionary")
            else:
                # Check for required hyperparameters
                required_params = ['epochs', 'learning_rate', 'batch_size']
                for param in required_params:
                    if param not in hyperparams:
                        errors.append(f"Missing required hyperparameter: {param}")
        
        return len(errors) == 0, errors
    
    def create_model_id(self) -> str:
        """Create unique model ID"""
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"model_{timestamp}_{unique_id}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models"""
        return {
            'supported_models': [
                'LSTM', 'GRU', 'Transformer', 'CNN', 'RNN'
            ],
            'model_types': [
                'Time Series', 'Classification', 'Regression', 'Sequence'
            ],
            'hyperparameters': [
                'epochs', 'learning_rate', 'batch_size', 'hidden_layers'
            ],
            'data_requirements': [
                'Time series data', 'Numerical features', 'Target variable'
            ]
        }
    
    def get_model_statistics(self, model_data: list) -> Dict[str, Any]:
        """Get statistics about model data"""
        if not model_data:
            return {
                'total_models': 0,
                'trained_models': 0,
                'active_models': 0,
                'average_accuracy': 0.0
            }
        
        stats = {
            'total_models': len(model_data),
            'trained_models': len([m for m in model_data if m.get('status') == 'trained']),
            'active_models': len([m for m in model_data if m.get('active', False)]),
            'average_accuracy': sum(m.get('accuracy', 0) for m in model_data) / len(model_data) if model_data else 0.0
        }
        
        return stats



