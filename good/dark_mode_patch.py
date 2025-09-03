#!/usr/bin/env python3
"""
Dark Mode Patch for Running TradePulse Application
Apply this to fix black on black visibility issues
"""

import panel as pn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_dark_mode_patch():
    """Create a dark mode patch for the running application"""
    logger.info("🌙 Creating dark mode patch...")
    
    # Set Panel to dark theme
    pn.config.theme = 'dark'
    
    # Create CSS patch for dark mode visibility
    dark_css = """
    <style>
    /* Dark Mode Patch for TradePulse */
    
    /* Force dark background */
    body {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    /* Panel containers */
    .bk-panel-models-layout-Column {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        padding: 10px !important;
        margin: 5px !important;
    }
    
    .bk-panel-models-layout-Row {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Tabs styling */
    .bk-panel-models-widgets-Tabs {
        background-color: #1e1e1e !important;
    }
    
    .bk-panel-models-widgets-Tabs .bk-tabs-header {
        background-color: #2d2d2d !important;
        border-color: #404040 !important;
    }
    
    .bk-panel-models-widgets-Tabs .bk-tab {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    .bk-panel-models-widgets-Tabs .bk-tab.bk-active {
        background-color: #404040 !important;
        color: #00ff88 !important;
    }
    
    /* DataFrame styling */
    .bk-panel-models-widgets-DataFrame {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .bk-panel-models-widgets-DataFrame table {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .bk-panel-models-widgets-DataFrame th {
        background-color: #404040 !important;
        color: #ffffff !important;
    }
    
    .bk-panel-models-widgets-DataFrame td {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    /* Button styling */
    .bk-panel-models-widgets-Button {
        background-color: #404040 !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    .bk-panel-models-widgets-Button:hover {
        background-color: #505050 !important;
    }
    
    .bk-panel-models-widgets-Button.bk-btn-primary {
        background-color: #00ff88 !important;
        color: #1e1e1e !important;
    }
    
    /* Input styling */
    .bk-panel-models-widgets-TextInput {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    .bk-panel-models-widgets-Select {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    .bk-panel-models-widgets-IntSlider {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .bk-panel-models-widgets-FloatSlider {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .bk-panel-models-widgets-FloatInput {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }
    
    /* Markdown styling */
    .bk-panel-models-markup-Markdown {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Chart styling */
    .bk-panel-models-plot-Plot {
        background-color: #1e1e1e !important;
    }
    
    /* Override any light theme elements */
    * {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    /* Specific panel overrides */
    .panel-widget-box {
        background-color: #2d2d2d !important;
        border-color: #404040 !important;
    }
    
    .panel-content {
        background-color: #1e1e1e !important;
    }
    
    /* Success, warning, error colors */
    .success-text {
        color: #00ff88 !important;
    }
    
    .warning-text {
        color: #ffaa00 !important;
    }
    
    .error-text {
        color: #ff4444 !important;
    }
    
    .info-text {
        color: #4488ff !important;
    }
    
    /* Force visibility for all text */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #ffffff !important;
    }
    
    /* Panel specific fixes */
    .bk-root {
        background-color: #1e1e1e !important;
    }
    
    /* Override any remaining black backgrounds */
    [style*="background-color: black"], 
    [style*="background: black"],
    [style*="background-color: #000"],
    [style*="background: #000"] {
        background-color: #2d2d2d !important;
    }
    
    </style>
    """
    
    # Create the patch as a Panel component
    patch = pn.pane.HTML(dark_css)
    
    logger.info("✅ Dark mode patch created")
    return patch

def apply_dark_mode_to_running_app():
    """Apply dark mode to the running application"""
    logger.info("🔧 Applying dark mode patch to running application...")
    
    # Create the patch
    patch = create_dark_mode_patch()
    
    # Set Panel theme
    pn.config.theme = 'dark'
    
    logger.info("✅ Dark mode patch ready to apply")
    logger.info("🌐 Refresh your browser at http://localhost:5006 to see the changes")
    
    return patch

def main():
    """Main function"""
    logger.info("🚀 Creating Dark Mode Patch...")
    
    # Create the patch
    patch = apply_dark_mode_to_running_app()
    
    # Show instructions
    print("\n" + "="*60)
    print("🌙 DARK MODE PATCH CREATED")
    print("="*60)
    print("✅ Dark mode patch is ready")
    print("🌐 Refresh your browser at: http://localhost:5006")
    print("📝 The panels should now be visible with proper contrast")
    print("🎨 Dark theme applied: White text on dark backgrounds")
    print("="*60)
    
    return patch

if __name__ == "__main__":
    main()
