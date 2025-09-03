#!/usr/bin/env python3
"""
Test script to verify data persistence between modules
"""

import sys
import os
import pandas as pd
import numpy as np
import logging
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_data_persistence_issue():
    """Test to demonstrate the data persistence issue"""
    try:
        logger.info("🔍 Testing Data Persistence Issue")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from modular_panels.data_panel import DataPanel
        from modular_panels.models_panel import ModelsPanel
        
        # Scenario 1: Fresh app start (like when the web app starts)
        logger.info("\n📊 Scenario 1: Fresh Application Start")
        data_manager1 = DataManager()
        data_access_manager1 = DataAccessManager(data_manager1)
        
        data_panel1 = DataPanel(data_manager1, data_access_manager1)
        models_panel1 = ModelsPanel(data_manager1, data_access_manager1)
        
        # Check initial state
        uploaded_data1 = models_panel1.data_access.get_uploaded_data()
        logger.info(f"Initial state - Models panel datasets: {len(uploaded_data1)}")
        
        # Scenario 2: User uploads data
        logger.info("\n📤 Scenario 2: User Uploads Data")
        
        # Create sample data
        sample_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=100),
            'Symbol': ['TEST'] * 100,
            'Open': np.random.uniform(100, 150, 100),
            'High': np.random.uniform(100, 150, 100),
            'Low': np.random.uniform(100, 150, 100),
            'Close': np.random.uniform(100, 150, 100),
            'Volume': np.random.randint(1000000, 5000000, 100)
        })
        
        # Simulate upload process
        dataset_id = f"dataset_test_upload_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        data_manager1.add_uploaded_data(dataset_id, sample_data, {
            'filename': 'test_upload.csv',
            'file_type': 'CSV',
            'upload_time': pd.Timestamp.now(),
            'shape': sample_data.shape,
            'columns': list(sample_data.columns),
            'memory_usage': sample_data.memory_usage(deep=True).sum()
        })
        
        logger.info(f"✅ Data uploaded: {dataset_id}")
        
        # Check if data is immediately available
        uploaded_data2 = models_panel1.data_access.get_uploaded_data()
        logger.info(f"After upload - Models panel datasets: {len(uploaded_data2)}")
        
        if uploaded_data2:
            logger.info("✅ Data is immediately available to models panel")
        else:
            logger.error("❌ Data is NOT available to models panel")
            return False
        
        # Scenario 3: User switches tabs (simulated by creating new panel instances)
        logger.info("\n🔄 Scenario 3: User Switches Tabs (New Panel Instances)")
        
        # This simulates what happens when Panel creates new instances
        models_panel2 = ModelsPanel(data_manager1, data_access_manager1)
        uploaded_data3 = models_panel2.data_access.get_uploaded_data()
        logger.info(f"New models panel instance - datasets: {len(uploaded_data3)}")
        
        if uploaded_data3:
            logger.info("✅ Data persists across panel instances")
        else:
            logger.error("❌ Data does NOT persist across panel instances")
            return False
        
        # Scenario 4: Different DataManager instances (the real problem)
        logger.info("\n⚠️ Scenario 4: Different DataManager Instances (Real Problem)")
        
        # This simulates what might be happening in the web app
        data_manager2 = DataManager()  # New instance!
        data_access_manager2 = DataAccessManager(data_manager2)
        models_panel3 = ModelsPanel(data_manager2, data_access_manager2)
        
        uploaded_data4 = models_panel3.data_access.get_uploaded_data()
        logger.info(f"Different DataManager instance - datasets: {len(uploaded_data4)}")
        
        if uploaded_data4:
            logger.info("✅ Data persists across DataManager instances")
        else:
            logger.error("❌ Data does NOT persist across DataManager instances")
            logger.error("🔍 This is likely the root cause of the issue!")
            return False
        
        logger.info("\n🎉 All persistence tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Persistence test failed: {e}")
        return False

def test_singleton_solution():
    """Test a singleton-based solution for data persistence"""
    try:
        logger.info("\n🔧 Testing Singleton Solution")
        
        # Import components
        from ui_components.data_manager import DataManager
        
        # Check if multiple DataManager instances share data
        logger.info("📊 Creating multiple DataManager instances...")
        
        dm1 = DataManager()
        dm2 = DataManager()
        
        # Add data to first instance
        sample_data = pd.DataFrame({
            'Symbol': ['AAPL', 'GOOGL'],
            'Price': [150.0, 2500.0]
        })
        
        dataset_id = "test_singleton_data"
        dm1.add_uploaded_data(dataset_id, sample_data, {
            'filename': 'test.csv',
            'file_type': 'CSV',
            'upload_time': pd.Timestamp.now()
        })
        
        logger.info(f"✅ Added data to first DataManager: {dataset_id}")
        
        # Check if second instance can see the data
        if hasattr(dm2, 'uploaded_datasets'):
            datasets_dm2 = len(dm2.uploaded_datasets)
            logger.info(f"Second DataManager sees {datasets_dm2} datasets")
            
            # Look for the actual dataset ID (it will have a timestamp suffix)
            found_data = False
            for ds_id in dm2.uploaded_datasets.keys():
                if 'test_singleton_data' in ds_id:
                    found_data = True
                    logger.info(f"✅ Found shared dataset: {ds_id}")
                    break
            
            if found_data:
                logger.info("✅ Singleton pattern working - data shared across instances")
                return True
            else:
                logger.error("❌ Singleton pattern not working - data not shared")
                return False
        else:
            logger.error("❌ DataManager missing uploaded_datasets attribute")
            return False
        
    except Exception as e:
        logger.error(f"❌ Singleton test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Data Persistence Tests")
    logger.info("This will help identify why uploaded data isn't available across modules")
    
    # Run tests
    test1_success = test_data_persistence_issue()
    test2_success = test_singleton_solution()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 DATA PERSISTENCE TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Basic Persistence Test: {'PASSED' if test1_success else 'FAILED'}")
    logger.info(f"✅ Singleton Solution Test: {'PASSED' if test2_success else 'FAILED'}")
    
    if test1_success and test2_success:
        logger.info("\n🎉 ALL TESTS PASSED! Data persistence is working correctly.")
        logger.info("The issue may be in the web UI implementation.")
    else:
        logger.error("\n❌ TESTS FAILED! Data persistence issue confirmed.")
        logger.info("💡 SOLUTION: Need to implement proper data sharing mechanism.")
    
    sys.exit(0 if test1_success and test2_success else 1)
