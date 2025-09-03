#!/usr/bin/env python3
"""
TradePulse AI - Training Engine
Handles AI/ML model training operations
REFACTORED: Now uses modular components to stay under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from .training_engine_refactored import TrainingEngine as RefactoredTrainingEngine

logger = logging.getLogger(__name__)

class TrainingEngine:
    """Handles AI/ML model training operations"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_engine = RefactoredTrainingEngine()
    
    def start_training(self, model_config: Dict, training_data: Dict, 
                      hyperparameters: Dict) -> str:
        """Start a training job"""
        # Delegate to refactored implementation
        return self._refactored_engine.start_training(model_config, training_data, hyperparameters)
    
    def get_training_job(self, job_id: str) -> Optional[Dict]:
        """Get training job by ID"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_training_job(job_id)
    
    def get_all_training_jobs(self) -> List[Dict]:
        """Get all training jobs"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_all_training_jobs()
    
    def get_jobs_by_status(self, status: str) -> List[Dict]:
        """Get training jobs by status"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_jobs_by_status(status)
    
    def cancel_training_job(self, job_id: str) -> bool:
        """Cancel a running training job"""
        # Delegate to refactored implementation
        return self._refactored_engine.cancel_training_job(job_id)
    
    def get_training_statistics(self) -> Dict:
        """Get comprehensive training statistics"""
        # Delegate to refactored implementation
        return self._refactored_engine.get_training_statistics()
