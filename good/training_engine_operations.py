#!/usr/bin/env python3
"""
TradePulse AI Training Engine - Operations
Training-related operations for the training engine
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class TrainingEngineOperations:
    """Training-related operations for training engine"""
    
    def get_jobs_by_status(self, training_jobs: Dict, status: str) -> List[Dict]:
        """Get training jobs by status"""
        return [job for job in training_jobs.values() if job['status'] == status]
    
    def cancel_training_job(self, training_jobs: Dict, job_id: str) -> bool:
        """Cancel a running training job"""
        try:
            job = training_jobs.get(job_id)
            if job and job['status'] == 'running':
                job['status'] = 'cancelled'
                job['cancelled_at'] = pd.Timestamp.now()
                logger.info(f"✅ Training job {job_id} cancelled")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to cancel training job {job_id}: {e}")
            return False
    
    def get_training_statistics(self, training_jobs: Dict) -> Dict:
        """Get comprehensive training statistics"""
        try:
            total_jobs = len(training_jobs)
            status_counts = {}
            model_type_counts = {}
            
            for job in training_jobs.values():
                status = job['status']
                model_type = job['model_config']['type']
                
                status_counts[status] = status_counts.get(status, 0) + 1
                model_type_counts[model_type] = model_type_counts.get(model_type, 0) + 1
            
            return {
                'total_jobs': total_jobs,
                'status_distribution': status_counts,
                'model_type_distribution': model_type_counts,
                'running_jobs': len(self.get_jobs_by_status(training_jobs, 'running')),
                'completed_jobs': len(self.get_jobs_by_status(training_jobs, 'completed'))
            }
            
        except Exception as e:
            logger.error(f"Failed to get training statistics: {e}")
            return {}
    
    def validate_training_config(self, model_config: Dict, training_data: Dict, 
                               hyperparameters: Dict) -> Tuple[bool, List[str]]:
        """Validate training configuration"""
        errors = []
        
        # Check model config
        if 'type' not in model_config:
            errors.append("Missing model type in configuration")
        
        # Check training data
        if not training_data:
            errors.append("Training data is required")
        
        # Check hyperparameters
        if 'epochs' in hyperparameters and not isinstance(hyperparameters['epochs'], int):
            errors.append("Epochs must be an integer")
        
        if 'learning_rate' in hyperparameters and not isinstance(hyperparameters['learning_rate'], (int, float)):
            errors.append("Learning rate must be a number")
        
        if 'batch_size' in hyperparameters and not isinstance(hyperparameters['batch_size'], int):
            errors.append("Batch size must be an integer")
        
        return len(errors) == 0, errors
    
    def export_training_jobs_to_json(self, training_jobs: Dict, filename: str = None) -> str:
        """Export training jobs to JSON file"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"training_jobs_export_{timestamp}.json"
            
            # Convert jobs to serializable format
            export_data = {}
            for job_id, job in training_jobs.items():
                export_data[job_id] = {
                    'id': job['id'],
                    'model_config': job['model_config'],
                    'hyperparameters': job['hyperparameters'],
                    'status': job['status'],
                    'started_at': str(job['started_at']),
                    'progress': job['progress'],
                    'current_epoch': job['current_epoch'],
                    'total_epochs': job['total_epochs'],
                    'metrics': job['metrics']
                }
                
                if 'completed_at' in job:
                    export_data[job_id]['completed_at'] = str(job['completed_at'])
                if 'failed_at' in job:
                    export_data[job_id]['failed_at'] = str(job['failed_at'])
                if 'cancelled_at' in job:
                    export_data[job_id]['cancelled_at'] = str(job['cancelled_at'])
                if 'error' in job:
                    export_data[job_id]['error'] = job['error']
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"📤 Training jobs exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export training jobs to JSON: {e}")
            return None
    
    def import_training_jobs_from_json(self, training_jobs: Dict, filename: str) -> int:
        """Import training jobs from JSON file"""
        try:
            import json
            
            with open(filename, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for job_id, job_data in import_data.items():
                # Convert string timestamps back to pandas timestamps
                if job_data.get('started_at'):
                    job_data['started_at'] = pd.Timestamp(job_data['started_at'])
                if job_data.get('completed_at'):
                    job_data['completed_at'] = pd.Timestamp(job_data['completed_at'])
                if job_data.get('failed_at'):
                    job_data['failed_at'] = pd.Timestamp(job_data['failed_at'])
                if job_data.get('cancelled_at'):
                    job_data['cancelled_at'] = pd.Timestamp(job_data['cancelled_at'])
                
                training_jobs[job_id] = job_data
                imported_count += 1
            
            logger.info(f"📥 Imported {imported_count} training jobs from {filename}")
            return imported_count
            
        except Exception as e:
            logger.error(f"Failed to import training jobs from JSON: {e}")
            return 0
    
    def get_job_summary(self, job: Dict) -> str:
        """Get text summary of training job"""
        try:
            if not job:
                return "No job data available"
            
            summary_lines = [
                f"**Job ID**: {job.get('id', 'Unknown')}",
                f"**Model Type**: {job.get('model_config', {}).get('type', 'Unknown')}",
                f"**Status**: {job.get('status', 'Unknown')}",
                f"**Progress**: {job.get('progress', 0):.1f}%",
                f"**Current Epoch**: {job.get('current_epoch', 0)} / {job.get('total_epochs', 0)}",
                f"**Started**: {job.get('started_at', 'Unknown')}"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create job summary: {e}")
            return "Error creating summary"

