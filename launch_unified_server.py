#!/usr/bin/env python3
"""
TradePulse Unified Server Launcher
Launches the unified FastAPI + Panel server
"""

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
    """Launch the unified server"""
    try:
        logger.info("🚀 TradePulse Unified Server Launcher")
        logger.info("=" * 50)
        
        # Import and run the advanced integration
        from fastapi_panel_advanced_integration import app
        
        import uvicorn
        
        logger.info("✅ Server components loaded successfully")
        logger.info("")
        logger.info("🎯 Available endpoints:")
        logger.info("   📊 Panel UI: http://localhost:8000")
        logger.info("   📡 API Base: http://localhost:8000/api")
        logger.info("   📚 API Docs: http://localhost:8000/api/docs")
        logger.info("   🔍 Health Check: http://localhost:8000/health")
        logger.info("   📋 Status: http://localhost:8000/status")
        logger.info("")
        logger.info("🚀 Starting server...")
        
        uvicorn.run(
            "fastapi_panel_advanced_integration:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 Make sure all dependencies are installed:")
        logger.error("   pip install fastapi uvicorn panel aiohttp python-multipart")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
