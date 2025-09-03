#!/usr/bin/env python3
"""
TradePulse AI Training Engine - Core Functionality
Core training engine class with basic functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .training_engine_components import TrainingEngineComponents
from .training_engine_operations import TrainingEngineOperations
from .training_engine_management import TrainingEngineManagement
from .training_engine_algorithms import TrainingEngineAlgorithms

logger = logging.getLogger(__name__)

class TrainingEngineCore:
    """Core training engine functionality"""
    
    def __init__(self):
        self.training_jobs = {}
        self.job_counter = 0
        
        # Initialize components
        self.components = TrainingEngineComponents()
        self.operations = TrainingEngineOperations()
        self.management = TrainingEngineManagement()
        self.algorithms = TrainingEngineAlgorithms()
    
    def start_training(self, model_config: Dict, training_data: Dict, 
                      hyperparameters: Dict) -> str:
        """Start a training job"""
        try:
            self.job_counter += 1
            job_id = f"training_job_{self.job_counter}"
            
            # Create training job
            training_job = {
                'id': job_id,
                'model_config': model_config,
                'training_data': training_data,
                'hyperparameters': hyperparameters,
                'status': 'running',
                'started_at': pd.Timestamp.now(),
                'progress': 0.0,
                'current_epoch': 0,
                'total_epochs': hyperparameters.get('epochs', 100),
                'metrics': {}
            }
            
            self.training_jobs[job_id] = training_job
            
            # Start training in background (simulated)
            self._run_training_job(job_id)
            
            logger.info(f"🚀 Training job {job_id} started for {model_config['type']} model")
            return job_id
            
        except Exception as e:
            logger.error(f"❌ Failed to start training job: {e}")
            raise
    
    def _run_training_job(self, job_id: str):
        """Run the training job (simulated)"""
        try:
            job = self.training_jobs[job_id]
            model_type = job['model_config']['type']
            
            # Run the appropriate training algorithm
            success = self.algorithms.train_model_by_type(job, model_type)
            
            if success:
                job['status'] = 'completed'
                job['progress'] = 100.0
                job['completed_at'] = pd.Timestamp.now()
                logger.info(f"✅ Training job {job_id} completed successfully")
            else:
                job['status'] = 'failed'
                job['failed_at'] = pd.Timestamp.now()
                logger.error(f"❌ Training job {job_id} failed")
                
        except Exception as e:
            logger.error(f"Training job {job_id} failed: {e}")
            job = self.training_jobs.get(job_id)
            if job:
                job['status'] = 'failed'
                job['error'] = str(e)
    
    def get_training_job(self, job_id: str) -> Optional[Dict]:
        """Get training job by ID"""
        return self.training_jobs.get(job_id)
    
    def get_all_training_jobs(self) -> List[Dict]:
        """Get all training jobs"""
        return list(self.training_jobs.values())
    
    def get_jobs_by_status(self, status: str) -> List[Dict]:
        """Get training jobs by status"""
        return self.operations.get_jobs_by_status(self.training_jobs, status)
    
    def cancel_training_job(self, job_id: str) -> bool:
        """Cancel a running training job"""
        return self.operations.cancel_training_job(self.training_jobs, job_id)
    
    def get_training_statistics(self) -> Dict:
        """Get comprehensive training statistics"""
        return self.operations.get_training_statistics(self.training_jobs)
    
    def validate_training_config(self, model_config: Dict, training_data: Dict, 
                               hyperparameters: Dict) -> Tuple[bool, List[str]]:
        """Validate training configuration"""
        return self.operations.validate_training_config(model_config, training_data, hyperparameters)



