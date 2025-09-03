#!/usr/bin/env python3
"""
TradePulse Authentication System Test Script
Tests all authentication components and functionality
"""

import sys
import os
import logging
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main test function"""
    print("🚀 TradePulse Authentication System Test Suite")
    print("=" * 60)
    
    # Ensure data directory exists
    os.makedirs("./data", exist_ok=True)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("SecurityUtils", "test_auth_security_utils"),
        ("UserManager", "test_auth_user_manager"),
        ("RBAC", "test_auth_rbac"),
        ("SessionManager", "test_auth_session_manager"),
        ("AuthService", "test_auth_service"),
        ("Admin Functionality", "test_auth_admin")
    ]
    
    for test_name, test_module in tests:
        print(f"\n📋 Running {test_name} tests...")
        try:
            # Import and run the test module
            module = __import__(test_module)
            result = module.run_tests()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))
    
    # Print test summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All authentication system tests passed successfully!")
        print("🔐 The authentication system is ready for integration!")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    # Cleanup
    cleanup_test_data()
    
    return passed == total

def cleanup_test_data():
    """Clean up test data files"""
    print("🧹 Cleaning up test data...")
    
    try:
        test_files = [
            "./data/test_users.db",
            "./data/test_users.db-shm",
            "./data/test_users.db-wal"
        ]
        
        for file_path in test_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"  ✅ Removed: {file_path}")
        
        print("  🎯 Test data cleanup completed!")
        
    except Exception as e:
        print(f"  ❌ Test data cleanup failed: {e}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
