#!/usr/bin/env python3
"""
Debug script to check the data structure returned by uploaded_data
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

def debug_data_structure():
    """Debug the structure of uploaded data"""
    try:
        logger.info("🔍 Debugging Data Structure")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from ui_components.module_data_access import ModuleDataAccess
        
        # Initialize components
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        module_data_access = ModuleDataAccess(data_manager, data_access_manager, 'models')
        
        # Add test data
        sample_data = pd.DataFrame({
            'Symbol': ['TEST'],
            'Price': [100.0]
        })
        
        dataset_id = data_manager.add_uploaded_data("debug_test", sample_data, {
            'filename': 'debug.csv',
            'file_type': 'CSV'
        })
        
        logger.info(f"✅ Added dataset: {dataset_id}")
        
        # Check data structure
        uploaded_data = module_data_access.get_uploaded_data()
        logger.info(f"📊 Uploaded data type: {type(uploaded_data)}")
        logger.info(f"📊 Uploaded data keys: {list(uploaded_data.keys()) if uploaded_data else 'None'}")
        
        if uploaded_data:
            for ds_id, data in uploaded_data.items():
                logger.info(f"📁 Dataset {ds_id}:")
                logger.info(f"   Type: {type(data)}")
                
                if isinstance(data, pd.DataFrame):
                    logger.info(f"   Shape: {data.shape}")
                    logger.info(f"   Columns: {list(data.columns)}")
                elif isinstance(data, dict):
                    logger.info(f"   Dict keys: {list(data.keys())}")
                    if 'data' in data:
                        logger.info(f"   Data type: {type(data['data'])}")
                        logger.info(f"   Data shape: {data['data'].shape}")
                else:
                    logger.info(f"   Unknown structure: {data}")
        
        # Check global store directly
        global_store = data_manager.global_store
        logger.info(f"\n🌐 Global Store Debug:")
        logger.info(f"   Store type: {type(global_store)}")
        logger.info(f"   Store datasets: {len(global_store.uploaded_datasets)}")
        
        for ds_id, data in global_store.uploaded_datasets.items():
            logger.info(f"   Global dataset {ds_id}: {type(data)} {data.shape if hasattr(data, 'shape') else 'no shape'}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_data_structure()
