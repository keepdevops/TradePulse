#!/usr/bin/env python3
"""
TradePulse Application Runner
Launches the modular TradePulse application with enhanced architecture
"""

import panel as pn
import logging
import sys
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
    """Launch the TradePulse application"""
    try:
        logger.info("🚀 TradePulse Application Launcher")
        logger.info("=" * 50)
        
        # Import the modular UI
        from modular_panel_ui_main_refactored import create_refactored_modular_ui
        
        logger.info("✅ Application components loaded successfully")
        logger.info("")
        logger.info("🎯 Available features:")
        logger.info("   📊 Data Panel with M3 file browsing")
        logger.info("   🤖 Models Panel with ML capabilities")
        logger.info("   💼 Portfolio Panel with risk management")
        logger.info("   🧠 AI Panel with advanced analytics")
        logger.info("   📈 Charts Panel with interactive visualizations")
        logger.info("   🚨 Alerts Panel with real-time notifications")
        logger.info("   ⚙️ System Panel with configuration")
        logger.info("")
        logger.info("🎨 Creating modular UI...")
        
        # Create the modular UI
        app = create_refactored_modular_ui()
        
        logger.info("✅ Modular UI created successfully")
        logger.info("")
        logger.info("🌐 Starting Panel server...")
        logger.info("   📱 Panel UI: http://localhost:5006")
        logger.info("")
        
        # Show the application
        app.show(
            title="TradePulse - Modular Trading System",
            port=5006,
            browser=True
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 Make sure all dependencies are installed:")
        logger.error("   pip install panel pandas numpy yfinance")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
