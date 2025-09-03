#!/usr/bin/env python3
"""
TradePulse Model Storage Module
Handles persistent storage of model training data
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ModelStorage:
    """Handles persistent storage of model training data"""
    
    def __init__(self, storage_dir: str = "model_training_data"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        logger.info(f"📁 Model storage initialized at: {self.storage_dir}")
    
    def save_model_data(self, model_name: str, hyperparameters: Dict, metrics: Dict, dataset_info: Dict = None) -> Optional[str]:
        """Save model training data to persistent storage"""
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{model_name}_{timestamp}.json"
            filepath = os.path.join(self.storage_dir, filename)
            
            # Prepare data record
            training_record = {
                "model_name": model_name,
                "timestamp": timestamp,
                "hyperparameters": hyperparameters,
                "performance_metrics": metrics,
                "dataset_info": dataset_info,
                "training_status": "completed"
            }
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(training_record, f, indent=2)
            
            logger.info(f"💾 Model training data saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Failed to save model data: {e}")
            return None
    
    def load_saved_model_data(self) -> Dict:
        """Load all saved model training data from storage"""
        try:
            saved_models = {}
            if os.path.exists(self.storage_dir):
                for filename in os.listdir(self.storage_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.storage_dir, filename)
                        with open(filepath, 'r') as f:
                            model_data = json.load(f)
                            model_name = model_data['model_name']
                            if model_name not in saved_models:
                                saved_models[model_name] = []
                            saved_models[model_name].append(model_data)
            
            logger.info(f"📂 Loaded {sum(len(models) for models in saved_models.values())} saved model records")
            return saved_models
            
        except Exception as e:
            logger.error(f"❌ Failed to load saved model data: {e}")
            return {}
    
    def get_model_summary(self) -> str:
        """Get a formatted summary of saved model data"""
        try:
            saved_models = self.load_saved_model_data()
            
            if not saved_models:
                return "⚠️ **No saved model data found**\n\n**Train models to save data automatically.**"
            
            # Create summary
            summary = ["### 📂 Saved Model Data"]
            summary.append(f"**Total Models**: {len(saved_models)}")
            summary.append("")
            
            for model_name, training_records in saved_models.items():
                summary.append(f"**🤖 {model_name}**")
                summary.append(f"- Training Runs: {len(training_records)}")
                
                # Show latest training info
                latest = training_records[-1]
                summary.append(f"- Latest: {latest['timestamp']}")
                if 'performance_metrics' in latest:
                    metrics = latest['performance_metrics']
                    summary.append(f"- Best Accuracy: {metrics.get('accuracy', 'N/A')}%")
                
                summary.append("")
            
            return "\n".join(summary)
            
        except Exception as e:
            logger.error(f"❌ Error generating model summary: {e}")
            return f"❌ **Error loading data**: {e}"
    
    def clear_old_records(self, days_to_keep: int = 30) -> int:
        """Clear old training records older than specified days"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            removed_count = 0
            
            if os.path.exists(self.storage_dir):
                for filename in os.listdir(self.storage_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.storage_dir, filename)
                        file_time = os.path.getmtime(filepath)
                        
                        if file_time < cutoff_date:
                            os.remove(filepath)
                            removed_count += 1
                            logger.info(f"🗑️ Removed old record: {filename}")
            
            if removed_count > 0:
                logger.info(f"🧹 Cleaned up {removed_count} old training records")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"❌ Error clearing old records: {e}")
            return 0
