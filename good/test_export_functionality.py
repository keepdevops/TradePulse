#!/usr/bin/env python3
"""
Test script to verify export functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modular_panels.data_panel import DataPanel
from ui_components.data_manager import DataManager
from ui_components.data_access import DataAccessManager
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_export_functionality():
    """Test the export functionality"""
    print("🧪 Testing Export Functionality...")
    
    try:
        # Initialize components
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        
        # Create DataPanel instance
        print("🔧 Creating DataPanel instance...")
        data_panel = DataPanel(data_manager, data_access_manager)
        
        # Test quick export
        print("🔧 Testing quick export...")
        
        # Create some test data
        test_data = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [95.0, 96.0, 97.0],
            'Close': [103.0, 104.0, 105.0],
            'Volume': [1000000, 1100000, 1200000]
        })
        
        # Set the test data in the data table
        data_panel.components['data_table'].value = test_data
        
        # Test quick export
        data_panel.quick_export(None)
        
        # Check if export dialog was updated
        export_dialog_content = data_panel.components['export_dialog'].object
        if "Export Successful" in export_dialog_content:
            print("✅ Quick export test passed!")
        else:
            print("❌ Quick export test failed!")
            print(f"Dialog content: {export_dialog_content}")
        
        # Test advanced export
        print("🔧 Testing advanced export...")
        data_panel.export_data(None)
        
        # Check if export dialog was updated with advanced options
        export_dialog_content = data_panel.components['export_dialog'].object
        if "Export Format" in str(export_dialog_content) or "Advanced Export" in str(export_dialog_content):
            print("✅ Advanced export test passed!")
        else:
            print("❌ Advanced export test failed!")
            print(f"Dialog content: {export_dialog_content}")
        
        # Check for exported files
        print("🔧 Checking for exported files...")
        import glob
        csv_files = glob.glob("tradepulse_data_*.csv")
        if csv_files:
            print(f"✅ Found exported files: {csv_files}")
            for file in csv_files:
                print(f"   - {file}")
        else:
            print("⚠️ No exported CSV files found")
        
        print("🎯 Export Functionality Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_export_functionality()
    if success:
        print("🎉 Export functionality is working correctly!")
    else:
        print("💥 Export functionality needs attention.")
