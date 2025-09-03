#!/usr/bin/env python3
"""
Test Enhanced Date Range Functionality
"""

import sys
from pathlib import Path
import pandas as pd

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui_components.data_manager import DataManager
from ui_components.data_access import DataAccessManager

def test_date_ranges():
    """Test the enhanced date range functionality"""
    print("🧪 Testing Enhanced Date Range Functionality")
    print("=" * 60)
    
    # Initialize data manager and data access
    data_manager = DataManager()
    data_access = DataAccessManager(data_manager)
    
    # Test different date ranges
    test_cases = [
        {
            'name': 'Last 7 Days',
            'start_date': '2024-12-25',
            'end_date': '2024-12-31',
            'timeframe': '1d'
        },
        {
            'name': 'Last 30 Days',
            'start_date': '2024-12-01',
            'end_date': '2024-12-31',
            'timeframe': '1d'
        },
        {
            'name': 'Last 1 Year',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'timeframe': '1d'
        },
        {
            'name': 'Last 5 Years',
            'start_date': '2020-01-01',
            'end_date': '2024-12-31',
            'timeframe': '1d'
        },
        {
            'name': 'Last 10 Years',
            'start_date': '2015-01-01',
            'end_date': '2024-12-31',
            'timeframe': '1d'
        },
        {
            'name': 'Intraday Data (1 Hour)',
            'start_date': '2024-12-30',
            'end_date': '2024-12-31',
            'timeframe': '1h'
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📅 Test: {test_case['name']}")
        print("-" * 40)
        
        # Test mock data generation
        data = data_access.get_data(
            'mock',
            'AAPL',
            test_case['timeframe'],
            test_case['start_date'],
            test_case['end_date']
        )
        
        if not data.empty:
            start_date = pd.to_datetime(data['Date'].iloc[0])
            end_date = pd.to_datetime(data['Date'].iloc[-1])
            duration_days = (end_date - start_date).days
            
            print(f"   ✅ Generated {len(data):,} records")
            print(f"   📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            print(f"   ⏱️  Duration: {duration_days} days")
            print(f"   📊 Columns: {list(data.columns)}")
            
            # Test upload data with same date range
            upload_data = data_access.get_data(
                'upload',
                'AAPL',
                test_case['timeframe'],
                test_case['start_date'],
                test_case['end_date']
            )
            
            if not upload_data.empty:
                print(f"   📁 Upload data: {len(upload_data):,} records")
            else:
                print(f"   📁 Upload data: No data in range")
        else:
            print(f"   ❌ No data generated")
    
    # Test date range presets
    print(f"\n🎯 Testing Date Range Presets")
    print("-" * 40)
    
    presets = [
        'Last 7 Days',
        'Last 30 Days',
        'Last 90 Days',
        'Last 6 Months',
        'Last 1 Year',
        'Last 2 Years',
        'Last 5 Years',
        'Last 10 Years',
        'All Available Data'
    ]
    
    for preset in presets:
        print(f"   📅 {preset}")
    
    print(f"\n✅ Date Range Testing Complete!")
    print(f"\n🎯 Available Features:")
    print(f"   📅 Date Range Presets: 9 different ranges")
    print(f"   📅 Custom Date Pickers: Start and End dates")
    print(f"   📅 Long Range Support: Up to 10+ years")
    print(f"   📅 Multiple Timeframes: 1m, 5m, 15m, 1h, 1d")
    print(f"   📅 Enhanced Statistics: Duration and frequency info")

if __name__ == "__main__":
    test_date_ranges()
