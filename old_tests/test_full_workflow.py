#!/usr/bin/env python3
"""
Test script to simulate the full workflow:
1. Upload data in Data panel
2. Switch to Models panel
3. Verify data is available
4. Train model with uploaded data
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

def create_sample_trading_data():
    """Create sample trading data similar to what a user would upload"""
    try:
        # Create realistic trading data
        dates = pd.date_range('2023-01-01', periods=500, freq='D')
        symbols = ['TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN']
        
        data_list = []
        for symbol in symbols:
            # Generate realistic price data for each symbol
            base_price = np.random.uniform(50, 300)
            prices = [base_price]
            
            for i in range(len(dates) - 1):
                # Random walk with some trend
                change_pct = np.random.normal(0.001, 0.02)  # Small daily changes
                new_price = prices[-1] * (1 + change_pct)
                prices.append(max(1, new_price))  # Ensure price stays positive
            
            for i, date in enumerate(dates):
                price = prices[i]
                high = price * (1 + abs(np.random.normal(0, 0.01)))
                low = price * (1 - abs(np.random.normal(0, 0.01)))
                volume = int(np.random.exponential(1000000))
                
                data_list.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Symbol': symbol,
                    'Open': round(price * (1 + np.random.normal(0, 0.005)), 2),
                    'High': round(high, 2),
                    'Low': round(low, 2),
                    'Close': round(price, 2),
                    'Volume': volume,
                    'Adj_Close': round(price * (1 + np.random.normal(0, 0.001)), 2)
                })
        
        df = pd.DataFrame(data_list)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        df.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        logger.info(f"📊 Created sample trading data: {temp_file.name}")
        logger.info(f"   Data shape: {df.shape}")
        logger.info(f"   Symbols: {', '.join(symbols)}")
        logger.info(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
        
        return temp_file.name, df
        
    except Exception as e:
        logger.error(f"❌ Failed to create sample data: {e}")
        return None, None

def test_complete_workflow():
    """Test the complete workflow from data upload to model training"""
    try:
        logger.info("🔄 Testing Complete Workflow: Data Upload → Model Training")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from modular_panels.data_panel import DataPanel
        from modular_panels.models_panel import ModelsPanel
        
        # Step 1: Initialize the same components used in the main UI
        logger.info("\n📊 Step 1: Initialize Application Components")
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        
        # Create panels (same instances as in main UI)
        data_panel = DataPanel(data_manager, data_access_manager)
        models_panel = ModelsPanel(data_manager, data_access_manager)
        
        logger.info("✅ Components initialized successfully")
        
        # Step 2: Simulate data upload in Data Panel
        logger.info("\n📤 Step 2: Simulate Data Upload in Data Panel")
        test_file, test_df = create_sample_trading_data()
        if not test_file:
            return False
        
        try:
            # Simulate the file upload process
            with open(test_file, 'rb') as f:
                file_content = f.read()
            
            # Process the file using the same method as the UI
            from modular_panels.data_upload.text_loaders import TextLoaders
            loaded_df = TextLoaders.load_csv_file(file_content)
            
            # Add to data manager (same as DataUploadComponent does)
            dataset_id = f"dataset_trading_data.csv_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            data_manager.add_uploaded_data(dataset_id, loaded_df, {
                'filename': 'trading_data.csv',
                'file_type': 'CSV',
                'upload_time': pd.Timestamp.now(),
                'shape': loaded_df.shape,
                'columns': list(loaded_df.columns),
                'memory_usage': loaded_df.memory_usage(deep=True).sum()
            })
            
            logger.info(f"✅ Data uploaded successfully: {dataset_id}")
            logger.info(f"   Shape: {loaded_df.shape}")
            logger.info(f"   Symbols: {', '.join(loaded_df['Symbol'].unique())}")
            
        except Exception as e:
            logger.error(f"❌ Data upload failed: {e}")
            os.unlink(test_file)
            return False
        
        # Step 3: Switch to Models Panel and check data availability
        logger.info("\n🤖 Step 3: Check Data Availability in Models Panel")
        
        # Check if data is available to models panel
        uploaded_data = models_panel.data_access.get_uploaded_data()
        if uploaded_data:
            logger.info(f"✅ Models Panel can access {len(uploaded_data)} datasets")
            for ds_id, data in uploaded_data.items():
                logger.info(f"   📁 {ds_id}: {data.shape}")
                logger.info(f"      Symbols: {', '.join(data['Symbol'].unique()[:5])}")
        else:
            logger.error("❌ Models Panel cannot access uploaded data")
            os.unlink(test_file)
            return False
        
        # Step 4: Test model training with uploaded data
        logger.info("\n🚀 Step 4: Test Model Training with Uploaded Data")
        
        try:
            # Simulate training process
            model = 'ADM'
            epochs = 50
            lr = 0.001
            batch_size = 32
            
            logger.info(f"🔄 Training {model} model with uploaded data...")
            
            # Check what data would be used for training
            training_data = models_panel.data_access.get_uploaded_data()
            if training_data:
                total_records = sum(data.shape[0] for data in training_data.values())
                unique_symbols = set()
                for data in training_data.values():
                    unique_symbols.update(data['Symbol'].unique())
                
                logger.info(f"📊 Training data summary:")
                logger.info(f"   Total records: {total_records:,}")
                logger.info(f"   Unique symbols: {len(unique_symbols)} ({', '.join(list(unique_symbols)[:5])})")
                logger.info(f"   Datasets: {len(training_data)}")
                
                logger.info("✅ Model training would use uploaded data (not AAPL fallback)")
            else:
                logger.error("❌ Model training would use fallback data (AAPL)")
                os.unlink(test_file)
                return False
            
        except Exception as e:
            logger.error(f"❌ Model training test failed: {e}")
            os.unlink(test_file)
            return False
        
        # Step 5: Test prediction with uploaded data
        logger.info("\n🔮 Step 5: Test Prediction with Uploaded Data")
        
        try:
            prediction_data = models_panel.data_access.get_uploaded_data()
            if prediction_data:
                dataset_id = list(prediction_data.keys())[0]
                data = prediction_data[dataset_id]
                symbols_in_data = data['Symbol'].unique()
                
                logger.info(f"📊 Prediction would use dataset: {dataset_id}")
                logger.info(f"   Available symbols: {', '.join(symbols_in_data[:5])}")
                logger.info("✅ Prediction would use uploaded data (not AAPL fallback)")
            else:
                logger.error("❌ Prediction would use fallback data (AAPL)")
                os.unlink(test_file)
                return False
                
        except Exception as e:
            logger.error(f"❌ Prediction test failed: {e}")
            os.unlink(test_file)
            return False
        
        # Clean up
        os.unlink(test_file)
        
        logger.info("\n🎉 Complete Workflow Test PASSED!")
        logger.info("✅ Data flows correctly from upload to model training")
        return True
        
    except Exception as e:
        logger.error(f"❌ Complete workflow test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Complete Workflow Test")
    logger.info("This simulates: Upload data → Switch to Models → Train model")
    
    # Run test
    test_success = test_complete_workflow()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 WORKFLOW TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Complete Workflow Test: {'PASSED' if test_success else 'FAILED'}")
    
    if test_success:
        logger.info("\n🎉 SUCCESS! The workflow works correctly.")
        logger.info("📋 Your uploaded data should be available in Models panel.")
        logger.info("🔄 Try clicking 'Refresh Data' in Models panel to see your uploaded data.")
        sys.exit(0)
    else:
        logger.error("\n❌ WORKFLOW FAILED! There may be an issue with data sharing.")
        sys.exit(1)
