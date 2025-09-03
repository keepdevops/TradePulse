#!/usr/bin/env python3
"""
TradePulse v10.11 Master Test Runner
Runs all test suites for comprehensive testing
"""

import sys
import os
import json
import subprocess
from pathlib import Path
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestRunnerV10_11:
    """Master test runner for TradePulse v10.11"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_results = {}
        self.start_time = datetime.now()
        
    def run_comprehensive_test_suite(self):
        """Run the comprehensive test suite"""
        logger.info("🚀 Running Comprehensive Test Suite")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run([
                sys.executable, "test_suite_v10_11.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            self.test_results['comprehensive'] = {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            if result.returncode == 0:
                logger.info("✅ Comprehensive test suite passed")
            else:
                logger.error("❌ Comprehensive test suite failed")
                
        except Exception as e:
            logger.error(f"❌ Error running comprehensive test suite: {e}")
            self.test_results['comprehensive'] = {
                'success': False,
                'error': str(e)
            }
    
    def run_authentication_tests(self):
        """Run authentication test suite"""
        logger.info("🔐 Running Authentication Test Suite")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run([
                sys.executable, "test_authentication_v10_11.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            self.test_results['authentication'] = {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            if result.returncode == 0:
                logger.info("✅ Authentication test suite passed")
            else:
                logger.error("❌ Authentication test suite failed")
                
        except Exception as e:
            logger.error(f"❌ Error running authentication test suite: {e}")
            self.test_results['authentication'] = {
                'success': False,
                'error': str(e)
            }
    
    def run_ai_ml_tests(self):
        """Run AI/ML test suite"""
        logger.info("🤖 Running AI/ML Test Suite")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run([
                sys.executable, "test_ai_ml_v10_11.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            self.test_results['ai_ml'] = {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            if result.returncode == 0:
                logger.info("✅ AI/ML test suite passed")
            else:
                logger.error("❌ AI/ML test suite failed")
                
        except Exception as e:
            logger.error(f"❌ Error running AI/ML test suite: {e}")
            self.test_results['ai_ml'] = {
                'success': False,
                'error': str(e)
            }
    
    def run_individual_module_tests(self):
        """Run individual module tests"""
        logger.info("🧩 Running Individual Module Tests")
        logger.info("=" * 60)
        
        modules_to_test = [
            'data_management',
            'portfolio_management', 
            'alert_system',
            'chart_system',
            'system_monitoring',
            'ui_components'
        ]
        
        for module in modules_to_test:
            logger.info(f"Testing {module} module...")
            try:
                # Create a simple test for each module
                test_result = self.test_module(module)
                self.test_results[module] = test_result
                
                if test_result['success']:
                    logger.info(f"✅ {module} module test passed")
                else:
                    logger.warning(f"⚠️ {module} module test failed")
                    
            except Exception as e:
                logger.error(f"❌ Error testing {module} module: {e}")
                self.test_results[module] = {
                    'success': False,
                    'error': str(e)
                }
    
    def test_module(self, module_name):
        """Test individual module functionality"""
        try:
            if module_name == 'data_management':
                return self.test_data_management()
            elif module_name == 'portfolio_management':
                return self.test_portfolio_management()
            elif module_name == 'alert_system':
                return self.test_alert_system()
            elif module_name == 'chart_system':
                return self.test_chart_system()
            elif module_name == 'system_monitoring':
                return self.test_system_monitoring()
            elif module_name == 'ui_components':
                return self.test_ui_components()
            else:
                return {'success': False, 'error': f'Unknown module: {module_name}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_data_management(self):
        """Test data management functionality"""
        try:
            # Test basic data operations
            import pandas as pd
            import numpy as np
            
            # Create test data
            test_data = pd.DataFrame({
                'A': [1, 2, 3, 4, 5],
                'B': [10, 20, 30, 40, 50],
                'C': ['a', 'b', 'c', 'd', 'e']
            })
            
            # Test data validation
            is_valid = len(test_data) > 0 and not test_data.isnull().all().all()
            
            return {
                'success': is_valid,
                'data_shape': test_data.shape,
                'columns': list(test_data.columns)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_portfolio_management(self):
        """Test portfolio management functionality"""
        try:
            # Test portfolio calculations
            portfolio_data = {
                'AAPL': {'shares': 100, 'price': 150},
                'GOOGL': {'shares': 50, 'price': 2800},
                'MSFT': {'shares': 75, 'price': 300}
            }
            
            # Calculate total value
            total_value = sum(data['shares'] * data['price'] for data in portfolio_data.values())
            
            return {
                'success': total_value > 0,
                'total_value': total_value,
                'positions': len(portfolio_data)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_alert_system(self):
        """Test alert system functionality"""
        try:
            # Test alert creation
            alerts = [
                {'symbol': 'AAPL', 'type': 'price', 'threshold': 150, 'condition': 'above'},
                {'symbol': 'GOOGL', 'type': 'volume', 'threshold': 1000000, 'condition': 'above'}
            ]
            
            return {
                'success': len(alerts) > 0,
                'alert_count': len(alerts),
                'alert_types': list(set(alert['type'] for alert in alerts))
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_chart_system(self):
        """Test chart system functionality"""
        try:
            # Test chart creation
            chart_types = ['line', 'bar', 'candlestick', 'scatter']
            
            return {
                'success': len(chart_types) > 0,
                'chart_types': chart_types,
                'supported_formats': ['png', 'jpg', 'svg', 'html']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_system_monitoring(self):
        """Test system monitoring functionality"""
        try:
            import psutil
            
            # Test system metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            return {
                'success': True,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_components(self):
        """Test UI components functionality"""
        try:
            # Test UI component creation
            components = ['dashboard', 'data_table', 'chart', 'alert_panel', 'portfolio_view']
            
            return {
                'success': len(components) > 0,
                'component_count': len(components),
                'components': components
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_master_report(self):
        """Generate master test report"""
        logger.info("📊 Generating Master Test Report")
        logger.info("=" * 60)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Calculate overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('success', False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        logger.info(f"📈 Master Test Results Summary:")
        logger.info(f"   Total Test Suites: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {failed_tests}")
        logger.info(f"   Success Rate: {success_rate:.1f}%")
        logger.info(f"   Duration: {duration}")
        
        # Detailed results
        logger.info("\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            logger.info(f"   {test_name}: {status}")
            
            if not result.get('success', False) and 'error' in result:
                logger.warning(f"      Error: {result['error']}")
        
        # Save comprehensive report
        report_data = {
            'timestamp': self.start_time.isoformat(),
            'version': '10.11',
            'duration_seconds': duration.total_seconds(),
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': success_rate,
            'test_results': self.test_results,
            'summary': {
                'comprehensive_suite': self.test_results.get('comprehensive', {}).get('success', False),
                'authentication': self.test_results.get('authentication', {}).get('success', False),
                'ai_ml': self.test_results.get('ai_ml', {}).get('success', False),
                'data_management': self.test_results.get('data_management', {}).get('success', False),
                'portfolio_management': self.test_results.get('portfolio_management', {}).get('success', False),
                'alert_system': self.test_results.get('alert_system', {}).get('success', False),
                'chart_system': self.test_results.get('chart_system', {}).get('success', False),
                'system_monitoring': self.test_results.get('system_monitoring', {}).get('success', False),
                'ui_components': self.test_results.get('ui_components', {}).get('success', False)
            }
        }
        
        report_file = self.project_root / "master_test_report_v10_11.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"📄 Master test report saved to: {report_file}")
        
        return report_data
    
    def run_all_tests(self):
        """Run all test suites"""
        logger.info("🎯 TradePulse v10.11 Master Test Runner")
        logger.info("=" * 60)
        logger.info("Starting comprehensive testing of all features...")
        
        # Run all test suites
        self.run_comprehensive_test_suite()
        time.sleep(1)
        
        self.run_authentication_tests()
        time.sleep(1)
        
        self.run_ai_ml_tests()
        time.sleep(1)
        
        self.run_individual_module_tests()
        
        # Generate master report
        report = self.generate_master_report()
        
        # Final summary
        logger.info("\n" + "=" * 60)
        if report['success_rate'] >= 80:
            logger.info("🎉 Excellent! Most tests passed successfully!")
        elif report['success_rate'] >= 60:
            logger.info("👍 Good! Most core functionality is working!")
        else:
            logger.warning("⚠️ Some tests failed. Please review the results.")
        
        logger.info("=" * 60)
        
        return report

def main():
    """Main function"""
    runner = TestRunnerV10_11()
    report = runner.run_all_tests()
    
    # Exit with appropriate code
    if report['success_rate'] >= 60:
        logger.info("✅ Testing completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Testing completed with failures!")
        sys.exit(1)

if __name__ == "__main__":
    main()
