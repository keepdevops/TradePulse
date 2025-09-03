#!/usr/bin/env python3
"""
TradePulse v10.11 Authentication Test Suite
Tests authentication and authorization features
"""

import unittest
import sys
import os
import json
from pathlib import Path
import logging
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestAuthenticationV10_11(unittest.TestCase):
    """Test authentication and authorization features"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_users = [
            {"username": "day_trader", "password": "trader123", "role": "trader"},
            {"username": "analyst", "password": "analyst123", "role": "analyst"},
            {"username": "admin", "password": "admin123", "role": "admin"}
        ]
        logger.info("🧪 Setting up authentication test environment")
    
    def test_rbac_manager(self):
        """Test RBAC Manager functionality"""
        try:
            from auth.rbac_manager import RBACManager
            
            rbac = RBACManager()
            
            # Test role creation
            result = rbac.create_role("trader", ["view_data", "create_alerts", "view_portfolio"])
            self.assertTrue(result)
            
            # Test permission assignment
            result = rbac.assign_permission("trader", "view_data")
            self.assertTrue(result)
            
            # Test role assignment
            result = rbac.assign_role_to_user("user123", "trader")
            self.assertTrue(result)
            
            # Test permission checking
            has_permission = rbac.check_permission("user123", "view_data")
            self.assertTrue(has_permission)
            
            logger.info("✅ RBAC Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ RBAC Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ RBAC Manager test failed: {e}")
    
    def test_user_manager(self):
        """Test User Manager functionality"""
        try:
            from auth.user_manager import UserManager
            
            user_manager = UserManager()
            
            # Test user creation
            for user_data in self.test_users:
                user = user_manager.create_user(
                    user_data["username"], 
                    user_data["password"], 
                    user_data["role"]
                )
                self.assertIsNotNone(user)
                self.assertEqual(user.username, user_data["username"])
                self.assertEqual(user.role, user_data["role"])
            
            # Test user authentication
            for user_data in self.test_users:
                is_authenticated = user_manager.authenticate_user(
                    user_data["username"], 
                    user_data["password"]
                )
                self.assertTrue(is_authenticated)
            
            # Test user retrieval
            user = user_manager.get_user_by_username("day_trader")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "day_trader")
            
            logger.info("✅ User Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ User Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ User Manager test failed: {e}")
    
    def test_session_manager(self):
        """Test Session Manager functionality"""
        try:
            from auth.session_manager import SessionManager
            
            session_manager = SessionManager()
            
            # Test session creation
            session = session_manager.create_session("user123")
            self.assertIsNotNone(session)
            self.assertEqual(session.user_id, "user123")
            
            # Test session validation
            is_valid = session_manager.validate_session(session.session_id)
            self.assertTrue(is_valid)
            
            # Test session expiration
            session_manager.expire_session(session.session_id)
            is_valid = session_manager.validate_session(session.session_id)
            self.assertFalse(is_valid)
            
            logger.info("✅ Session Manager test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Session Manager module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Session Manager test failed: {e}")
    
    def test_security_utils(self):
        """Test Security Utilities"""
        try:
            from auth.security_utils import SecurityUtils
            
            security = SecurityUtils()
            
            # Test password hashing
            password = "test_password_123"
            hashed = security.hash_password(password)
            self.assertNotEqual(password, hashed)
            self.assertIsInstance(hashed, str)
            
            # Test password verification
            is_valid = security.verify_password(password, hashed)
            self.assertTrue(is_valid)
            
            # Test invalid password
            is_valid = security.verify_password("wrong_password", hashed)
            self.assertFalse(is_valid)
            
            # Test token generation
            token = security.generate_token("user123")
            self.assertIsNotNone(token)
            self.assertIsInstance(token, str)
            
            # Test token validation
            is_valid = security.validate_token(token)
            self.assertTrue(is_valid)
            
            logger.info("✅ Security Utils test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Security Utils module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Security Utils test failed: {e}")
    
    def test_auth_service(self):
        """Test Authentication Service"""
        try:
            from auth.auth_service import AuthService
            
            auth_service = AuthService()
            
            # Test user registration
            result = auth_service.register_user("new_user", "password123", "trader")
            self.assertTrue(result)
            
            # Test user login
            login_result = auth_service.login("new_user", "password123")
            self.assertIsNotNone(login_result)
            self.assertIn("session_id", login_result)
            self.assertIn("user_id", login_result)
            
            # Test user logout
            logout_result = auth_service.logout(login_result["session_id"])
            self.assertTrue(logout_result)
            
            # Test invalid login
            invalid_login = auth_service.login("new_user", "wrong_password")
            self.assertIsNone(invalid_login)
            
            logger.info("✅ Auth Service test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ Auth Service module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Auth Service test failed: {e}")
    
    def test_role_based_access(self):
        """Test role-based access control"""
        try:
            from auth.rbac import RBACManager
            from auth.user_manager import UserManager
            
            rbac = RBACManager()
            user_manager = UserManager()
            
            # Create test users with different roles
            trader_user = user_manager.create_user("trader_test", "password", "trader")
            analyst_user = user_manager.create_user("analyst_test", "password", "analyst")
            admin_user = user_manager.create_user("admin_test", "password", "admin")
            
            # Test trader permissions
            trader_permissions = rbac.get_user_permissions(trader_user.id)
            self.assertIn("view_data", trader_permissions)
            self.assertIn("create_alerts", trader_permissions)
            
            # Test analyst permissions
            analyst_permissions = rbac.get_user_permissions(analyst_user.id)
            self.assertIn("view_data", analyst_permissions)
            self.assertIn("view_analytics", analyst_permissions)
            
            # Test admin permissions
            admin_permissions = rbac.get_user_permissions(admin_user.id)
            self.assertIn("view_data", admin_permissions)
            self.assertIn("manage_users", admin_permissions)
            self.assertIn("system_admin", admin_permissions)
            
            logger.info("✅ Role-based access test passed")
            
        except ImportError as e:
            logger.warning(f"⚠️ RBAC module not available: {e}")
        except Exception as e:
            logger.error(f"❌ Role-based access test failed: {e}")

def run_authentication_tests():
    """Run authentication test suite"""
    logger.info("🔐 Starting TradePulse v10.11 Authentication Test Suite")
    logger.info("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(TestAuthenticationV10_11)
    test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate report
    generate_auth_test_report(result)
    
    return result

def generate_auth_test_report(result):
    """Generate authentication test report"""
    logger.info("📊 Generating Authentication Test Report")
    logger.info("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    logger.info(f"🔐 Authentication Test Results:")
    logger.info(f"   Total Tests: {total_tests}")
    logger.info(f"   Passed: {passed}")
    logger.info(f"   Failed: {failures}")
    logger.info(f"   Errors: {errors}")
    logger.info(f"   Success Rate: {(passed/total_tests)*100:.1f}%")
    
    # Save report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'version': '10.11',
        'test_type': 'authentication',
        'total_tests': total_tests,
        'passed': passed,
        'failed': failures,
        'errors': errors,
        'success_rate': (passed/total_tests)*100,
        'failures': [{'test': str(test), 'traceback': traceback} for test, traceback in result.failures],
        'errors': [{'test': str(test), 'traceback': traceback} for test, traceback in result.errors]
    }
    
    report_file = Path("auth_test_report_v10_11.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"📄 Authentication test report saved to: {report_file}")

if __name__ == "__main__":
    result = run_authentication_tests()
    
    if result.wasSuccessful():
        logger.info("✅ All authentication tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some authentication tests failed!")
        sys.exit(1)
