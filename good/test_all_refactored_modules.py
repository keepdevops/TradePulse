#!/usr/bin/env python3
"""
TradePulse V10.9 - Comprehensive Module Testing
Tests all refactored modules to ensure they work correctly
"""

import sys
import traceback
from typing import Dict, List, Tuple

def main():
    """Main testing function"""
    print("🚀 TradePulse V10.9 - Comprehensive Module Testing")
    print("=" * 60)
    
    all_errors = []
    test_results = {}
    
    # Test all modules
    tests = [
        ("Modular Panels", "test_modular_panels"),
        ("Integrated Panels", "test_integrated_panels"),
        ("UI Panels", "test_ui_panels"),
        ("Demo Panels", "test_demo_panels"),
        ("UI Components", "test_ui_components"),
        ("Launch Scripts", "test_launch_scripts")
    ]
    
    for test_name, test_module in tests:
        try:
            # Import and run the test module
            module = __import__(test_module)
            result = module.run_tests()
            # Ensure we have a boolean result
            success = bool(result) if result is not None else False
            test_results[test_name] = success
            if not success:
                all_errors.append(f"❌ {test_name} test failed")
            
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            error_msg = f"❌ {test_name} test crashed: {e}"
            print(error_msg)
            all_errors.append(error_msg)
            test_results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, success in test_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} modules passed")
    
    if all_errors:
        print(f"\n❌ ERRORS FOUND ({len(all_errors)} total):")
        for i, error in enumerate(all_errors, 1):
            print(f"{i}. {error}")
    else:
        print("\n🎉 ALL MODULES PASSED! No errors found.")
    
    # Recommendations
    if all_errors:
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Fix the errors listed above")
        print("2. Re-run tests to verify fixes")
        print("3. Only delete old files after all tests pass")
    else:
        print("\n🎯 NEXT STEPS:")
        print("1. All refactored modules are working correctly")
        print("2. Safe to delete any remaining old monolithic files")
        print("3. Proceed with V10.9 deployment")
    
    return len(all_errors) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
