#!/usr/bin/env python3
"""
TradePulse Upload Data Utility
Upload data from M3 hard drive to TradePulse
"""

import sys
import os
import logging
from pathlib import Path
from api.fastapi_client import TradePulseAPIClientSync

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function for uploading data"""
    try:
        logger.info("🚀 TradePulse Upload Data Utility")
        
        # Initialize API client
        client = TradePulseAPIClientSync()
        
        # Check server health
        try:
            health = client.health_check()
            logger.info(f"✅ API Server Health: {health['status']}")
        except Exception as e:
            logger.error(f"❌ Cannot connect to API server: {e}")
            logger.info("💡 Make sure the FastAPI server is running: python launch_fastapi_server.py")
            return
        
        # Scan M3 drive for upload data
        logger.info("🔍 Scanning M3 hard drive for upload data...")
        
        # Common M3 drive paths
        m3_paths = [
            "/Volumes",
            "/Users/moose/Desktop",
            "/Users/moose/Documents",
            "/Users/moose/Downloads"
        ]
        
        found_files = {}
        
        for path in m3_paths:
            if os.path.exists(path):
                try:
                    scan_result = client.scan_m3_drive(path)
                    if scan_result.get("total_files", 0) > 0:
                        found_files[path] = scan_result["found_files"]
                        logger.info(f"📁 Found {scan_result['total_files']} files in {path}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not scan {path}: {e}")
        
        if not found_files:
            logger.warning("⚠️ No data files found in common M3 locations")
            logger.info("💡 Try specifying a custom path or check file permissions")
            return
        
        # Display found files
        logger.info("\n📋 Found data files:")
        for path, file_types in found_files.items():
            logger.info(f"\n📍 Location: {path}")
            for file_type, files in file_types.items():
                logger.info(f"  📄 {file_type.upper()}: {len(files)} files")
                for file_info in files[:5]:  # Show first 5 files
                    logger.info(f"    - {file_info['filename']} ({file_info['size']} bytes)")
                if len(files) > 5:
                    logger.info(f"    ... and {len(files) - 5} more files")
        
        # Interactive file selection
        logger.info("\n🎯 Select files to import:")
        logger.info("1. Enter file path to import specific file")
        logger.info("2. Enter 'scan' to scan a different path")
        logger.info("3. Enter 'quit' to exit")
        
        while True:
            try:
                user_input = input("\nEnter file path or command: ").strip()
                
                if user_input.lower() == 'quit':
                    logger.info("👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'scan':
                    custom_path = input("Enter path to scan: ").strip()
                    if os.path.exists(custom_path):
                        scan_result = client.scan_m3_drive(custom_path)
                        logger.info(f"📁 Found {scan_result['total_files']} files in {custom_path}")
                    else:
                        logger.error(f"❌ Path not found: {custom_path}")
                
                elif os.path.exists(user_input):
                    # Import the file
                    logger.info(f"📥 Importing file: {user_input}")
                    
                    # Determine file type
                    file_ext = Path(user_input).suffix.lower()
                    if file_ext in ['.csv', '.json', '.feather', '.parquet', '.duckdb', '.h5', '.xlsx']:
                        file_type = "upload"
                    else:
                        file_type = "data"
                    
                    # Import file
                    result = client.import_from_m3_drive(user_input, file_type)
                    logger.info(f"✅ Successfully imported: {result['filename']}")
                    logger.info(f"   File ID: {result['file_id']}")
                    logger.info(f"   Imported to: {result['imported_path']}")
                
                else:
                    logger.error(f"❌ File not found: {user_input}")
            
            except KeyboardInterrupt:
                logger.info("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
