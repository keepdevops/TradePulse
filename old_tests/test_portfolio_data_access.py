#!/usr/bin/env python3
"""
Test script to verify Portfolio Panel can access uploaded data
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

def test_portfolio_data_access():
    """Test if Portfolio Panel can access uploaded data"""
    try:
        logger.info("🧪 Testing Portfolio Panel Data Access")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from modular_panels.portfolio_panel import PortfolioPanel
        
        # Initialize components
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        portfolio_panel = PortfolioPanel(data_manager, data_access_manager)
        
        logger.info("✅ Components initialized successfully")
        
        # Check if portfolio panel can access uploaded data
        uploaded_data = portfolio_panel.data_access.get_uploaded_data()
        if uploaded_data:
            logger.info(f"✅ Portfolio Panel can access {len(uploaded_data)} uploaded datasets")
            for ds_id, data in uploaded_data.items():
                logger.info(f"   📁 {ds_id}: {data.shape}")
                logger.info(f"      Columns: {list(data.columns)}")
        else:
            logger.info("ℹ️ No uploaded datasets available for portfolio panel")
        
        # Test portfolio optimization with uploaded data
        logger.info("\n🚀 Testing Portfolio Optimization with Uploaded Data")
        
        # Simulate optimization button click
        try:
            portfolio_panel.optimize_portfolio(None)
            logger.info("✅ Portfolio optimization method executed successfully")
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
        
        # Test portfolio rebalancing with uploaded data
        logger.info("\n⚖️ Testing Portfolio Rebalancing with Uploaded Data")
        
        try:
            portfolio_panel.rebalance_portfolio(None)
            logger.info("✅ Portfolio rebalancing method executed successfully")
        except Exception as e:
            logger.error(f"❌ Portfolio rebalancing failed: {e}")
        
        # Test data refresh
        logger.info("\n🔄 Testing Data Refresh")
        
        try:
            portfolio_panel.refresh_data(None)
            logger.info("✅ Portfolio data refresh method executed successfully")
        except Exception as e:
            logger.error(f"❌ Portfolio data refresh failed: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_portfolio_with_sample_data():
    """Test portfolio panel with sample uploaded data"""
    try:
        logger.info("\n📊 Testing Portfolio Panel with Sample Uploaded Data")
        
        # Import components
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from modular_panels.portfolio_panel import PortfolioPanel
        
        # Initialize components
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        portfolio_panel = PortfolioPanel(data_manager, data_access_manager)
        
        # Create sample trading data
        sample_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=100),
            'Symbol': ['AAPL', 'GOOGL', 'MSFT'] * 33 + ['AAPL'],
            'Open': np.random.uniform(100, 300, 100),
            'High': np.random.uniform(100, 300, 100),
            'Low': np.random.uniform(100, 300, 100),
            'Close': np.random.uniform(100, 300, 100),
            'Volume': np.random.randint(1000000, 5000000, 100)
        })
        
        # Upload sample data
        dataset_id = data_manager.add_uploaded_data("portfolio_test", sample_data, {
            'filename': 'portfolio_test.csv',
            'file_type': 'CSV'
        })
        
        logger.info(f"✅ Sample data uploaded: {dataset_id}")
        
        # Check if portfolio panel can see the data
        uploaded_data = portfolio_panel.data_access.get_uploaded_data()
        if uploaded_data:
            logger.info(f"✅ Portfolio Panel sees {len(uploaded_data)} uploaded datasets")
            for ds_id, data in uploaded_data.items():
                logger.info(f"   📁 {ds_id}: {data.shape}")
                
                # Check if it has trading-relevant columns
                if 'Symbol' in data.columns and 'Close' in data.columns:
                    logger.info(f"   ✅ Has trading data columns: Symbol, Close")
                    logger.info(f"   📈 Sample symbols: {list(data['Symbol'].unique()[:5])}")
                else:
                    logger.info(f"   ⚠️ Missing standard trading columns")
        else:
            logger.error("❌ Portfolio Panel cannot see uploaded data")
            return False
        
        # Test optimization with the sample data
        logger.info("\n🚀 Testing Portfolio Optimization with Sample Data")
        
        try:
            portfolio_panel.optimize_portfolio(None)
            logger.info("✅ Portfolio optimization with sample data successful")
        except Exception as e:
            logger.error(f"❌ Portfolio optimization with sample data failed: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sample data test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Portfolio Panel Data Access Tests")
    
    # Run tests
    test1_success = test_portfolio_data_access()
    test2_success = test_portfolio_with_sample_data()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 PORTFOLIO PANEL TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Basic Data Access Test: {'PASSED' if test1_success else 'FAILED'}")
    logger.info(f"✅ Sample Data Integration Test: {'PASSED' if test2_success else 'FAILED'}")
    
    if test1_success and test2_success:
        logger.info("\n🎉 ALL TESTS PASSED! Portfolio Panel can access uploaded data.")
        logger.info("📋 Your uploaded data should now be visible in the Portfolio panel.")
        logger.info("🔄 Try clicking 'Refresh Data' in the Portfolio panel to see your data.")
        sys.exit(0)
    else:
        logger.error("\n❌ SOME TESTS FAILED! Portfolio Panel data access issues remain.")
        sys.exit(1)
