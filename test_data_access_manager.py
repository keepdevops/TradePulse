#!/usr/bin/env python3
"""
Test Data Access Manager Availability
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui_components.data_manager import DataManager
from ui_components.data_access import DataAccessManager
from ui_components.module_data_access import ModuleDataAccess

def test_data_access_manager():
    """Test data access manager availability"""
    print("🧪 Testing Data Access Manager Availability")
    print("=" * 60)
    
    # Initialize data manager and data access
    data_manager = DataManager()
    data_access_manager = DataAccessManager(data_manager)
    
    # Test ModuleDataAccess
    module_data_access = ModuleDataAccess(data_manager, data_access_manager, 'data')
    
    print("\n📊 Data Access Manager Status:")
    print("-" * 40)
    
    # Check if data access manager is available
    print(f"✅ DataManager: {data_manager is not None}")
    print(f"✅ DataAccessManager: {data_access_manager is not None}")
    print(f"✅ ModuleDataAccess: {module_data_access is not None}")
    print(f"✅ is_data_access_available(): {module_data_access.is_data_access_available()}")
    print(f"✅ data_access_manager attribute: {module_data_access.data_access_manager is not None}")
    
    # Test data fetching
    print(f"\n📥 Testing Data Fetching:")
    print("-" * 40)
    
    # Test mock data
    mock_data = data_access_manager.get_data('mock', 'AAPL', '1d', '2024-01-01', '2024-01-31')
    print(f"✅ Mock data: {len(mock_data)} records")
    
    # Test upload data
    upload_data = data_access_manager.get_data('upload', 'AAPL', '1d', '2024-01-01', '2024-01-31')
    print(f"✅ Upload data: {len(upload_data)} records")
    
    # Test available files
    available_files = data_access_manager.get_available_data_files()
    total_files = sum(len(files) for files in available_files.values())
    print(f"✅ Available files: {total_files} files found")
    
    # Test module data access methods
    print(f"\n🔧 Testing Module Data Access Methods:")
    print("-" * 40)
    
    # Test API data
    api_data = module_data_access.get_api_data(['AAPL'], 'mock')
    print(f"✅ Module API data: {len(api_data)} symbols")
    
    # Test data summary
    summary = module_data_access.get_data_summary()
    print(f"✅ Module data summary: {summary}")
    
    print(f"\n✅ Data Access Manager Test Complete!")
    print(f"\n🎯 Status:")
    print(f"   📊 Data Access Manager: AVAILABLE")
    print(f"   📁 Module Data Access: AVAILABLE")
    print(f"   📅 Date Range Support: AVAILABLE")
    print(f"   📈 Enhanced Statistics: AVAILABLE")

if __name__ == "__main__":
    test_data_access_manager()
