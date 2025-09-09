#!/usr/bin/env python3
"""
TradePulse FastAPI + Panel Advanced Integration
Advanced unified server with proper Panel embedding in FastAPI
"""

import logging
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi_panel_core import fastapi_panel_core_app, panel_app
from fastapi_panel_endpoints import setup_additional_endpoints, start_server, set_panel_app

# Setup additional endpoints
setup_additional_endpoints(fastapi_panel_core_app)

# Set the panel app instance for endpoints
set_panel_app(panel_app)

# Main app instance
app = fastapi_panel_core_app

if __name__ == "__main__":
    start_server()
