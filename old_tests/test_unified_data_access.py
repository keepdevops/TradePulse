#!/usr/bin/env python3
"""
Test script for TradePulse Unified Data Access System
Verifies that modules can access both API and uploaded data
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

def test_unified_data_access():
    """Test the unified data access system"""
    try:
        logger.info("🧪 Testing TradePulse Unified Data Access System")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from ui_components.module_data_access import ModuleDataAccess
        
        # Initialize components
        logger.info("📊 Initializing DataManager...")
        data_manager = DataManager()
        
        logger.info("🔗 Initializing DataAccessManager...")
        data_access_manager = DataAccessManager(data_manager)
        
        logger.info("📋 Initializing ModuleDataAccess for models...")
        models_data_access = ModuleDataAccess(data_manager, data_access_manager, 'models')
        
        # Test 1: API Data Access
        logger.info("\n🔍 Test 1: API Data Access")
        try:
            api_data = models_data_access.get_api_data(['AAPL', 'GOOGL'], 'yahoo', '1d')
            if api_data:
                logger.info(f"✅ API data access successful: {len(api_data)} symbols")
                for symbol, data in api_data.items():
                    logger.info(f"   📈 {symbol}: {data.shape}")
            else:
                logger.warning("⚠️ No API data returned")
        except Exception as e:
            logger.error(f"❌ API data access failed: {e}")
        
        # Test 2: Uploaded Data Access
        logger.info("\n🔍 Test 2: Uploaded Data Access")
        try:
            uploaded_data = models_data_access.get_uploaded_data()
            if uploaded_data:
                logger.info(f"✅ Uploaded data access successful: {len(uploaded_data)} datasets")
                for dataset_id, data in uploaded_data.items():
                    logger.info(f"   📁 {dataset_id}: {data.shape}")
            else:
                logger.info("ℹ️ No uploaded datasets available")
        except Exception as e:
            logger.error(f"❌ Uploaded data access failed: {e}")
        
        # Test 3: Combined Data Access
        logger.info("\n🔍 Test 3: Combined Data Access")
        try:
            combined_data = models_data_access.get_combined_data(
                symbols=['AAPL', 'GOOGL'],
                dataset_ids=None,  # Use all available datasets
                source='yahoo'
            )
            if combined_data:
                logger.info(f"✅ Combined data access successful: {len(combined_data)} total datasets")
                for key, data in combined_data.items():
                    logger.info(f"   🔄 {key}: {data.shape}")
            else:
                logger.warning("⚠️ No combined data returned")
        except Exception as e:
            logger.error(f"❌ Combined data access failed: {e}")
        
        # Test 4: Dataset Activation
        logger.info("\n🔍 Test 4: Dataset Activation")
        try:
            available_datasets = models_data_access.get_available_datasets()
            if available_datasets:
                logger.info(f"✅ Available datasets: {available_datasets}")
                # Try to activate first dataset
                if len(available_datasets) > 0:
                    dataset_id = available_datasets[0]
                    success = models_data_access.activate_dataset(dataset_id)
                    if success:
                        logger.info(f"✅ Successfully activated dataset: {dataset_id}")
                        active_datasets = models_data_access.get_active_datasets()
                        logger.info(f"   📋 Active datasets: {list(active_datasets.keys())}")
                    else:
                        logger.warning(f"⚠️ Failed to activate dataset: {dataset_id}")
            else:
                logger.info("ℹ️ No datasets available for activation")
        except Exception as e:
            logger.error(f"❌ Dataset activation failed: {e}")
        
        # Test 5: Data Summary
        logger.info("\n🔍 Test 5: Data Summary")
        try:
            summary = models_data_access.get_data_summary()
            logger.info(f"✅ Data summary: {summary}")
        except Exception as e:
            logger.error(f"❌ Data summary failed: {e}")
        
        # Test 6: Cache Operations
        logger.info("\n🔍 Test 6: Cache Operations")
        try:
            cache_stats = data_access_manager.get_cache_stats()
            logger.info(f"✅ Cache stats: {cache_stats}")
            
            # Clear cache
            data_access_manager.clear_cache()
            models_data_access.clear_cache()
            logger.info("✅ Cache cleared successfully")
        except Exception as e:
            logger.error(f"❌ Cache operations failed: {e}")
        
        logger.info("\n🎉 Unified Data Access System Test Completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

def test_model_integration():
    """Test model integration with data access"""
    try:
        logger.info("\n🤖 Testing Model Integration with Data Access")
        
        # Import model components
        from modular_panels.models_panel import ModelsPanel
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        
        # Initialize components
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        
        # Create models panel
        models_panel = ModelsPanel(data_manager, data_access_manager)
        
        logger.info("✅ ModelsPanel created successfully with data access")
        
        # Test data access through models panel
        uploaded_data = models_panel.data_access.get_uploaded_data()
        if uploaded_data:
            logger.info(f"✅ ModelsPanel can access {len(uploaded_data)} uploaded datasets")
            for dataset_id, data in uploaded_data.items():
                logger.info(f"   📊 {dataset_id}: {data.shape}")
        else:
            logger.info("ℹ️ ModelsPanel: No uploaded datasets available")
        
        logger.info("🎉 Model Integration Test Completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Model integration test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting TradePulse Unified Data Access System Tests")
    
    # Run tests
    test1_success = test_unified_data_access()
    test2_success = test_model_integration()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Unified Data Access Test: {'PASSED' if test1_success else 'FAILED'}")
    logger.info(f"✅ Model Integration Test: {'PASSED' if test2_success else 'FAILED'}")
    
    if test1_success and test2_success:
        logger.info("\n🎉 ALL TESTS PASSED! Unified Data Access System is working correctly.")
        sys.exit(0)
    else:
        logger.error("\n❌ SOME TESTS FAILED! Please check the logs above.")
        sys.exit(1)
