#!/usr/bin/env python3
"""
TradePulse File Browser Standalone Launcher
Launches the file browser component independently
"""

import panel as pn
import logging
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_components.data_manager import DataManager
from modular_panels.file_browser_component import FileBrowserComponent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to launch the file browser"""
    try:
        logger.info("🚀 TradePulse File Browser Standalone Launcher")
        logger.info("=" * 50)
        
        # Initialize data manager
        logger.info("🔧 Initializing Data Manager...")
        data_manager = DataManager()
        logger.info("✅ Data Manager initialized")
        
        # Initialize file browser component
        logger.info("🔧 Initializing File Browser Component...")
        file_browser = FileBrowserComponent(data_manager)
        logger.info("✅ File Browser Component initialized")
        
        # Create the main layout
        main_layout = pn.Column(
            pn.pane.Markdown("# 📁 TradePulse File Browser"),
            pn.pane.Markdown("**Browse local directories and load data files**"),
            pn.pane.Markdown("---"),
            file_browser.get_component(),
            sizing_mode='stretch_width'
        )
        
        # Create the Panel app
        app = pn.Column(
            main_layout,
            sizing_mode='stretch_width'
        )
        
        logger.info("✅ File Browser application created successfully")
        logger.info("")
        logger.info("🎯 Available endpoints:")
        logger.info("   📁 File Browser: http://localhost:5006")
        logger.info("")
        logger.info("🚀 Starting File Browser server...")
        
        # Serve the app
        app.show(port=5006, show=False)
        
        logger.info("✅ File Browser server started successfully")
        logger.info("🌐 Access the File Browser at: http://localhost:5006")
        
        # Keep the server running
        pn.serve(app, port=5006, show=True)
        
    except Exception as e:
        logger.error(f"❌ Failed to launch File Browser: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
