#!/usr/bin/env python3
"""
Quick Dark Mode Fix for TradePulse
Run this to immediately see visible UI panels in dark mode
"""

import panel as pn
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def quick_dark_fix():
    """Quick fix for dark mode visibility"""
    logger.info("🌙 Applying quick dark mode fix...")
    
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
    
    # Create visible dark mode panels
    data_panel = pn.Column(
        pn.pane.Markdown("# 📊 Data Panel", styles={'color': 'white', 'font-size': '24px', 'font-weight': 'bold'}),
        pn.widgets.DataFrame(stock_data.head(10), width=800, height=300),
        background='#2d2d2d',
        styles={'border': '2px solid #404040', 'padding': '15px', 'margin': '10px'}
    )
    
    portfolio_panel = pn.Column(
        pn.pane.Markdown("# 💼 Portfolio Panel", styles={'color': 'white', 'font-size': '24px', 'font-weight': 'bold'}),
        pn.pane.Markdown("**Total Value: $289,000**", styles={'color': '#00ff88', 'font-size': '20px', 'font-weight': 'bold'}),
        pn.pane.Markdown("**AAPL: 100 shares @ $160**", styles={'color': 'white', 'font-size': '16px'}),
        pn.pane.Markdown("**GOOGL: 50 shares @ $2900**", styles={'color': 'white', 'font-size': '16px'}),
        pn.pane.Markdown("**MSFT: 75 shares @ $320**", styles={'color': 'white', 'font-size': '16px'}),
        background='#2d2d2d',
        styles={'border': '2px solid #404040', 'padding': '15px', 'margin': '10px'}
    )
    
    ai_panel = pn.Column(
        pn.pane.Markdown("# 🤖 AI Panel", styles={'color': 'white', 'font-size': '24px', 'font-weight': 'bold'}),
        pn.widgets.Select(name='Model Type', options=['ADM', 'CIPO', 'BICIPO'], value='ADM'),
        pn.widgets.Button(name='🚀 Train Model', button_type='primary'),
        pn.pane.Markdown("**Status: Ready**", styles={'color': '#00ff88', 'font-size': '18px', 'font-weight': 'bold'}),
        background='#2d2d2d',
        styles={'border': '2px solid #404040', 'padding': '15px', 'margin': '10px'}
    )
    
    alerts_panel = pn.Column(
        pn.pane.Markdown("# 🚨 Alerts Panel", styles={'color': 'white', 'font-size': '24px', 'font-weight': 'bold'}),
        pn.widgets.TextInput(name='Symbol', placeholder='Enter stock symbol'),
        pn.widgets.FloatInput(name='Price', value=150.0),
        pn.widgets.Button(name='🔔 Create Alert', button_type='primary'),
        pn.pane.Markdown("**Active Alerts: 3**", styles={'color': '#ffaa00', 'font-size': '18px', 'font-weight': 'bold'}),
        background='#2d2d2d',
        styles={'border': '2px solid #404040', 'padding': '15px', 'margin': '10px'}
    )
    
    # Create tabs with strong dark theme
    tabs = pn.Tabs(
        ('📊 Data', data_panel),
        ('💼 Portfolio', portfolio_panel),
        ('🤖 AI', ai_panel),
        ('🚨 Alerts', alerts_panel),
        styles={'background': '#1e1e1e', 'color': 'white'}
    )
    
    # Create header with strong contrast
    header = pn.Column(
        pn.pane.Markdown("# 🌙 TradePulse - Dark Mode", 
                        styles={'color': '#00ff88', 'text-align': 'center', 'font-size': '36px', 'font-weight': 'bold'}),
        pn.pane.Markdown("**Trading Platform - Dark Mode Optimized**", 
                        styles={'color': 'white', 'text-align': 'center', 'font-size': '20px'}),
        background='#1e1e1e',
        styles={'border-bottom': '3px solid #404040', 'padding': '20px'}
    )
    
    # Create main layout with strong dark theme
    main_layout = pn.Column(
        header,
        tabs,
        background='#1e1e1e',
        styles={'min-height': '100vh'}
    )
    
    logger.info("✅ Quick dark mode fix applied")
    return main_layout

def main():
    """Main function"""
    logger.info("🚀 Starting Quick Dark Mode Fix...")
    
    # Create the UI with quick fix
    app = quick_dark_fix()
    
    # Show the app
    app.show(
        port=5010,
        host='localhost',
        title='TradePulse - Quick Dark Mode Fix'
    )
    
    logger.info("🌐 Quick dark mode fix available at: http://localhost:5010")
    logger.info("✅ UI panels should now be clearly visible in dark mode!")

if __name__ == "__main__":
    main()
