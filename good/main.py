#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Main Entry Point
Main function to run the Integrated Panel UI
"""

import logging
from .integrated_panel_ui import TradePulseIntegratedUI

logger = logging.getLogger(__name__)

def main():
    """Main function to run the Integrated Panel UI"""
    try:
        # Create the integrated UI
        ui = TradePulseIntegratedUI()
        
        # Get the main layout
        app = ui.get_layout()
        
        # Configure the app
        app.servable()
        
        return app
        
    except Exception as e:
        logger.error(f"Failed to create Integrated Panel UI: {e}")
        return None

if __name__ == "__main__":
    app = main()
    if app:
        app.show()
