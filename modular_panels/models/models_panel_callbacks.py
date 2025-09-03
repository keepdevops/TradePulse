#!/usr/bin/env python3
"""
TradePulse Models Panel - Callbacks Manager
Callback management for the models panel
"""

import logging

logger = logging.getLogger(__name__)

class ModelsPanelCallbacks:
    """Callback management for models panel"""
    
    def __init__(self, performance_tracker, model_trainer, ui_components, components):
        self.performance_tracker = performance_tracker
        self.model_trainer = model_trainer
        self.ui_components = ui_components
        self.components = components
    
    def update_performance_callback(self, model_name: str, metrics: dict):
        """Update performance metrics display"""
        try:
            # Update performance tracker
            self.performance_tracker.update_performance(model_name, metrics)
            
            # Update UI display
            performance_data = self.performance_tracker.get_performance_data()
            self.components['performance_table'].value = performance_data
            
            logger.info(f"✅ Performance updated for {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update performance: {e}")
    
    def update_status_callback(self, model_name: str, status: str, message: str = ""):
        """Update model status display"""
        try:
            status_message = f"""
            ### 🤖 Model Status
            **Model**: {model_name}
            **Status**: {status}
            """
            
            if message:
                status_message += f"\n**Message**: {message}"
            
            self.components['model_status'].object = status_message
            logger.info(f"✅ Status updated for {model_name}: {status}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update status: {e}")
    
    def update_progress_callback(self, model_name: str, progress: int, current_epoch: int = None, total_epochs: int = None):
        """Update training progress display"""
        try:
            # Update progress bar
            self.components['training_progress'].value = progress
            
            # Update status with progress info
            progress_message = f"""
            ### 🤖 Model Status
            **Model**: {model_name}
            **Status**: Training in Progress
            **Progress**: {progress}%
            """
            
            if current_epoch is not None and total_epochs is not None:
                progress_message += f"\n**Epoch**: {current_epoch}/{total_epochs}"
            
            self.components['model_status'].object = progress_message
            
            logger.info(f"✅ Progress updated for {model_name}: {progress}%")
            
        except Exception as e:
            logger.error(f"❌ Failed to update progress: {e}")
    
    def refresh_data(self, event, data_access, data_manager_helper):
        """Refresh data display"""
        try:
            # Get current data
            uploaded_data = data_access.get_uploaded_data()
            api_data = data_access.get_api_data(['AAPL', 'GOOGL'], 'yahoo', '1d')
            
            # Update data status
            data_info = data_manager_helper.get_training_data_info(uploaded_data)
            self.components['data_status'].object = self.ui_components.create_data_status_message(data_info)
            
            logger.info("✅ Data refreshed successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to refresh data: {e}")
    
    def reset_performance(self, event):
        """Reset performance metrics"""
        try:
            self.performance_tracker.reset_performance()
            self.components['performance_table'].value = self.performance_tracker.get_performance_data()
            
            logger.info("✅ Performance metrics reset")
            
        except Exception as e:
            logger.error(f"❌ Failed to reset performance: {e}")
    
    def view_saved_models(self, event):
        """View saved models"""
        try:
            saved_models = self.model_trainer.get_saved_models()
            
            if saved_models:
                models_info = "### 📁 Saved Models\n"
                for model in saved_models:
                    models_info += f"- **{model['name']}**: {model['type']} (Accuracy: {model.get('accuracy', 'N/A')})\n"
            else:
                models_info = "### 📁 Saved Models\nNo saved models found."
            
            self.components['model_status'].object = models_info
            logger.info("✅ Saved models displayed")
            
        except Exception as e:
            logger.error(f"❌ Failed to view saved models: {e}")
    
    def train_model(self, event):
        """Train model callback"""
        try:
            # This will be overridden by the panel's train_model method
            logger.info("🔄 Train model callback triggered")
            
        except Exception as e:
            logger.error(f"❌ Train model callback failed: {e}")
    
    def make_prediction(self, event):
        """Make prediction callback"""
        try:
            # This will be overridden by the panel's make_prediction method
            logger.info("🔮 Make prediction callback triggered")
            
        except Exception as e:
            logger.error(f"❌ Make prediction callback failed: {e}")
    
    def on_model_change(self, event):
        """Handle model selection change"""
        try:
            model_name = event.new
            logger.info(f"🔄 Model changed to: {model_name}")
            
            # Update model status
            status_message = f"""
            ### 🤖 Model Status
            **Selected Model**: {model_name}
            **Status**: Ready
            """
            self.components['model_status'].object = status_message
            
            # Update performance data for selected model
            performance_data = self.performance_tracker.get_performance_data()
            if model_name in performance_data:
                self.components['performance_table'].value = performance_data[performance_data['Model'] == model_name]
            else:
                # Show empty performance for new model
                empty_data = performance_data[performance_data['Model'] == 'No Data']
                self.components['performance_table'].value = empty_data
            
            logger.info(f"✅ Model change handled for {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to handle model change: {e}")
    
    def view_saved_model_data(self, event, model_storage):
        """View saved model data"""
        try:
            saved_models = model_storage.get_saved_models()
            
            if saved_models:
                models_info = "### 📁 Saved Models\n"
                for model in saved_models:
                    models_info += f"- **{model['name']}**: {model['type']} (Accuracy: {model.get('accuracy', 'N/A')})\n"
            else:
                models_info = "### 📁 Saved Models\nNo saved models found."
            
            self.components['model_status'].object = models_info
            logger.info("✅ Saved model data displayed")
            
        except Exception as e:
            logger.error(f"❌ Failed to view saved model data: {e}")



