#!/usr/bin/env python3
"""
TradePulse Model Callbacks Module
Handles callback methods for the Models Panel
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class ModelCallbacks:
    """Manages callback methods for the Models Panel"""
    
    def __init__(self, performance_tracker, model_trainer, ui_components, components):
        self.performance_tracker = performance_tracker
        self.model_trainer = model_trainer
        self.ui_components = ui_components
        self.components = components
    
    def update_performance_callback(self, model_name: str, metrics: Dict, hyperparameters: Dict):
        """Callback to update model performance"""
        self.performance_tracker.update_model_performance(model_name, metrics, hyperparameters)
        performance_data = self.performance_tracker.create_performance_data()
        self.components['performance_table'].value = performance_data
    
    def update_status_callback(self, model_name: str, metrics: Dict, hyperparameters: Dict, data_info: Dict):
        """Callback to update training status"""
        status_message = self.model_trainer.generate_training_status(
            model_name, metrics, hyperparameters, data_info
        )
        self.components['model_status'].object = status_message
    
    def update_progress_callback(self, progress: int):
        """Callback to update training progress"""
        self.components['training_progress'].value = progress
    
    def on_model_change(self, event):
        """Handle model change"""
        model = event.new
        logger.info(f"🔄 Model changed to {model}")
        # Update performance table for selected model
        performance_data = self.performance_tracker.create_performance_data()
        self.components['performance_table'].value = performance_data
    
    def reset_performance(self, event):
        """Reset all model performance metrics"""
        try:
            self.performance_tracker.reset_model_performance()  # Reset all models
            # Update the performance table
            performance_data = self.performance_tracker.create_performance_data()
            self.components['performance_table'].value = performance_data
            
            # Update model status
            self.components['model_status'].object = self.performance_tracker.get_reset_status_message()
            
            logger.info("🔄 All model performance metrics have been reset")
            
        except Exception as e:
            logger.error(f"❌ Error resetting performance: {e}")
    
    def view_saved_model_data(self, event, model_storage):
        """Display saved model training data"""
        try:
            summary = model_storage.get_model_summary()
            self.components['data_status'].object = summary
            logger.info("📂 Displayed saved model data summary")
            
        except Exception as e:
            logger.error(f"❌ Error viewing saved model data: {e}")
            self.components['data_status'].object = f"""
            ### 📂 Saved Model Data
            ❌ **Error loading data**: {e}
            """
    
    def refresh_data(self, event, data_access, data_manager_helper):
        """Refresh available data for training"""
        try:
            # Get uploaded datasets
            uploaded_data = data_access.get_uploaded_data()
            
            # Update data status display using UI components
            status_message = self.ui_components.create_data_status_message(uploaded_data)
            self.components['data_status'].object = status_message
            
            if uploaded_data:
                logger.info(f"✅ Found {len(uploaded_data)} uploaded datasets")
            else:
                logger.warning("⚠️ No uploaded datasets found")
            
        except Exception as e:
            logger.error(f"❌ Error refreshing data: {e}")
            self.components['data_status'].object = f"""
            ### 📊 Available Data
            ❌ **Error loading data**: {e}
            """
    
    def train_model(self, event):
        """Handle train model button click"""
        try:
            # This method will be overridden by the main panel
            logger.info("🔄 Train model callback triggered")
        except Exception as e:
            logger.error(f"❌ Error in train model callback: {e}")
    
    def make_prediction(self, event):
        """Handle make prediction button click"""
        try:
            # This method will be overridden by the main panel
            logger.info("🔄 Make prediction callback triggered")
        except Exception as e:
            logger.error(f"❌ Error in make prediction callback: {e}")
