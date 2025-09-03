#!/usr/bin/env python3
"""
Test script to check if the running application has uploaded data
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

def create_test_data():
    """Create test CSV data for upload simulation"""
    try:
        # Create sample financial data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Date': dates,
            'Symbol': ['TEST'] * 100,
            'Open': np.random.uniform(100, 150, 100),
            'High': np.random.uniform(100, 150, 100),
            'Low': np.random.uniform(100, 150, 100),
            'Close': np.random.uniform(100, 150, 100),
            'Volume': np.random.randint(1000000, 5000000, 100)
        }
        
        df = pd.DataFrame(data)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        df.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        logger.info(f"📊 Created test data file: {temp_file.name}")
        logger.info(f"   Data shape: {df.shape}")
        logger.info(f"   Columns: {list(df.columns)}")
        
        return temp_file.name, df
        
    except Exception as e:
        logger.error(f"❌ Failed to create test data: {e}")
        return None, None

def test_data_upload_simulation():
    """Simulate data upload and test if it's accessible"""
    try:
        logger.info("🧪 Testing Data Upload Simulation")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from modular_panels.data_upload_component import DataUploadComponent
        
        # Initialize components
        logger.info("📊 Initializing DataManager...")
        data_manager = DataManager()
        
        logger.info("📤 Creating DataUploadComponent...")
        upload_component = DataUploadComponent(data_manager)
        
        logger.info("🔗 Initializing DataAccessManager...")
        data_access_manager = DataAccessManager(data_manager)
        
        # Create test data
        test_file, test_df = create_test_data()
        if not test_file:
            return False
        
        try:
            # Read test file content
            with open(test_file, 'rb') as f:
                file_content = f.read()
            
            logger.info(f"📁 Simulating file upload: {os.path.basename(test_file)}")
            
            # Simulate file upload process
            from modular_panels.data_upload.text_loaders import TextLoaders
            
            # Load the CSV data
            loaded_df = TextLoaders.load_csv_file(file_content)
            logger.info(f"✅ CSV loaded successfully: {loaded_df.shape}")
            
            # Add to data manager
            dataset_id = f"dataset_test_data.csv_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            data_manager.add_uploaded_data(dataset_id, loaded_df, {
                'filename': 'test_data.csv',
                'file_type': 'CSV',
                'upload_time': pd.Timestamp.now(),
                'shape': loaded_df.shape,
                'columns': list(loaded_df.columns),
                'memory_usage': loaded_df.memory_usage(deep=True).sum()
            })
            
            logger.info(f"📊 Added to DataManager with ID: {dataset_id}")
            
            # Check if data is accessible
            uploaded_data = data_access_manager.get_uploaded_data()
            if uploaded_data:
                logger.info(f"✅ Data accessible via DataAccessManager: {len(uploaded_data)} datasets")
                for ds_id, data in uploaded_data.items():
                    logger.info(f"   📁 {ds_id}: {data.shape}")
            else:
                logger.error("❌ Data not accessible via DataAccessManager")
                return False
            
            # Test ModelsPanel access
            from modular_panels.models_panel import ModelsPanel
            models_panel = ModelsPanel(data_manager, data_access_manager)
            
            models_uploaded_data = models_panel.data_access.get_uploaded_data()
            if models_uploaded_data:
                logger.info(f"✅ Data accessible via ModelsPanel: {len(models_uploaded_data)} datasets")
                for ds_id, data in models_uploaded_data.items():
                    logger.info(f"   📁 {ds_id}: {data.shape}")
                    logger.info(f"   Columns: {list(data.columns)}")
            else:
                logger.error("❌ Data not accessible via ModelsPanel")
                return False
            
            # Clean up
            os.unlink(test_file)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error in upload simulation: {e}")
            # Clean up
            if os.path.exists(test_file):
                os.unlink(test_file)
            return False
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Data Upload Simulation Test")
    
    # Run test
    test_success = test_data_upload_simulation()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Data Upload Simulation Test: {'PASSED' if test_success else 'FAILED'}")
    
    if test_success:
        logger.info("\n🎉 TEST PASSED! Data upload and access working correctly.")
        logger.info("🔍 The issue may be with data persistence between application instances.")
        sys.exit(0)
    else:
        logger.error("\n❌ TEST FAILED! Data upload or access not working correctly.")
        sys.exit(1)
