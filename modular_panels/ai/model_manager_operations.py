#!/usr/bin/env python3
"""
TradePulse AI Model Manager - Operations
Model-related operations for the model manager
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class ModelManagerOperations:
    """Model-related operations for model manager"""
    
    def update_model(self, models: Dict, model_id: str, updates: Dict) -> bool:
        """Update an existing model"""
        try:
            model = models.get(model_id)
            if model:
                model.update(updates)
                logger.info(f"✅ Model {model_id} updated successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to update model {model_id}: {e}")
            return False
    
    def delete_model(self, models: Dict, model_id: str) -> bool:
        """Delete a model"""
        try:
            if model_id in models:
                del models[model_id]
                logger.info(f"✅ Model {model_id} deleted successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to delete model {model_id}: {e}")
            return False
    
    def get_model_performance(self, models: Dict, model_id: str) -> Dict:
        """Get performance metrics for a specific model"""
        try:
            model = models.get(model_id)
            if not model:
                return {}
            
            return model.get('performance_metrics', {})
            
        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            return {}
    
    def get_models_by_type(self, models: Dict, model_type: str) -> List[Dict]:
        """Get all models of a specific type"""
        return [model for model in models.values() if model['type'] == model_type]
    
    def get_trained_models(self, models: Dict) -> List[Dict]:
        """Get all trained models"""
        return [model for model in models.values() if model['status'] == 'trained']
    
    def get_model_statistics(self, models: Dict) -> Dict:
        """Get comprehensive model statistics"""
        try:
            total_models = len(models)
            status_counts = {}
            type_counts = {}
            
            for model in models.values():
                status = model['status']
                model_type = model['type']
                
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[model_type] = type_counts.get(model_type, 0) + 1
            
            return {
                'total_models': total_models,
                'status_distribution': status_counts,
                'type_distribution': type_counts,
                'trained_models': len(self.get_trained_models(models))
            }
            
        except Exception as e:
            logger.error(f"Failed to get model statistics: {e}")
            return {}
    
    def validate_model_config(self, model_config: Dict, supported_models: List[str]) -> Tuple[bool, List[str]]:
        """Validate model configuration and return errors if any"""
        errors = []
        
        # Check required fields
        if 'type' not in model_config:
            errors.append("Missing required field: type")
        elif model_config['type'] not in supported_models:
            errors.append(f"Unsupported model type: {model_config['type']}")
        
        # Check hyperparameters
        if 'hyperparameters' in model_config:
            hyperparams = model_config['hyperparameters']
            if 'epochs' in hyperparams and not isinstance(hyperparams['epochs'], int):
                errors.append("Epochs must be an integer")
            if 'learning_rate' in hyperparams and not isinstance(hyperparams['learning_rate'], (int, float)):
                errors.append("Learning rate must be a number")
        
        return len(errors) == 0, errors
    
    def export_models_to_json(self, models: Dict, filename: str = None) -> str:
        """Export models to JSON file"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"models_export_{timestamp}.json"
            
            # Convert models to serializable format
            export_data = {}
            for model_id, model in models.items():
                export_data[model_id] = {
                    'id': model['id'],
                    'name': model['name'],
                    'type': model['type'],
                    'status': model['status'],
                    'created': str(model['created']),
                    'last_trained': str(model['last_trained']) if model['last_trained'] else None,
                    'hyperparameters': model['hyperparameters'],
                    'performance_metrics': model['performance_metrics'],
                    'datasets': model['datasets']
                }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"📤 Models exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export models to JSON: {e}")
            return None
    
    def import_models_from_json(self, models: Dict, filename: str) -> int:
        """Import models from JSON file"""
        try:
            import json
            
            with open(filename, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for model_id, model_data in import_data.items():
                # Convert string timestamps back to pandas timestamps
                if model_data.get('created'):
                    model_data['created'] = pd.Timestamp(model_data['created'])
                if model_data.get('last_trained'):
                    model_data['last_trained'] = pd.Timestamp(model_data['last_trained'])
                
                models[model_id] = model_data
                imported_count += 1
            
            logger.info(f"📥 Imported {imported_count} models from {filename}")
            return imported_count
            
        except Exception as e:
            logger.error(f"Failed to import models from JSON: {e}")
            return 0
    
    def get_model_summary(self, model: Dict) -> str:
        """Get text summary of model"""
        try:
            if not model:
                return "No model data available"
            
            summary_lines = [
                f"**Model ID**: {model.get('id', 'Unknown')}",
                f"**Name**: {model.get('name', 'Unknown')}",
                f"**Type**: {model.get('type', 'Unknown')}",
                f"**Status**: {model.get('status', 'Unknown')}",
                f"**Created**: {model.get('created', 'Unknown')}",
                f"**Last Trained**: {model.get('last_trained', 'Never')}",
                f"**Datasets**: {len(model.get('datasets', []))}"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create model summary: {e}")
            return "Error creating summary"



