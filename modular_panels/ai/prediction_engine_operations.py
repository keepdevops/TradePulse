#!/usr/bin/env python3
"""
TradePulse AI Prediction Engine - Operations
Prediction-related operations for the prediction engine
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class PredictionEngineOperations:
    """Prediction-related operations for prediction engine"""
    
    def batch_predict(self, engine, model: Dict, input_data: pd.DataFrame, 
                     batch_size: int = 1000) -> List[Dict]:
        """Make predictions in batches"""
        try:
            logger.info(f"🔮 Starting batch prediction with batch size {batch_size}")
            
            predictions = []
            total_samples = len(input_data)
            
            for i in range(0, total_samples, batch_size):
                batch_end = min(i + batch_size, total_samples)
                batch_data = input_data.iloc[i:batch_end]
                
                logger.info(f"Processing batch {i//batch_size + 1}: samples {i+1}-{batch_end}")
                
                # Make prediction for this batch
                batch_result = engine.make_prediction(model, batch_data)
                predictions.append(batch_result)
            
            logger.info(f"✅ Batch prediction completed: {len(predictions)} batches")
            return predictions
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            raise
    
    def get_prediction_history(self, prediction_history: List[Dict], model_id: Optional[str] = None) -> List[Dict]:
        """Get prediction history, optionally filtered by model ID"""
        if model_id:
            return [p for p in prediction_history if p['model_id'] == model_id]
        return prediction_history.copy()
    
    def get_prediction_statistics(self, prediction_history: List[Dict]) -> Dict:
        """Get comprehensive prediction statistics"""
        try:
            total_predictions = len(prediction_history)
            
            if total_predictions == 0:
                return {'total_predictions': 0}
            
            # Count by prediction type
            type_counts = {}
            model_type_counts = {}
            
            for prediction in prediction_history:
                pred_type = prediction['prediction_type']
                model_type = prediction['model_type']
                
                type_counts[pred_type] = type_counts.get(pred_type, 0) + 1
                model_type_counts[model_type] = model_type_counts.get(model_type, 0) + 1
            
            # Calculate average confidence scores
            all_confidence = []
            for prediction in prediction_history:
                all_confidence.extend(prediction['confidence_scores'])
            
            avg_confidence = np.mean(all_confidence) if all_confidence else 0
            
            return {
                'total_predictions': total_predictions,
                'prediction_type_distribution': type_counts,
                'model_type_distribution': model_type_counts,
                'average_confidence': avg_confidence,
                'last_prediction': prediction_history[-1]['prediction_time'] if prediction_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get prediction statistics: {e}")
            return {}
    
    def clear_prediction_history(self, prediction_history: List[Dict]) -> int:
        """Clear prediction history and return count of cleared records"""
        try:
            count = len(prediction_history)
            prediction_history.clear()
            logger.info(f"🗑️ Cleared {count} prediction records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear prediction history: {e}")
            return 0
    
    def validate_model_for_prediction(self, model: Dict) -> bool:
        """Validate model for prediction"""
        try:
            # Check required fields
            required_fields = ['id', 'type', 'status']
            for field in required_fields:
                if field not in model:
                    return False
            
            # Check model status
            if model['status'] != 'trained':
                return False
            
            # Check model type
            valid_types = ['Random Forest', 'XGBoost', 'LSTM', 'ADM', 'CIPO', 'BICIPO']
            if model['type'] not in valid_types:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate model for prediction: {e}")
            return False
    
    def export_predictions_to_csv(self, predictions: List[Dict], filename: str = None) -> str:
        """Export predictions to CSV file"""
        try:
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"predictions_{timestamp}.csv"
            
            # Flatten predictions for CSV export
            flat_predictions = []
            for pred in predictions:
                flat_pred = {
                    'prediction_type': pred.get('prediction_type', 'Unknown'),
                    'predictions_count': len(pred.get('predictions', [])),
                    'avg_confidence': np.mean(pred.get('confidence_scores', [0])),
                    'metadata': str(pred.get('metadata', {}))
                }
                flat_predictions.append(flat_pred)
            
            # Convert to DataFrame and export
            df = pd.DataFrame(flat_predictions)
            df.to_csv(filename, index=False)
            
            logger.info(f"📤 Predictions exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export predictions to CSV: {e}")
            return None
    
    def get_prediction_summary_text(self, prediction_result: Dict) -> str:
        """Get text summary of prediction results"""
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



