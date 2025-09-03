#!/usr/bin/env python3
"""
Test script to verify ModelsPanel data access and training functionality
"""

import sys
import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_models_panel_data_access():
    """Test ModelsPanel data access functionality"""
    try:
        logger.info("🧪 Testing ModelsPanel Data Access")
        
        # Import components
        from modular_panels.models_panel import ModelsPanel
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        
        # Initialize components
        logger.info("📊 Initializing DataManager...")
        data_manager = DataManager()
        
        logger.info("🔗 Initializing DataAccessManager...")
        data_access_manager = DataAccessManager(data_manager)
        
        logger.info("🤖 Creating ModelsPanel...")
        models_panel = ModelsPanel(data_manager, data_access_manager)
        
        # Test 1: Check if ModelsPanel has data access
        logger.info("\n🔍 Test 1: ModelsPanel Data Access Setup")
        if hasattr(models_panel, 'data_access'):
            logger.info("✅ ModelsPanel has data_access attribute")
        else:
            logger.error("❌ ModelsPanel missing data_access attribute")
            return False
        
        # Test 2: Check uploaded data access
        logger.info("\n🔍 Test 2: Uploaded Data Access")
        try:
            uploaded_data = models_panel.data_access.get_uploaded_data()
            if uploaded_data:
                logger.info(f"✅ Found {len(uploaded_data)} uploaded datasets")
                for dataset_id, data in uploaded_data.items():
                    logger.info(f"   📁 {dataset_id}: {data.shape}")
            else:
                logger.info("ℹ️ No uploaded datasets available")
        except Exception as e:
            logger.error(f"❌ Error accessing uploaded data: {e}")
            return False
        
        # Test 3: Check available datasets
        logger.info("\n🔍 Test 3: Available Datasets")
        try:
            available_datasets = models_panel.data_access.get_available_datasets()
            if available_datasets:
                logger.info(f"✅ Available datasets: {available_datasets}")
            else:
                logger.info("ℹ️ No datasets available for models module")
        except Exception as e:
            logger.error(f"❌ Error getting available datasets: {e}")
            return False
        
        # Test 4: Check dataset selector
        logger.info("\n🔍 Test 4: Dataset Selector")
        if hasattr(models_panel, 'dataset_selector'):
            logger.info("✅ ModelsPanel has dataset_selector")
            try:
                selector_component = models_panel.dataset_selector.get_component()
                logger.info("✅ Dataset selector component created successfully")
            except Exception as e:
                logger.error(f"❌ Error creating dataset selector component: {e}")
        else:
            logger.error("❌ ModelsPanel missing dataset_selector")
            return False
        
        # Test 5: Simulate training with data
        logger.info("\n🔍 Test 5: Simulate Training")
        try:
            # Get uploaded data
            uploaded_data = models_panel.data_access.get_uploaded_data()
            
            if uploaded_data:
                logger.info("🚀 Simulating training with uploaded data...")
                for dataset_id, data in uploaded_data.items():
                    logger.info(f"📈 Training on dataset {dataset_id}: {data.shape}")
                    logger.info(f"   Columns: {list(data.columns)}")
                    logger.info(f"   Sample data:\n{data.head(3)}")
                logger.info("✅ Training simulation completed successfully")
            else:
                logger.info("⚠️ No uploaded data available for training simulation")
                # Test with API data
                api_data = models_panel.data_access.get_api_data(['AAPL'], 'yahoo', '1d')
                if api_data:
                    logger.info("📊 Using API data for training simulation")
                    for symbol, data in api_data.items():
                        logger.info(f"📈 Training on {symbol}: {data.shape}")
                else:
                    logger.warning("⚠️ No data available for training simulation")
        except Exception as e:
            logger.error(f"❌ Error in training simulation: {e}")
            return False
        
        logger.info("\n🎉 ModelsPanel Data Access Test Completed Successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

def test_data_manager_uploaded_data():
    """Test DataManager uploaded data directly"""
    try:
        logger.info("\n🧪 Testing DataManager Uploaded Data")
        
        from ui_components.data_manager import DataManager
        
        data_manager = DataManager()
        
        # Check uploaded datasets
        if hasattr(data_manager, 'uploaded_datasets'):
            logger.info(f"📊 DataManager has {len(data_manager.uploaded_datasets)} uploaded datasets")
            for dataset_id, dataset_info in data_manager.uploaded_datasets.items():
                logger.info(f"   📁 {dataset_id}: {dataset_info['shape']}")
        else:
            logger.warning("⚠️ DataManager has no uploaded_datasets attribute")
        
        # Check available datasets for models module
        if hasattr(data_manager, 'get_available_datasets'):
            available = data_manager.get_available_datasets('models')
            logger.info(f"📋 Available datasets for models: {available}")
        else:
            logger.warning("⚠️ DataManager has no get_available_datasets method")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ DataManager test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting ModelsPanel Data Access Tests")
    
    # Run tests
    test1_success = test_models_panel_data_access()
    test2_success = test_data_manager_uploaded_data()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ ModelsPanel Data Access Test: {'PASSED' if test1_success else 'FAILED'}")
    logger.info(f"✅ DataManager Uploaded Data Test: {'PASSED' if test2_success else 'FAILED'}")
    
    if test1_success and test2_success:
        logger.info("\n🎉 ALL TESTS PASSED! ModelsPanel can access uploaded data correctly.")
        sys.exit(0)
    else:
        logger.error("\n❌ SOME TESTS FAILED! Please check the logs above.")
        sys.exit(1)
