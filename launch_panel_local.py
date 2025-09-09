#!/usr/bin/env python3
"""
TradePulse Panel Local Launcher
Runs Panel UI locally while connecting to FastAPI server in Docker
"""

import panel as pn
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Launch Panel UI locally"""
    try:
        logger.info("🚀 TradePulse Panel Local Launcher")
        logger.info("=" * 50)
        
        # Import Panel components
        from modular_panel_ui_main_refactored import create_refactored_modular_ui
        
        # Create Panel app
        logger.info("🔧 Creating Panel application...")
        panel_app = create_refactored_modular_ui()
        
        logger.info("✅ Panel application created successfully")
        logger.info("")
        logger.info("🎯 Available endpoints:")
        logger.info("   📊 Panel UI: http://localhost:5006")
        logger.info("   📡 FastAPI Server: http://localhost:8000")
        logger.info("   📚 API Documentation: http://localhost:8000/docs")
        logger.info("   🔍 Health Check: http://localhost:8000/health")
        logger.info("")
        logger.info("💡 Make sure the FastAPI server is running in Docker:")
        logger.info("   docker-compose -f docker-compose.api-only.yml up -d")
        logger.info("")
        logger.info("🚀 Starting Panel server...")
        
        # Start Panel server
        panel_app.show(
            port=5006,
            host="0.0.0.0",
            title="TradePulse - Panel UI"
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 Make sure all dependencies are installed:")
        logger.error("   pip install panel bokeh param")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Failed to start Panel server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
