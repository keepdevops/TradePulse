#!/usr/bin/env python3
"""
TradePulse AI Prediction Engine - Management
UI management for the prediction engine
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class PredictionEngineManagement:
    """UI management for prediction engine"""
    
    @staticmethod
    def get_prediction_summary(prediction_result: Dict) -> str:
        """Get prediction summary for display"""
        try:
            if not prediction_result:
                return "No prediction results available"
            
            pred_type = prediction_result.get('prediction_type', 'Unknown')
            pred_count = len(prediction_result.get('predictions', []))
            avg_confidence = np.mean(prediction_result.get('confidence_scores', [0]))
            metadata = prediction_result.get('metadata', {})
            
            summary_lines = [
                f"**Prediction Type**: {pred_type}",
                f"**Number of Predictions**: {pred_count}",
                f"**Average Confidence**: {avg_confidence:.3f}",
                f"**Metadata**: {metadata}"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create prediction summary: {e}")
            return "Error creating summary"
    
    @staticmethod
    def create_prediction_display(prediction_result: Dict):
        """Create prediction results display"""
        try:
            if not prediction_result:
                return pn.pane.Markdown("""
                ### 📈 Prediction Results
                No predictions made yet
                """)
            
            pred_type = prediction_result.get('prediction_type', 'Unknown')
            pred_count = len(prediction_result.get('predictions', []))
            avg_confidence = np.mean(prediction_result.get('confidence_scores', [0]))
            metadata = prediction_result.get('metadata', {})
            
            display_text = f"""
            ### 📈 Prediction Results
            
            **Type**: {pred_type}  
            **Predictions**: {pred_count}  
            **Avg Confidence**: {avg_confidence:.3f}  
            **Metadata**: {metadata}
            """
            
            return pn.pane.Markdown(display_text)
            
        except Exception as e:
            logger.error(f"Failed to create prediction display: {e}")
            return pn.pane.Markdown("Error: Failed to create prediction display")
    
    @staticmethod
    def create_statistics_display(statistics: Dict):
        """Create statistics display"""
        try:
            if not statistics or statistics.get('total_predictions', 0) == 0:
                return pn.pane.Markdown("""
                ### 📊 Prediction Statistics
                No predictions recorded
                """)
            
            total_preds = statistics.get('total_predictions', 0)
            type_dist = statistics.get('prediction_type_distribution', {})
            model_dist = statistics.get('model_type_distribution', {})
            avg_conf = statistics.get('average_confidence', 0)
            last_pred = statistics.get('last_prediction', 'Never')
            
            stats_text = f"""
            ### 📊 Prediction Statistics
            
            **Total Predictions**: {total_preds}  
            **Average Confidence**: {avg_conf:.3f}  
            **Last Prediction**: {last_pred}  
            
            **Type Distribution**: {type_dist}  
            **Model Distribution**: {model_dist}
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
        ### ⏳ Making Prediction...
        Please wait while we process your data.
        """)
    
    @staticmethod
    def create_model_status_display(model: Dict):
        """Create model status display"""
        try:
            if not model:
                return pn.pane.Markdown("""
                ### 🤖 Model Status
                No model selected
                """)
            
            model_id = model.get('id', 'Unknown')
            model_type = model.get('type', 'Unknown')
            model_status = model.get('status', 'Unknown')
            
            status_text = f"""
            ### 🤖 Model Status
            
            **Model ID**: {model_id}  
            **Type**: {model_type}  
            **Status**: {model_status}  
            """
            
            return pn.pane.Markdown(status_text)
            
        except Exception as e:
            logger.error(f"Failed to create model status display: {e}")
            return pn.pane.Markdown("Error: Failed to create model status display")



