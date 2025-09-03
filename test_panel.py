#!/usr/bin/env python3
"""
Simple Panel Test
"""

import panel as pn

def main():
    """Simple Panel test"""
    print("🚀 Testing Panel...")
    
    # Create a simple app
    app = pn.Column(
        pn.pane.Markdown("# 🎉 TradePulse Panel Test"),
        pn.pane.Markdown("Panel is working correctly!"),
        pn.widgets.Button(name="Test Button", button_type="primary"),
        sizing_mode='stretch_width'
    )
    
    print("✅ Panel app created successfully")
    print("🌐 Starting Panel server on http://localhost:5006")
    
    # Start the server
    app.show(port=5006, host='localhost')

if __name__ == "__main__":
    main()
