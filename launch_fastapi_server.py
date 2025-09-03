#!/usr/bin/env python3
"""
TradePulse FastAPI Server Launcher
Simple launcher for the FastAPI server
"""

import uvicorn
import logging
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Launch the FastAPI server"""
    try:
        logger.info("🚀 Starting TradePulse FastAPI Server...")
        
        # Server configuration
        host = "0.0.0.0"
        port = 8000
        reload = True
        log_level = "info"
        
        logger.info(f"📡 Server will be available at: http://{host}:{port}")
        logger.info(f"📚 API documentation at: http://{host}:{port}/docs")
        logger.info(f"📖 ReDoc documentation at: http://{host}:{port}/redoc")
        
        # Run the server
        uvicorn.run(
            "api.fastapi_server:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
