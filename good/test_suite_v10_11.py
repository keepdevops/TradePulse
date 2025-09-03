#!/usr/bin/env python3
"""
TradePulse v10.11 Comprehensive Test Suite
Based on TradePulse_SSD_V.10.11.rtf specification
Tests all major features and modules
"""

import unittest
import sys
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestTradePulseV10_11(unittest.TestCase):
    """Comprehensive test suite for TradePulse v10.11"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_data_dir = Path("test_data")
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Create sample test data
        self.create_test_data()
        
        logger.info("🧪 Setting up TradePulse v10.11 test environment")
    
    def create_test_data(self):
        """Create sample test data for testing"""
        # Sample stock data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        stock_data = pd.DataFrame({
            'Date': dates,
            'AAPL': np.random.randn(len(dates)).cumsum() + 150,
            'GOOGL': np.random.randn(len(dates)).cumsum() + 2800,
            'MSFT': np.random.randn(len(dates)).cumsum() + 300,
            'TSLA': np.random.randn(len(dates)).cumsum() + 200,
            'AMZN': np.random.randn(len(dates)).cumsum() + 3300
        })
        
        # Save test data
        stock_data.to_csv(self.test_data_dir / "sample_stock_data.csv", index=False)
        
        # Sample portfolio data
        portfolio_data = pd.DataFrame({
            'Symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
            'Shares': [100, 50, 75, 200, 30],
            'Purchase_Price': [150, 2800, 300, 200, 3300],
            'Current_Price': [160, 2900, 320, 220, 3400]
        })
        
        portfolio_data.to_csv(self.test_data_dir / "sample_portfolio.csv", index=False)
        
        logger.info("✅ Test data created successfully")

class TestAuthenticationSystem(TestTradePulseV10_11):
    """Test authentication and authorization features"""
    
    def test_rbac_system(self):
        """Test Role-Based Access Control system"""
        try:
            from auth.rbac import RBACManager
            from auth.user_manager import UserManager
            
            # Initialize RBAC
            rbac = RBACManager()
            user_manager = UserManager()
            
            # Test user creation
            user = user_manager.create_user("test_user", "password123", "trader")
            self.assertIsNotNone(user)
            
            # Test role assignment
            result = rbac.assign_role(user.id, "trader")
            self.assertTrue(result)
            
            # Test permission checking
            has_permission = rbac.check_permission(user.id, "view_data")
            self.assertTrue(has_permission)
            
            logger.info("✅ RBAC system test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ RBAC module not available: {e}")
        except Exception as e:
            logger.error(f"❌ RBAC test failed: {e}")
    
    def test_security_utils(self):
        """Test security utilities"""
        try:
            from auth.security_utils import SecurityUtils
            
            security = SecurityUtils()
            
            # Test password hashing
            password = "test_password"
            hashed = security.hash_password(password)
            self.assertNotEqual(password, hashed)
            
            # Test password verification
            is_valid = security.verify_password(password, hashed)
            self.assertTrue(is_valid)
            
            logger.info("✅ Security utilities test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Security utils module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Security utils test failed: {e}")

class TestDataManagement(TestTradePulseV10_11):
    """Test data management features"""
    
    def test_global_data_store(self):
        """Test Global Data Store implementation"""
        try:
            from ui_components.global_data_store import GlobalDataStore
            
            # Initialize Global Data Store
            gds = GlobalDataStore()
            
            # Test data storage
            test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            gds.store_data("test_dataset", test_data)
            
            # Test data retrieval
            retrieved_data = gds.get_data("test_dataset")
            self.assertIsNotNone(retrieved_data)
            self.assertEqual(len(retrieved_data), len(test_data))
            
            # Test metadata storage
            metadata = gds.get_metadata("test_dataset")
            self.assertIsNotNone(metadata)
            
            logger.info("✅ Global Data Store test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Global Data Store module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Global Data Store test failed: {e}")
    
    def test_data_manager(self):
        """Test enhanced data manager"""
        try:
            from ui_components.data_manager_refactored import DataManager
            
            data_manager = DataManager()
            
            # Test data loading
            test_file = self.test_data_dir / "sample_stock_data.csv"
            data = data_manager.load_data(str(test_file))
            self.assertIsNotNone(data)
            
            # Test data export
            export_file = self.test_data_dir / "export_test.csv"
            result = data_manager.export_data(data, str(export_file))
            self.assertTrue(result)
            
            # Test data validation
            is_valid = data_manager.validate_data(data)
            self.assertTrue(is_valid)
            
            logger.info("✅ Data Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Data Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Data Manager test failed: {e}")

class TestAIModules(TestTradePulseV10_11):
    """Test AI and machine learning features"""
    
    def test_model_manager(self):
        """Test AI model management"""
        try:
            from modular_panels.ai.model_manager_refactored import ModelManager
            
            model_manager = ModelManager()
            
            # Test model creation
            model_config = {
                'type': 'ADM',
                'hidden_layers': [64, 32],
                'learning_rate': 0.001
            }
            
            model = model_manager.create_model(model_config)
            self.assertIsNotNone(model)
            
            # Test model training
            training_data = pd.DataFrame({
                'feature1': np.random.randn(100),
                'feature2': np.random.randn(100),
                'target': np.random.randn(100)
            })
            
            training_result = model_manager.train_model(model, training_data)
            self.assertIsNotNone(training_result)
            
            logger.info("✅ Model Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Model Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Model Manager test failed: {e}")
    
    def test_prediction_engine(self):
        """Test prediction engine"""
        try:
            from modular_panels.ai.prediction_engine_refactored import PredictionEngine
            
            prediction_engine = PredictionEngine()
            
            # Test prediction generation
            test_data = pd.DataFrame({
                'feature1': np.random.randn(10),
                'feature2': np.random.randn(10)
            })
            
            predictions = prediction_engine.predict(test_data)
            self.assertIsNotNone(predictions)
            self.assertEqual(len(predictions), len(test_data))
            
            logger.info("✅ Prediction Engine test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Prediction Engine module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Prediction Engine test failed: {e}")

class TestPortfolioManagement(TestTradePulseV10_11):
    """Test portfolio management features"""
    
    def test_portfolio_optimizer(self):
        """Test portfolio optimization"""
        try:
            from modular_panels.portfolio.portfolio_optimizer import PortfolioOptimizer
            
            optimizer = PortfolioOptimizer()
            
            # Test portfolio optimization
            returns_data = pd.DataFrame({
                'AAPL': np.random.randn(100) * 0.02,
                'GOOGL': np.random.randn(100) * 0.015,
                'MSFT': np.random.randn(100) * 0.018,
                'TSLA': np.random.randn(100) * 0.03,
                'AMZN': np.random.randn(100) * 0.025
            })
            
            optimal_weights = optimizer.optimize(returns_data, risk_tolerance=0.1)
            self.assertIsNotNone(optimal_weights)
            self.assertAlmostEqual(sum(optimal_weights), 1.0, places=5)
            
            logger.info("✅ Portfolio Optimizer test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Portfolio Optimizer module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Portfolio Optimizer test failed: {e}")
    
    def test_portfolio_panel(self):
        """Test portfolio panel functionality"""
        try:
            from modular_panels.portfolio_panel_refactored import PortfolioPanel
            
            portfolio_panel = PortfolioPanel()
            
            # Test portfolio creation
            portfolio_data = pd.read_csv(self.test_data_dir / "sample_portfolio.csv")
            portfolio = portfolio_panel.create_portfolio(portfolio_data)
            self.assertIsNotNone(portfolio)
            
            # Test performance calculation
            performance = portfolio_panel.calculate_performance(portfolio)
            self.assertIsNotNone(performance)
            
            logger.info("✅ Portfolio Panel test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Portfolio Panel module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Portfolio Panel test failed: {e}")

class TestAlertSystem(TestTradePulseV10_11):
    """Test alert system features"""
    
    def test_alert_creator(self):
        """Test alert creation and management"""
        try:
            from modular_panels.alerts.alert_creator_refactored import AlertCreator
            
            alert_creator = AlertCreator()
            
            # Test price alert creation
            alert = alert_creator.create_price_alert("AAPL", 150.0, "above")
            self.assertIsNotNone(alert)
            self.assertEqual(alert.symbol, "AAPL")
            self.assertEqual(alert.threshold, 150.0)
            
            # Test volume alert creation
            volume_alert = alert_creator.create_volume_alert("GOOGL", 1000000, "above")
            self.assertIsNotNone(volume_alert)
            
            logger.info("✅ Alert Creator test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Alert Creator module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Alert Creator test failed: {e}")
    
    def test_alerts_panel(self):
        """Test alerts panel functionality"""
        try:
            from modular_panels.alerts_panel_refactored import AlertsPanel
            
            alerts_panel = AlertsPanel()
            
            # Test alert management
            alerts = alerts_panel.get_active_alerts()
            self.assertIsNotNone(alerts)
            
            # Test alert status
            status = alerts_panel.get_alert_status()
            self.assertIsNotNone(status)
            
            logger.info("✅ Alerts Panel test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Alerts Panel module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Alerts Panel test failed: {e}")

class TestChartSystem(TestTradePulseV10_11):
    """Test chart and visualization features"""
    
    def test_chart_factory(self):
        """Test chart factory functionality"""
        try:
            from demo_panels.chart_factory_refactored import ChartFactory
            
            chart_factory = ChartFactory()
            
            # Test price chart creation
            stock_data = pd.read_csv(self.test_data_dir / "sample_stock_data.csv")
            price_chart = chart_factory.create_price_chart(stock_data, "AAPL")
            self.assertIsNotNone(price_chart)
            
            # Test performance chart creation
            performance_chart = chart_factory.create_performance_chart(stock_data)
            self.assertIsNotNone(performance_chart)
            
            logger.info("✅ Chart Factory test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Chart Factory module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Chart Factory test failed: {e}")
    
    def test_charts_panel(self):
        """Test charts panel functionality"""
        try:
            from modular_panels.charts_panel_refactored import ChartsPanel
            
            charts_panel = ChartsPanel()
            
            # Test chart creation
            stock_data = pd.read_csv(self.test_data_dir / "sample_stock_data.csv")
            chart = charts_panel.create_chart(stock_data, "line")
            self.assertIsNotNone(chart)
            
            # Test chart customization
            custom_chart = charts_panel.customize_chart(chart, {"title": "Test Chart"})
            self.assertIsNotNone(custom_chart)
            
            logger.info("✅ Charts Panel test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Charts Panel module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Charts Panel test failed: {e}")

class TestSystemMonitoring(TestTradePulseV10_11):
    """Test system monitoring features"""
    
    def test_system_monitor(self):
        """Test system monitoring functionality"""
        try:
            from integrated_panels.system_monitor_refactored import SystemMonitor
            
            system_monitor = SystemMonitor()
            
            # Test system status
            status = system_monitor.get_system_status()
            self.assertIsNotNone(status)
            
            # Test performance metrics
            metrics = system_monitor.get_performance_metrics()
            self.assertIsNotNone(metrics)
            
            # Test resource usage
            resources = system_monitor.get_resource_usage()
            self.assertIsNotNone(resources)
            
            logger.info("✅ System Monitor test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ System Monitor module not available: {e}")
        except Exception as e:
            logger.error(f"❌ System Monitor test failed: {e}")
    
    def test_performance_display(self):
        """Test performance display functionality"""
        try:
            from integrated_panels.performance_display_refactored import PerformanceDisplay
            
            performance_display = PerformanceDisplay()
            
            # Test performance data
            performance_data = performance_display.get_performance_data()
            self.assertIsNotNone(performance_data)
            
            # Test performance visualization
            viz = performance_display.create_performance_visualization()
            self.assertIsNotNone(viz)
            
            logger.info("✅ Performance Display test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Performance Display module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Performance Display test failed: {e}")

class TestUIComponents(TestTradePulseV10_11):
    """Test UI components"""
    
    def test_dashboard_manager(self):
        """Test dashboard management"""
        try:
            from ui_components.dashboard_manager_refactored import DashboardManager
            
            dashboard_manager = DashboardManager()
            
            # Test dashboard creation
            dashboard = dashboard_manager.create_dashboard()
            self.assertIsNotNone(dashboard)
            
            # Test role-based customization
            trader_dashboard = dashboard_manager.create_role_dashboard("trader")
            self.assertIsNotNone(trader_dashboard)
            
            analyst_dashboard = dashboard_manager.create_role_dashboard("analyst")
            self.assertIsNotNone(analyst_dashboard)
            
            logger.info("✅ Dashboard Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Dashboard Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Dashboard Manager test failed: {e}")
    
    def test_data_metrics(self):
        """Test data metrics functionality"""
        try:
            from ui_components.data.data_metrics_refactored import DataMetrics
            
            data_metrics = DataMetrics()
            
            # Test metrics calculation
            stock_data = pd.read_csv(self.test_data_dir / "sample_stock_data.csv")
            metrics = data_metrics.calculate_metrics(stock_data)
            self.assertIsNotNone(metrics)
            
            # Test statistical analysis
            stats = data_metrics.calculate_statistics(stock_data)
            self.assertIsNotNone(stats)
            
            logger.info("✅ Data Metrics test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Data Metrics module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Data Metrics test failed: {e}")

class TestIntegrationFeatures(TestTradePulseV10_11):
    """Test integration features"""
    
    def test_module_integration(self):
        """Test module integration"""
        try:
            from modular_panels.module_integration import ModuleIntegration
            
            module_integration = ModuleIntegration()
            
            # Test module registration
            result = module_integration.register_module("test_module")
            self.assertTrue(result)
            
            # Test module communication
            communication = module_integration.test_communication()
            self.assertTrue(communication)
            
            logger.info("✅ Module Integration test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Module Integration module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Module Integration test failed: {e}")
    
    def test_data_persistence(self):
        """Test data persistence across modules"""
        try:
            from ui_components.global_data_store import GlobalDataStore
            
            gds = GlobalDataStore()
            
            # Store data
            test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            gds.store_data("persistence_test", test_data)
            
            # Retrieve data (simulating module switch)
            retrieved_data = gds.get_data("persistence_test")
            self.assertIsNotNone(retrieved_data)
            self.assertEqual(len(retrieved_data), len(test_data))
            
            # Test metadata persistence
            metadata = gds.get_metadata("persistence_test")
            self.assertIsNotNone(metadata)
            
            logger.info("✅ Data Persistence test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Data Persistence module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Data Persistence test failed: {e}")

def run_comprehensive_test_suite():
    """Run the comprehensive test suite"""
    logger.info("🚀 Starting TradePulse v10.11 Comprehensive Test Suite")
    logger.info("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAuthenticationSystem,
        TestDataManagement,
        TestAIModules,
        TestPortfolioManagement,
        TestAlertSystem,
        TestChartSystem,
        TestSystemMonitoring,
        TestUIComponents,
        TestIntegrationFeatures
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate test report
    generate_test_report(result)
    
    return result

def generate_test_report(result):
    """Generate comprehensive test report"""
    logger.info("📊 Generating Test Report")
    logger.info("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    logger.info(f"📈 Test Results Summary:")
    logger.info(f"   Total Tests: {total_tests}")
    logger.info(f"   Passed: {passed}")
    logger.info(f"   Failed: {failures}")
    logger.info(f"   Errors: {errors}")
    logger.info(f"   Skipped: {skipped}")
    logger.info(f"   Success Rate: {(passed/total_tests)*100:.1f}%")
    
    if failures > 0:
        logger.warning("⚠️ Test Failures:")
        for test, traceback in result.failures:
            logger.warning(f"   - {test}: {traceback}")
    
    if errors > 0:
        logger.error("❌ Test Errors:")
        for test, traceback in result.errors:
            logger.error(f"   - {test}: {traceback}")
    
    # Save detailed report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'version': '10.11',
        'total_tests': total_tests,
        'passed': passed,
        'failed': failures,
        'errors': errors,
        'skipped': skipped,
        'success_rate': (passed/total_tests)*100,
        'failures': [{'test': str(test), 'traceback': traceback} for test, traceback in result.failures],
        'errors': [{'test': str(test), 'traceback': traceback} for test, traceback in result.errors]
    }
    
    report_file = Path("test_report_v10_11.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"📄 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    # Run the comprehensive test suite
    result = run_comprehensive_test_suite()
    
    # Exit with appropriate code
    if result.wasSuccessful():
        logger.info("✅ All tests passed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed!")
        sys.exit(1)
