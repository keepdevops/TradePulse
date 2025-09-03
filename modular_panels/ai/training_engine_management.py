#!/usr/bin/env python3
"""
TradePulse AI Training Engine - Management
UI management for the training engine
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class TrainingEngineManagement:
    """UI management for training engine"""
    
    @staticmethod
    def create_job_display(job: Dict):
        """Create job display"""
        try:
            if not job:
                return pn.pane.Markdown("""
                ### 📋 Training Job
                No job selected
                """)
            
            display_text = f"""
            ### 📋 Training Job
            
            **Job ID**: {job.get('id', 'Unknown')}  
            **Model Type**: {job.get('model_config', {}).get('type', 'Unknown')}  
            **Status**: {job.get('status', 'Unknown')}  
            **Progress**: {job.get('progress', 0):.1f}%  
            **Current Epoch**: {job.get('current_epoch', 0)} / {job.get('total_epochs', 0)}  
            **Started**: {job.get('started_at', 'Unknown')}
            """
            
            return pn.pane.Markdown(display_text)
            
        except Exception as e:
            logger.error(f"Failed to create job display: {e}")
            return pn.pane.Markdown("Error: Failed to create job display")
    
    @staticmethod
    def create_metrics_display(metrics: Dict):
        """Create metrics display"""
        try:
            if not metrics:
                return pn.pane.Markdown("""
                ### 📈 Training Metrics
                No metrics available
                """)
            
            final_metrics = metrics.get('final', {})
            metrics_text = f"""
            ### 📈 Training Metrics
            
            **Final Loss**: {final_metrics.get('loss', 'N/A'):.4f}  
            **Final Accuracy**: {final_metrics.get('accuracy', 'N/A'):.3f}  
            **Training Time**: {final_metrics.get('training_time', 'N/A'):.1f}s
            """
            
            return pn.pane.Markdown(metrics_text)
            
        except Exception as e:
            logger.error(f"Failed to create metrics display: {e}")
            return pn.pane.Markdown("Error: Failed to create metrics display")
    
    @staticmethod
    def create_statistics_display(statistics: Dict):
        """Create statistics display"""
        try:
            if not statistics or statistics.get('total_jobs', 0) == 0:
                return pn.pane.Markdown("""
                ### 📊 Training Statistics
                No training jobs available
                """)
            
            total_jobs = statistics.get('total_jobs', 0)
            status_dist = statistics.get('status_distribution', {})
            model_dist = statistics.get('model_type_distribution', {})
            running_jobs = statistics.get('running_jobs', 0)
            completed_jobs = statistics.get('completed_jobs', 0)
            
            stats_text = f"""
            ### 📊 Training Statistics
            
            **Total Jobs**: {total_jobs}  
            **Running Jobs**: {running_jobs}  
            **Completed Jobs**: {completed_jobs}  
            
            **Status Distribution**: {status_dist}  
            **Model Type Distribution**: {model_dist}
            """
            
            return pn.pane.Markdown(stats_text)
            
        except Exception as e:
            logger.error(f"Failed to create statistics display: {e}")
            return pn.pane.Markdown("Error: Failed to create statistics display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Training...
        Please wait while the model is training.
        """)
    
    @staticmethod
    def create_progress_bar(progress: float):
        """Create progress bar display"""
        try:
            progress_text = f"""
            ### 📊 Progress: {progress:.1f}%
            
            █████████████████████████████████████████████████████████████████████████████████████████████████████
            """
            
            # Calculate filled portion
            filled_length = int(progress / 100 * 100)
            progress_bar = "█" * filled_length + "░" * (100 - filled_length)
            
            return pn.pane.Markdown(f"""
            ### 📊 Progress: {progress:.1f}%
            
            {progress_bar}
            """)
            
        except Exception as e:
            logger.error(f"Failed to create progress bar: {e}")
            return pn.pane.Markdown("Error: Failed to create progress bar")



