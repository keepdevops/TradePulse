#!/usr/bin/env python3
"""
Simple Dark Mode Launcher for TradePulse
Quick fix for UI visibility issues in dark mode
"""

import panel as pn
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_simple_dark_ui():
    """Create a simple dark mode UI that's immediately visible"""
    logger.info("🌙 Creating simple dark mode UI...")
    
    # Set Panel to dark theme
    pn.config.theme = 'dark'
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    stock_data = pd.DataFrame({
        'Date': dates,
        'AAPL': np.random.randn(len(dates)).cumsum() + 150,
        'GOOGL': np.random.randn(len(dates)).cumsum() + 2800,
        'MSFT': np.random.randn(len(dates)).cumsum() + 300,
    })
    
    # Create simple dark mode components
    data_panel = pn.Column(
        pn.pane.Markdown("# 📊 Data Panel", styles={'color': 'white', 'font-size': '24px'}),
        pn.widgets.DataFrame(stock_data.head(10), width=800, height=300),
        background='#2d2d2d',
        styles={'border': '1px solid #404040', 'padding': '10px'}
    )
    
    portfolio_panel = pn.Column(
        pn.pane.Markdown("# 💼 Portfolio Panel", styles={'color': 'white', 'font-size': '24px'}),
        pn.pane.Markdown("**Total Value: $289,000**", styles={'color': '#00ff88', 'font-size': '18px'}),
        pn.pane.Markdown("**AAPL: 100 shares @ $160**", styles={'color': 'white'}),
        pn.pane.Markdown("**GOOGL: 50 shares @ $2900**", styles={'color': 'white'}),
        pn.pane.Markdown("**MSFT: 75 shares @ $320**", styles={'color': 'white'}),
        background='#2d2d2d',
        styles={'border': '1px solid #404040', 'padding': '10px'}
    )
    
    ai_panel = pn.Column(
        pn.pane.Markdown("# 🤖 AI Panel", styles={'color': 'white', 'font-size': '24px'}),
        pn.widgets.Select(name='Model Type', options=['ADM', 'CIPO', 'BICIPO'], value='ADM'),
        pn.widgets.Button(name='🚀 Train Model', button_type='primary'),
        pn.pane.Markdown("**Status: Ready**", styles={'color': '#00ff88'}),
        background='#2d2d2d',
        styles={'border': '1px solid #404040', 'padding': '10px'}
    )
    
    alerts_panel = pn.Column(
        pn.pane.Markdown("# 🚨 Alerts Panel", styles={'color': 'white', 'font-size': '24px'}),
        pn.widgets.TextInput(name='Symbol', placeholder='Enter stock symbol'),
        pn.widgets.FloatInput(name='Price', value=150.0),
        pn.widgets.Button(name='🔔 Create Alert', button_type='primary'),
        pn.pane.Markdown("**Active Alerts: 3**", styles={'color': '#ffaa00'}),
        background='#2d2d2d',
        styles={'border': '1px solid #404040', 'padding': '10px'}
    )
    
    # Create tabs with dark theme
    tabs = pn.Tabs(
        ('📊 Data', data_panel),
        ('💼 Portfolio', portfolio_panel),
        ('🤖 AI', ai_panel),
        ('🚨 Alerts', alerts_panel),
        styles={'background': '#1e1e1e', 'color': 'white'}
    )
    
    # Create header
    header = pn.Column(
        pn.pane.Markdown("# 🌙 TradePulse - Dark Mode", 
                        styles={'color': '#00ff88', 'text-align': 'center', 'font-size': '32px'}),
        pn.pane.Markdown("**Trading Platform - Dark Mode Optimized**", 
                        styles={'color': 'white', 'text-align': 'center', 'font-size': '18px'}),
        background='#1e1e1e',
        styles={'border-bottom': '2px solid #404040', 'padding': '10px'}
    )
    
    # Create main layout
    main_layout = pn.Column(
        header,
        tabs,
        background='#1e1e1e',
        styles={'min-height': '100vh'}
    )
    
    logger.info("✅ Simple dark mode UI created")
    return main_layout

def main():
    """Main function"""
    logger.info("🚀 Starting Simple Dark Mode TradePulse...")
    
    # Create the UI
    app = create_simple_dark_ui()
    
    # Show the app
    app.show(
        port=5009,
        host='localhost',
        title='TradePulse - Simple Dark Mode',
        show=False
    )
    
    logger.info("🌐 Simple dark mode app available at: http://localhost:5009")

if __name__ == "__main__":
    main()
