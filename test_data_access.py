#!/usr/bin/env python3
"""
Test Enhanced Data Access
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui_components.data_manager import DataManager
from ui_components.data_access import DataAccessManager

def test_data_access():
    """Test the enhanced data access functionality"""
    print("🧪 Testing Enhanced Data Access")
    print("=" * 50)
    
    # Initialize data manager and data access
    data_manager = DataManager()
    data_access = DataAccessManager(data_manager)
    
    # Test 1: Get available data files
    print("\n📁 Test 1: Available Data Files")
    print("-" * 30)
    available_files = data_access.get_available_data_files()
    
    if available_files:
        total_files = sum(len(files) for files in available_files.values())
        print(f"✅ Found {total_files} data files:")
        for file_type, files in available_files.items():
            if files:
                print(f"   {file_type.upper()}: {len(files)} files")
                for file_path in files[:3]:  # Show first 3 files
                    print(f"     - {file_path}")
                if len(files) > 3:
                    print(f"     - ... and {len(files) - 3} more")
    else:
        print("❌ No data files found")
    
    # Test 2: Try to fetch data from upload source
    print("\n📥 Test 2: Fetch Data from Upload Source")
    print("-" * 30)
    
    test_symbols = ['AAPL', 'GOOGL', 'MSFT']
    for symbol in test_symbols:
        print(f"\n🔍 Testing {symbol}:")
        data = data_access.get_data('upload', symbol, '1d')
        
        if not data.empty:
            print(f"   ✅ Found {len(data)} records")
            print(f"   📊 Columns: {list(data.columns)}")
            if 'Date' in data.columns:
                print(f"   📅 Date range: {data['Date'].min()} to {data['Date'].max()}")
        else:
            print(f"   ❌ No data found for {symbol}")
    
    # Test 3: Test hard drive scanning
    print("\n🔍 Test 3: Hard Drive Scanning")
    print("-" * 30)
    
    data_files = data_access._scan_for_data_files()
    if data_files:
        print(f"✅ Found {len(data_files)} potential data files on hard drive:")
        for file_path in data_files[:5]:  # Show first 5
            print(f"   - {file_path}")
        if len(data_files) > 5:
            print(f"   - ... and {len(data_files) - 5} more")
    else:
        print("❌ No data files found on hard drive")
    
    print("\n✅ Data Access Test Complete!")

if __name__ == "__main__":
    test_data_access()
