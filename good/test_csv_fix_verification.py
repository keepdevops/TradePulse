#!/usr/bin/env python3
"""
Quick test to verify CSV loading fix is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modular_panels.data_upload.text_loaders import TextLoaders

def test_csv_loading():
    """Test CSV loading functionality"""
    print("🧪 Testing CSV loading fix...")
    
    # Create test CSV data
    csv_data = """name,age,city
John,30,New York
Jane,25,Los Angeles
Bob,35,Chicago"""
    
    # Encode to bytes (simulating file upload)
    csv_bytes = csv_data.encode('utf-8')
    
    try:
        # Test the CSV loading
        df = TextLoaders.load_csv_file(csv_bytes)
        
        print(f"✅ CSV loading successful!")
        print(f"📊 Data shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        print(f"📄 First row: {df.iloc[0].to_dict()}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
        return False

if __name__ == "__main__":
    success = test_csv_loading()
    if success:
        print("\n🎉 CSV loading fix is working correctly!")
    else:
        print("\n💥 CSV loading fix verification failed!")
    
    # Clean up
    if os.path.exists(__file__):
        os.unlink(__file__)
