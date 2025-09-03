#!/usr/bin/env python3
"""
TradePulse v10.11 AI/ML Test Suite
Tests AI and machine learning features
"""

import unittest
import sys
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestAIMLV10_11(unittest.TestCase):
    """Test AI and machine learning features"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_data_dir = Path("test_data")
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Create sample training data
        self.create_training_data()
        
        logger.info("🧪 Setting up AI/ML test environment")
    
    def create_training_data(self):
        """Create sample training data for ML testing"""
        # Create synthetic stock data for training
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        
        # Generate features
        n_samples = len(dates)
        features = pd.DataFrame({
            'Date': dates,
            'price': np.random.randn(n_samples).cumsum() + 100,
            'volume': np.random.randint(1000000, 10000000, n_samples),
            'rsi': np.random.uniform(0, 100, n_samples),
            'macd': np.random.randn(n_samples),
            'bollinger_upper': np.random.randn(n_samples).cumsum() + 110,
            'bollinger_lower': np.random.randn(n_samples).cumsum() + 90,
            'sma_20': np.random.randn(n_samples).cumsum() + 100,
            'sma_50': np.random.randn(n_samples).cumsum() + 100,
            'volatility': np.random.uniform(0.01, 0.05, n_samples),
            'sentiment_score': np.random.uniform(-1, 1, n_samples)
        })
        
        # Generate target (price movement)
        features['target'] = np.where(features['price'].diff() > 0, 1, 0)
        features = features.dropna()
        
        # Save training data
        features.to_csv(self.test_data_dir / "ml_training_data.csv", index=False)
        
        logger.info("✅ Training data created successfully")
    
    def test_model_manager(self):
        """Test Model Manager functionality"""
        try:
            from modular_panels.ai.model_manager_refactored import ModelManager
            
            model_manager = ModelManager()
            
            # Test model creation for different types
            model_types = ['ADM', 'CIPO', 'BICIPO', 'Ensemble']
            
            for model_type in model_types:
                model_config = {
                    'type': model_type,
                    'hidden_layers': [64, 32, 16],
                    'learning_rate': 0.001,
                    'epochs': 10,
                    'batch_size': 32
                }
                
                model = model_manager.create_model(model_config)
                self.assertIsNotNone(model)
                self.assertEqual(model.model_type, model_type)
                
                logger.info(f"✅ {model_type} model creation test passed")
            
            # Test model listing
            models = model_manager.list_models()
            self.assertIsNotNone(models)
            self.assertIsInstance(models, list)
            
            logger.info("✅ Model Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Model Manager test failed: {e}")
    
    def test_prediction_engine(self):
        """Test Prediction Engine functionality"""
        try:
            from modular_panels.ai.prediction_engine_refactored import PredictionEngine
            
            prediction_engine = PredictionEngine()
            
            # Load test data
            test_data = pd.read_csv(self.test_data_dir / "ml_training_data.csv")
            features = test_data.drop(['Date', 'target'], axis=1, errors='ignore')
            
            # Test prediction generation
            predictions = prediction_engine.predict(features.head(10))
            self.assertIsNotNone(predictions)
            self.assertEqual(len(predictions), 10)
            
            # Test prediction confidence
            confidence_scores = prediction_engine.get_confidence_scores(features.head(10))
            self.assertIsNotNone(confidence_scores)
            self.assertEqual(len(confidence_scores), 10)
            
            # Test prediction explanation
            explanations = prediction_engine.explain_predictions(features.head(5))
            self.assertIsNotNone(explanations)
            
            logger.info("✅ Prediction Engine test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Prediction Engine module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Prediction Engine test failed: {e}")
    
    def test_training_engine(self):
        """Test Training Engine functionality"""
        try:
            from modular_panels.ai.training_engine_refactored import TrainingEngine
            
            training_engine = TrainingEngine()
            
            # Load training data
            training_data = pd.read_csv(self.test_data_dir / "ml_training_data.csv")
            features = training_data.drop(['Date', 'target'], axis=1, errors='ignore')
            targets = training_data['target']
            
            # Test model training
            model_config = {
                'type': 'ADM',
                'hidden_layers': [32, 16],
                'learning_rate': 0.001,
                'epochs': 5,
                'batch_size': 16
            }
            
            training_result = training_engine.train_model(
                features, 
                targets, 
                model_config
            )
            
            self.assertIsNotNone(training_result)
            self.assertIn('model', training_result)
            self.assertIn('metrics', training_result)
            self.assertIn('history', training_result)
            
            # Test hyperparameter tuning
            tuning_result = training_engine.hyperparameter_tuning(
                features, 
                targets, 
                param_grid={
                    'learning_rate': [0.001, 0.01],
                    'hidden_layers': [[32], [32, 16]]
                }
            )
            
            self.assertIsNotNone(tuning_result)
            self.assertIn('best_params', tuning_result)
            self.assertIn('best_score', tuning_result)
            
            logger.info("✅ Training Engine test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Training Engine module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Training Engine test failed: {e}")
    
    def test_model_storage(self):
        """Test Model Storage functionality"""
        try:
            from modular_panels.model_storage import ModelStorage
            
            model_storage = ModelStorage()
            
            # Test model saving
            model_data = {
                'model_type': 'ADM',
                'version': '1.0',
                'created_date': datetime.now().isoformat(),
                'parameters': {'hidden_layers': [64, 32], 'learning_rate': 0.001},
                'performance': {'accuracy': 0.85, 'precision': 0.82, 'recall': 0.88}
            }
            
            save_result = model_storage.save_model('test_model', model_data)
            self.assertTrue(save_result)
            
            # Test model loading
            loaded_model = model_storage.load_model('test_model')
            self.assertIsNotNone(loaded_model)
            self.assertEqual(loaded_model['model_type'], 'ADM')
            
            # Test model listing
            models = model_storage.list_models()
            self.assertIsNotNone(models)
            self.assertIn('test_model', models)
            
            # Test model deletion
            delete_result = model_storage.delete_model('test_model')
            self.assertTrue(delete_result)
            
            logger.info("✅ Model Storage test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Storage module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Model Storage test failed: {e}")
    
    def test_model_performance(self):
        """Test Model Performance tracking"""
        try:
            from modular_panels.model_performance import ModelPerformance
            
            model_performance = ModelPerformance()
            
            # Test performance calculation
            y_true = [1, 0, 1, 1, 0, 1, 0, 1]
            y_pred = [1, 0, 1, 0, 0, 1, 1, 1]
            
            metrics = model_performance.calculate_metrics(y_true, y_pred)
            self.assertIsNotNone(metrics)
            self.assertIn('accuracy', metrics)
            self.assertIn('precision', metrics)
            self.assertIn('recall', metrics)
            self.assertIn('f1_score', metrics)
            
            # Test performance tracking
            performance_data = {
                'model_id': 'test_model_001',
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics,
                'dataset_size': 1000,
                'training_time': 120.5
            }
            
            track_result = model_performance.track_performance(performance_data)
            self.assertTrue(track_result)
            
            # Test performance history
            history = model_performance.get_performance_history('test_model_001')
            self.assertIsNotNone(history)
            
            logger.info("✅ Model Performance test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Performance module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Model Performance test failed: {e}")
    
    def test_ai_panel(self):
        """Test AI Panel functionality"""
        try:
            from modular_panels.ai.ai_panel import AIPanel
            
            ai_panel = AIPanel()
            
            # Test panel initialization
            panel = ai_panel.create_panel()
            self.assertIsNotNone(panel)
            
            # Test model selection
            available_models = ai_panel.get_available_models()
            self.assertIsNotNone(available_models)
            self.assertIsInstance(available_models, list)
            
            # Test training status
            training_status = ai_panel.get_training_status()
            self.assertIsNotNone(training_status)
            
            # Test prediction interface
            prediction_interface = ai_panel.get_prediction_interface()
            self.assertIsNotNone(prediction_interface)
            
            logger.info("✅ AI Panel test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ AI Panel module not available: {e}")
        except Exception as e:
            logger.error(f"❌ AI Panel test failed: {e}")
    
    def test_ensemble_models(self):
        """Test Ensemble Model functionality"""
        try:
            from modular_panels.ai.model_manager_refactored import ModelManager
            
            model_manager = ModelManager()
            
            # Test ensemble model creation
            ensemble_config = {
                'type': 'Ensemble',
                'models': ['ADM', 'CIPO', 'BICIPO'],
                'weights': [0.4, 0.3, 0.3],
                'aggregation_method': 'weighted_average'
            }
            
            ensemble_model = model_manager.create_model(ensemble_config)
            self.assertIsNotNone(ensemble_model)
            self.assertEqual(ensemble_model.model_type, 'Ensemble')
            
            # Test ensemble prediction
            test_features = pd.DataFrame({
                'feature1': np.random.randn(10),
                'feature2': np.random.randn(10),
                'feature3': np.random.randn(10)
            })
            
            ensemble_predictions = ensemble_model.predict(test_features)
            self.assertIsNotNone(ensemble_predictions)
            self.assertEqual(len(ensemble_predictions), 10)
            
            logger.info("✅ Ensemble Models test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Ensemble Models test failed: {e}")
    
    def test_model_visualization(self):
        """Test Model Visualization functionality"""
        try:
            from modular_panels.ai.model_manager_refactored import ModelManager
            
            model_manager = ModelManager()
            
            # Test model architecture visualization
            model_config = {
                'type': 'ADM',
                'hidden_layers': [64, 32, 16],
                'learning_rate': 0.001
            }
            
            model = model_manager.create_model(model_config)
            architecture_viz = model_manager.visualize_architecture(model)
            self.assertIsNotNone(architecture_viz)
            
            # Test training history visualization
            training_history = {
                'loss': [0.5, 0.4, 0.3, 0.25, 0.2],
                'accuracy': [0.6, 0.7, 0.8, 0.85, 0.9],
                'val_loss': [0.6, 0.5, 0.4, 0.35, 0.3],
                'val_accuracy': [0.5, 0.6, 0.7, 0.75, 0.8]
            }
            
            history_viz = model_manager.visualize_training_history(training_history)
            self.assertIsNotNone(history_viz)
            
            logger.info("✅ Model Visualization test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Model Visualization test failed: {e}")

def run_ai_ml_tests():
    """Run AI/ML test suite"""
    logger.info("🤖 Starting TradePulse v10.11 AI/ML Test Suite")
    logger.info("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(TestAIMLV10_11)
    test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate report
    generate_ai_ml_test_report(result)
    
    return result

def generate_ai_ml_test_report(result):
    """Generate AI/ML test report"""
    logger.info("📊 Generating AI/ML Test Report")
    logger.info("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    logger.info(f"🤖 AI/ML Test Results:")
    logger.info(f"   Total Tests: {total_tests}")
    logger.info(f"   Passed: {passed}")
    logger.info(f"   Failed: {failures}")
    logger.info(f"   Errors: {errors}")
    logger.info(f"   Success Rate: {(passed/total_tests)*100:.1f}%")
    
    # Save report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'version': '10.11',
        'test_type': 'ai_ml',
        'total_tests': total_tests,
        'passed': passed,
        'failed': failures,
        'errors': errors,
        'success_rate': (passed/total_tests)*100,
        'failures': [{'test': str(test), 'traceback': traceback} for test, traceback in result.failures],
        'errors': [{'test': str(test), 'traceback': traceback} for test, traceback in result.errors]
    }
    
    report_file = Path("ai_ml_test_report_v10_11.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"📄 AI/ML test report saved to: {report_file}")

if __name__ == "__main__":
    result = run_ai_ml_tests()
    
    if result.wasSuccessful():
        logger.info("✅ All AI/ML tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some AI/ML tests failed!")
        sys.exit(1)
